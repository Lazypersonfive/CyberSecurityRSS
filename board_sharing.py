"""Deterministic cross-board candidate sharing.

AI-security RSS coverage is sparse. When that board runs, reuse the same
Shanghai-date security fetch and keep only items that already look like
AI-security technical stories. Generic AI, ordinary software supply-chain
and political/commercial news stay out.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from digest_clock import DIGEST_TIMEZONE
from security_editorial import is_strong_ai_security_candidate

logger = logging.getLogger(__name__)

_FUTURE_SKEW = timedelta(hours=6)


def merge_ai_security_from_security(
    entries: list[dict[str, Any]],
    *,
    security_path: Path,
    as_of: date,
    fetch_hours: int,
    now: datetime | None = None,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Append strong AI-security items from the same-round security fetch."""
    stats = {
        "considered": 0,
        "shared": 0,
        "skipped_missing": 0,
        "skipped_date": 0,
        "skipped_window": 0,
        "skipped_semantic": 0,
        "skipped_duplicate": 0,
    }
    payload = _load_security_payload(security_path, stats)
    if payload is None:
        return list(entries), stats

    fetched_at = str(payload.get("fetched_at") or "")
    if fetched_at != as_of.isoformat():
        stats["skipped_date"] = 1
        logger.info(
            "ai_security share skipped: security fetched_at=%s as_of=%s",
            fetched_at,
            as_of.isoformat(),
        )
        return list(entries), stats

    window_end = _window_end(as_of, now)
    cutoff = window_end - timedelta(hours=max(1, int(fetch_hours)))
    seen_urls = {_normalize_url(entry.get("url")) for entry in entries}
    seen_urls.discard("")

    merged = list(entries)
    for raw in payload.get("entries") or []:
        if not isinstance(raw, dict):
            continue
        stats["considered"] += 1
        url = _normalize_url(raw.get("url"))
        if not url or url in seen_urls:
            stats["skipped_duplicate"] += 1
            continue
        published = _parse_datetime(raw.get("published"))
        if published is None or published < cutoff or published > window_end + _FUTURE_SKEW:
            stats["skipped_window"] += 1
            continue
        if not is_strong_ai_security_candidate(raw):
            stats["skipped_semantic"] += 1
            continue
        shared = dict(raw)
        shared["shared_from"] = "security"
        merged.append(shared)
        seen_urls.add(url)
        stats["shared"] += 1

    if stats["shared"]:
        logger.info(
            "ai_security shared %d/%d security entries (window=%dh)",
            stats["shared"],
            stats["considered"],
            fetch_hours,
        )
    return merged, stats


def trim_llm_candidates(
    entries: list[dict[str, Any]],
    max_llm_entries: int,
) -> list[dict[str, Any]]:
    """Cap the LLM scoring set, but keep shared AI-security items in the pool.

    Native board entries stay first. Shared security items get up to one third
    of the cap so a large native list cannot drop them entirely.
    """
    if max_llm_entries <= 0 or len(entries) <= max_llm_entries:
        return list(entries)

    shared = [entry for entry in entries if entry.get("shared_from") == "security"]
    native = [entry for entry in entries if entry.get("shared_from") != "security"]
    reserved_shared = min(len(shared), max_llm_entries // 3)
    native_keep = min(len(native), max_llm_entries - reserved_shared)
    shared_keep = min(len(shared), max_llm_entries - native_keep)
    kept = native[:native_keep] + shared[:shared_keep]
    leftover = native[native_keep:] + shared[shared_keep:]
    for extra in leftover:
        if len(kept) >= max_llm_entries:
            break
        kept.append(extra)
    return kept


def _load_security_payload(path: Path, stats: dict[str, int]) -> dict[str, Any] | None:
    if not path.exists():
        stats["skipped_missing"] = 1
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        stats["skipped_missing"] = 1
        logger.warning("ai_security share skipped: cannot read %s (%s)", path, exc)
        return None
    if not isinstance(payload, dict):
        stats["skipped_missing"] = 1
        return None
    return payload


def _window_end(as_of: date, now: datetime | None) -> datetime:
    if now is not None:
        if now.tzinfo is None:
            return now.replace(tzinfo=timezone.utc)
        return now.astimezone(timezone.utc)
    local_end = datetime.combine(as_of, time(23, 59, 59), tzinfo=DIGEST_TIMEZONE)
    return local_end.astimezone(timezone.utc)


def _parse_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        text = value.strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
    else:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _normalize_url(url: Any) -> str:
    text = str(url or "").strip()
    if not text:
        return ""
    parsed = urlparse(text)
    host = (parsed.hostname or "").removeprefix("www.").lower()
    path = parsed.path or ""
    query = f"?{parsed.query}" if parsed.query else ""
    if host:
        return f"{host}{path}{query}".rstrip("/")
    return text.rstrip("/")

"""Concurrently fetch RSS feeds and filter entries from the last N hours."""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import date as _date, datetime, timedelta, timezone
from pathlib import Path

try:
    import feedparser
except ImportError as exc:
    feedparser = None
    FEEDPARSER_IMPORT_ERROR: ImportError | None = exc
else:
    FEEDPARSER_IMPORT_ERROR = None

try:
    import httpx
except ImportError as exc:
    httpx = None
    HTTPX_IMPORT_ERROR: ImportError | None = exc
else:
    HTTPX_IMPORT_ERROR = None

logger = logging.getLogger(__name__)

ARCHIVE_DIR = Path(__file__).parent / "archive"


@dataclass
class FeedEntry:
    title: str
    url: str
    summary: str
    category: str
    published: datetime
    feed_url: str = ""
    feed_title: str = ""


def load_seen_urls(date_str: str, lookback_days: int = 7, include_today: bool = True) -> set[str]:
    """Merge URLs from the last N days of archive/<date>.json files.

    When include_today is false, the current date is skipped so a same-day
    site refresh does not become an incremental run.

    The fetch window for sparse boards (finance) can span up to 14 days, but
    URL collisions outside a 7-day rolling window are rare in practice. This
    keeps the dedup set bounded while covering same-story republication
    across consecutive cron runs.
    """
    target = _date.fromisoformat(date_str)
    seen: set[str] = set()
    start_offset = 0 if include_today else 1
    stop_offset = start_offset + max(1, lookback_days)
    for offset in range(start_offset, stop_offset):
        path = ARCHIVE_DIR / f"{(target - timedelta(days=offset)).isoformat()}.json"
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("archive %s unreadable: %s", path.name, exc)
            continue
        seen.update(data.get("urls", []))
    return seen


def archive_urls(date_str: str, urls: list[str]) -> Path:
    """Persist URLs to archive/<date>.json, merging with any existing entries."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    path = ARCHIVE_DIR / f"{date_str}.json"
    existing: set[str] = set()
    if path.exists():
        try:
            existing = set(json.loads(path.read_text(encoding="utf-8")).get("urls", []))
        except (OSError, json.JSONDecodeError):
            existing = set()
    merged = sorted(existing | {u for u in urls if u})
    path.write_text(json.dumps({"urls": merged}, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


async def fetch_all_entries(
    feeds: dict[str, list[str]],
    hours: int = 24,
    timeout: int = 10,
    seen_urls: set[str] | None = None,
    max_per_category: int = 30,
    feed_titles: dict[str, str] | None = None,
) -> tuple[list[FeedEntry], dict[str, int]]:
    """Fetch all feeds concurrently and return recent entries.

    Args:
        feeds: Category -> list of feed URLs.
        hours: Only include entries published within this many hours.
        timeout: Per-request timeout in seconds.
        seen_urls: URLs already delivered; these will be skipped.
        max_per_category: Cap entries per category to limit API cost.
        feed_titles: Optional feed URL -> feed label mapping from OPML.

    Returns:
        Tuple of (entry list, health dict mapping url -> error_count).
    """
    if httpx is None:
        raise RuntimeError(f"httpx is required to fetch feeds: {HTTPX_IMPORT_ERROR}")

    seen_urls = seen_urls or set()
    feed_titles = feed_titles or {}
    cutoff = datetime.now(timezone.utc).timestamp() - hours * 3600

    entries: list[FeedEntry] = []
    health: dict[str, int] = {}

    limits = httpx.Limits(max_connections=80, max_keepalive_connections=30)
    semaphore = asyncio.Semaphore(40)
    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        limits=limits,
        headers={"User-Agent": "Mozilla/5.0 (daily-digest-bot)"},
    ) as client:
        tasks = []
        meta = []  # (category, url) pairs matching tasks
        for category, urls in feeds.items():
            for url in urls:
                tasks.append(_fetch_one_bounded(semaphore, client, url))
                meta.append((category, url))

        results = await asyncio.gather(*tasks, return_exceptions=True)

    category_entries: dict[str, list[FeedEntry]] = {}
    for (category, url), result in zip(meta, results):
        if isinstance(result, Exception):
            logger.debug("Feed error %s: %s", url, result)
            health[url] = health.get(url, 0) + 1
            continue

        for entry in result:
            if entry.url in seen_urls:
                continue
            if entry.published.timestamp() < cutoff:
                continue
            entry.category = category
            entry.feed_url = url
            entry.feed_title = feed_titles.get(url, url)
            category_entries.setdefault(category, []).append(entry)

    for category in feeds:
        ranked = sorted(
            category_entries.get(category, []),
            key=lambda entry: entry.published,
            reverse=True,
        )
        entries.extend(ranked[:max_per_category])

    entries.sort(key=lambda e: e.published, reverse=True)
    return entries, health


async def _fetch_one_bounded(
    semaphore: asyncio.Semaphore, client: httpx.AsyncClient, url: str
) -> list[FeedEntry]:
    async with semaphore:
        return await _fetch_one(client, url)


async def _fetch_one(client: httpx.AsyncClient, url: str) -> list[FeedEntry]:
    if feedparser is None:
        raise RuntimeError(f"feedparser is required to parse feeds: {FEEDPARSER_IMPORT_ERROR}")

    response = await client.get(url)
    response.raise_for_status()
    parsed = feedparser.parse(response.text)

    entries: list[FeedEntry] = []
    for item in parsed.entries:
        link = item.get("link", "")
        if not link:
            continue
        title = item.get("title", "(no title)").strip()
        summary = _clean_summary(item.get("summary", item.get("description", "")))
        published = _parse_date(item)
        if published is None:
            continue
        entries.append(FeedEntry(
            title=title,
            url=link,
            summary=summary,
            category="",  # filled by caller
            published=published,
        ))
    return entries


def _parse_date(item: feedparser.FeedParserDict) -> datetime | None:
    for field in ("published_parsed", "updated_parsed", "created_parsed"):
        val = item.get(field)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except Exception:
                continue
    return None


def _clean_summary(raw: str) -> str:
    import re
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:400]

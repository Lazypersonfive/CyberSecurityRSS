"""Source tier/kind registry for deterministic editorial weighting."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

PROJECT_DIR = Path(__file__).parent
REGISTRY_PATH = PROJECT_DIR / "source_registry.yaml"

DEFAULT_PROFILE = {"tier": "unknown", "kind": "media", "label": "未登记源"}


@lru_cache(maxsize=1)
def load_source_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"defaults": DEFAULT_PROFILE, "domains": {}, "x_handles": {}}
    data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    return {
        "defaults": {**DEFAULT_PROFILE, **(data.get("defaults") or {})},
        "domains": data.get("domains") or {},
        "x_handles": data.get("x_handles") or {},
    }


def registry_match(*, host: str = "", feed_host: str = "", x_handle: str = "") -> dict[str, str]:
    """Return registry metadata with deterministic defaults."""
    registry = load_source_registry()
    defaults = dict(registry["defaults"])
    domains = registry["domains"]
    handles = registry["x_handles"]

    if x_handle:
        by_handle = handles.get(x_handle) or handles.get(x_handle.lower())
        if by_handle:
            return _clean({**defaults, **by_handle})

    for candidate in (host, feed_host):
        match = _domain_lookup(candidate, domains)
        if match:
            return _clean({**defaults, **match})
    return _clean(defaults)


def _domain_lookup(host: str, domains: dict[str, Any]) -> dict[str, Any] | None:
    host = (host or "").removeprefix("www.").lower()
    if not host:
        return None
    if host in domains:
        return domains[host]
    parts = host.split(".")
    for i in range(1, max(1, len(parts) - 1)):
        parent = ".".join(parts[i:])
        if parent in domains:
            return domains[parent]
    return None


def x_handle_from_urls(url: str = "", feed_url: str = "") -> str:
    """Extract an X/Twitter handle from RSSHub feed URL or item URL."""
    for raw in (feed_url, url):
        try:
            parsed = urlparse(raw or "")
        except ValueError:
            continue
        host = (parsed.hostname or "").lower()
        parts = [part for part in parsed.path.split("/") if part]
        if "rsshub" in host and len(parts) >= 3 and parts[:2] == ["twitter", "user"]:
            return parts[2]
        if host in {"x.com", "twitter.com"} and parts:
            handle = parts[0]
            if handle not in {"i", "intent", "share", "home", "search"}:
                return handle
    return ""


def _clean(data: dict[str, Any]) -> dict[str, str]:
    return {
        "tier": str(data.get("tier") or DEFAULT_PROFILE["tier"]),
        "kind": str(data.get("kind") or DEFAULT_PROFILE["kind"]),
        "label": str(data.get("label") or DEFAULT_PROFILE["label"]),
    }

"""Concurrently fetch RSS feeds and filter entries from the last N hours."""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import httpx

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


def load_seen_urls(date_str: str) -> set[str]:
    """Load already-sent URLs for a given date to avoid duplicates."""
    path = ARCHIVE_DIR / f"{date_str}.json"
    if not path.exists():
        return set()
    data = json.loads(path.read_text())
    return set(data.get("urls", []))


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

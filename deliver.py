"""Deliver digest to Discord via webhook and archive sent URLs."""

import json
import logging
from datetime import date
from pathlib import Path

import httpx

from fetch_feeds import FeedEntry

logger = logging.getLogger(__name__)

ARCHIVE_DIR = Path(__file__).parent / "archive"
DISCORD_CHAR_LIMIT = 1900  # safe margin under 2000


def deliver(
    digest: str,
    entries: list[FeedEntry],
    webhook_url: str,
    dry_run: bool = False,
    today: date | None = None,
) -> None:
    """Send digest to Discord webhook and archive entry URLs.

    Args:
        digest: Markdown digest string.
        entries: High-value entries that were included in the digest.
        webhook_url: Discord webhook URL.
        dry_run: If True, print to stdout instead of sending.
        today: Date key for archive. Defaults to today.
    """
    chunks = _split_message(digest)

    if dry_run:
        print("\n" + "=" * 60)
        for chunk in chunks:
            print(chunk)
            print("-" * 60)
        print(f"[dry-run] Would send {len(chunks)} message(s) to Discord")
        return

    _send_to_discord(chunks, webhook_url)
    _archive_urls(entries, today or date.today())


def _split_message(text: str) -> list[str]:
    if len(text) <= DISCORD_CHAR_LIMIT:
        return [text]

    chunks: list[str] = []
    current = ""
    for line in text.splitlines(keepends=True):
        if len(current) + len(line) > DISCORD_CHAR_LIMIT:
            if current:
                chunks.append(current.rstrip())
            current = line
        else:
            current += line
    if current.strip():
        chunks.append(current.rstrip())
    return chunks


def _send_to_discord(chunks: list[str], webhook_url: str) -> None:
    with httpx.Client(timeout=15) as client:
        for i, chunk in enumerate(chunks):
            payload = {"content": chunk}
            response = client.post(webhook_url, json=payload)
            if response.status_code not in (200, 204):
                logger.error("Discord webhook failed: %d %s", response.status_code, response.text)
                response.raise_for_status()
            logger.info("Sent chunk %d/%d", i + 1, len(chunks))


def _archive_urls(entries: list[FeedEntry], today: date) -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    path = ARCHIVE_DIR / f"{today.isoformat()}.json"

    existing: set[str] = set()
    if path.exists():
        existing = set(json.loads(path.read_text()).get("urls", []))

    new_urls = {e.url for e in entries}
    all_urls = sorted(existing | new_urls)
    path.write_text(json.dumps({"urls": all_urls}, ensure_ascii=False, indent=2))
    logger.info("Archived %d URLs for %s", len(all_urls), today)

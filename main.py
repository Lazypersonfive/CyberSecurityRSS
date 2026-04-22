"""Daily security digest pipeline: fetch -> score -> deliver."""

import argparse
import asyncio
import logging
import os
import sys
from datetime import date
from pathlib import Path

import yaml

# Load .env file if it exists (before any env checks)
_ENV_FILE = Path(__file__).parent / ".env"
if _ENV_FILE.exists():
    for _line in _ENV_FILE.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        logger.error("config.yaml not found at %s", CONFIG_PATH)
        sys.exit(1)
    with CONFIG_PATH.open() as f:
        return yaml.safe_load(f)


def validate_env() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)


def run(dry_run: bool = False, hours: int | None = None) -> None:
    from fetch_opml import fetch_opml
    from fetch_feeds import fetch_all_entries, load_seen_urls
    from generate_digest import generate_digest
    from deliver import deliver

    validate_env()
    config = load_config()

    webhook_url = config.get("discord_webhook_url", "")
    if not dry_run and (not webhook_url or "YOUR_WEBHOOK" in webhook_url):
        logger.error("Discord webhook URL not configured in config.yaml")
        sys.exit(1)

    fetch_hours = hours or config.get("fetch_hours", 24)
    today_str = date.today().isoformat()
    seen_urls = load_seen_urls(today_str)

    logger.info("Fetching OPML...")
    feeds = fetch_opml(use_cache=config.get("use_opml_cache", True))
    total_feeds = sum(len(v) for v in feeds.values())
    logger.info("Loaded %d feeds across %d categories", total_feeds, len(feeds))

    logger.info("Fetching entries (last %dh)...", fetch_hours)
    entries, health = asyncio.run(
        fetch_all_entries(
            feeds,
            hours=fetch_hours,
            timeout=config.get("fetch_timeout", 10),
            seen_urls=seen_urls,
            max_per_category=config.get("max_per_category", 30),
        )
    )
    logger.info("Got %d new entries", len(entries))

    if health:
        failed = len(health)
        logger.warning("%d feeds returned errors", failed)

    logger.info("Generating digest with Claude Haiku...")
    digest = generate_digest(entries)

    deliver(
        digest=digest,
        entries=entries,
        webhook_url=webhook_url,
        dry_run=dry_run,
    )

    if not dry_run:
        logger.info("Done. Digest delivered to Discord.")
    else:
        logger.info("Done. Dry run complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily cybersecurity digest")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print digest to stdout, do not send to Discord",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=None,
        help="Hours back to fetch (overrides config.yaml)",
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run, hours=args.hours)


if __name__ == "__main__":
    main()

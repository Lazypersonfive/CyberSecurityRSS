"""Fetch RSS feeds for a named board and save raw entries to output/<board>_latest.json.

No Claude API key required. ``digest_pipeline.py`` consumes the JSON downstream.

Usage:
    python fetch_and_save.py --board security [--hours N]
    python fetch_and_save.py --board ai
    python fetch_and_save.py --board finance

When --board is omitted, falls back to the legacy single-board mode
(zer0yu tiny.opml) and writes to output/latest.json for backward compat.
"""

import argparse
import asyncio
import json
import logging
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from fetch_feeds import fetch_all_entries, load_seen_urls
from fetch_opml import fetch_opml
from filter_entries import filter_and_dedup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "output"
CONFIG_PATH = PROJECT_DIR / "config.yaml"


def _load_board_config(board: str) -> dict[str, Any]:
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    boards = cfg.get("boards") or {}
    if board not in boards:
        raise SystemExit(f"Board '{board}' not found in config.yaml (known: {list(boards)})")
    bcfg = dict(boards[board])
    bcfg["opml"] = PROJECT_DIR / bcfg["opml"]
    return bcfg


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a board's RSS feeds")
    parser.add_argument(
        "--board",
        type=str,
        default=None,
        help="Board name from config.yaml (security|ai|finance). Omit for legacy mode.",
    )
    parser.add_argument("--hours", type=int, default=None, help="Override board fetch_hours")
    parser.add_argument("--no-dedup", action="store_true", help="Skip URL-level dedup")
    args = parser.parse_args()

    if args.board:
        bcfg = _load_board_config(args.board)
        opml_source = bcfg["opml"]
        hours = args.hours if args.hours is not None else int(bcfg.get("fetch_hours", 24))
        out_path = OUTPUT_DIR / f"{args.board}_latest.json"
        board_label = args.board
    else:
        opml_source = None  # legacy
        hours = args.hours if args.hours is not None else 24
        out_path = OUTPUT_DIR / "latest.json"
        board_label = "legacy"

    logger.info("[%s] Loading OPML from %s", board_label, opml_source or "(legacy cache)")
    feeds = fetch_opml(opml_source, use_cache=True)
    total_feeds = sum(len(v) for v in feeds.values())
    logger.info("[%s] %d feeds across %d categories", board_label, total_feeds, len(feeds))

    today_str = date.today().isoformat()
    seen_urls = set() if args.no_dedup else load_seen_urls(today_str)

    logger.info("[%s] Fetching entries (last %dh)...", board_label, hours)
    entries, health = asyncio.run(
        fetch_all_entries(
            feeds,
            hours=hours,
            timeout=25,
            seen_urls=seen_urls,
        )
    )
    logger.info("[%s] Got %d raw entries (%d feeds errored)", board_label, len(entries), len(health))

    filtered, filter_stats = filter_and_dedup(entries)
    logger.info(
        "[%s] Filter: %d -> %d", board_label, filter_stats.get("input", 0), filter_stats.get("output", 0)
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "board": args.board,
        "fetched_at": today_str,
        "hours": hours,
        "total_feeds": total_feeds,
        "raw_entry_count": len(entries),
        "entry_count": len(filtered),
        "filter_stats": filter_stats,
        "entries": [
            {
                "title": fe.title,
                "url": fe.url,
                "summary": fe.summary,
                "category": fe.category,
                "published": fe.published,
                "fetch_status": fe.fetch_status,
                "cve_ids": fe.cve_ids,
                "related_urls": fe.related_urls,
                "quality_score": fe.quality_score,
            }
            for fe in filtered
        ],
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    logger.info("[%s] Saved to %s", board_label, out_path)

    print(f"\n=== FETCH COMPLETE [{board_label}] ===")
    print(f"Date: {today_str} | Hours: {hours}h")
    print(f"Raw: {len(entries)} -> Filtered: {len(filtered)}")
    print(f"Saved: {out_path}")
    counts = Counter(fe.category for fe in filtered)
    if counts:
        print("\nCategory breakdown:")
        for cat, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {n}")


if __name__ == "__main__":
    main()

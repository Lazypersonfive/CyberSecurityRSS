"""Append-only CLI for daily digest feedback."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from digest_clock import digest_today

FEEDBACK_DIR = Path(__file__).parent / "feedback"
VALID_ACTIONS = {"upvote", "downvote", "must_include", "bad_summary", "bad_source"}


def add_feedback(
    *,
    board: str,
    url: str,
    action: str,
    reason: str,
    feedback_date: str | None = None,
    source: str = "",
    title_zh: str = "",
) -> Path:
    if action not in VALID_ACTIONS:
        raise ValueError(f"invalid action: {action}")
    if not urlparse(url).scheme:
        raise ValueError("url must include scheme")
    day = feedback_date or digest_today().isoformat()
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    path = FEEDBACK_DIR / f"{day}.jsonl"
    record = {
        "date": day,
        "board": board,
        "url": url,
        "action": action,
        "reason": reason,
        "source": source or _host(url),
        "title_zh": title_zh,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").removeprefix("www.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Record digest feedback")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("--board", required=True)
    add.add_argument("--url", required=True)
    add.add_argument("--action", required=True, choices=sorted(VALID_ACTIONS))
    add.add_argument("--reason", required=True)
    add.add_argument("--date", default=None)
    add.add_argument("--source", default="")
    add.add_argument("--title-zh", default="")
    args = parser.parse_args()

    if args.command == "add":
        path = add_feedback(
            board=args.board,
            url=args.url,
            action=args.action,
            reason=args.reason,
            feedback_date=args.date,
            source=args.source,
            title_zh=args.title_zh,
        )
        print(path)


if __name__ == "__main__":
    main()

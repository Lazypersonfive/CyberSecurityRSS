"""Render digest/*.json into docs/ as a static GitHub Pages site.

Produces:
    docs/index.html              — single-page app shell, loads feed_<date>.json
    docs/feed_<YYYY-MM-DD>.json  — per-date aggregated data (all boards)
    docs/feed.json               — alias to latest feed_<date>.json (for deep links)

Usage:
    python site_builder.py [--lookback 7]
"""

import argparse
import json
import logging
import shutil
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.yaml"
DIGEST_DIR = PROJECT_DIR / "digest"
DOCS_DIR = PROJECT_DIR / "docs"
TEMPLATE_DIR = PROJECT_DIR / "templates"


def _load_digest(board: str, d: date) -> dict[str, Any] | None:
    path = DIGEST_DIR / f"{board}_{d.isoformat()}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _build_feed_for_date(boards: dict[str, dict], d: date) -> dict[str, Any] | None:
    out: dict[str, Any] = {"date": d.isoformat(), "boards": {}}
    any_content = False
    for board, bcfg in boards.items():
        digest = _load_digest(board, d)
        if not digest:
            out["boards"][board] = {
                "display_name": bcfg.get("display_name", board),
                "items": [],
                "raw_count": 0,
                "generated_at": "",
            }
            continue
        any_content = any_content or bool(digest.get("items"))
        out["boards"][board] = {
            "display_name": bcfg.get("display_name", board),
            "items": digest.get("items", []),
            "raw_count": digest.get("raw_count", 0),
            "generated_at": digest.get("generated_at", ""),
        }
    return out if any_content else None


def build(lookback_days: int = 7) -> None:
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    boards = cfg.get("boards") or {}
    site = cfg.get("site") or {}
    lookback = int(site.get("lookback_days", lookback_days))

    today = date.today()
    dates_with_content: list[str] = []

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(lookback):
        d = today - timedelta(days=i)
        feed = _build_feed_for_date(boards, d)
        if feed is None:
            continue
        out_path = DOCS_DIR / f"feed_{d.isoformat()}.json"
        out_path.write_text(json.dumps(feed, ensure_ascii=False, indent=2))
        dates_with_content.append(d.isoformat())

    if not dates_with_content:
        # Seed one empty feed so the UI has something to load.
        empty = {"date": today.isoformat(), "boards": {
            b: {"display_name": bc.get("display_name", b), "items": [], "raw_count": 0, "generated_at": ""}
            for b, bc in boards.items()
        }}
        path = DOCS_DIR / f"feed_{today.isoformat()}.json"
        path.write_text(json.dumps(empty, ensure_ascii=False, indent=2))
        dates_with_content = [today.isoformat()]

    # Alias latest → feed.json (deep-link friendly)
    latest = dates_with_content[0]
    shutil.copy(DOCS_DIR / f"feed_{latest}.json", DOCS_DIR / "feed.json")

    # Render index.html
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "j2"]),
    )
    tmpl = env.get_template("index.html.j2")
    html = tmpl.render(
        title=site.get("title", "每日科技情报"),
        subtitle=site.get("subtitle", ""),
        boards_json=json.dumps(
            {b: {"display_name": bc.get("display_name", b)} for b, bc in boards.items()},
            ensure_ascii=False,
        ),
        board_order_json=json.dumps(list(boards.keys()), ensure_ascii=False),
        dates_json=json.dumps(dates_with_content, ensure_ascii=False),
    )
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")

    # GitHub Pages: skip Jekyll so underscore-prefixed files aren't ignored (safe default).
    (DOCS_DIR / ".nojekyll").write_text("")

    logger.info(
        "site built: %d dates, latest=%s, docs=%s",
        len(dates_with_content),
        latest,
        DOCS_DIR,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback", type=int, default=None)
    args = parser.parse_args()
    build(lookback_days=args.lookback or 7)


if __name__ == "__main__":
    main()

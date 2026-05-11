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

from digest_clock import digest_today
from source_policy import source_mix_stats, source_profile

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
SOURCE_MIX_KEYS = {
    "total",
    "google_news",
    "aggregator",
    "chinese",
    "direct",
    "wechat",
}
SOURCE_MIX_PREFIXES = ("tier_", "kind_")
SOURCE_TIER_RANK = {
    "t1": 4,
    "t1_5": 3,
    "t2": 2,
    "unknown": 0,
}
SOURCE_KIND_RANK = {
    "official": 8,
    "official_x": 7,
    "expert": 6,
    "expert_x": 6,
    "cn_official": 6,
    "cn_expert": 5,
    "media": 3,
    "community": 2,
    "google_news": 1,
}


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
        items = _sort_display_items([_with_source_metadata(item) for item in digest.get("items", [])])
        selection_stats = dict(digest.get("selection_stats") or {})
        selection_stats = _without_stale_source_mix(selection_stats)
        selection_stats.update(source_mix_stats(items))
        out["boards"][board] = {
            "display_name": bcfg.get("display_name", board),
            "items": items,
            "raw_count": digest.get("raw_count", 0),
            "selected_count": digest.get("selected_count", len(digest.get("items", []))),
            "selection_stats": selection_stats,
            "clustering_stats": digest.get("clustering_stats") or {},
            "generated_at": digest.get("generated_at", ""),
        }
    return out if any_content else None


def _without_stale_source_mix(selection_stats: dict[str, Any]) -> dict[str, Any]:
    """Drop stale source-mix counters before registry backfill recomputes them."""
    return {
        key: value
        for key, value in selection_stats.items()
        if key not in SOURCE_MIX_KEYS and not key.startswith(SOURCE_MIX_PREFIXES)
    }



def _with_source_metadata(item: dict[str, Any]) -> dict[str, Any]:
    """Backfill source registry metadata for older digest files."""
    enriched = dict(item)
    profile = source_profile(enriched)
    enriched["source_tier"] = profile.source_tier
    enriched["source_kind"] = profile.source_kind
    enriched["source_label"] = profile.source_label
    enriched["source_key"] = profile.source_key
    return enriched


def _sort_display_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Order cards by editorial value, then source authority.

    `final_score` already includes source and freshness bonuses. Tier/kind are
    tie-breakers and also keep older digest files sensible when score metadata
    is missing.
    """
    indexed = list(enumerate(items))
    indexed.sort(key=lambda pair: _display_sort_key(pair[0], pair[1]), reverse=True)
    return [item for _idx, item in indexed]


def _display_sort_key(index: int, item: dict[str, Any]) -> tuple[float, int, int, str, int]:
    return (
        _score_value(item),
        SOURCE_TIER_RANK.get(str(item.get("source_tier") or "unknown"), 0),
        SOURCE_KIND_RANK.get(str(item.get("source_kind") or "media"), 0),
        str(item.get("published") or ""),
        -index,
    )


def _score_value(item: dict[str, Any]) -> float:
    for key in ("final_score", "score", "dimension_score"):
        try:
            return float(item.get(key))
        except (TypeError, ValueError):
            continue
    return -1.0

def build(lookback_days: int = 7) -> None:
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    boards = cfg.get("boards") or {}
    site = cfg.get("site") or {}
    lookback = int(lookback_days if lookback_days is not None else site.get("lookback_days", 7))

    today = digest_today()
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
    build(lookback_days=args.lookback)


if __name__ == "__main__":
    main()

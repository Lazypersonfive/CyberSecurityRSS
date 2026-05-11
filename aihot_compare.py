"""Manual AIHOT benchmark for AI and AI-security boards.

This tool is intentionally not part of the production source pipeline. AIHOT is
used as an external benchmark to spot missed AI stories, not as a primary feed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import feedparser
import httpx

from digest_clock import digest_today

PROJECT_DIR = Path(__file__).parent
DOCS_DIR = PROJECT_DIR / "docs"
REPORTS_DIR = PROJECT_DIR / "reports"
AIHOT_BASE_URL = "https://aihot.virxact.com"
AIHOT_SELECTED_RSS_URL = f"{AIHOT_BASE_URL}/feed.xml"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 Chrome/124 Safari/537.36"
)


def fetch_aihot_selected(*, take: int = 50, timeout: int = 20) -> list[dict[str, Any]]:
    with httpx.Client(timeout=timeout, headers={"User-Agent": USER_AGENT}) as client:
        response = client.get(f"{AIHOT_BASE_URL}/api/public/items", params={"mode": "selected", "take": take})
        response.raise_for_status()
        data = response.json()
    return list(data.get("items") or [])


def fetch_aihot_rss_selected(*, timeout: int = 20) -> list[dict[str, Any]]:
    with httpx.Client(timeout=timeout, headers={"User-Agent": USER_AGENT}) as client:
        response = client.get(AIHOT_SELECTED_RSS_URL)
        response.raise_for_status()
    return parse_aihot_rss_items(response.text)


def parse_aihot_rss_items(text: str) -> list[dict[str, Any]]:
    parsed = feedparser.parse(text)
    items: list[dict[str, Any]] = []
    for entry in parsed.entries:
        items.append(
            {
                "title": str(entry.get("title") or ""),
                "url": str(entry.get("link") or ""),
                "source": "AIHOT RSS",
                "summary": _clean_html(str(entry.get("summary") or entry.get("description") or "")),
                "publishedAt": str(entry.get("published") or entry.get("updated") or ""),
            }
        )
    return items


def build_aihot_compare(
    *,
    docs_dir: Path = DOCS_DIR,
    reports_dir: Path = REPORTS_DIR,
    take: int = 50,
    source: str = "rss",
) -> Path:
    feed = json.loads((docs_dir / "feed.json").read_text(encoding="utf-8"))
    if source == "api":
        aihot_items = fetch_aihot_selected(take=take)
    elif source == "rss":
        aihot_items = fetch_aihot_rss_selected()[:take]
    else:
        raise SystemExit(f"unknown AIHOT compare source: {source}")
    comparison = compare_aihot_items(aihot_items, feed)
    comparison["source"] = source
    markdown = render_aihot_compare(comparison)
    reports_dir.mkdir(parents=True, exist_ok=True)
    out = reports_dir / "aihot_compare.md"
    out.write_text(markdown, encoding="utf-8")
    return out


def compare_aihot_items(aihot_items: list[dict[str, Any]], ours_feed: dict[str, Any]) -> dict[str, Any]:
    ours = _our_ai_items(ours_feed)
    unmatched_ours = list(ours)
    matched: list[dict[str, Any]] = []
    aihot_only: list[dict[str, Any]] = []

    for item in aihot_items:
        match = _best_match(item, unmatched_ours)
        if match is None:
            aihot_only.append(item)
            continue
        unmatched_ours.remove(match)
        matched.append(
            {
                "title": str(item.get("title") or ""),
                "url": str(item.get("url") or ""),
                "source": str(item.get("source") or ""),
                "ours_title": str(match.get("title_zh") or match.get("title_orig") or ""),
                "ours_url": str(match.get("url") or ""),
                "ours_board": str(match.get("_board") or ""),
            }
        )

    return {
        "date": str(ours_feed.get("date") or digest_today().isoformat()),
        "aihot_count": len(aihot_items),
        "ours_count": len(ours),
        "matched": matched,
        "aihot_only": aihot_only,
        "ours_only": unmatched_ours,
    }


def render_aihot_compare(comparison: dict[str, Any]) -> str:
    matched = comparison.get("matched") or []
    aihot_only = comparison.get("aihot_only") or []
    ours_only = comparison.get("ours_only") or []
    lines = [
        "# AIHOT External Benchmark",
        "",
        f"- date: {comparison.get('date')}",
        f"- source: {comparison.get('source', 'unknown')}",
        f"- AIHOT selected: {comparison.get('aihot_count')}",
        f"- Ours AI + AI Security: {comparison.get('ours_count')}",
        f"- Overlap: {len(matched)}",
        "",
        "## AIHOT-Only Candidates",
        "",
    ]
    if not aihot_only:
        lines.append("No AIHOT-only items in this sample.")
    else:
        for item in aihot_only[:15]:
            title = _clean(str(item.get("title") or ""))
            source = _clean(str(item.get("source") or ""))
            summary = _clean(str(item.get("summary") or ""))[:180]
            url = str(item.get("url") or "")
            lines.append(f"- [{title}]({url}) · {source} — {summary}")

    lines.extend(["", "## Matched Examples", ""])
    if not matched:
        lines.append("No overlap detected by URL/token heuristic.")
    else:
        for item in matched[:10]:
            title = _clean(str(item.get("title") or ""))
            ours_title = _clean(str(item.get("ours_title") or ""))
            lines.append(f"- AIHOT: {title} / Ours: {ours_title}")

    lines.extend(["", "## Ours-Only Candidates", ""])
    if not ours_only:
        lines.append("No ours-only items after matching.")
    else:
        for item in ours_only[:15]:
            title = _clean(str(item.get("title_zh") or item.get("title_orig") or ""))
            board = _clean(str(item.get("_board") or ""))
            source = _clean(str(item.get("source") or ""))
            url = str(item.get("url") or "")
            lines.append(f"- [{title}]({url}) · {board} · {source}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- AIHOT-only 高价值项应回查我们的源池或评分，而不是直接复制进生产。",
            "- Ours-only 项如果质量低，优先检查 source registry、Google News cap 和 final_score 规则。",
        ]
    )
    return "\n".join(lines) + "\n"


def _our_ai_items(feed: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for board in ("ai", "ai_security"):
        for item in ((feed.get("boards") or {}).get(board) or {}).get("items") or []:
            copied = dict(item)
            copied["_board"] = board
            rows.append(copied)
    return rows


def _best_match(aihot_item: dict[str, Any], ours: list[dict[str, Any]]) -> dict[str, Any] | None:
    aihot_url = str(aihot_item.get("url") or "")
    aihot_tokens = _entity_tokens(
        " ".join(str(aihot_item.get(k) or "") for k in ("title", "title_en", "summary", "source"))
    )
    best: tuple[float, dict[str, Any]] | None = None
    for item in ours:
        if aihot_url and aihot_url == str(item.get("url") or ""):
            return item
        item_tokens = _entity_tokens(
            " ".join(str(item.get(k) or "") for k in ("title_zh", "title_orig", "summary", "source"))
        )
        overlap = aihot_tokens & item_tokens
        if not overlap:
            continue
        score = len(overlap) / max(1, min(len(aihot_tokens), len(item_tokens)))
        if len(overlap) >= 3 and score >= 0.5 and (best is None or score > best[0]):
            best = (score, item)
    return best[1] if best else None


def _entity_tokens(text: str) -> set[str]:
    """Extract conservative entity-like tokens for cross-feed matching.

    Chinese titles share many generic two-character fragments ("发布", "模型",
    "企业"), so using CJK bigrams creates false overlap. For benchmark matching
    we only trust explicit ASCII/number entities such as OpenAI, Cerebras,
    GPT-5.5, Claude, CVE IDs, product names, and domains. URL equality remains
    the primary exact-match path.
    """
    lowered = text.lower()
    stop = {
        "ai",
        "api",
        "rss",
        "www",
        "com",
        "http",
        "https",
        "news",
        "model",
        "models",
        "agent",
        "agents",
    }
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9+._-]{2,}", lowered)
        if token not in stop and not token.isdigit()
    }


def _clean(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _clean_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value)
    text = text.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--take", type=int, default=50)
    parser.add_argument("--source", choices=["rss", "api"], default="rss")
    args = parser.parse_args()
    out = build_aihot_compare(take=args.take, source=args.source)
    print(f"AIHOT compare wrote {out}")


if __name__ == "__main__":
    main()

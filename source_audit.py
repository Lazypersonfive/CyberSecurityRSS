"""Audit source registry coverage in generated site feeds."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from digest_clock import digest_today

PROJECT_DIR = Path(__file__).parent
DOCS_DIR = PROJECT_DIR / "docs"
REPORTS_DIR = PROJECT_DIR / "reports"


@dataclass(frozen=True)
class UnknownSource:
    source: str
    board: str
    date: str
    title: str
    url: str


def build_source_audit(
    *,
    docs_dir: Path = DOCS_DIR,
    reports_dir: Path = REPORTS_DIR,
    lookback_days: int = 7,
) -> Path:
    feeds = _load_recent_feeds(docs_dir, lookback_days)
    markdown = render_source_audit(feeds)
    reports_dir.mkdir(parents=True, exist_ok=True)
    out = reports_dir / "source_audit.md"
    out.write_text(markdown, encoding="utf-8")
    return out


def render_source_audit(feeds: list[dict[str, Any]]) -> str:
    dates = [feed.get("date", "") for feed in feeds]
    board_rows: dict[str, Counter[str]] = defaultdict(Counter)
    unknowns: list[UnknownSource] = []

    for feed in feeds:
        date = str(feed.get("date") or "")
        for board, block in (feed.get("boards") or {}).items():
            items = block.get("items") or []
            row = board_rows[board]
            for item in items:
                row["items"] += 1
                tier = str(item.get("source_tier") or "unknown")
                kind = str(item.get("source_kind") or "media")
                row[f"tier_{tier}"] += 1
                row[f"kind_{kind}"] += 1
                if tier == "unknown" or item.get("source_label") == "未登记源":
                    source = str(item.get("source") or _host(item.get("url", "")) or "unknown")
                    row["unknown"] += 1
                    unknowns.append(
                        UnknownSource(
                            source=source,
                            board=board,
                            date=date,
                            title=str(item.get("title_zh") or item.get("title_orig") or ""),
                            url=str(item.get("url") or ""),
                        )
                    )

    lines = [
        "# Source Registry Audit",
        "",
        f"- generated_for: {digest_today().isoformat()}",
        f"- dates: {', '.join(dates) if dates else '-'}",
        "",
        "## Board Coverage",
        "",
        "| Board | Items | T1 | T1.5 | T2 | Unknown | Google News | Official | X | CN Expert |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for board in sorted(board_rows):
        row = board_rows[board]
        x_count = row["kind_official_x"] + row["kind_expert_x"]
        lines.append(
            "| "
            f"{board} | {row['items']} | {row['tier_t1']} | {row['tier_t1_5']} | "
            f"{row['tier_t2']} | {row['unknown']} | {row['kind_google_news']} | "
            f"{row['kind_official']} | {x_count} | {row['kind_cn_expert']} |"
        )

    lines.extend(["", "## Unknown Selected Sources", ""])
    if not unknowns:
        lines.append("No unknown selected sources in the audited window.")
    else:
        by_source: dict[str, list[UnknownSource]] = defaultdict(list)
        for item in unknowns:
            by_source[item.source].append(item)
        lines.extend(["| Source | Count | Boards | Latest Example |", "|---|---:|---|---|"])
        for source, rows in sorted(by_source.items(), key=lambda pair: (-len(pair[1]), pair[0])):
            boards = ", ".join(sorted({row.board for row in rows}))
            latest = max(rows, key=lambda row: row.date)
            title = _clean_cell(latest.title)[:80]
            url = latest.url
            example = f"[{title}]({url})" if url else title
            lines.append(f"| `{source}` | {len(rows)} | {boards} | {example} |")

    lines.extend(
        [
            "",
            "## Review Rule",
            "",
            "- 入选条目出现 `Unknown` 时，优先判断是否应加入 `source_registry.yaml`。",
            "- 如果是低质源，不要登记为高权重；应在后续 source policy / OPML 中降权或移除。",
            "- AIHOT 原则：信源分层由代码和人工维护，不交给 LLM 临场判断。",
        ]
    )
    return "\n".join(lines) + "\n"


def _load_recent_feeds(docs_dir: Path, lookback_days: int) -> list[dict[str, Any]]:
    paths = sorted(docs_dir.glob("feed_*.json"), reverse=True)[:lookback_days]
    feeds: list[dict[str, Any]] = []
    for path in paths:
        try:
            feeds.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return feeds


def _host(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").removeprefix("www.").lower()
    except ValueError:
        return ""


def _clean_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback", type=int, default=7)
    args = parser.parse_args()
    out = build_source_audit(lookback_days=args.lookback)
    print(f"source audit wrote {out}")


if __name__ == "__main__":
    main()

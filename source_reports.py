"""Human-readable source quality reports for the RSS digest pipeline."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean, median
from typing import Any, Iterable

PROJECT_DIR = Path(__file__).parent
REPORTS_DIR = PROJECT_DIR / "reports"


def render_source_report(
    board: str,
    display_name: str,
    report_date: date,
    feed_stats: dict[str, dict[str, Any]],
    entries: Iterable[dict[str, Any]],
    score_by_url: dict[str, int],
    selected_urls: set[str],
    merged_urls: Iterable[str],
) -> str:
    entries_list = list(entries)
    entry_by_url = {entry.get("url", ""): entry for entry in entries_list}

    filtered_counts: Counter[str] = Counter()
    scores_by_feed: dict[str, list[int]] = defaultdict(list)
    selected_counts: Counter[str] = Counter()
    merged_counts: Counter[str] = Counter()

    for entry in entries_list:
        feed_url = entry.get("feed_url") or ""
        if not feed_url:
            continue
        filtered_counts[feed_url] += 1
        url = entry.get("url", "")
        if url in score_by_url:
            scores_by_feed[feed_url].append(score_by_url[url])
        if url in selected_urls:
            selected_counts[feed_url] += 1

    for url in merged_urls:
        entry = entry_by_url.get(url)
        if entry:
            feed_url = entry.get("feed_url") or ""
            if feed_url:
                merged_counts[feed_url] += 1

    lines = [
        f"# {display_name} 源质量报表 {report_date.isoformat()}",
        "",
        f"- board: `{board}`",
        f"- entries: {len(entries_list)}",
        "",
        "| Feed | 抓取 | 条目 | LLM 均分 | 低分占比 | 入选 | 去重被合并 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for feed_url, stats in _sorted_feed_rows(
        feed_stats,
        scores_by_feed,
        filtered_counts,
        selected_counts,
    ):
        title = _clean_cell(stats.get("feed_title") or feed_url)
        attempted = int(stats.get("attempted") or 0)
        succeeded = int(stats.get("succeeded") or 0)
        raw_count = int(stats.get("raw_count") or 0)
        filtered_count = filtered_counts[feed_url]
        scores = scores_by_feed.get(feed_url, [])
        score_text = _format_score(scores)
        low_text = _format_low_ratio(scores)
        lines.append(
            "| "
            f"{title} | "
            f"{succeeded}/{attempted} | "
            f"{raw_count} -> {filtered_count} | "
            f"{score_text} | "
            f"{low_text} | "
            f"{selected_counts[feed_url]} | "
            f"{merged_counts[feed_url]} |"
        )

    return "\n".join(lines) + "\n"


def write_board_report(
    board: str,
    report_date: date,
    markdown: str,
    reports_dir: Path = REPORTS_DIR,
) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{board}_{report_date.isoformat()}.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def refresh_latest_report(
    report_date: date,
    board_order: list[str],
    reports_dir: Path = REPORTS_DIR,
) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    sections: list[str] = []
    for board in board_order:
        path = reports_dir / f"{board}_{report_date.isoformat()}.md"
        if path.exists():
            sections.append(path.read_text(encoding="utf-8").strip())

    latest = reports_dir / "latest.md"
    if sections:
        latest.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")
    else:
        latest.write_text(f"# 源质量报表 {report_date.isoformat()}\n\n暂无数据。\n", encoding="utf-8")
    return latest


def _sorted_feed_rows(
    feed_stats: dict[str, dict[str, Any]],
    scores_by_feed: dict[str, list[int]],
    filtered_counts: Counter[str],
    selected_counts: Counter[str],
) -> list[tuple[str, dict[str, Any]]]:
    return sorted(
        feed_stats.items(),
        key=lambda item: (
            -selected_counts[item[0]],
            -_avg_score(scores_by_feed.get(item[0], [])),
            -filtered_counts[item[0]],
            str(item[1].get("feed_title") or item[0]).lower(),
        ),
    )


def _avg_score(scores: list[int]) -> float:
    return float(mean(scores)) if scores else -1.0


def _format_score(scores: list[int]) -> str:
    if not scores:
        return "-"
    return f"{mean(scores):.1f} · {median(scores):g}"


def _format_low_ratio(scores: list[int]) -> str:
    if not scores:
        return "-"
    return f"{round(sum(1 for score in scores if score < 5) * 100 / len(scores))}%"


def _clean_cell(value: Any) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()

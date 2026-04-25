"""Human-readable source quality reports for the RSS digest pipeline."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, timedelta
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
    selection_reason_by_url: dict[str, str] | None = None,
) -> str:
    entries_list = list(entries)
    entry_by_url = {entry.get("url", ""): entry for entry in entries_list}
    selection_reason_by_url = selection_reason_by_url or {}

    filtered_counts: Counter[str] = Counter()
    scores_by_feed: dict[str, list[int]] = defaultdict(list)
    selected_counts: Counter[str] = Counter()
    merged_counts: Counter[str] = Counter()
    selected_reason_candidates: dict[str, list[tuple[int, str]]] = defaultdict(list)

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
            reason = _clean_reason(selection_reason_by_url.get(url, ""))
            if reason:
                selected_reason_candidates[feed_url].append((score_by_url.get(url, -1), reason))

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

    zero_feed_count = 0
    zero_attempted = 0
    zero_succeeded = 0
    selected_reasons: list[tuple[str, str]] = []

    for feed_url, stats in _sorted_feed_rows(
        feed_stats,
        scores_by_feed,
        filtered_counts,
        selected_counts,
    ):
        raw_count = int(stats.get("raw_count") or 0)
        filtered_count = filtered_counts[feed_url]
        if raw_count == 0 and filtered_count == 0:
            zero_feed_count += 1
            zero_attempted += int(stats.get("attempted") or 0)
            zero_succeeded += int(stats.get("succeeded") or 0)
            continue

        title = _clean_cell(stats.get("feed_title") or feed_url)
        attempted = int(stats.get("attempted") or 0)
        succeeded = int(stats.get("succeeded") or 0)
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
        reason = _best_reason(selected_reason_candidates.get(feed_url, []))
        if reason:
            selected_reasons.append((title, reason))

    if zero_feed_count:
        lines.extend(
            [
                "",
                f"另有 {zero_feed_count} 个源今日 0 条目（{zero_succeeded}/{zero_attempted} 抓取成功）。",
            ]
        )

    if selected_reasons:
        lines.extend(["", "## 入选理由摘录"])
        for title, reason in selected_reasons:
            lines.append(f"- **{title}**：*为什么入选：{reason}*")

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
        else:
            sections.append(f"# {board} 源质量报表 {report_date.isoformat()}\n\n未生成报表。")

    latest = reports_dir / "latest.md"
    if sections:
        latest.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")
    else:
        latest.write_text(f"# 源质量报表 {report_date.isoformat()}\n\n暂无数据。\n", encoding="utf-8")
    return latest


def refresh_weekly_report(
    report_date: date,
    board_order: list[str],
    reports_dir: Path = REPORTS_DIR,
    days: int = 7,
) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    start_date = report_date - timedelta(days=days - 1)
    lines = [
        f"# 7 日源质量汇总 {start_date.isoformat()} 至 {report_date.isoformat()}",
        "",
        "只聚合每日源质量报表中展开的有条目源；零条目源请看各日报尾部汇总。",
    ]

    for board in board_order:
        rows: dict[str, dict[str, Any]] = {}
        display_name = board
        for offset in range(days):
            current = start_date + timedelta(days=offset)
            path = reports_dir / f"{board}_{current.isoformat()}.md"
            if not path.exists():
                continue
            body = path.read_text(encoding="utf-8")
            display_name = _report_display_name(body, board)
            for parsed in _parse_report_rows(body):
                if parsed["raw"] == 0:
                    continue
                row = rows.setdefault(
                    parsed["feed"],
                    {
                        "attempted": 0,
                        "succeeded": 0,
                        "raw": 0,
                        "score_total": 0.0,
                        "score_weight": 0,
                        "selected": 0,
                        "merged": 0,
                    },
                )
                row["succeeded"] += parsed["succeeded"]
                row["attempted"] += parsed["attempted"]
                row["raw"] += parsed["raw"]
                row["score_total"] += parsed["avg_score"] * parsed["filtered"]
                row["score_weight"] += parsed["filtered"]
                row["selected"] += parsed["selected"]
                row["merged"] += parsed["merged"]

        lines.extend(["", f"## {display_name}", "", "| Feed | 抓取 | Raw | LLM 均分 | 入选总数 | 合并总数 |", "|---|---:|---:|---:|---:|---:|"])
        if not rows:
            lines.append("| - | - | - | - | - | - |")
            continue

        for feed, row in sorted(
            rows.items(),
            key=lambda item: (
                -int(item[1]["selected"]),
                -float(item[1]["score_total"] / item[1]["score_weight"]) if item[1]["score_weight"] else -1.0,
                -int(item[1]["raw"]),
                item[0].lower(),
            ),
        ):
            avg_score = "-"
            if row["score_weight"]:
                avg_score = f"{row['score_total'] / row['score_weight']:.1f}"
            lines.append(
                "| "
                f"{_clean_cell(feed)} | "
                f"{row['succeeded']}/{row['attempted']} | "
                f"{row['raw']} | "
                f"{avg_score} | "
                f"{row['selected']} | "
                f"{row['merged']} |"
            )

    weekly = reports_dir / "weekly.md"
    weekly.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return weekly


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


def _clean_reason(value: Any) -> str:
    return _clean_cell(value)[:30]


def _best_reason(candidates: list[tuple[int, str]]) -> str:
    if not candidates:
        return ""
    return max(candidates, key=lambda item: item[0])[1]


def _report_display_name(body: str, fallback: str) -> str:
    first_line = body.splitlines()[0] if body.splitlines() else ""
    prefix = "# "
    marker = " 源质量报表 "
    if first_line.startswith(prefix) and marker in first_line:
        return first_line[len(prefix):first_line.index(marker)]
    return fallback


def _parse_report_rows(body: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in body.splitlines():
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7 or cells[0] == "Feed":
            continue
        succeeded, attempted = _parse_ratio(cells[1])
        raw_count, filtered_count = _parse_counts(cells[2])
        avg_score = _parse_avg_score(cells[3])
        rows.append(
            {
                "feed": cells[0],
                "succeeded": succeeded,
                "attempted": attempted,
                "raw": raw_count,
                "filtered": filtered_count,
                "avg_score": avg_score,
                "selected": _parse_int(cells[5]),
                "merged": _parse_int(cells[6]),
            }
        )
    return rows


def _parse_ratio(value: str) -> tuple[int, int]:
    left, _, right = value.partition("/")
    return _parse_int(left), _parse_int(right)


def _parse_counts(value: str) -> tuple[int, int]:
    left, _, right = value.partition("->")
    return _parse_int(left), _parse_int(right)


def _parse_avg_score(value: str) -> float:
    if value == "-":
        return 0.0
    left = value.split("·", 1)[0].strip()
    try:
        return float(left)
    except ValueError:
        return 0.0


def _parse_int(value: str) -> int:
    try:
        return int(value.strip())
    except ValueError:
        return 0

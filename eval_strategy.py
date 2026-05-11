"""Offline evaluation for board targets and source-mix health."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from digest_clock import digest_today

PROJECT_DIR = Path(__file__).parent
DOCS_DIR = PROJECT_DIR / "docs"
REPORTS_DIR = PROJECT_DIR / "reports"
CONFIG_PATH = PROJECT_DIR / "config.yaml"


@dataclass(frozen=True)
class BoardEval:
    board: str
    display_name: str
    days: int
    avg_selected: float
    target_top_n: int
    full_days: int
    avg_chinese: float
    min_chinese: int
    cn_ok_days: int
    avg_google_news: float
    max_google_news: int | None
    unknown_items: int
    avg_final_score: float | None
    merged_total: int
    tier_counts: Counter[str]
    kind_counts: Counter[str]


@dataclass(frozen=True)
class EvalMiss:
    date: str
    board: str
    selected: int
    target_top_n: int
    chinese: int
    min_chinese: int
    google_news: int
    max_google_news: int | None
    unknown: int


def build_offline_eval(
    *,
    docs_dir: Path = DOCS_DIR,
    reports_dir: Path = REPORTS_DIR,
    config_path: Path = CONFIG_PATH,
    lookback_days: int = 7,
) -> Path:
    feeds = _load_recent_feeds(docs_dir, lookback_days)
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    markdown = render_offline_eval(feeds, cfg)
    reports_dir.mkdir(parents=True, exist_ok=True)
    out = reports_dir / "offline_eval.md"
    out.write_text(markdown, encoding="utf-8")
    return out


def render_offline_eval(feeds: list[dict[str, Any]], cfg: dict[str, Any]) -> str:
    board_cfgs = cfg.get("boards") or {}
    evaluations, misses = _evaluate_boards(feeds, board_cfgs)
    dates = [str(feed.get("date") or "") for feed in feeds]

    lines = [
        "# Offline Strategy Eval",
        "",
        f"- generated_for: {digest_today().isoformat()}",
        f"- dates: {', '.join(dates) if dates else '-'}",
        "",
        "## Board Health",
        "",
        (
            "| Board | Name | Days | Avg Selected | Target | Full Days | Avg CN | "
            "Min CN | CN OK Days | Avg GN | Max GN | Unknown | Avg Final | Merged |"
        ),
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for evaluation in evaluations:
        max_gn = "-" if evaluation.max_google_news is None else str(evaluation.max_google_news)
        lines.append(
            "| "
            f"{evaluation.board} | {evaluation.display_name} | {evaluation.days} | "
            f"{evaluation.avg_selected:.1f} | {evaluation.target_top_n} | "
            f"{evaluation.full_days}/{evaluation.days} | {evaluation.avg_chinese:.1f} | "
            f"{evaluation.min_chinese} | {evaluation.cn_ok_days}/{evaluation.days} | "
            f"{evaluation.avg_google_news:.1f} | {max_gn} | {evaluation.unknown_items} | "
            f"{_format_optional_float(evaluation.avg_final_score)} | {evaluation.merged_total} |"
        )

    lines.extend(
        [
            "",
            "## Source Mix",
            "",
            "| Board | T1 | T1.5 | T2 | Unknown | Official | X | Google News | CN Expert | Community |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for evaluation in evaluations:
        tiers = evaluation.tier_counts
        kinds = evaluation.kind_counts
        x_count = kinds["official_x"] + kinds["expert_x"]
        lines.append(
            "| "
            f"{evaluation.board} | {tiers['t1']} | {tiers['t1_5']} | {tiers['t2']} | "
            f"{tiers['unknown']} | {kinds['official']} | {x_count} | "
            f"{kinds['google_news']} | {kinds['cn_expert']} | {kinds['community']} |"
        )

    lines.extend(["", "## Target Misses", ""])
    if not misses:
        lines.append("No target misses in the audited window.")
    else:
        for miss in misses:
            parts = [
                f"{miss.date} {miss.board}：selected {miss.selected}/{miss.target_top_n}",
            ]
            if miss.min_chinese:
                parts.append(f"中文 {miss.chinese}/{miss.min_chinese}")
            if miss.max_google_news is not None and miss.google_news > miss.max_google_news:
                parts.append(f"Google News {miss.google_news}/{miss.max_google_news}")
            if miss.unknown:
                parts.append(f"unknown {miss.unknown}")
            lines.append(f"- {'，'.join(parts)}")

    lines.extend(
        [
            "",
            "## Read This",
            "",
            "- `Full Days` 低说明该板块供给或 caps 仍不足。",
            "- `CN OK Days` 低说明中文源目标没有稳定满足，应优先检查源池而不是继续调 prompt。",
            "- `Unknown > 0` 必须先登记或降权；否则 final_score 无法稳定接管。",
        ]
    )
    return "\n".join(lines) + "\n"


def _evaluate_boards(
    feeds: list[dict[str, Any]],
    board_cfgs: dict[str, Any],
) -> tuple[list[BoardEval], list[EvalMiss]]:
    daily: dict[str, list[tuple[str, dict[str, int], int, float | None, int]]] = defaultdict(list)
    misses: list[EvalMiss] = []

    for feed in feeds:
        date = str(feed.get("date") or "")
        for board, block in (feed.get("boards") or {}).items():
            cfg = board_cfgs.get(board) or {}
            stats = _stats_for_block(block)
            selected = stats["total"]
            daily[board].append((date, stats, selected, _avg_final_score(block), _clustering_merged_total(block)))

            target_top_n = int(cfg.get("top_n") or selected)
            policy = cfg.get("source_policy") or {}
            min_chinese = int(policy.get("min_chinese") or 0)
            max_google_news = _optional_int(policy.get("max_google_news"))
            failed = (
                selected < target_top_n
                or (min_chinese and stats["chinese"] < min_chinese)
                or (max_google_news is not None and stats["google_news"] > max_google_news)
                or stats["tier_unknown"] > 0
            )
            if failed:
                misses.append(
                    EvalMiss(
                        date=date,
                        board=board,
                        selected=selected,
                        target_top_n=target_top_n,
                        chinese=stats["chinese"],
                        min_chinese=min_chinese,
                        google_news=stats["google_news"],
                        max_google_news=max_google_news,
                        unknown=stats["tier_unknown"],
                    )
                )

    evaluations: list[BoardEval] = []
    for board in sorted(daily):
        cfg = board_cfgs.get(board) or {}
        policy = cfg.get("source_policy") or {}
        target_top_n = int(cfg.get("top_n") or 0)
        min_chinese = int(policy.get("min_chinese") or 0)
        max_google_news = _optional_int(policy.get("max_google_news"))
        rows = daily[board]
        days = len(rows)
        total_selected = sum(selected for _date, _stats, selected, _avg_final, _merged in rows)
        total_chinese = sum(stats["chinese"] for _date, stats, _selected, _avg_final, _merged in rows)
        total_google_news = sum(stats["google_news"] for _date, stats, _selected, _avg_final, _merged in rows)
        final_score_values = [
            avg_final
            for _date, _stats, _selected, avg_final, _merged in rows
            if avg_final is not None
        ]
        tier_counts: Counter[str] = Counter()
        kind_counts: Counter[str] = Counter()
        for _date, stats, _selected, _avg_final, _merged in rows:
            for key, value in stats.items():
                if key.startswith("tier_"):
                    tier_counts[key.removeprefix("tier_")] += value
                elif key.startswith("kind_"):
                    kind_counts[key.removeprefix("kind_")] += value

        evaluations.append(
            BoardEval(
                board=board,
                display_name=str(cfg.get("display_name") or board),
                days=days,
                avg_selected=total_selected / days if days else 0.0,
                target_top_n=target_top_n,
                full_days=sum(1 for _date, _stats, selected, _avg_final, _merged in rows if selected >= target_top_n),
                avg_chinese=total_chinese / days if days else 0.0,
                min_chinese=min_chinese,
                cn_ok_days=sum(
                    1
                    for _date, stats, _selected, _avg_final, _merged in rows
                    if not min_chinese or stats["chinese"] >= min_chinese
                ),
                avg_google_news=total_google_news / days if days else 0.0,
                max_google_news=max_google_news,
                unknown_items=tier_counts["unknown"],
                avg_final_score=sum(final_score_values) / len(final_score_values) if final_score_values else None,
                merged_total=sum(merged for _date, _stats, _selected, _avg_final, merged in rows),
                tier_counts=tier_counts,
                kind_counts=kind_counts,
            )
        )

    return evaluations, misses


def _stats_for_block(block: dict[str, Any]) -> Counter[str]:
    stats = Counter({str(k): int(v) for k, v in (block.get("selection_stats") or {}).items() if _is_int(v)})
    items = block.get("items") or []
    if not stats.get("total"):
        stats["total"] = len(items)
    if not any(key.startswith("tier_") or key.startswith("kind_") for key in stats):
        for item in items:
            tier = str(item.get("source_tier") or "unknown")
            kind = str(item.get("source_kind") or "media")
            stats[f"tier_{tier}"] += 1
            stats[f"kind_{kind}"] += 1
    return stats


def _avg_final_score(block: dict[str, Any]) -> float | None:
    values = [
        float(item["final_score"])
        for item in (block.get("items") or [])
        if _is_number(item.get("final_score"))
    ]
    if not values:
        return None
    return sum(values) / len(values)


def _clustering_merged_total(block: dict[str, Any]) -> int:
    stats = block.get("clustering_stats") or {}
    value = stats.get("merged_total")
    if _is_int(value):
        return int(value)
    return 0


def _load_recent_feeds(docs_dir: Path, lookback_days: int) -> list[dict[str, Any]]:
    paths = sorted(docs_dir.glob("feed_*.json"), reverse=True)[:lookback_days]
    feeds: list[dict[str, Any]] = []
    for path in paths:
        try:
            feeds.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return feeds


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    parsed = int(value)
    return parsed if parsed >= 0 else None


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    return isinstance(value, int | float)


def _format_optional_float(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.1f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback", type=int, default=7)
    args = parser.parse_args()
    out = build_offline_eval(lookback_days=args.lookback)
    print(f"offline eval wrote {out}")


if __name__ == "__main__":
    main()

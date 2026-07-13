"""Generate a human-feedback evaluation report without changing production policy."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import timedelta
from pathlib import Path
from typing import Any

from digest_clock import digest_today

PROJECT_DIR = Path(__file__).parent
FEEDBACK_DIR = PROJECT_DIR / "feedback"
DIGEST_DIR = PROJECT_DIR / "digest"
OUTPUT_DIR = PROJECT_DIR / "output"
REPORTS_DIR = PROJECT_DIR / "reports"
WEEKLY_START = "<!-- feedback-summary:start -->"
WEEKLY_END = "<!-- feedback-summary:end -->"


def load_feedback(days: int = 14) -> list[dict[str, Any]]:
    end = digest_today()
    wanted = {(end - timedelta(days=offset)).isoformat() for offset in range(max(1, days))}
    records: list[dict[str, Any]] = []
    for path in sorted(FEEDBACK_DIR.glob("*.jsonl")):
        if path.stem not in wanted:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                records.append({"date": path.stem, "action": "invalid", "reason": f"line {line_no}: {exc}"})
                continue
            records.append(record)
    return records


def classify_feedback(record: dict[str, Any]) -> str:
    board = str(record.get("board") or "")
    url = str(record.get("url") or "")
    if not board or not url:
        return "invalid"
    if _url_in_digest(board, url):
        return "selected"
    if _url_in_latest_output(board, url):
        return "fetched_not_selected"
    return "not_found_recent_artifacts"


def build_report(records: list[dict[str, Any]]) -> str:
    lines = ["# Human Feedback Eval", ""]
    if not records:
        lines.extend([
            "最近窗口内没有人工反馈。",
            "",
            "建议先用 `python feedback_cli.py add ...` 记录 3-5 条明确反馈，再调整源权重或策略。",
        ])
        return "\n".join(lines) + "\n"

    by_action = Counter(str(r.get("action") or "") for r in records)
    by_board = Counter(str(r.get("board") or "") for r in records)
    by_stage = Counter(classify_feedback(r) for r in records)
    source_actions: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for record in records:
        source = str(record.get("source") or _host(str(record.get("url") or "")) or "unknown")
        board = str(record.get("board") or "unknown")
        action = str(record.get("action") or "unknown")
        source_actions[(board, source)][action] += 1

    lines.extend(["## Summary", ""])
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.extend(f"| action:{key} | {value} |" for key, value in sorted(by_action.items()))
    lines.extend(f"| board:{key} | {value} |" for key, value in sorted(by_board.items()))
    lines.extend(f"| stage:{key} | {value} |" for key, value in sorted(by_stage.items()))
    lines.append("")

    lines.extend(["## Items", ""])
    lines.append("| Date | Board | Action | Stage | Source | Title/URL | Reason |")
    lines.append("|---|---|---|---|---|---|---|")
    for record in records:
        title = str(record.get("title_zh") or record.get("url") or "")
        lines.append(
            "| {date} | {board} | {action} | {stage} | {source} | {title} | {reason} |".format(
                date=_cell(record.get("date")),
                board=_cell(record.get("board")),
                action=_cell(record.get("action")),
                stage=classify_feedback(record),
                source=_cell(record.get("source") or _host(str(record.get("url") or ""))),
                title=_cell(title),
                reason=_cell(record.get("reason")),
            )
        )
    lines.append("")

    recommendations = _recommendations(source_actions)
    lines.extend(["## Recommendations", ""])
    if recommendations:
        lines.extend(f"- {item}" for item in recommendations)
    else:
        lines.append("- 暂无足够重复信号；单条反馈只记录，不直接调权。")
    lines.append("")
    lines.append("所有建议都只供人工 review；本脚本不修改 `config.yaml` 或 `source_registry.yaml`。")
    return "\n".join(lines) + "\n"


def write_report(days: int = 14) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / "feedback_eval.md"
    records = load_feedback(days)
    path.write_text(build_report(records), encoding="utf-8")
    sync_weekly_feedback(records, REPORTS_DIR / "weekly.md")
    return path


def sync_weekly_feedback(records: list[dict[str, Any]], weekly_path: Path) -> None:
    if not weekly_path.exists():
        return
    body = weekly_path.read_text(encoding="utf-8")
    if WEEKLY_START in body:
        body = body.split(WEEKLY_START, 1)[0].rstrip()
    actions = Counter(str(record.get("action") or "invalid") for record in records)
    boards = Counter(str(record.get("board") or "unknown") for record in records)
    lines = [
        body,
        "",
        WEEKLY_START,
        "## 人工反馈（最近 14 天）",
        "",
    ]
    if not records:
        lines.append("- 暂无反馈；可在站点点击“有用 / 不想看 / 摘要有问题”后导出 JSONL。")
    else:
        lines.append(f"- 总计：{len(records)} 条")
        lines.append("- 动作：" + "，".join(f"{key}={value}" for key, value in sorted(actions.items())))
        lines.append("- 板块：" + "，".join(f"{key}={value}" for key, value in sorted(boards.items())))
    lines.extend([WEEKLY_END, ""])
    weekly_path.write_text("\n".join(lines), encoding="utf-8")


def _url_in_digest(board: str, url: str) -> bool:
    for path in DIGEST_DIR.glob(f"{board}_*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if any(item.get("url") == url for item in data.get("items") or []):
            return True
    return False


def _url_in_latest_output(board: str, url: str) -> bool:
    path = OUTPUT_DIR / f"{board}_latest.json"
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return any(item.get("url") == url for item in data.get("entries") or [])


def _recommendations(source_actions: dict[tuple[str, str], Counter[str]]) -> list[str]:
    items: list[str] = []
    for (board, source), counter in sorted(source_actions.items()):
        positive = counter["upvote"] + counter["must_include"]
        negative = counter["downvote"] + counter["bad_source"]
        if positive >= 3:
            items.append(f"[{board}] `{source}` 收到 {positive} 次正反馈：考虑提高 source cap 或登记更准确 tier/kind。")
        if negative >= 3:
            items.append(f"[{board}] `{source}` 收到 {negative} 次负反馈：考虑降低 source cap、降权或移出 OPML。")
        if counter["bad_summary"] >= 3:
            items.append(f"[{board}] `{source}` 摘要问题 ≥3 次：优先检查该板块摘要 prompt 或原文抽取质量。")
    return items


def _host(url: str) -> str:
    from urllib.parse import urlparse

    return (urlparse(url).hostname or "").removeprefix("www.")


def _cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=14)
    args = parser.parse_args()
    print(write_report(args.days))


if __name__ == "__main__":
    main()

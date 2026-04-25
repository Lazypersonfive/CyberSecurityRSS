"""LLM pipeline (Gemini backend): score + summarize with Gemini 2.5 Flash.

Reads output/<board>_latest.json and writes digest/<board>_YYYY-MM-DD.json.

Usage:
    python digest_pipeline_gemini.py --board security
    python digest_pipeline_gemini.py --board ai
    python digest_pipeline_gemini.py --board finance

Environment:
    GEMINI_API_KEY (required)

Cost: Gemini 2.5 Flash is ~$0.075/M input, $0.30/M output. A full 3-board run
touching ~200 entries costs roughly $0.02-0.05/day.
"""

import argparse
import json
import logging
import os
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

from digest_clock import digest_today
from digest_postprocess import normalize_summary_text, summary_needs_repair
from digest_postprocess import count_chinese_chars, SUMMARY_TARGET_MAX_CHARS, SUMMARY_TARGET_MIN_CHARS
from source_reports import refresh_latest_report, render_source_report, write_board_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).parent
CONFIG_PATH = PROJECT_DIR / "config.yaml"
OUTPUT_DIR = PROJECT_DIR / "output"
DIGEST_DIR = PROJECT_DIR / "digest"

SCORE_MODEL = "gemini-3-flash-preview"
SUMMARIZE_MODEL = "gemini-3-flash-preview"

SCORE_BATCH_SIZE = 40
SUMMARIZE_BATCH_SIZE = 8

MAX_RETRIES = 3
RETRY_BACKOFF_SEC = 4

BOARD_SCORE_SYSTEM = {
    "security": """你是资深网安分析师，对安全资讯做 0-10 打分。
评分标准：
- 9-10: 在野利用 0day、重大 APT 活动、大规模供应链攻击
- 7-8: 新型攻击技术、高危 CVE 详解、红蓝工具发布、关键威胁情报
- 5-6: 安全研究、技术博客、可观察性分析
- 0-4: 招聘、营销软文、职业规划、入门求助帖
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
    "ai": """你是 AI 产业观察者，对 AI 资讯做 0-10 打分。
评分标准：
- 9-10: 主流实验室（Anthropic/OpenAI/Google/Meta/DeepSeek 等）重大模型发布、里程碑论文、Agentic 能力突破、产业格局级新闻
- 7-8: 有实质技术增益的开源模型、能力评测、应用层关键动态、监管与安全政策
- 5-6: 技术博客、一般产品更新、行业分析
- 0-4: 纯营销 PR、个人观点水文、融资新闻（无技术细节）、招聘/培训广告
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
    "finance": """你是金融科技观察者，关注金融机构（尤其是头部银行、支付网络、卡组织）
的真实科技动作。对资讯做 0-10 打分。
评分标准：
- 9-10: 大行核心系统升级、支付网络战略动作（Visa/Mastercard/Stripe/中国顶级银行）、监管拐点、CBDC / 稳定币关键进展
- 7-8: 具体技术合作、区域性支付新基建、金融 AI / 风控落地案例、关键数据披露
- 5-6: 产品发布、一般性行业动态、高质量行业分析
- 0-4: 融资 PR、营销软文、泛观点文章
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
}

SUMMARIZE_SYSTEM = """你是一位科技资讯编辑。你的任务是把给定的新闻原文加工成中文摘要卡片。
严格规则：
1. 所有输出字段使用简体中文（即便原文是英文）。
2. 摘要只使用原文提供的信息，不得补充外部知识、不得猜测、不得夸大。
3. 中文标题不超过 28 字，去除所有客套词和营销语。
4. 摘要必须是 220-260 个汉字，不是英文字符数；写成 2-3 句，先讲发生了什么，再讲为什么值得关注 / 对谁有影响。
5. tags 给 1-3 个中文关键词，每个不超过 6 字。
6. selection_reason 用不超过 30 个中文字符说明这条新闻为何值得关注。
7. 严格按 JSON 数组返回，不要解释、不要 Markdown 包裹。
输出格式：[{"idx":0,"title_zh":"...","summary":"...","tags":["..."],"selection_reason":"..."}]"""

REPAIR_SUMMARIZE_SYSTEM = """你要修正新闻摘要的长度问题。
严格规则：
1. 只依据给定原文信息改写，不得补充外部知识。
2. 只输出 summary 字段，必须是 220-260 个汉字。
3. 使用简体中文，2-3 句，不要项目符号，不要解释。
4. 如果原草稿太短，就补足关键事实、影响对象和关注原因；如果太长，就压缩但保留核心信息。
输出格式：[{"idx":0,"summary":"..."}]"""

REPAIR_TITLE_SYSTEM = """你要把英文新闻标题译成简体中文短标题。
严格规则：
1. 只依据原文信息翻译，不得补充外部知识、不得夸张。
2. 输出标题必须是简体中文，≤28 字，去除客套词和营销语。
3. 严格按 JSON 数组返回：[{"idx":0,"title_zh":"..."}]"""

DEDUPE_SYSTEM = """你要对新闻条目做去重聚类。
判断规则：
1. 多条报道如果讲的是同一件事（同一次发布、同一份研究、同一起事件），即便角度不同、措辞不同、来源不同，视为同一组。
2. 同一家公司 / 监管机构在不同地区发的同一公告，视为同一组。
3. 主语相同但事件不同（例如都提到 OpenAI，一条讲融资、一条讲模型），视为不同组。
4. 不确定时倾向于视为不同组，避免误合并独立新闻。
输出严格按 JSON 数组返回聚类结果，例如 [[0,3,7],[1],[2,5]]，每个 idx 必须且仅出现一次。不要解释、不要 Markdown 包裹。"""

DEDUPE_POOL_MULTIPLIER = 2
DEDUPE_MAX_CANDIDATES = 80


def _load_config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def _load_input(board: str) -> dict[str, Any]:
    path = OUTPUT_DIR / f"{board}_latest.json"
    if not path.exists():
        raise SystemExit(f"{path} missing — run fetch_and_save.py --board {board} first")
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_llm_json(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip("` \n")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Gemini occasionally returns concatenated JSON. Extract first balanced array.
        start = raw.find("[")
        if start < 0:
            raise
        depth = 0
        in_str = False
        esc = False
        for i, ch in enumerate(raw[start:], start=start):
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return json.loads(raw[start : i + 1])
        raise


def _generate_json(
    client: genai.Client,
    model: str,
    system: str,
    user_prompt: str,
    max_output_tokens: int,
) -> str:
    cfg = types.GenerateContentConfig(
        system_instruction=system,
        temperature=0.2,
        max_output_tokens=max_output_tokens,
        response_mime_type="application/json",
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )
    last_exc: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=cfg,
            )
            text = resp.text or ""
            if not text.strip():
                raise RuntimeError("empty response text")
            return text
        except (genai_errors.APIError, RuntimeError) as exc:
            last_exc = exc
            wait = RETRY_BACKOFF_SEC * (attempt + 1)
            logger.warning("gemini call failed (attempt %d/%d): %s — retry in %ds",
                           attempt + 1, MAX_RETRIES, exc, wait)
            time.sleep(wait)
    raise RuntimeError(f"gemini call exhausted retries: {last_exc}")


def _score_entries(
    client: genai.Client, board: str, entries: list[dict[str, Any]]
) -> list[int]:
    system = BOARD_SCORE_SYSTEM[board]
    scores: list[int] = [0] * len(entries)
    for i in range(0, len(entries), SCORE_BATCH_SIZE):
        batch = entries[i : i + SCORE_BATCH_SIZE]
        items = [
            {
                "idx": j,
                "title": e.get("title", ""),
                "summary": (e.get("summary") or "")[:240],
                "category": e.get("category", ""),
            }
            for j, e in enumerate(batch)
        ]
        user_prompt = (
            "对以下条目逐一打分。\n"
            f"条目：\n{json.dumps(items, ensure_ascii=False)}"
        )
        try:
            text = _generate_json(client, SCORE_MODEL, system, user_prompt, 2000)
            parsed = _parse_llm_json(text)
            smap = {int(r["idx"]): int(r["score"]) for r in parsed}
        except Exception as exc:
            logger.warning("score parse failed (batch %d): %s", i, exc)
            smap = {}
        for j in range(len(batch)):
            scores[i + j] = smap.get(j, 5)
    return scores


def _summarize(
    client: genai.Client, entries: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for i in range(0, len(entries), SUMMARIZE_BATCH_SIZE):
        batch = entries[i : i + SUMMARIZE_BATCH_SIZE]
        payload = [
            {
                "idx": j,
                "title": e.get("title", ""),
                "summary": (e.get("summary") or "")[:1200],
                "url": e.get("url", ""),
                "source_category": e.get("category", ""),
            }
            for j, e in enumerate(batch)
        ]
        user_prompt = (
            "以下是需要加工的原始新闻。按系统指令返回 JSON 数组。\n\n"
            f"输入：\n{json.dumps(payload, ensure_ascii=False)}"
        )
        smap: dict[int, Any] = {}
        for retry in range(2):
            try:
                text = _generate_json(client, SUMMARIZE_MODEL, SUMMARIZE_SYSTEM, user_prompt, 6000)
                parsed = _parse_llm_json(text)
                smap = {int(r["idx"]): r for r in parsed}
                break
            except Exception as exc:
                logger.warning("summarize parse failed (batch %d, retry %d): %s", i, retry, exc)

        repaired_summaries = _repair_summaries(client, batch, smap)
        repaired_titles = _repair_titles(client, batch, smap)

        for j, e in enumerate(batch):
            s = smap.get(j, {})
            results.append(
                {
                    "title_zh": repaired_titles.get(j, (s.get("title_zh") or e.get("title", "")).strip()[:40]),
                    "title_orig": e.get("title", ""),
                    "summary": repaired_summaries.get(j, normalize_summary_text(s.get("summary") or "")),
                    "tags": s.get("tags") or [],
                    "url": e.get("url", ""),
                    "source": _infer_source(e.get("url", "")),
                    "category": e.get("category", ""),
                    "published": e.get("published", ""),
                    "cve_ids": e.get("cve_ids", []),
                    "selection_reason": _selection_reason(s),
                }
            )
    return results


def _selection_reason(item: dict[str, Any]) -> str:
    reason = normalize_summary_text(item.get("selection_reason") or "")
    return reason[:30]


def _repair_summaries(
    client: genai.Client,
    batch: list[dict[str, Any]],
    smap: dict[int, dict[str, Any]],
) -> dict[int, str]:
    repaired = {
        idx: normalize_summary_text(item.get("summary") or "")
        for idx, item in smap.items()
    }
    to_fix = []
    for idx, entry in enumerate(batch):
        summary = repaired.get(idx, "")
        if summary_needs_repair(summary):
            to_fix.append(
                {
                    "idx": idx,
                    "title": entry.get("title", ""),
                    "source_summary": (entry.get("summary") or "")[:1200],
                    "draft_summary": summary,
                }
            )
    if not to_fix:
        return repaired

    for _attempt in range(3):
        pending = []
        for row in to_fix:
            current = repaired.get(row["idx"], row["draft_summary"])
            if summary_needs_repair(current):
                pending.append(
                    {
                        **row,
                        "draft_summary": current,
                        "current_chinese_chars": count_chinese_chars(current),
                        "target_range": f"{SUMMARY_TARGET_MIN_CHARS}-{SUMMARY_TARGET_MAX_CHARS}",
                    }
                )
        if not pending:
            break

        user_prompt = (
            "以下摘要长度不符合要求，请逐条改写。\n"
            f"输入：\n{json.dumps(pending, ensure_ascii=False)}"
        )
        try:
            text = _generate_json(client, SUMMARIZE_MODEL, REPAIR_SUMMARIZE_SYSTEM, user_prompt, 4000)
            parsed = _parse_llm_json(text)
            for row in parsed:
                idx = int(row["idx"])
                repaired[idx] = normalize_summary_text(row.get("summary") or repaired.get(idx, ""))
        except Exception as exc:
            logger.warning("summary repair parse failed: %s", exc)
            break
    return repaired


def _title_needs_repair(title: str) -> bool:
    text = (title or "").strip()
    if not text:
        return True
    return count_chinese_chars(text) == 0


def _repair_titles(
    client: genai.Client,
    batch: list[dict[str, Any]],
    smap: dict[int, dict[str, Any]],
) -> dict[int, str]:
    repaired: dict[int, str] = {}
    for idx, item in smap.items():
        title = (item.get("title_zh") or "").strip()
        if title:
            repaired[idx] = title

    to_fix = []
    for idx, entry in enumerate(batch):
        current = repaired.get(idx, "")
        if _title_needs_repair(current):
            to_fix.append(
                {
                    "idx": idx,
                    "title": entry.get("title", ""),
                    "source_summary": (entry.get("summary") or "")[:600],
                    "draft_title": current,
                }
            )
    if not to_fix:
        return repaired

    for _attempt in range(3):
        pending = [row for row in to_fix if _title_needs_repair(repaired.get(row["idx"], row["draft_title"]))]
        if not pending:
            break
        user_prompt = (
            "以下标题不是简体中文或缺失，请逐条翻译。\n"
            f"输入：\n{json.dumps(pending, ensure_ascii=False)}"
        )
        try:
            text = _generate_json(client, SUMMARIZE_MODEL, REPAIR_TITLE_SYSTEM, user_prompt, 1500)
            parsed = _parse_llm_json(text)
            for row in parsed:
                idx = int(row["idx"])
                zh = (row.get("title_zh") or "").strip()
                if zh:
                    repaired[idx] = zh[:40]
        except Exception as exc:
            logger.warning("title repair parse failed: %s", exc)
            break
    return repaired


def _llm_dedupe(
    client: genai.Client,
    candidates: list[tuple[dict[str, Any], int]],
) -> tuple[list[tuple[dict[str, Any], int]], list[str]]:
    """Cluster same-story items via Gemini and keep the highest-scored per cluster.

    candidates are (entry, score) tuples already sorted by score desc.
    """
    if len(candidates) <= 1:
        return candidates, []

    payload = [
        {
            "idx": i,
            "title": e.get("title", ""),
            "source": _infer_source(e.get("url", "")),
            "published": (e.get("published") or "")[:10],
        }
        for i, (e, _sc) in enumerate(candidates)
    ]
    user_prompt = (
        "对以下新闻条目做去重聚类。\n"
        f"输入：\n{json.dumps(payload, ensure_ascii=False)}"
    )

    clusters: list[list[int]] | None = None
    try:
        text = _generate_json(client, SUMMARIZE_MODEL, DEDUPE_SYSTEM, user_prompt, 4000)
        parsed = _parse_llm_json(text)
        if isinstance(parsed, list) and all(isinstance(g, list) for g in parsed):
            clusters = [[int(x) for x in g] for g in parsed]
    except Exception as exc:
        logger.warning("llm dedupe parse failed: %s — keeping originals", exc)

    if not clusters:
        return candidates, []

    seen: set[int] = set()
    result: list[tuple[dict[str, Any], int]] = []
    merged_urls: list[str] = []
    for group in clusters:
        members = [i for i in group if 0 <= i < len(candidates) and i not in seen]
        if not members:
            continue
        best = max(members, key=lambda i: candidates[i][1])
        merged_urls.extend(
            candidates[i][0].get("url", "")
            for i in members
            if i != best and candidates[i][0].get("url")
        )
        seen.update(members)
        result.append(candidates[best])

    # Preserve any idx the LLM forgot to include (defensive)
    for i, item in enumerate(candidates):
        if i not in seen:
            result.append(item)

    # Re-sort by score desc since cluster order is arbitrary
    result.sort(key=lambda x: -x[1])
    logger.info("llm dedupe: %d candidates -> %d unique stories", len(candidates), len(result))
    return result, merged_urls


def _infer_source(url: str) -> str:
    try:
        from urllib.parse import urlparse

        host = urlparse(url).netloc
        return host.removeprefix("www.")
    except Exception:
        return ""


def run(board: str, as_of: date | None = None) -> Path:
    cfg = _load_config()
    bcfg = (cfg.get("boards") or {}).get(board)
    if not bcfg:
        raise SystemExit(f"Board '{board}' not found in config.yaml")

    threshold = int(bcfg.get("score_threshold", 6))
    top_n = int(bcfg.get("top_n", 20))

    data = _load_input(board)
    entries = data.get("entries", [])
    if not entries:
        logger.warning("[%s] no entries to digest", board)

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY (or GOOGLE_API_KEY) env var is required")
    client = genai.Client(api_key=api_key)

    scored: list[tuple[dict[str, Any], int]] = []
    if entries:
        scores = _score_entries(client, board, entries)
        scored = sorted(zip(entries, scores), key=lambda x: -x[1])

    above_threshold = [(e, sc) for e, sc in scored if sc >= threshold]
    pool_size = min(top_n * DEDUPE_POOL_MULTIPLIER, DEDUPE_MAX_CANDIDATES)
    pool = above_threshold[:pool_size]
    deduped, merged_urls = _llm_dedupe(client, pool) if pool else ([], [])
    selected = [e for e, _sc in deduped[:top_n]]
    logger.info("[%s] scored=%d above_threshold=%d pool=%d unique=%d selected=%d (threshold=%d, top_n=%d)",
                board, len(scored), len(above_threshold), len(pool), len(deduped),
                len(selected), threshold, top_n)

    items = _summarize(client, selected) if selected else []

    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    as_of = as_of or digest_today()
    from datetime import timezone as _tz
    out_path = DIGEST_DIR / f"{board}_{as_of.isoformat()}.json"
    payload = {
        "board": board,
        "display_name": bcfg.get("display_name", board),
        "date": as_of.isoformat(),
        "generated_at": datetime.now(_tz.utc).isoformat().replace("+00:00", "Z"),
        "raw_count": data.get("entry_count", 0),
        "selected_count": len(items),
        "items": items,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    logger.info("[%s] wrote %s", board, out_path)

    report = render_source_report(
        board=board,
        display_name=bcfg.get("display_name", board),
        report_date=as_of,
        feed_stats=data.get("feed_stats") or _fallback_feed_stats(entries),
        entries=entries,
        score_by_url={entry.get("url", ""): score for entry, score in scored if entry.get("url")},
        selected_urls={entry.get("url", "") for entry in selected if entry.get("url")},
        merged_urls=merged_urls,
    )
    write_board_report(board, as_of, report)
    refresh_latest_report(as_of, list((cfg.get("boards") or {}).keys()))
    return out_path


def _fallback_feed_stats(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for entry in entries:
        feed_url = entry.get("feed_url") or _infer_source(entry.get("url", ""))
        if not feed_url:
            continue
        row = stats.setdefault(
            feed_url,
            {
                "feed_title": entry.get("feed_title") or feed_url,
                "category": entry.get("category", ""),
                "attempted": 1,
                "succeeded": 1,
                "raw_count": 0,
            },
        )
        row["raw_count"] += 1
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--board", required=True, choices=["security", "ai", "finance"])
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default today)")
    args = parser.parse_args()

    as_of = date.fromisoformat(args.date) if args.date else None
    run(args.board, as_of=as_of)


if __name__ == "__main__":
    main()

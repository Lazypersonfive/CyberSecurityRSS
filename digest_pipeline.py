"""LLM pipeline: score raw entries with Haiku, then summarize top N with Sonnet.

Reads output/<board>_latest.json and writes digest/<board>_YYYY-MM-DD.json.

Usage:
    python digest_pipeline.py --board security
    python digest_pipeline.py --board ai
    python digest_pipeline.py --board finance

Environment:
    ANTHROPIC_API_KEY (required)
"""

import argparse
import json
import logging
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import anthropic
import yaml

from digest_clock import digest_today
from digest_postprocess import normalize_summary_text, summary_needs_repair
from digest_postprocess import count_chinese_chars, SUMMARY_TARGET_MAX_CHARS, SUMMARY_TARGET_MIN_CHARS
from source_policy import select_with_source_policy, sort_scored_candidates, source_mix_stats

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

SCORE_MODEL = "claude-haiku-4-5-20251001"
SUMMARIZE_MODEL = "claude-sonnet-4-5-20250929"

# Fall-back summarize model if the primary id isn't enabled on the API key.
SUMMARIZE_MODEL_FALLBACK = "claude-haiku-4-5-20251001"

SCORE_BATCH_SIZE = 40
SUMMARIZE_BATCH_SIZE = 8

# Per-board scoring rubric
BOARD_SCORE_SYSTEM = {
    "security": """你是资深网安分析师，对安全资讯做 0-10 打分。
评分标准：
- 9-10: 在野利用 0day、重大 APT 活动、大规模供应链攻击
- 7-8: 新型攻击技术、高危 CVE 详解、红蓝工具发布、关键威胁情报
- 5-6: 安全研究、技术博客、可观察性分析
- 0-4: 招聘、营销软文、职业规划、入门求助帖
评分只看新闻价值，不因语言、来源篇幅长短打折扣；中文一线媒体或官方源首发，权重等同英文媒体。
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
    "ai": """你是 AI 产业观察者，对 AI 资讯做 0-10 打分。
评分标准：
- 9-10: 主流实验室（Anthropic/OpenAI/Google/Meta/DeepSeek 等）重大模型发布、里程碑论文、Agentic 能力突破、产业格局级新闻
- 7-8: 有实质技术增益的开源模型、能力评测、应用层关键动态、监管与安全政策
- 5-6: 技术博客、一般产品更新、行业分析
- 0-4: 纯营销 PR、个人观点水文、融资新闻（无技术细节）、招聘/培训广告
评分只看新闻价值，不因语言、来源篇幅长短打折扣；中文一线媒体或官方源首发，权重等同英文媒体。
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
    "finance": """你是金融科技观察者，关注金融机构（尤其是头部银行、支付网络、卡组织）
的真实科技动作。对资讯做 0-10 打分。
评分标准：
- 9-10: 大行核心系统升级、支付网络战略动作（Visa/Mastercard/Stripe/中国顶级银行）、监管拐点、CBDC / 稳定币关键进展
- 7-8: 具体技术合作、区域性支付新基建、金融 AI / 风控落地案例、关键数据披露
- 5-6: 产品发布、一般性行业动态、高质量行业分析
- 0-4: 融资 PR、营销软文、泛观点文章
评分只看新闻价值，不因语言、来源篇幅长短打折扣；中文一线媒体或官方源首发，权重等同英文媒体。
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
}

SUMMARIZE_SYSTEM = """你是一位科技资讯编辑。你的任务是把给定的新闻原文加工成中文摘要卡片。
严格规则：
1. 所有输出字段使用简体中文（即便原文是英文）。
2. 摘要只使用原文提供的信息，不得补充外部知识、不得猜测、不得夸大。
3. 中文标题建议 24-48 字，必须表达完整事件，不得半句截断；去除所有客套词和营销语。
4. 摘要必须是 120-180 个汉字，不是英文字符数；写成 2 句，先讲发生了什么，再讲为什么值得关注 / 对谁有影响。
5. tags 给 1-3 个中文关键词，每个不超过 6 字。
6. 严格按 JSON 数组返回，不要解释、不要 Markdown 包裹。
输出格式：[{"idx":0,"title_zh":"...","summary":"...","tags":["..."]}]"""

REPAIR_SUMMARIZE_SYSTEM = """你要修正新闻摘要的长度问题。
严格规则：
1. 只依据给定原文信息改写，不得补充外部知识。
2. 只输出 summary 字段，必须是 120-180 个汉字。
3. 使用简体中文，2 句，不要项目符号，不要解释。
4. 如果原草稿太短，就补足关键事实、影响对象和关注原因；如果太长，就压缩但保留核心信息。
输出格式：[{"idx":0,"summary":"..."}]"""


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
    return json.loads(raw)


def _score_entries(
    client: anthropic.Anthropic, board: str, entries: list[dict[str, Any]]
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
        resp = client.messages.create(
            model=SCORE_MODEL,
            max_tokens=1500,
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user_prompt}],
        )
        try:
            parsed = _parse_llm_json(resp.content[0].text)
            smap = {int(r["idx"]): int(r["score"]) for r in parsed}
        except Exception as exc:
            logger.warning("score parse failed (batch %d): %s", i, exc)
            smap = {}
        for j in range(len(batch)):
            scores[i + j] = smap.get(j, 5)
    return scores


def _summarize(
    client: anthropic.Anthropic, entries: list[dict[str, Any]]
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
        model_id = SUMMARIZE_MODEL
        try:
            resp = client.messages.create(
                model=model_id,
                max_tokens=3500,
                system=[
                    {"type": "text", "text": SUMMARIZE_SYSTEM, "cache_control": {"type": "ephemeral"}}
                ],
                messages=[{"role": "user", "content": user_prompt}],
            )
        except anthropic.NotFoundError:
            logger.warning("model %s unavailable, falling back to %s", model_id, SUMMARIZE_MODEL_FALLBACK)
            model_id = SUMMARIZE_MODEL_FALLBACK
            resp = client.messages.create(
                model=model_id,
                max_tokens=3500,
                system=[
                    {"type": "text", "text": SUMMARIZE_SYSTEM, "cache_control": {"type": "ephemeral"}}
                ],
                messages=[{"role": "user", "content": user_prompt}],
            )

        try:
            parsed = _parse_llm_json(resp.content[0].text)
            smap = {int(r["idx"]): r for r in parsed}
        except Exception as exc:
            logger.warning("summarize parse failed (batch %d): %s", i, exc)
            smap = {}

        repaired_summaries = _repair_summaries(client, batch, smap, model_id)

        for j, e in enumerate(batch):
            s = smap.get(j, {})
            results.append(
                {
                    "title_zh": (s.get("title_zh") or e.get("title", "")).strip(),
                    "title_orig": e.get("title", ""),
                    "summary": repaired_summaries.get(j, normalize_summary_text(s.get("summary") or "")),
                    "tags": s.get("tags") or [],
                    "url": e.get("url", ""),
                    "source": _infer_source(e.get("url", "")),
                    "category": e.get("category", ""),
                    "published": e.get("published", ""),
                    "cve_ids": e.get("cve_ids", []),
                }
            )
    return results


def _repair_summaries(
    client: anthropic.Anthropic,
    batch: list[dict[str, Any]],
    smap: dict[int, dict[str, Any]],
    model_id: str,
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
        resp = client.messages.create(
            model=model_id,
            max_tokens=2500,
            system=[{"type": "text", "text": REPAIR_SUMMARIZE_SYSTEM, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user_prompt}],
        )
        try:
            parsed = _parse_llm_json(resp.content[0].text)
            for row in parsed:
                idx = int(row["idx"])
                repaired[idx] = normalize_summary_text(row.get("summary") or repaired.get(idx, ""))
        except Exception as exc:
            logger.warning("summary repair parse failed: %s", exc)
            break
    return repaired


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
    fill_score_floor = int(bcfg.get("fill_score_floor", max(0, threshold - 1)))
    top_n = int(bcfg.get("top_n", 20))

    data = _load_input(board)
    entries = data.get("entries", [])
    max_llm_entries = int(bcfg.get("llm_max_entries", 0) or 0)
    if max_llm_entries > 0 and len(entries) > max_llm_entries:
        logger.info("[%s] trim LLM scoring set: %d -> %d", board, len(entries), max_llm_entries)
        entries = entries[:max_llm_entries]
    if not entries:
        logger.warning("[%s] no entries to digest", board)

    if "ANTHROPIC_API_KEY" not in os.environ:
        raise SystemExit("ANTHROPIC_API_KEY env var is required")
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    scored: list[tuple[dict[str, Any], int]] = []
    if entries:
        scores = _score_entries(client, board, entries)
        scored = sort_scored_candidates(zip(entries, scores))

    above_threshold = [(e, sc) for e, sc in scored if sc >= threshold]
    candidates = [(e, sc) for e, sc in scored if sc >= fill_score_floor]
    source_policy = dict(bcfg.get("source_policy") or {})
    # TODO: Port Gemini's LLM story clustering here before making Anthropic the
    # primary backend again. This backup path currently relies on fetch-time
    # title/CVE dedupe plus deterministic source policy.
    selected_scored = select_with_source_policy(candidates, top_n, source_policy)
    selected = [e for e, _sc in selected_scored]
    mix_stats = source_mix_stats(selected)
    logger.info(
        "[%s] scored=%d above_threshold=%d candidates=%d selected=%d mix=%s "
        "(threshold=%d, fill_floor=%d, top_n=%d, policy=%s)",
        board, len(scored), len(above_threshold), len(candidates), len(selected),
        mix_stats, threshold, fill_score_floor, top_n, source_policy,
    )

    items = _summarize(client, selected) if selected else []

    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    as_of = as_of or digest_today()
    out_path = DIGEST_DIR / f"{board}_{as_of.isoformat()}.json"
    payload = {
        "board": board,
        "display_name": bcfg.get("display_name", board),
        "date": as_of.isoformat(),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "raw_count": data.get("entry_count", 0),
        "selected_count": len(items),
        "selection_stats": mix_stats,
        "items": items,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    logger.info("[%s] wrote %s", board, out_path)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--board", required=True, choices=["security", "ai", "finance"])
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default today)")
    args = parser.parse_args()

    as_of = date.fromisoformat(args.date) if args.date else None
    run(args.board, as_of=as_of)


if __name__ == "__main__":
    main()

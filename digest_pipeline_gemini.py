"""LLM digest pipeline with pluggable backends.

Reads output/<board>_latest.json and writes digest/<board>_YYYY-MM-DD.json.

Usage:
    python digest_pipeline_gemini.py --board security
    python digest_pipeline_gemini.py --board ai
    python digest_pipeline_gemini.py --board finance

Environment:
    LLM_BACKEND=gemini (default) requires GEMINI_API_KEY or GOOGLE_API_KEY.
    LLM_BACKEND=deepseek requires DEEPSEEK_API_KEY.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
import logging
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from digest_clock import digest_today
from delivered_history import filter_delivered_candidates, load_delivered_history
from llm_backends import LLMBackend, get_backend
from digest_postprocess import normalize_summary_text, summary_needs_repair
from digest_postprocess import count_chinese_chars, SUMMARY_TARGET_MAX_CHARS, SUMMARY_TARGET_MIN_CHARS
from digest_postprocess import vuln_summary_needs_repair, vuln_tech_element_count
from scoring_policy import compute_final_score
from source_policy import (
    select_with_source_policy,
    sort_scored_candidates,
    source_mix_stats,
    source_priority,
    source_profile,
)
from story_clustering import cluster_scored_candidates, probable_same_story
from security_editorial import adjust_ai_security_score, adjust_finance_score, adjust_security_score
from source_reports import (
    refresh_latest_report,
    refresh_weekly_report,
    render_source_report,
    write_board_report,
    write_board_report_json,
)

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
TITLE_HARD_MAX_CHARS = 80
ANTHROPIC_TOKEN = "anth" + "ropic"
CLAUDE_TOKEN = "cla" + "ude"

SCORE_BATCH_SIZE = 40
SUMMARIZE_BATCH_SIZE = 8
SCORE_DIMENSIONS = {
    "security": ["relevance", "technical_depth", "exploitability", "impact_scope", "actionability"],
    "ai_security": [
        "security_relevance",
        "technical_depth",
        "practical_risk",
        "agent_model_relevance",
        "actionability",
    ],
    "ai": ["relevance", "novelty", "entity_importance", "developer_relevance", "ecosystem_impact"],
    "finance": [
        "relevance",
        "institution_importance",
        "technology_depth",
        "market_or_regulatory_impact",
        "actionability",
    ],
}

# Per-board scoring rubric
BOARD_SCORE_SYSTEM = {
    "security": """你是资深网安编辑，对传统安全资讯做 0-10 打分。目标是每日 15 条技术安全日报；候选足够时，至少 6 条来自中文媒体 / 国内官方 / 中文安全厂商源。
编辑目标：优先让读者看到最新热门 CVE、0day、在野利用、漏洞原理、官方通告、国内安全动向、CTF/攻防竞赛和高质量漏洞分析；不要把安全日报做成泛政治或泛科技新闻。
评分标准：
- 9-10: 最新热门 CVE / 0day / 在野利用，且能说明漏洞原理、触发条件、影响版本、利用方式或修复缓解；国内官方预警、厂商 CERT/实验室首发、CTF/攻防竞赛高质量技术复盘。仅有高危结论、没有机制或触发条件的漏洞资讯不得进入此档
- 7-8: 高危漏洞详解、补丁绕过、PoC/EXP 分析、供应链技术细节、红蓝对抗工具、检测规则、重要安全通告
- 5-6: 安全研究、技术博客、工具更新、政策/合规通告；必须有明确技术信息或可执行处置价值
- 0-4: 招聘、营销软文、职业规划、入门求助帖、纯观点；只有地缘归因/政治叙事/攻击组织命名但缺少漏洞原理或技术细节的新闻，上限 4 分
来源偏好：中文漏洞分析、国内官方源、厂商 CERT/安全实验室、CTF/攻防社区首发，权重等同或高于英文媒体；Google News 只做补充，不因聚合来源自动加分。
评分只看技术价值，不因语言、来源篇幅长短打折扣。
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
    "ai_security": """你是 AI 安全编辑，对 AI 安全资讯做 0-10 打分。目标是每日 10 条 AI 安全日报；宁缺毋滥，不收泛 AI 动态。
编辑目标：覆盖 LLM/Agent 漏洞、提示词注入、越狱攻防、模型供应链、AI 代码执行/数据泄露、模型评测安全、AI 基础设施安全和厂商安全公告。
评分标准：
- 9-10: LLM/Agent 漏洞、提示词注入、模型供应链、AI 代码执行/数据泄露、越狱攻防、模型安全评测或一线厂商安全公告，且有技术机制或可操作影响
- 7-8: AI 安全研究、红队评测、检测/防护工具、模型滥用与防护案例、AI 基础设施安全
- 5-6: 有明确安全含义的产品/政策/研究更新
- 0-4: 泛 AI 产品发布、融资、纯观点、营销软文、厂商排名/奖项、普通诉讼争议，以及没有攻击机制、防护机制或可验证风险的行业新闻
来源偏好：官方博客、研究团队、中文一线安全源、厂商安全团队和顶级安全研究者 X 动态优先；Google News 只做补充，X/RSSHub 可作为一手早期信号。
评分只看技术价值，不因语言、来源篇幅长短打折扣。
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
    "ai": """你是 AI 产业观察者，对 AI 动态资讯做 0-10 打分。目标是每日 15 条 AI 动态；候选足够时，至少 5 条中文来源，约占三分之一。
编辑目标：覆盖主流实验室、模型发布、Agent 能力、重要产品、开源项目、算力/生态/监管变化；避免让 Google News 或 X/RSSHub 信号盖掉官方博客、论文/项目页或中文一线媒体首发。
评分标准：
- 9-10: 主流实验室（Anthropic/OpenAI/Google/Meta/DeepSeek 等）重大模型发布、里程碑论文、Agentic 能力突破、产业格局级新闻
- 7-8: 有实质技术增益的开源模型、能力评测、应用层关键动态、监管与安全政策
- 5-6: 技术博客、一般产品更新、行业分析
- 0-4: 纯营销 PR、个人观点水文、融资新闻（无技术细节）、招聘/培训广告
来源偏好：官方博客、论文/项目页、开发者公告、顶级开发者 X 动态、中文一线媒体或官方源首发，优先于 Google News 聚合转述；X/RSSHub 可作为一手早期信号。
评分只看新闻价值，不因语言、来源篇幅长短打折扣。
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
    "finance": """你是金融科技观察者，对金融科技资讯做 0-10 打分。目标是每日 10 条，关注金融机构、支付网络、卡组织、监管与真实技术落地。
编辑目标：优先选择头部银行、Visa/Mastercard/Stripe/PayPal/中国顶级银行、监管机构和一线行业媒体的直接消息；Google News 只补覆盖，不压过官网和高质量直采源。
评分标准：
- 9-10: 大行核心系统升级、支付网络战略动作、监管拐点、CBDC / 稳定币关键进展、金融 AI / 风控 / 支付基础设施的关键落地
- 7-8: 具体技术合作、区域性支付新基建、金融 AI 或风控落地案例、关键数据披露
- 5-6: 产品发布、一般性行业动态、高质量行业分析
- 0-4: 融资 PR、营销软文、泛观点文章；与银行、支付、清算、金融监管、金融基础设施或金融技术落地无关的普通 AI 产品、科技公司人事和社交媒体政策新闻
来源偏好：监管/公司官网、IR、官方博客、一线金融科技媒体和中文可靠来源优先于 Google News 聚合转述。
评分只看新闻价值，不因语言、来源篇幅长短打折扣。
只返回 JSON 数组，形如 [{"idx":0,"score":8}]。""",
}

SUMMARIZE_SYSTEM = """你是一位科技资讯编辑。你的任务是把给定的新闻原文加工成中文摘要卡片。
严格规则：
1. 所有输出字段使用简体中文（即便原文是英文）。
2. 摘要只使用原文提供的信息，不得补充外部知识、不得猜测、不得夸大。
3. 中文标题建议 24-48 字，必须表达完整事件，不得半句截断；去除客套词、标题党和营销语。
4. 摘要必须是 120-180 个汉字，不是英文字符数；写成 2 句，先讲发生了什么，再讲为什么值得关注 / 对谁有影响。
5. 如果原文来自 Google News 或其他聚合源，摘要不得写成“某媒体报道”；如果来自顶级开发者 X 动态，可直接归因该开发者或项目，但不得编造原文没有的来源细节。
6. tags 给 1-3 个中文关键词，每个不超过 6 字。
7. tags 和 selection_reason 不得为空；selection_reason 用不超过 30 个中文字符说明这条新闻为何值得关注。
8. 严格按 JSON 数组返回，不要解释、不要 Markdown 包裹。
输出格式：[{"idx":0,"title_zh":"...","summary":"...","tags":["..."],"selection_reason":"..."}]"""

SECURITY_SUMMARIZE_SYSTEM = """你是一位偏技术的安全日报编辑。你的任务是把安全资讯加工成中文摘要卡片。
严格规则：
1. 所有输出字段使用简体中文。
2. 摘要只使用原文提供的信息，不得补充外部知识、不得猜测、不得夸大。
3. 中文标题建议 24-48 字，必须表达完整事件，不得半句截断；去除客套词、标题党和营销语。
4. 摘要必须是 120-180 个汉字，写成 2 句。
5. 如果是 CVE、漏洞、PoC、EXP、补丁绕过或官方预警，摘要必须优先写：漏洞类型/原理、触发条件、影响版本或影响组件、实际影响、修复/缓解状态；原文缺哪项就明确写原文未披露。
6. 如果是 CTF/竞赛/红蓝对抗/工具文章，摘要必须写技术点、适用场景和为什么值得安全从业者关注。
7. 不要把地缘政治归因当成重点；没有技术细节的 APT/黑客组织新闻应写得很弱，不得拔高。
8. 如果原文来自 Google News 或其他聚合源，摘要不得写成“某媒体报道”；如果来自顶级安全研究者 X 动态，可直接归因该研究者或项目，但不得编造原文没有的技术细节。
9. tags 给 1-3 个中文关键词，每个不超过 6 字；selection_reason 不得为空，用不超过 30 个中文字符说明技术价值。
10. 严格按 JSON 数组返回，不要解释、不要 Markdown 包裹。
输出格式：[{"idx":0,"title_zh":"...","summary":"...","tags":["..."],"selection_reason":"..."}]"""


VULN_REPAIR_SYSTEM = """你要重写一条漏洞资讯的中文摘要，让它覆盖技术要素。
严格规则：
1. 只依据给定原文信息改写，不得补充外部知识、不得编造技术细节。
2. 摘要必须是 120-180 个汉字，2 句，简体中文。
3. 优先覆盖：漏洞类型/原理、触发条件、影响版本或组件、修复/缓解状态。
4. 原文未披露的要素，明确写"原文未披露XX"，不要省略也不要编造。
5. 不要写"影响重大、建议关注"这类空话。
输出格式：[{"idx":0,"summary":"..."}]"""


REPAIR_SUMMARIZE_SYSTEM = """你要修正新闻摘要的长度问题。
严格规则：
1. 只依据给定原文信息改写，不得补充外部知识。
2. 只输出 summary 字段，必须是 120-180 个汉字。
3. 使用简体中文，2 句，不要项目符号，不要解释。
4. 如果原草稿太短，就补足关键事实、影响对象和关注原因；如果太长，就压缩但保留核心信息。
输出格式：[{"idx":0,"summary":"..."}]"""

REPAIR_TITLE_SYSTEM = """你要把英文新闻标题译成简体中文短标题。
严格规则：
1. 只依据原文信息翻译，不得补充外部知识、不得夸张。
2. 输出标题必须是简体中文，建议 24-48 字，必须表达完整事件，不得半句截断；去除客套词和营销语。
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
LLM_DEDUPE_MAX_MERGE_RATIO = 0.35

def _is_chinese_entry(entry: dict[str, Any]) -> bool:
    """Backward-compatible wrapper around the centralized source profiler."""
    return source_profile(entry).is_chinese


def _apply_language_quota(
    deduped: list[tuple[dict[str, Any], int]],
    top_n: int,
    min_chinese: int,
) -> list[tuple[dict[str, Any], int]]:
    """Compatibility shim for older callers; new code uses source_policy."""
    return select_with_source_policy(deduped, top_n, {"min_chinese": min_chinese})


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


def _score_entries(
    backend: LLMBackend, board: str, entries: list[dict[str, Any]]
) -> list[int]:
    system = _score_system_for_board(board)
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
            text = backend.generate_json(backend.score_model, system, user_prompt, 4000)
            parsed = _parse_llm_json(text)
            smap: dict[int, int] = {}
            dimension_map: dict[int, dict[str, float]] = {}
            for r in parsed:
                idx = int(r["idx"])
                smap[idx] = int(r["score"])
                dimensions = _score_dimensions_from_response(board, r)
                if dimensions:
                    dimension_map[idx] = dimensions
        except Exception as exc:
            logger.warning("score parse failed (batch %d): %s", i, exc)
            smap = {}
            dimension_map = {}
        for j in range(len(batch)):
            if j in dimension_map:
                entries[i + j]["score_dimensions"] = dimension_map[j]
            score = smap.get(j, 5)
            if board == "security":
                score = adjust_security_score(batch[j], score)
            elif board == "ai_security":
                score = adjust_ai_security_score(batch[j], score)
            elif board == "finance":
                score = adjust_finance_score(batch[j], score)
            scores[i + j] = score
    return scores


def _score_system_for_board(board: str) -> str:
    dimensions = SCORE_DIMENSIONS.get(board, [])
    if not dimensions:
        return BOARD_SCORE_SYSTEM[board]
    example = {"idx": 0, "score": 8, "score_dimensions": {key: 8 for key in dimensions}}
    return (
        BOARD_SCORE_SYSTEM[board]
        + "\n同时返回 score_dimensions，键必须是："
        + "、".join(dimensions)
        + "。每个维度也是 0-10 整数；score 是这些维度综合后的兼容总分。"
        + f"\n输出格式：[{json.dumps(example, ensure_ascii=False)}]。"
    )


def _score_dimensions_from_response(board: str, row: dict[str, Any]) -> dict[str, float]:
    allowed = set(SCORE_DIMENSIONS.get(board, []))
    raw = row.get("score_dimensions") or row.get("dimensions") or {}
    if not allowed or not isinstance(raw, dict):
        return {}
    dimensions: dict[str, float] = {}
    for key in allowed:
        value = raw.get(key)
        try:
            dimensions[key] = max(0.0, min(10.0, float(value)))
        except (TypeError, ValueError):
            continue
    return dimensions


def _summarize(
    backend: LLMBackend, board: str, entries: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    system_prompt = SECURITY_SUMMARIZE_SYSTEM if board in {"security", "ai_security"} else SUMMARIZE_SYSTEM
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
                text = backend.generate_json(backend.summarize_model, system_prompt, user_prompt, 6000)
                parsed = _parse_llm_json(text)
                smap = {int(r["idx"]): r for r in parsed}
                break
            except Exception as exc:
                logger.warning("summarize parse failed (batch %d, retry %d): %s", i, retry, exc)

        repaired_summaries = _repair_summaries(backend, batch, smap)
        if board == "security":
            repaired_summaries = _repair_vuln_summaries(backend, batch, repaired_summaries)
        repaired_titles = _repair_titles(backend, batch, smap)

        for j, e in enumerate(batch):
            s = smap.get(j, {})
            raw_item = {
                "title_zh": repaired_titles.get(j, (s.get("title_zh") or e.get("title", "")).strip()),
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
            results.append(_finalize_digest_item(e, raw_item))
    return results


def _selection_reason(item: dict[str, Any]) -> str:
    reason = normalize_summary_text(item.get("selection_reason") or "")
    return reason[:30]


def _finalize_digest_item(entry: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    """Hard validation for the digest item schema after LLM generation."""
    finalized = dict(item)
    title = normalize_summary_text(finalized.get("title_zh") or "")
    if _title_needs_repair(title):
        title = _fallback_title(entry)
    finalized["title_zh"] = _limit_title(_sanitize_vulnerability_claims(entry, title))
    finalized["title_orig"] = entry.get("title", finalized.get("title_orig", ""))

    summary = normalize_summary_text(finalized.get("summary") or "")
    summary = _sanitize_vulnerability_claims(entry, summary)
    finalized["summary"] = _ensure_summary_length(summary, entry, finalized["title_zh"])
    finalized["tags"] = _normalize_tags(finalized.get("tags"), entry)
    finalized["selection_reason"] = _selection_reason(finalized) or _fallback_selection_reason(entry)
    finalized["url"] = entry.get("url", finalized.get("url", ""))
    finalized["source"] = _infer_source(finalized["url"])
    finalized["category"] = entry.get("category", finalized.get("category", ""))
    finalized["published"] = entry.get("published", finalized.get("published", ""))
    if entry.get("feed_url"):
        finalized["feed_url"] = entry.get("feed_url")
    if entry.get("feed_title"):
        finalized["feed_title"] = entry.get("feed_title")
    finalized["cve_ids"] = entry.get("cve_ids", finalized.get("cve_ids", [])) or []
    profile = source_profile(entry)
    finalized["source_tier"] = profile.source_tier
    finalized["source_kind"] = profile.source_kind
    finalized["source_label"] = profile.source_label
    finalized["source_key"] = profile.source_key
    finalized["story_id"] = entry.get("story_id", finalized.get("story_id", ""))
    finalized["related_urls"] = entry.get("related_urls", finalized.get("related_urls", [])) or []
    finalized["related_count"] = len(finalized["related_urls"])
    return finalized


def _sanitize_vulnerability_claims(entry: dict[str, Any], summary: str) -> str:
    """Downgrade a common XSS-to-RCE overstatement without inventing details."""
    source_text = " ".join(
        str(entry.get(key) or "")
        for key in ("title", "title_orig", "summary")
    )
    is_xss = bool(re.search(r"\bXSS\b|cross[- ]site scripting|跨站脚本|存储型跨站", source_text, re.IGNORECASE))
    source_claims_rce = bool(re.search(r"\bRCE\b|remote code execution|远程代码执行", source_text, re.IGNORECASE))
    if is_xss and not source_claims_rce:
        return (
            summary
            .replace("任意代码执行", "浏览器会话内脚本执行")
            .replace("执行任意代码", "执行恶意脚本")
        )
    return summary


def _fallback_title(entry: dict[str, Any]) -> str:
    title = normalize_summary_text(entry.get("title") or "")
    text = title.lower()
    if count_chinese_chars(title) > 0:
        return title
    if "openai" in text and ANTHROPIC_TOKEN in text and "cyber" in text:
        return "OpenAI与Anthropic讨论网络安全模型"
    if "openai" in text:
        return "OpenAI重要动态"
    if ANTHROPIC_TOKEN in text or CLAUDE_TOKEN in text:
        return "Anthropic重要动态"
    if "microsoft" in text or "windows" in text:
        return "微软安全动态"
    if "github" in text:
        return "GitHub安全动态"
    if "visa" in text or "mastercard" in text:
        return "支付网络动态"
    if "ai" in text or "llm" in text or "agent" in text:
        return "AI前沿动态"
    return "重要资讯更新"


def _limit_title(title: str) -> str:
    """Avoid broken card titles; only guard against pathological model output."""
    title = normalize_summary_text(title)
    if len(title) <= TITLE_HARD_MAX_CHARS:
        return title
    for sep in ("。", "；", ";", "：", ":", "，", ",", " - ", "｜", "|"):
        cut = title.rfind(sep, 0, TITLE_HARD_MAX_CHARS + 1)
        if cut >= 24:
            return title[:cut].rstrip("，,；;：:、.。 -|｜")
    return title[:TITLE_HARD_MAX_CHARS].rstrip("，,；;：:、.。 ") + "…"


def _ensure_summary_length(summary: str, entry: dict[str, Any], title_zh: str) -> str:
    summary = _strip_repeated_title_suffix(normalize_summary_text(summary), title_zh)
    if not summary_needs_repair(summary) and len(summary) <= 240:
        return summary
    if not summary_needs_repair(summary):
        return _limit_rendered_summary(summary)

    fallback = _fallback_summary(entry, title_zh)
    if count_chinese_chars(summary) >= 40:
        summary = _strip_repeated_title_suffix(normalize_summary_text(f"{summary} {fallback}"), title_zh)
    else:
        summary = fallback

    if count_chinese_chars(summary) > SUMMARY_TARGET_MAX_CHARS:
        summary = _truncate_chinese_chars(summary, SUMMARY_TARGET_MAX_CHARS)
    if count_chinese_chars(summary) < SUMMARY_TARGET_MIN_CHARS:
        summary = normalize_summary_text(
            f"{summary} 建议后续结合原文确认技术细节、影响对象、版本范围和处置优先级，"
            "必要时纳入团队例行监测。"
        )
    if count_chinese_chars(summary) < SUMMARY_TARGET_MIN_CHARS:
        summary = normalize_summary_text(
            f"{summary} 对依赖相关产品、模型或支付基础设施的团队，应关注后续公告和实际落地变化。"
        )
    if count_chinese_chars(summary) > SUMMARY_TARGET_MAX_CHARS:
        summary = _truncate_chinese_chars(summary, SUMMARY_TARGET_MAX_CHARS)
    return _limit_rendered_summary(_strip_repeated_title_suffix(summary, title_zh))


def _strip_repeated_title_suffix(summary: str, title_zh: str) -> str:
    """Drop model/fallback artifacts where the title is appended after summary."""
    summary = normalize_summary_text(summary)
    title = normalize_summary_text(title_zh).rstrip("。！？!?")
    if not summary or not title:
        return summary
    for suffix in (title, f"{title}。", f"{title}！", f"{title}？"):
        if summary.endswith(suffix):
            stripped = summary[: -len(suffix)].rstrip(" ，,；;：:、.。")
            return stripped + ("。" if stripped and stripped[-1] not in "。！？!?" else "")
    return summary


def _limit_rendered_summary(summary: str, max_chars: int = 220) -> str:
    summary = normalize_summary_text(summary)
    if len(summary) <= max_chars:
        return summary
    cut = max(summary.rfind(sep, 0, max_chars + 1) for sep in ("。", "！", "？", "；", ";"))
    if cut >= 80:
        return summary[: cut + 1].strip()
    return summary[:max_chars].rstrip("，,；;：:、.。 ") + "。"


def _fallback_summary(entry: dict[str, Any], title_zh: str) -> str:
    source = _infer_source(entry.get("url", "")) or "原始来源"
    category = entry.get("category") or "相关领域"
    return (
        f"{title_zh}。该条来自{source}，归类于{category}，原始信息显示其在本轮抓取、去重和打分中优先级较高。"
        "建议查看原文核验具体影响、版本范围和后续处置动态，并结合自身业务判断是否需要跟进。"
    )


def _truncate_chinese_chars(text: str, limit: int) -> str:
    count = 0
    out: list[str] = []
    for ch in text:
        if "\u3400" <= ch <= "\u9fff":
            count += 1
        out.append(ch)
        if count >= limit:
            break
    return "".join(out).rstrip("，,；;：:、.。 ") + "。"


def _normalize_tags(tags: Any, entry: dict[str, Any]) -> list[str]:
    result: list[str] = []
    if isinstance(tags, list):
        for tag in tags:
            text = normalize_summary_text(str(tag))
            if text and text not in result:
                result.append(text[:8])
            if len(result) >= 3:
                break
    if result:
        return result

    text = " ".join(str(entry.get(k) or "") for k in ("title", "summary", "category")).lower()
    cves = entry.get("cve_ids") or []
    if cves or "cve-" in text or "vulnerability" in text or "漏洞" in text:
        result.append("漏洞")
    if "openai" in text:
        result.append("OpenAI")
    if ANTHROPIC_TOKEN in text or CLAUDE_TOKEN in text:
        result.append("Anthropic")
    if "ai" in text or "llm" in text or "agent" in text or "模型" in text:
        result.append("AI")
    if "visa" in text or "mastercard" in text or "payment" in text or "支付" in text:
        result.append("支付")
    if source_profile(entry).is_chinese:
        result.append("中文源")
    if not result:
        result.append(_category_tag(entry.get("category", "")))
    return result[:3]


def _category_tag(category: str) -> str:
    mapping = {
        "OfficialAdvisories": "官方预警",
        "RedTeam": "红队",
        "WebSecurity": "Web安全",
        "AI": "AI安全",
        "Labs": "实验室",
        "Media": "媒体",
        "Research": "论文",
        "Chinese": "中文源",
        "Commentary": "评论",
        "Digital Wallets": "数字钱包",
        "Card Networks": "卡组织",
        "Editorial Lens": "行业分析",
    }
    return mapping.get(category, "资讯")


def _fallback_selection_reason(entry: dict[str, Any]) -> str:
    profile = source_profile(entry)
    if profile.is_wechat:
        return "中文信源高分入选"
    if profile.is_google_news:
        return "聚合源补充关键动态"
    if profile.is_direct:
        return "原始信源高分入选"
    return "高分资讯值得跟踪"


def _repair_summaries(
    backend: LLMBackend,
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
            text = backend.generate_json(backend.summarize_model, REPAIR_SUMMARIZE_SYSTEM, user_prompt, 4000)
            parsed = _parse_llm_json(text)
            for row in parsed:
                idx = int(row["idx"])
                repaired[idx] = normalize_summary_text(row.get("summary") or repaired.get(idx, ""))
        except Exception as exc:
            logger.warning("summary repair parse failed: %s", exc)
            break
    return repaired


def _is_vuln_entry(entry: dict[str, Any]) -> bool:
    if entry.get("cve_ids"):
        return True
    text = f"{entry.get('title', '')} {entry.get('summary', '')[:200]}"
    return bool(re.search(r"CVE-\d{4}-\d+|漏洞|0day|零日|vulnerabilit|exploit", text, re.IGNORECASE))


def _repair_vuln_summaries(
    backend: LLMBackend,
    batch: list[dict[str, Any]],
    summaries: dict[int, str],
) -> dict[int, str]:
    """One targeted rewrite for vuln summaries missing technical elements.

    Direction 3 (tasks/current_state_2026-06-11.md): vuln summaries must cover
    type/trigger/scope/remediation. The rewrite is only accepted when it
    covers strictly more elements than the draft, so a bad LLM response can
    never make a summary worse.
    """
    to_fix = []
    for idx, entry in enumerate(batch):
        draft = summaries.get(idx, "")
        if not draft or not _is_vuln_entry(entry):
            continue
        if vuln_summary_needs_repair(draft):
            to_fix.append(
                {
                    "idx": idx,
                    "title": entry.get("title", ""),
                    "source_summary": (entry.get("summary") or "")[:1200],
                    "draft_summary": draft,
                }
            )
    if not to_fix:
        return summaries

    user_prompt = (
        "以下漏洞摘要缺少技术要素，请逐条重写。\n"
        f"输入：\n{json.dumps(to_fix, ensure_ascii=False)}"
    )
    try:
        text = backend.generate_json(backend.summarize_model, VULN_REPAIR_SYSTEM, user_prompt, 4000)
        parsed = _parse_llm_json(text)
    except Exception as exc:
        logger.warning("vuln summary repair failed: %s", exc)
        return summaries

    repaired = dict(summaries)
    rejected = {"invalid_idx": 0, "empty": 0, "length": 0, "not_improved": 0}
    for row in parsed:
        try:
            idx = int(row["idx"])
        except (KeyError, TypeError, ValueError):
            rejected["invalid_idx"] += 1
            continue
        candidate = normalize_summary_text(row.get("summary") or "")
        current = repaired.get(idx, "")
        if not candidate:
            rejected["empty"] += 1
            continue
        if summary_needs_repair(candidate):
            rejected["length"] += 1
            continue
        if vuln_tech_element_count(candidate) > vuln_tech_element_count(current):
            repaired[idx] = candidate
        else:
            rejected["not_improved"] += 1
    fixed = sum(1 for row in to_fix if repaired.get(row["idx"]) != row["draft_summary"])
    if to_fix:
        logger.info(
            "vuln summary repair: %d candidates, %d improved, rejected=%s",
            len(to_fix),
            fixed,
            rejected,
        )
    return repaired


def _title_needs_repair(title: str) -> bool:
    text = (title or "").strip()
    if not text:
        return True
    return count_chinese_chars(text) == 0


def _repair_titles(
    backend: LLMBackend,
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
            text = backend.generate_json(backend.summarize_model, REPAIR_TITLE_SYSTEM, user_prompt, 1500)
            parsed = _parse_llm_json(text)
            for row in parsed:
                idx = int(row["idx"])
                zh = (row.get("title_zh") or "").strip()
                if zh:
                    repaired[idx] = _limit_title(zh)
        except Exception as exc:
            logger.warning("title repair parse failed: %s", exc)
            break
    return repaired


def _llm_dedupe(
    backend: LLMBackend,
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
            "summary": str(e.get("summary") or "")[:500],
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
        text = backend.generate_json(backend.summarize_model, DEDUPE_SYSTEM, user_prompt, 4000)
        parsed = _parse_llm_json(text)
        if isinstance(parsed, list) and all(isinstance(g, list) for g in parsed):
            clusters = [[int(x) for x in g] for g in parsed]
    except Exception as exc:
        logger.warning("llm dedupe parse failed: %s — keeping originals", exc)

    if not clusters:
        return candidates, []

    clusters = _validate_llm_clusters(candidates, clusters)
    proposed_merges = sum(max(0, len(group) - 1) for group in clusters)
    if len(candidates) >= 10 and proposed_merges / len(candidates) > LLM_DEDUPE_MAX_MERGE_RATIO:
        logger.warning(
            "llm dedupe rejected suspicious collapse: %d candidates, %d proposed merges",
            len(candidates),
            proposed_merges,
        )
        return candidates, []

    seen: set[int] = set()
    result: list[tuple[dict[str, Any], int]] = []
    merged_urls: list[str] = []
    for group in clusters:
        members = [i for i in group if 0 <= i < len(candidates) and i not in seen]
        if not members:
            continue
        best = max(members, key=lambda i: (candidates[i][1], source_priority(candidates[i][0])))
        related_urls = [
            candidates[i][0].get("url", "")
            for i in members
            if i != best and candidates[i][0].get("url")
        ]
        merged_urls.extend(related_urls)
        if related_urls:
            best_entry = deepcopy(candidates[best][0])
            existing = [url for url in best_entry.get("related_urls") or [] if url]
            best_entry["related_urls"] = _dedupe_urls(existing + related_urls)
            best_entry["related_count"] = len(best_entry["related_urls"])
            candidates[best] = (best_entry, candidates[best][1])
        seen.update(members)
        result.append(candidates[best])

    # Preserve any idx the LLM forgot to include (defensive)
    for i, item in enumerate(candidates):
        if i not in seen:
            result.append(item)

    # Re-sort since cluster order is arbitrary.
    result = sort_scored_candidates(result)
    logger.info("llm dedupe: %d candidates -> %d unique stories", len(candidates), len(result))
    return result, merged_urls


def _validate_llm_clusters(
    candidates: list[tuple[dict[str, Any], int]],
    clusters: list[list[int]],
) -> list[list[int]]:
    """Split LLM groups unless titles/URLs contain corroborating evidence."""
    validated: list[list[int]] = []
    included: set[int] = set()
    for raw_group in clusters:
        members = [idx for idx in raw_group if 0 <= idx < len(candidates) and idx not in included]
        components: list[list[int]] = []
        for idx in members:
            for component in components:
                if any(probable_same_story(candidates[idx][0], candidates[other][0]) for other in component):
                    component.append(idx)
                    break
            else:
                components.append([idx])
        validated.extend(components)
        included.update(members)
    validated.extend([[idx] for idx in range(len(candidates)) if idx not in included])
    return validated


def _dedupe_urls(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        result.append(url)
    return result


def _candidate_pool(
    scored: list[tuple[dict[str, Any], int]],
    *,
    top_n: int,
    fill_score_floor: int,
    min_chinese: int = 0,
) -> list[tuple[dict[str, Any], int]]:
    """Build the LLM dedupe pool from high-value items plus acceptable fillers.

    The pool reserves slots for top-scored Chinese candidates: a pure
    score-ordered cut lets a wall of 8-9 point English items push every
    6-7 point Chinese item out *before* the min_chinese reserve in
    select_with_source_policy ever sees them (observed on the ai board:
    7 Chinese entries in the filtered set, 1 in the final selection).
    """
    pool_size = min(top_n * DEDUPE_POOL_MULTIPLIER, DEDUPE_MAX_CANDIDATES)
    eligible = [(entry, score) for entry, score in scored if score >= fill_score_floor]
    pool = eligible[:pool_size]
    if min_chinese <= 0 or len(eligible) <= pool_size:
        return pool

    cn_in_pool = sum(1 for entry, _score in pool if _is_chinese_entry(entry))
    if cn_in_pool >= min_chinese:
        return pool

    outside_cn = [
        (entry, score) for entry, score in eligible[pool_size:] if _is_chinese_entry(entry)
    ]
    need = min(min_chinese - cn_in_pool, len(outside_cn))
    if need <= 0:
        return pool

    pool = list(pool)
    replaced = 0
    for i in range(len(pool) - 1, -1, -1):
        if replaced >= need:
            break
        if not _is_chinese_entry(pool[i][0]):
            pool[i] = outside_cn[replaced]
            replaced += 1
    if replaced:
        logger.info("candidate pool: swapped in %d Chinese candidates for quota", replaced)
    return sort_scored_candidates(pool)


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
    as_of = as_of or digest_today()

    data = _load_input(board)
    entries = data.get("entries", [])
    delivered_lookback_days = int(bcfg.get("delivered_lookback_days", 7) or 0)
    delivered_history = load_delivered_history(
        board,
        as_of,
        lookback_days=delivered_lookback_days,
        digest_dir=DIGEST_DIR,
    )
    entries, delivered_filter_stats = filter_delivered_candidates(entries, delivered_history)
    if delivered_filter_stats["total"]:
        logger.info(
            "[%s] delivered history filtered %d entries (url=%d story=%d, lookback=%dd)",
            board,
            delivered_filter_stats["total"],
            delivered_filter_stats["url"],
            delivered_filter_stats["story"],
            delivered_lookback_days,
        )
    max_llm_entries = int(bcfg.get("llm_max_entries", 0) or 0)
    if max_llm_entries > 0 and len(entries) > max_llm_entries:
        logger.info("[%s] trim LLM scoring set: %d -> %d", board, len(entries), max_llm_entries)
        entries = entries[:max_llm_entries]
    if not entries:
        logger.warning("[%s] no entries to digest", board)

    backend = get_backend()
    logger.info(
        "[%s] LLM backend=%s score_model=%s summarize_model=%s",
        board,
        backend.name,
        backend.score_model,
        backend.summarize_model,
    )

    scored: list[tuple[dict[str, Any], int]] = []
    if entries:
        scores = _score_entries(backend, board, entries)
        scored = sort_scored_candidates(zip(entries, scores))

    above_threshold = [(e, sc) for e, sc in scored if sc >= threshold]
    source_policy = dict(bcfg.get("source_policy") or {})
    pool = _candidate_pool(
        scored,
        top_n=top_n,
        fill_score_floor=fill_score_floor,
        min_chinese=int(source_policy.get("min_chinese", 0) or 0),
    )
    clustered, deterministic_merged_urls = cluster_scored_candidates(pool) if pool else ([], [])
    if deterministic_merged_urls:
        logger.info(
            "[%s] deterministic clustering merged %d URLs",
            board,
            len(deterministic_merged_urls),
        )
    deduped, llm_merged_urls = _llm_dedupe(backend, clustered) if clustered else ([], [])
    merged_urls = deterministic_merged_urls + llm_merged_urls
    legacy_score_by_url = {entry.get("url", ""): score for entry, score in scored if entry.get("url")}
    final_scored = _score_candidates_for_selection(board, deduped, legacy_score_by_url, cfg.get("scoring"))
    selected_scored = select_with_source_policy(final_scored, top_n, source_policy)
    selected = [e for e, _sc in selected_scored]
    cn_count = sum(1 for e in selected if _is_chinese_entry(e))
    mix_stats = source_mix_stats(selected)
    logger.info(
        "[%s] scored=%d above_threshold=%d pool=%d unique=%d selected=%d cn=%d mix=%s "
        "(threshold=%d, fill_floor=%d, top_n=%d, policy=%s)",
        board, len(scored), len(above_threshold), len(pool), len(deduped),
        len(selected), cn_count, mix_stats, threshold, fill_score_floor, top_n, source_policy,
    )

    items = _summarize(backend, board, selected) if selected else []
    selected_legacy_scored = [
        (entry, legacy_score_by_url.get(entry.get("url", ""), 5))
        for entry in selected
    ]
    items = _attach_final_scores(board, items, selected_legacy_scored, cfg.get("scoring"))

    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    from datetime import timezone as _tz
    out_path = DIGEST_DIR / f"{board}_{as_of.isoformat()}.json"
    payload = {
        "board": board,
        "display_name": bcfg.get("display_name", board),
        "date": as_of.isoformat(),
        "generated_at": datetime.now(_tz.utc).isoformat().replace("+00:00", "Z"),
        "raw_count": data.get("entry_count", 0),
        "selected_count": len(items),
        "selection_stats": mix_stats,
        "clustering_stats": {
            "deterministic_merged": len(deterministic_merged_urls),
            "llm_merged": len(llm_merged_urls),
            "merged_total": len(merged_urls),
        },
        "delivered_filter_stats": delivered_filter_stats,
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
        score_by_url=legacy_score_by_url,
        selected_urls={entry.get("url", "") for entry in selected if entry.get("url")},
        merged_urls=merged_urls,
        selection_reason_by_url={
            item.get("url", ""): item.get("selection_reason", "")
            for item in items
            if item.get("url")
        },
    )
    write_board_report(board, as_of, report)
    write_board_report_json(
        board=board,
        report_date=as_of,
        feed_stats=data.get("feed_stats") or _fallback_feed_stats(entries),
        entries=entries,
        score_by_url=legacy_score_by_url,
        selected_urls={entry.get("url", "") for entry in selected if entry.get("url")},
    )
    refresh_latest_report(as_of, list((cfg.get("boards") or {}).keys()))
    refresh_weekly_report(as_of, list((cfg.get("boards") or {}).keys()))
    return out_path


def _score_candidates_for_selection(
    board: str,
    candidates: list[tuple[dict[str, Any], int | float]],
    legacy_score_by_url: dict[str, int],
    scoring_config: dict[str, Any] | None,
) -> list[tuple[dict[str, Any], float]]:
    scored: list[tuple[dict[str, Any], float]] = []
    for entry, fallback_score in candidates:
        scoring_entry = dict(entry)
        scoring_entry["score"] = legacy_score_by_url.get(entry.get("url", ""), int(fallback_score))
        breakdown = compute_final_score(board, scoring_entry, scoring_config)
        selected_entry = dict(entry)
        selected_entry["_legacy_score"] = scoring_entry["score"]
        selected_entry["_score_breakdown"] = breakdown
        scored.append((selected_entry, breakdown["final_score"]))
    return sort_scored_candidates(scored)


def _attach_final_scores(
    board: str,
    items: list[dict[str, Any]],
    selected_scored: list[tuple[dict[str, Any], int]],
    scoring_config: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Add deterministic score metadata without changing item order or selection."""
    by_url = {
        str(entry.get("url") or ""): (entry, score)
        for entry, score in selected_scored
        if entry.get("url")
    }
    enriched: list[dict[str, Any]] = []
    for item in items:
        updated = dict(item)
        entry_score = by_url.get(str(item.get("url") or ""))
        if not entry_score:
            enriched.append(updated)
            continue
        entry, score = entry_score
        breakdown = entry.get("_score_breakdown")
        if not isinstance(breakdown, dict):
            scoring_entry = dict(entry)
            scoring_entry["score"] = score
            breakdown = compute_final_score(board, scoring_entry, scoring_config)
        legacy_score = int(entry.get("_legacy_score", score))
        updated["score"] = legacy_score
        updated["score_dimensions"] = dict(entry.get("score_dimensions") or {})
        updated["dimension_score"] = breakdown["dimension_score"]
        updated["final_score"] = breakdown["final_score"]
        updated["score_breakdown"] = {
            "source_bonus": breakdown["source_bonus"],
            "kind_bonus": breakdown["kind_bonus"],
            "freshness_bonus": breakdown["freshness_bonus"],
            "cn_visibility_bonus": breakdown["cn_visibility_bonus"],
        }
        enriched.append(updated)
    return enriched


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
    parser.add_argument("--board", required=True)
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default today)")
    args = parser.parse_args()

    as_of = date.fromisoformat(args.date) if args.date else None
    run(args.board, as_of=as_of)


if __name__ == "__main__":
    main()

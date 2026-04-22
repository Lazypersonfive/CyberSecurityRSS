"""Score entries and generate structured security digest using Claude Haiku."""

import json
import logging
import os
from datetime import date

import anthropic

from fetch_feeds import FeedEntry

logger = logging.getLogger(__name__)

MODEL = "claude-haiku-4-5-20251001"

# Categories to appear in the digest (order matters)
DIGEST_SECTIONS = [
    "漏洞与利用",
    "威胁情报",
    "红蓝对抗",
    "AI 安全",
    "逆向 / 二进制",
    "Web 安全",
    "IoT / 硬件",
    "综合资讯",
]

SYSTEM_PROMPT = """你是一名专业的网络安全分析师，负责整理每日安全情报日报。
你的任务：
1. 对提供的安全文章条目打分（0-10），评估维度：安全相关性、新颖性、实用价值。
2. 筛选高价值条目（分数 >= 6），按安全主题归类，生成中文结构化日报。

评分标准：
- 9-10：0day漏洞、活跃APT组织报告、重大供应链攻击
- 7-8：新型攻击技术、CVE详解、红蓝工具发布、威胁情报
- 5-6：安全研究、工具介绍、技术博客
- 0-4：营销内容、无实质技术价值、重复信息

日报归类映射（从原始分类映射到日报分类）：
- Vulnerability/Exploit/Web/Bug Bounty → 漏洞与利用
- ThreatIntel/APT/Malware → 威胁情报
- RedTeam/BlueTeam/Pentest/CTF → 红蓝对抗
- AI/ML Security → AI 安全
- Reverse/Binary/Pwn → 逆向 / 二进制
- Web Security → Web 安全
- IoT/Hardware → IoT / 硬件
- 其他 → 综合资讯"""


def generate_digest(entries: list[FeedEntry], today: date | None = None) -> str:
    """Score entries and produce a Markdown digest.

    Args:
        entries: Raw feed entries to process.
        today: Date for the report header. Defaults to today.

    Returns:
        Markdown string of the full digest.
    """
    if not entries:
        return _empty_digest(today or date.today())

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = today or date.today()

    scored = _score_entries(client, entries)
    high_value = [e for e, score in scored if score >= 6]

    logger.info("Entries: total=%d high_value=%d", len(entries), len(high_value))

    if not high_value:
        return _empty_digest(today)

    return _build_digest(client, high_value, today, len(entries))


def _score_entries(
    client: anthropic.Anthropic,
    entries: list[FeedEntry],
) -> list[tuple[FeedEntry, int]]:
    """Return (entry, score) pairs. Processes in batches of 50."""
    results: list[tuple[FeedEntry, int]] = []
    batch_size = 50

    for i in range(0, len(entries), batch_size):
        batch = entries[i : i + batch_size]
        scores = _score_batch(client, batch)
        results.extend(zip(batch, scores))

    return results


def _score_batch(client: anthropic.Anthropic, batch: list[FeedEntry]) -> list[int]:
    items = [
        {"idx": i, "title": e.title, "summary": e.summary[:200], "category": e.category}
        for i, e in enumerate(batch)
    ]
    prompt = (
        "请对以下安全文章条目打分（0-10整数）。\n"
        "以 JSON 数组返回，每个元素包含 idx 和 score 字段。\n"
        "只返回 JSON，不要解释。\n\n"
        f"条目列表：\n{json.dumps(items, ensure_ascii=False)}"
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        scored = json.loads(raw)
        score_map = {item["idx"]: int(item["score"]) for item in scored}
    except Exception as exc:
        logger.warning("Score parse failed: %s", exc)
        score_map = {}

    return [score_map.get(i, 5) for i in range(len(batch))]


def _build_digest(
    client: anthropic.Anthropic,
    entries: list[FeedEntry],
    today: date,
    total_fetched: int,
) -> str:
    # Group entries by mapped section
    grouped: dict[str, list[FeedEntry]] = {s: [] for s in DIGEST_SECTIONS}
    for entry in entries:
        section = _map_category(entry.category)
        grouped[section].append(entry)

    # Build entry list string for prompt
    entry_lines = []
    for section, items in grouped.items():
        if items:
            entry_lines.append(f"\n### {section}")
            for e in items[:10]:  # cap 10 per section
                entry_lines.append(f"- [{e.title}]({e.url})\n  摘要: {e.summary[:150]}")

    prompt = (
        "基于以下已分类的安全文章，生成今日安全日报正文。\n"
        "要求：\n"
        "1. 每个分类写 2-3 句简洁的中文总结，说明今日该方向的整体态势\n"
        "2. 列出该分类的重要文章（标题 + 链接），不超过 5 篇\n"
        "3. 语言专业、简洁，面向安全从业者\n"
        "4. 只输出日报正文，从第一个分类标题开始\n\n"
        + "\n".join(entry_lines)
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )

    body = response.content[0].text.strip()
    date_str = today.strftime("%Y-%m-%d")
    stats = f"\n\n---\n📊 今日抓取 **{total_fetched}** 条 | 精选 **{len(entries)}** 条"

    return f"## 🔐 安全日报 {date_str}\n\n{body}{stats}"


def _map_category(raw: str) -> str:
    raw_lower = raw.lower()
    mapping = {
        ("vuln", "exploit", "cve", "bug bounty", "0day"): "漏洞与利用",
        ("threat", "intel", "apt", "malware", "ransomware"): "威胁情报",
        ("red", "blue", "pentest", "ctf", "offensive", "c2"): "红蓝对抗",
        ("ai", "ml", "llm", "machine learning"): "AI 安全",
        ("reverse", "binary", "pwn", "re ", "rop", "kernel"): "逆向 / 二进制",
        ("web", "xss", "sqli", "injection"): "Web 安全",
        ("iot", "hardware", "firmware", "embedded"): "IoT / 硬件",
    }
    for keywords, section in mapping.items():
        if any(k in raw_lower for k in keywords):
            return section
    return "综合资讯"


def _empty_digest(today: date) -> str:
    date_str = today.strftime("%Y-%m-%d")
    return f"## 🔐 安全日报 {date_str}\n\n今日暂无高价值安全资讯。"

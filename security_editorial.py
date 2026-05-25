"""Security-board editorial scoring adjustments."""

from __future__ import annotations

from typing import Any


GEO_ATTRIBUTION_TERMS = (
    "dprk",
    "north korea",
    "lazarus",
    "apt",
    "state-sponsored",
    "nation-state",
    "朝鲜",
    "国家支持",
    "地缘",
)

AI_SECURITY_TERMS = (
    "ai security",
    "llm security",
    "agent security",
    "prompt injection",
    "jailbreak",
    "red team",
    "model supply chain",
    "supply chain",
    "data exfiltration",
    "data leakage",
    "vulnerability",
    "exploit",
    "rce",
    "cve-",
    "malware",
    "stealer",
    "phishing",
    "sandbox",
    "安全",
    "漏洞",
    "提示词注入",
    "越狱",
    "红队",
    "供应链",
    "数据泄露",
    "外泄",
    "攻击",
    "防护",
    "恶意",
    "窃密",
)

AI_CONTEXT_TERMS = (
    "ai",
    "llm",
    "agent",
    "mcp",
    "claude code",
    "copilot",
    "chatgpt",
    "gemini",
    "大模型",
    "智能体",
    "ai编程",
)

SECURITY_CONTEXT_TERMS = (
    "security",
    "vulnerability",
    "exploit",
    "prompt injection",
    "jailbreak",
    "supply chain",
    "postinstall",
    "credential",
    "stealer",
    "scanner",
    "audit",
    "安全",
    "漏洞",
    "攻击",
    "供应链",
    "凭据",
    "窃取",
    "审计",
)


def _get(entry: Any, key: str) -> str:
    if isinstance(entry, dict):
        return str(entry.get(key) or "")
    return str(getattr(entry, key, "") or "")


def adjust_security_score(entry: Any, score: int) -> int:
    """Apply deterministic editorial fit caps after LLM scoring.

    The security board should prioritize vulnerability mechanics, exploitability,
    official advisories, CTF/research writeups, and Chinese technical sources.
    Geopolitical attribution campaigns often read as news but do not match the
    desired daily technical digest unless manually promoted elsewhere.
    """
    text = " ".join(_get(entry, key).lower() for key in ("title", "summary", "title_orig"))
    if any(term in text for term in GEO_ATTRIBUTION_TERMS):
        return min(score, 4)
    return score


def adjust_ai_security_score(entry: Any, score: int) -> int:
    """Keep the AI-security board focused on technical security signals."""
    text = " ".join(
        _get(entry, key).lower()
        for key in ("title", "summary", "title_orig", "category", "feed_title")
    )
    if any(ai_term in text for ai_term in AI_CONTEXT_TERMS) and any(
        security_term in text for security_term in SECURITY_CONTEXT_TERMS
    ):
        return max(score, 6)
    if not any(term in text for term in AI_SECURITY_TERMS):
        return min(score, 3)
    return score

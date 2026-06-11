"""Security-board editorial scoring adjustments.

All ASCII terms are matched with word boundaries (compiled regexes below);
plain substring matching caused real production bugs: "ai" matched inside
"supply chAIn" / "emAIl" and "apt" matched inside "adAPT" / "chAPTer",
which let generic supply-chain news flood the AI-security board and capped
unrelated technical posts. CJK terms keep substring matching (no word
boundaries in Chinese).
"""

from __future__ import annotations

import re
from typing import Any

# In Python re, CJK characters count as word chars, so r"\bMCP\b" fails to
# match in "与MCP服务" (no boundary between 与 and M). Use ASCII-only
# lookarounds instead of \b for terms that must work in mixed CJK/ASCII text.
_L = r"(?<![A-Za-z0-9])"
_R = r"(?![A-Za-z0-9])"


def _ascii_terms(*terms: str) -> str:
    return _L + r"(?:" + "|".join(terms) + r")" + _R


# Geopolitical attribution: campaign coverage whose main hook is "country X
# attacked Y". Numbered APT groups (APT41) match; the bare word "apt" or
# substrings like "adapt" do not.
GEO_ATTRIBUTION_RE = re.compile(
    _ascii_terms(r"dprk", r"north\s+korea", r"lazarus", r"apt[-\s]?\d+",
                 r"state-sponsored", r"nation-state")
    + r"|朝鲜|国家支持|地缘",
    re.IGNORECASE,
)

# Is the entry about AI / LLM / agents at all?
AI_CONTEXT_RE = re.compile(
    _ascii_terms(r"ai", r"llm", r"gpt-?\d*", r"chatgpt", r"claude", r"gemini",
                 r"copilot", r"mcp", r"agentic", r"agents?", r"deepseek",
                 r"openai", r"anthropic")
    + r"|大模型|语言模型|智能体|提示词|人工智能|生成式",
    re.IGNORECASE,
)

# Concrete security mechanisms. Generic words like "security"/"audit"/"安全"
# deliberately do NOT count: "OpenAI announces security program" is still a
# generic-AI marketing item, not an AI-security item.
AI_SEC_MECHANISM_RE = re.compile(
    _ascii_terms(r"prompt\s+injection", r"jailbreak", r"exfiltrat\w*", r"poison\w*",
                 r"sandbox\s+escape", r"rce", r"cve-\d{4}-\d+", r"vulnerabilit\w*",
                 r"exploit\w*", r"malware", r"backdoor", r"stealer", r"postinstall",
                 r"payload", r"credential\s+theft", r"supply[-\s]chain\s+attack",
                 r"red\s+team\w*", r"security\s+benchmark", r"security\s+scan\w*",
                 r"guardrail\w*")
    + r"|提示词注入|越狱|投毒|数据泄露|外泄|漏洞|恶意|后门|窃密|沙箱逃逸|供应链攻击|利用链"
    + r"|红队|安全基准|安全扫描|安全护栏",
    re.IGNORECASE,
)

# Strong AI-security signals that justify flooring the score at selection
# threshold even when the LLM underrates them (often terse technical posts).
AI_SEC_STRONG_RE = re.compile(
    _ascii_terms(r"prompt\s+injection", r"model\s+poisoning", r"data\s+poisoning",
                 r"sandbox\s+escape", r"postinstall", r"supply[-\s]chain\s+attack")
    + r"|提示词注入|投毒|沙箱逃逸|供应链攻击",
    re.IGNORECASE,
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
    text = " ".join(_get(entry, key) for key in ("title", "summary", "title_orig"))
    if GEO_ATTRIBUTION_RE.search(text):
        return min(score, 4)
    return score


def adjust_ai_security_score(entry: Any, score: int) -> int:
    """Keep the AI-security board focused on technical security signals.

    Tiering (Direction 2 in tasks/current_state_2026-06-11.md):
    - not about AI at all       -> cap 3 (belongs on the security board)
    - AI without a mechanism    -> cap 4 (generic AI news, 宁缺毋滥)
    - AI + concrete mechanism   -> keep the LLM score
    - strong AI-security signal -> floor at 6 so terse technical posts the
      LLM underrates still reach the candidate pool
    """
    text = " ".join(
        _get(entry, key)
        for key in ("title", "summary", "title_orig", "category", "feed_title")
    )
    if not AI_CONTEXT_RE.search(text):
        return min(score, 3)
    if not AI_SEC_MECHANISM_RE.search(text):
        return min(score, 4)
    if AI_SEC_STRONG_RE.search(text):
        return max(score, 6)
    return score

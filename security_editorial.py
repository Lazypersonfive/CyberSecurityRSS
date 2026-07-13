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

# Broader editorial fit: legitimate AI-security analysis may describe a risk,
# defence framework or incident before a concrete exploit primitive is known.
# This decides whether the LLM score may stand; only the stronger mechanism
# regex below is allowed to raise a low score to the selection floor.
AI_SEC_CONTEXT_RE = re.compile(
    _ascii_terms(
        r"security", r"safety", r"risk\w*", r"privacy", r"threat\w*", r"attack\w*",
        r"defen[cs]e", r"protect\w*", r"misuse", r"abuse", r"incident", r"data\s+loss",
    )
    + r"|安全|风险|隐私|威胁|攻击|防御|防护|滥用|事故|数据丢失|文件删除|治理",
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

AI_SEC_LOW_VALUE_RE = re.compile(
    _ascii_terms(r"gartner", r"representative\s+vendor", r"market\s+guide", r"funding", r"lawsuit", r"sues?")
    + r"|入选.{0,12}(报告|厂商|榜单)|融资|起诉|商业纠纷",
    re.IGNORECASE,
)

VULN_CONTEXT_RE = re.compile(
    _ascii_terms(r"cve-\d{4}-\d+", r"vulnerabilit\w*", r"zero[-\s]?day", r"0day")
    + r"|漏洞|零日|提权|绕过",
    re.IGNORECASE,
)

VULN_MECHANISM_RE = re.compile(
    _ascii_terms(
        r"use[-\s]after[-\s]free", r"uaf", r"buffer\s+overflow", r"out[-\s]of[-\s]bounds",
        r"sql\s+injection", r"command\s+injection", r"path\s+traversal", r"deseriali[sz]ation",
        r"race\s+condition", r"authentication\s+bypass", r"memory\s+corruption", r"ssrf", r"xss",
    )
    + r"|释放后使用|缓冲区溢出|越界|注入|路径穿越|路径遍历|反序列化|条件竞争|认证绕过"
    + r"|身份验证绕过|内存损坏|跨站脚本|逻辑缺陷|硬编码|权限校验",
    re.IGNORECASE,
)

FINANCE_CONTEXT_RE = re.compile(
    _ascii_terms(
        r"fintech", r"financial", r"finance", r"bank\w*", r"payments?", r"card\s+network",
        r"visa", r"mastercard", r"paypal", r"stripe", r"stablecoin", r"cbdc", r"digital\s+currenc\w*",
        r"clearing", r"settlement", r"remittance", r"lending", r"credit", r"anti[-\s]money\s+laundering",
        r"aml", r"kyc", r"wallet", r"tokeni[sz]ation", r"mica", r"securities", r"insurance",
    )
    + r"|金融科技|金融机构|银行|支付|卡组织|稳定币|数字人民币|数字货币|央行|清算|结算|跨境"
    + r"|信贷|贷款|信用卡|风控|反洗钱|钱包|证券|保险|代币化",
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
    if VULN_CONTEXT_RE.search(text) and not VULN_MECHANISM_RE.search(text):
        return min(score, 8)
    return score


def adjust_ai_security_score(entry: Any, score: int) -> int:
    """Keep the AI-security board focused on technical security signals.

    Tiering (Direction 2 in tasks/current_state_2026-06-11.md):
    - not about AI at all       -> cap 3 (belongs on the security board)
    - AI without security fit   -> cap 3 (generic AI news, below backfill)
    - AI + security context     -> keep the LLM score
    - strong AI-security signal -> floor at 6 so terse technical posts the
      LLM underrates still reach the candidate pool
    """
    text = " ".join(
        _get(entry, key)
        for key in ("title", "summary", "title_orig", "category", "feed_title")
    )
    if not AI_CONTEXT_RE.search(text):
        return min(score, 3)
    if AI_SEC_LOW_VALUE_RE.search(text):
        return min(score, 3)
    if not AI_SEC_CONTEXT_RE.search(text) and not AI_SEC_MECHANISM_RE.search(text):
        return min(score, 3)
    if AI_SEC_STRONG_RE.search(text):
        return max(score, 6)
    return score


def adjust_finance_score(entry: Any, score: int) -> int:
    """Keep generic AI, personnel and platform-policy news out of fintech."""
    text = " ".join(
        _get(entry, key)
        for key in ("title", "summary", "title_orig", "category", "feed_title")
    )
    if not FINANCE_CONTEXT_RE.search(text):
        return min(score, 3)
    return score

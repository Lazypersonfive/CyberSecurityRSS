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


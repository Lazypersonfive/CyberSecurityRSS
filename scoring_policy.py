"""Deterministic final-score policy for selected digest items.

The model can judge item-level value, but source tier, source kind and
freshness should stay explicit and tunable in code.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from source_policy import source_profile


DEFAULT_SCORING_CONFIG: dict[str, Any] = {
    "default": {
        "source_bonus": {
            "t1": 1.0,
            "t1_5": 0.5,
            "t2": 0.0,
            "unknown": -0.3,
        },
        "kind_bonus": {
            "official": 0.5,
            "official_x": 0.3,
            "expert": 0.2,
            "expert_x": 0.2,
            "cn_official": 0.5,
            "cn_expert": 0.3,
            "google_news": -1.0,
            "community": -0.5,
        },
        "freshness_bonus": {
            "within_12h": 0.3,
            "within_24h": 0.1,
        },
        "cn_visibility_bonus": {
            "bonus": 0.3,
            "kinds": ["cn_official", "cn_expert"],
            "tiers": ["t1", "t1_5", "t2"],
        },
    },
    "boards": {
        "security": {
            "dimension_weights": {
                "relevance": 0.25,
                "technical_depth": 0.25,
                "exploitability": 0.20,
                "impact_scope": 0.20,
                "actionability": 0.10,
            }
        },
        "ai_security": {
            "dimension_weights": {
                "security_relevance": 0.30,
                "technical_depth": 0.25,
                "practical_risk": 0.20,
                "agent_model_relevance": 0.15,
                "actionability": 0.10,
            }
        },
        "ai": {
            "dimension_weights": {
                "relevance": 0.20,
                "novelty": 0.25,
                "entity_importance": 0.20,
                "developer_relevance": 0.20,
                "ecosystem_impact": 0.15,
            }
        },
        "finance": {
            "dimension_weights": {
                "relevance": 0.25,
                "institution_importance": 0.25,
                "technology_depth": 0.20,
                "market_or_regulatory_impact": 0.20,
                "actionability": 0.10,
            }
        },
    },
}


def load_scoring_config(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return merged scoring config from full config.yaml or scoring-only dict."""
    provided = config or {}
    if "scoring" in provided:
        provided = provided.get("scoring") or {}

    merged = deepcopy(DEFAULT_SCORING_CONFIG)
    _deep_update(merged, provided)
    return merged


def compute_dimension_score(
    board: str,
    entry: dict[str, Any],
    scoring_config: dict[str, Any] | None = None,
) -> float:
    """Compute the weighted 0-10 model dimension score.

    Missing multidimensional output falls back to the legacy scalar score so
    the pipeline can adopt dimensions gradually.
    """
    config = load_scoring_config(scoring_config)
    weights = (
        (config.get("boards") or {})
        .get(board, {})
        .get("dimension_weights", {})
    )
    dimensions = entry.get("score_dimensions") or entry.get("dimensions") or {}
    weighted_total = 0.0
    weight_total = 0.0
    if isinstance(dimensions, dict):
        for key, weight in weights.items():
            if key not in dimensions:
                continue
            value = _coerce_float(dimensions.get(key))
            if value is None:
                continue
            weighted_total += _clamp(value) * float(weight)
            weight_total += float(weight)
    if weight_total > 0:
        return round(weighted_total / weight_total, 2)

    fallback = _coerce_float(entry.get("score"))
    if fallback is None:
        fallback = _coerce_float(entry.get("quality_score"))
    if fallback is None:
        fallback = 5.0
    return round(_clamp(fallback), 2)


def compute_final_score(
    board: str,
    entry: dict[str, Any],
    scoring_config: dict[str, Any] | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, float]:
    """Combine model score and deterministic source/freshness bonuses."""
    config = load_scoring_config(scoring_config)
    defaults = config.get("default") or {}
    profile = source_profile(entry)
    dimension = compute_dimension_score(board, entry, config)
    source_bonus = float((defaults.get("source_bonus") or {}).get(profile.source_tier, 0.0))
    kind_bonus = float((defaults.get("kind_bonus") or {}).get(profile.source_kind, 0.0))
    freshness_bonus = _freshness_bonus(entry.get("published"), defaults.get("freshness_bonus") or {}, now)
    cn_visibility_bonus = _cn_visibility_bonus(profile, defaults.get("cn_visibility_bonus") or {})

    final = _clamp(dimension + source_bonus + kind_bonus + freshness_bonus + cn_visibility_bonus)
    return {
        "dimension_score": round(dimension, 2),
        "source_bonus": round(source_bonus, 2),
        "kind_bonus": round(kind_bonus, 2),
        "freshness_bonus": round(freshness_bonus, 2),
        "cn_visibility_bonus": round(cn_visibility_bonus, 2),
        "final_score": round(final, 2),
    }


def _deep_update(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = deepcopy(value)


def _coerce_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _clamp(value: float, low: float = 0.0, high: float = 10.0) -> float:
    return max(low, min(high, value))


def _freshness_bonus(published: Any, config: dict[str, Any], now: datetime | None) -> float:
    published_at = _parse_datetime(published)
    if not published_at:
        return 0.0
    reference = now or datetime.now(timezone.utc)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)
    seconds = max(0.0, (reference - published_at).total_seconds())
    if seconds <= 12 * 3600:
        return float(config.get("within_12h", 0.0))
    if seconds <= 24 * 3600:
        return float(config.get("within_24h", 0.0))
    return 0.0


def _parse_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        text = value.strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
    else:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _cn_visibility_bonus(profile: Any, config: dict[str, Any]) -> float:
    kinds = set(config.get("kinds") or [])
    tiers = set(config.get("tiers") or [])
    if profile.source_kind in kinds and profile.source_tier in tiers:
        return float(config.get("bonus", 0.0))
    return 0.0

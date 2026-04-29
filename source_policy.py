"""Deterministic source profiling and final-selection policy.

The LLM decides news value; this module enforces editorial constraints that
should not be left to stochastic model output: source diversity, Google News
caps, and Chinese-source visibility.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import urlparse


AGGREGATOR_HOSTS = {
    "news.google.com",
    "news.yahoo.com",
    "msn.com",
    "rss.app",
}

CHINESE_HOSTS = {
    # Explicit Chinese-language sources whose host is not under .cn.
    "mp.weixin.qq.com",
    "wechat2rss.xlab.app",
    "anquanke.com",
    "freebuf.com",
    "seebug.org",
}


@dataclass(frozen=True)
class SourceProfile:
    host: str
    feed_host: str
    source_key: str
    is_google_news: bool
    is_aggregator: bool
    is_wechat: bool
    is_chinese: bool
    is_direct: bool


def _get(entry: Any, key: str, default: str = "") -> str:
    if isinstance(entry, dict):
        return str(entry.get(key) or default)
    return str(getattr(entry, key, default) or default)


def _host(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").removeprefix("www.").lower()
    except ValueError:
        return ""


def _host_matches(host: str, candidates: Iterable[str]) -> bool:
    return any(host == candidate or host.endswith(f".{candidate}") for candidate in candidates)


def _has_cjk(text: str) -> bool:
    return any("\u3400" <= ch <= "\u9fff" for ch in text or "")


def source_profile(entry: Any) -> SourceProfile:
    """Classify one entry for deterministic editorial policy."""
    url = _get(entry, "url")
    feed_url = _get(entry, "feed_url")
    host = _host(url)
    feed_host = _host(feed_url)
    source_key = host or feed_host

    is_google_news = host == "news.google.com" or feed_host == "news.google.com"
    is_aggregator = _host_matches(host, AGGREGATOR_HOSTS) or _host_matches(
        feed_host,
        AGGREGATOR_HOSTS,
    )
    is_wechat = "wechat2rss" in feed_host or host == "mp.weixin.qq.com"
    text = " ".join(
        _get(entry, field)
        for field in ("title", "title_orig", "feed_title", "summary")
    )
    is_chinese = (
        _has_cjk(text)
        or is_wechat
        or _host_matches(host, CHINESE_HOSTS)
        or _host_matches(feed_host, CHINESE_HOSTS)
        or host.endswith(".cn")
        or feed_host.endswith(".cn")
    )

    return SourceProfile(
        host=host,
        feed_host=feed_host,
        source_key=source_key,
        is_google_news=is_google_news,
        is_aggregator=is_aggregator,
        is_wechat=is_wechat,
        is_chinese=is_chinese,
        is_direct=not is_aggregator,
    )


def source_priority(entry: Any) -> int:
    """Tie-breaker priority; the LLM score remains the primary signal."""
    profile = source_profile(entry)
    priority = 0
    if profile.is_direct:
        priority += 20
    if profile.is_wechat:
        priority += 2
    if profile.is_chinese:
        priority += 5
    if profile.is_aggregator:
        priority -= 15
    return priority


def sort_scored_candidates(
    candidates: Iterable[tuple[dict[str, Any], int]]
) -> list[tuple[dict[str, Any], int]]:
    return sorted(
        candidates,
        key=lambda item: (item[1], source_priority(item[0])),
        reverse=True,
    )


def select_with_source_policy(
    candidates: Iterable[tuple[dict[str, Any], int]],
    top_n: int,
    policy: dict[str, Any] | None = None,
) -> list[tuple[dict[str, Any], int]]:
    """Select top candidates while enforcing source diversity constraints.

    The function first reserves required Chinese/direct slots, then fills by
    score under caps. Caps are hard by default; sparse boards may publish fewer
    than top_n items unless allow_cap_relaxation is explicitly enabled.
    """
    policy = policy or {}
    ranked = sort_scored_candidates(candidates)
    if top_n <= 0 or not ranked:
        return []

    min_chinese = max(0, int(policy.get("min_chinese", 0)))
    min_direct = max(0, int(policy.get("min_direct", 0)))
    max_google_news = _optional_int(policy.get("max_google_news"), top_n)
    max_aggregator = _optional_int(policy.get("max_aggregator"), top_n)
    max_per_source = _optional_int(policy.get("max_per_source"), top_n)
    allow_cap_relaxation = bool(policy.get("allow_cap_relaxation", False))

    selected: list[tuple[dict[str, Any], int]] = []
    selected_ids: set[str] = set()
    source_counts: Counter[str] = Counter()
    google_count = 0
    aggregator_count = 0

    def identity(entry: dict[str, Any]) -> str:
        return str(entry.get("url") or id(entry))

    def can_add(
        item: tuple[dict[str, Any], int],
        *,
        enforce_source_cap: bool = True,
        enforce_aggregate_caps: bool = True,
    ) -> bool:
        nonlocal google_count, aggregator_count
        entry, _score = item
        if identity(entry) in selected_ids:
            return False
        if len(selected) >= top_n:
            return False

        profile = source_profile(entry)
        if enforce_source_cap and max_per_source is not None:
            if source_counts[profile.source_key] >= max_per_source:
                return False
        if enforce_aggregate_caps:
            if (
                profile.is_google_news
                and max_google_news is not None
                and google_count >= max_google_news
            ):
                return False
            if (
                profile.is_aggregator
                and max_aggregator is not None
                and aggregator_count >= max_aggregator
            ):
                return False
        return True

    def add(item: tuple[dict[str, Any], int]) -> None:
        nonlocal google_count, aggregator_count
        entry, _score = item
        profile = source_profile(entry)
        selected.append(item)
        selected_ids.add(identity(entry))
        source_counts[profile.source_key] += 1
        if profile.is_google_news:
            google_count += 1
        if profile.is_aggregator:
            aggregator_count += 1

    def reserve(predicate, count: int) -> None:
        if count <= 0:
            return
        current = sum(1 for entry, _score in selected if predicate(source_profile(entry)))
        for item in ranked:
            if current >= count:
                break
            if predicate(source_profile(item[0])) and can_add(item):
                add(item)
                current += 1

    reserve(lambda profile: profile.is_chinese, min_chinese)
    reserve(lambda profile: profile.is_direct, min_direct)

    for item in ranked:
        if can_add(item):
            add(item)

    if allow_cap_relaxation:
        # Explicit opt-in for sparse boards. Keep hard caps by default: source
        # quality is more important than filling every slot.
        for item in ranked:
            if can_add(item, enforce_aggregate_caps=False):
                add(item)

        for item in ranked:
            if can_add(item, enforce_source_cap=False, enforce_aggregate_caps=False):
                add(item)

    return sort_scored_candidates(selected)[:top_n]


def source_mix_stats(entries: Iterable[dict[str, Any]]) -> dict[str, int]:
    stats: Counter[str] = Counter()
    for entry in entries:
        profile = source_profile(entry)
        stats["total"] += 1
        if profile.is_google_news:
            stats["google_news"] += 1
        if profile.is_aggregator:
            stats["aggregator"] += 1
        if profile.is_chinese:
            stats["chinese"] += 1
        if profile.is_direct:
            stats["direct"] += 1
        if profile.is_wechat:
            stats["wechat"] += 1
    return dict(stats)


def _optional_int(value: Any, default: int | None) -> int | None:
    if value is None:
        return default
    parsed = int(value)
    return parsed if parsed >= 0 else None

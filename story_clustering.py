"""Deterministic story clustering before LLM dedupe.

This module only merges high-confidence duplicates. Ambiguous items should
remain separate and let the existing LLM dedupe act as a fallback.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlparse

from datetime import datetime, timedelta, timezone

from source_policy import source_priority, source_profile


CVE_RE = re.compile(r"CVE[-–—]\d{4}[-–—]\d{4,7}", re.IGNORECASE)
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+-]{2,}|\d{1,7}|[\u3400-\u9fff]{2,}")
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid"}
# Only strip short " - source" tails. Do not treat Chinese "导语 | 正文" as a suffix.
TITLE_SUFFIX_RE = re.compile(r"\s[-–—]\s[^-–—]{1,24}$")
RT_PREFIX_RE = re.compile(r"^rt\s+[^:]{1,80}:\s*", re.IGNORECASE)
SAME_SOURCE_WINDOW = timedelta(hours=36)
PRODUCT_JOIN_MIN = 8
STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "into", "over",
    "new", "news", "update", "updates", "launch", "launches", "release",
    "releases", "released", "announces", "says", "report", "reports",
    "security", "cybersecurity", "vulnerability", "vulnerabilities",
}
ANCHOR_TOKENS = {
    "openai", "chatgpt", "gpt", "codex", "anthropic", "claude", "google", "gemini",
    "deepseek", "microsoft", "windows", "apple", "linux", "kernel",
    "cisco", "fortinet", "ivanti", "palo", "zscaler", "sap", "github", "u-boot",
    "visa", "mastercard", "stripe", "paypal", "alipay", "wechat",
}
SOURCE_KIND_RANK = {
    "official": 70,
    "official_x": 60,
    "expert": 50,
    "expert_x": 50,
    "cn_official": 45,
    "cn_expert": 40,
    "media": 20,
    "community": 10,
    "google_news": -20,
}
NARROW_PRODUCT_TOKENS = {"u-boot"}
VULNERABILITY_TOPIC_TOKENS = {"漏洞", "flaw", "flaws", "cve", "zero-day", "0day"}
DYNAMIC_ANCHOR_STOPWORDS = {
    "attackers", "developers", "framework", "malicious", "malware",
    "ransomware", "researchers", "software", "technology",
}
GENERIC_PRODUCT_WORDS = STOPWORDS | DYNAMIC_ANCHOR_STOPWORDS | {
    "open", "source", "official", "beta", "today", "first", "live",
    "coding", "agent", "guess", "whose", "simulator", "accurate",
    "enough", "walk", "way", "model", "startup", "gateway",
    "finally", "strike", "deal", "acquire", "reportedly", "will",
    "releasing", "preview", "researchers", "support", "using",
}
CJK_GENERIC_TOKENS = {
    "安全", "漏洞", "攻击", "研究", "分析", "发布", "报告", "技术", "网络",
    "数据", "恶意", "关注", "一批", "相关", "公布", "资讯", "动态", "威胁",
    "情报", "防护", "检测", "更新", "补丁", "系统", "用户", "企业", "国内",
    "国际", "最新", "重要", "重大", "近日", "本周", "今日", "通过", "进行",
    "针对", "关于", "以及", "组织", "行动", "打击", "启动", "披露", "首批",
    "规模", "最大", "木马", "域名", "地址", "专项", "治理", "文章", "内容",
    "平台", "模型", "智能", "人工", "产品", "公司", "官方", "媒体", "新闻",
    "事件", "问题", "风险", "防御", "利用", "绕过", "提权", "一批",
}


def story_id_for_entry(entry: dict[str, Any]) -> str:
    cves = _extract_cves(entry)
    if cves:
        return "cve:" + ",".join(cves)
    key = _canonical_url_key(str(entry.get("url") or ""))
    if key:
        return "url:" + key
    tokens = sorted(_title_tokens(entry))
    digest = hashlib.sha1(" ".join(tokens).encode("utf-8")).hexdigest()[:12]
    return f"title:{digest}"


def probable_same_story(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Conservative gate for an LLM-proposed duplicate pair."""
    if set(_static_story_keys(left)) & set(_static_story_keys(right)):
        return True
    left_tokens = _llm_validation_tokens(left)
    right_tokens = _llm_validation_tokens(right)
    if _same_title_story(left_tokens, right_tokens):
        return True
    shared = left_tokens & right_tokens
    union = left_tokens | right_tokens
    # LLM-proposed cross-language pairs often retain only the entity and one
    # product/release token (for example Claude + Fable). That is enough as a
    # validation gate, but not enough for deterministic clustering on its own.
    shared_anchors = _shared_anchor_tokens(shared)
    if shared_anchors and shared - shared_anchors:
        return True
    return len(shared) >= 5 and bool(union) and len(shared) / len(union) >= 0.70


def cluster_scored_candidates(
    candidates: Iterable[tuple[dict[str, Any], float]],
) -> tuple[list[tuple[dict[str, Any], float]], list[str]]:
    items = [(dict(entry), score) for entry, score in candidates]
    if len(items) <= 1:
        return items, []

    clusters: dict[int, list[int]] = defaultdict(list)
    uf = _UnionFind(len(items))
    static_keys: dict[str, int] = {}
    tokens = [_title_tokens(entry) for entry, _score in items]

    for idx, (entry, _score) in enumerate(items):
        for key in _static_story_keys(entry):
            if key in static_keys:
                uf.union(static_keys[key], idx)
            else:
                static_keys[key] = idx

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if uf.find(i) == uf.find(j):
                continue
            left_entry, _left_score = items[i]
            right_entry, _right_score = items[j]
            if _same_title_story(tokens[i], tokens[j]) or _same_source_product_story(
                left_entry, right_entry
            ):
                uf.union(i, j)

    for idx in range(len(items)):
        clusters[uf.find(idx)].append(idx)

    result: list[tuple[dict[str, Any], float]] = []
    merged_urls: list[str] = []
    for idxs in clusters.values():
        if len(idxs) == 1:
            entry, score = items[idxs[0]]
            entry.setdefault("story_id", story_id_for_entry(entry))
            result.append((entry, score))
            continue
        best_idx = max(idxs, key=lambda i: _primary_rank(items[i]))
        best_entry, best_score = items[best_idx]
        related = []
        for i in idxs:
            if i == best_idx:
                continue
            url = str(items[i][0].get("url") or "")
            if url:
                related.append(url)
                merged_urls.append(url)
        existing_related = [url for url in best_entry.get("related_urls") or [] if url]
        best_entry["related_urls"] = _dedupe_preserve_order(existing_related + related)
        best_entry["related_count"] = len(best_entry["related_urls"])
        best_entry["story_id"] = _shared_story_id([items[i][0] for i in idxs])
        result.append((best_entry, best_score))

    result.sort(key=lambda item: (item[1], source_priority(item[0])), reverse=True)
    return result, merged_urls


def _static_story_keys(entry: dict[str, Any]) -> list[str]:
    keys = [f"cve:{cve}" for cve in _extract_cves(entry)]
    url_key = _canonical_url_key(str(entry.get("url") or ""))
    if url_key:
        keys.append(f"url:{url_key}")
    return keys


def _shared_story_id(entries: list[dict[str, Any]]) -> str:
    cves = sorted({cve for entry in entries for cve in _extract_cves(entry)})
    if cves:
        return "cve:" + ",".join(cves)
    first = min(entries, key=lambda entry: _stable_entry_key(entry))
    return story_id_for_entry(first)


def _extract_cves(entry: dict[str, Any]) -> list[str]:
    explicit = entry.get("cve_ids") or []
    text = " ".join(str(entry.get(key) or "") for key in ("title", "title_orig", "summary"))
    found = list(explicit) + CVE_RE.findall(text)
    return sorted({str(cve).lower().replace("–", "-").replace("—", "-") for cve in found if cve})


def _canonical_url_key(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").removeprefix("www.").lower()
    if not host or host in {"news.google.com", "rsshub.app", "rss.app"}:
        return ""
    path = re.sub(r"/+", "/", parsed.path or "/").rstrip("/").lower()
    if not path or path == "/":
        return ""
    query = urlencode([
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=False)
        if key.lower() not in TRACKING_PARAMS
    ])
    if query:
        return f"{host}{path}?{query}"
    return f"{host}{path}"


def _title_tokens(entry: dict[str, Any]) -> set[str]:
    title = str(entry.get("title") or entry.get("title_orig") or "")
    title = TITLE_SUFFIX_RE.sub("", title).lower()
    tokens = _tokens_from_text(title)
    tokens.update(_extract_cves(entry))
    return tokens


def _llm_validation_tokens(entry: dict[str, Any]) -> set[str]:
    """Use the RSS excerpt only to validate an LLM-proposed story group."""
    tokens = _title_tokens(entry)
    tokens.update(_tokens_from_text(str(entry.get("summary") or "")[:600].lower()))
    return tokens


def _tokens_from_text(text: str) -> set[str]:
    tokens: set[str] = set()
    for token in TOKEN_RE.findall(text):
        if token in STOPWORDS:
            continue
        if re.fullmatch(r"[\u3400-\u9fff]+", token):
            tokens.update(token[idx:idx + 2] for idx in range(len(token) - 1))
        else:
            tokens.add(token)
    return tokens


def _same_title_story(left: set[str], right: set[str]) -> bool:
    if not left or not right:
        return False
    shared = left & right
    if len(shared) < 3:
        if shared & NARROW_PRODUCT_TOKENS and shared & VULNERABILITY_TOPIC_TOKENS:
            return True
        return _vendor_and_specific_product(shared)
    shared_anchors = _shared_anchor_tokens(shared)
    if not shared_anchors:
        return False
    left_without_anchor = left - shared_anchors
    right_without_anchor = right - shared_anchors
    shared_without_anchor = left_without_anchor & right_without_anchor
    if len(shared_without_anchor) < 2:
        if shared_anchors & NARROW_PRODUCT_TOKENS and shared & VULNERABILITY_TOPIC_TOKENS:
            return True
        return _vendor_and_specific_product(shared)
    if shared_anchors - ANCHOR_TOKENS:
        return True
    if len(shared_without_anchor) >= 4:
        return True
    if len(shared_without_anchor) >= 3 and any(token.isdigit() for token in shared_without_anchor):
        return True
    union = left | right
    return len(shared) / len(union) >= 0.45


def _shared_anchor_tokens(shared: set[str]) -> set[str]:
    dynamic = {
        token
        for token in shared
        if token.isascii()
        and token.replace("-", "").isalnum()
        and len(token) >= 8
        and token not in DYNAMIC_ANCHOR_STOPWORDS
    }
    cjk_dynamic = {
        token
        for token in shared
        if re.fullmatch(r"[\u3400-\u9fff]{2}", token)
        and token not in CJK_GENERIC_TOKENS
    }
    return (shared & ANCHOR_TOKENS) | dynamic | cjk_dynamic


def _vendor_and_specific_product(shared: set[str]) -> bool:
    anchors = _shared_anchor_tokens(shared)
    return bool((anchors - ANCHOR_TOKENS) and (anchors & ANCHOR_TOKENS))


def _same_source_product_story(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Merge same-feed bursts that share a specific product, not a vendor name."""
    source_key = _source_cluster_key(left)
    if not source_key or source_key != _source_cluster_key(right):
        return False
    if not _within_hours(left, right, SAME_SOURCE_WINDOW):
        return False
    identity = _source_identity_tokens(left) | _source_identity_tokens(right)
    shared = (_product_tokens(left) & _product_tokens(right)) - identity
    return bool(shared)


def _source_cluster_key(entry: dict[str, Any]) -> str:
    profile = source_profile(entry)
    if profile.x_handle:
        return f"x:{profile.x_handle.lower()}"
    feed_url = str(entry.get("feed_url") or "").strip()
    if feed_url:
        return f"feed:{feed_url}"
    return f"source:{profile.source_key}" if profile.source_key else ""


def _source_identity_tokens(entry: dict[str, Any]) -> set[str]:
    profile = source_profile(entry)
    tokens = set(_tokens_from_text(str(entry.get("feed_title") or "").lower()))
    if profile.x_handle:
        handle = profile.x_handle.lower()
        tokens.add(handle)
        tokens.update(_tokens_from_text(handle))
    host = (profile.host or profile.feed_host or "").split(".")
    tokens.update(part for part in host if len(part) >= 3 and part not in {"com", "net", "org", "app"})
    return tokens


def _product_tokens(entry: dict[str, Any]) -> set[str]:
    title = str(entry.get("title") or entry.get("title_orig") or "")
    title = TITLE_SUFFIX_RE.sub("", title)
    title = RT_PREFIX_RE.sub("", title).lower()
    tokens = _tokens_from_text(title)
    products: set[str] = set()
    for token in tokens:
        if _is_specific_product_token(token):
            products.add(token)
        if re.fullmatch(r"[\u3400-\u9fff]{2}", token) and token not in CJK_GENERIC_TOKENS:
            products.add(token)
    words = [token.lower() for token in TOKEN_RE.findall(title) if token.lower() not in STOPWORDS]
    for idx in range(len(words) - 1):
        left, right = words[idx], words[idx + 1]
        if not left.isascii() or not right.isascii():
            continue
        if left in GENERIC_PRODUCT_WORDS and right in GENERIC_PRODUCT_WORDS:
            continue
        joined = re.sub(r"[^a-z0-9]", "", left + right)
        if len(joined) >= PRODUCT_JOIN_MIN:
            products.add(joined)
    return products


def _is_specific_product_token(token: str) -> bool:
    if token in GENERIC_PRODUCT_WORDS or token in DYNAMIC_ANCHOR_STOPWORDS:
        return False
    return _is_long_product_token(token)


def _is_long_product_token(token: str) -> bool:
    compact = token.replace("-", "").replace(" ", "")
    return compact.isascii() and compact.isalnum() and len(compact) >= 6


def _within_hours(left: dict[str, Any], right: dict[str, Any], window: timedelta) -> bool:
    left_at = _parse_datetime(left.get("published"))
    right_at = _parse_datetime(right.get("published"))
    if left_at is None or right_at is None:
        return False
    return abs(left_at - right_at) <= window


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


def _primary_rank(item: tuple[dict[str, Any], float]) -> tuple[int, float, int]:
    entry, score = item
    profile = source_profile(entry)
    return (
        SOURCE_KIND_RANK.get(profile.source_kind, 0),
        float(score),
        source_priority(entry),
    )


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _stable_entry_key(entry: dict[str, Any]) -> str:
    url_key = _canonical_url_key(str(entry.get("url") or ""))
    if url_key:
        return url_key
    return " ".join(sorted(_title_tokens(entry)))


class _UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self.parent[rb] = ra

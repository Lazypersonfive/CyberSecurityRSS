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

from source_policy import source_priority, source_profile


CVE_RE = re.compile(r"CVE[-–—]\d{4}[-–—]\d{4,7}", re.IGNORECASE)
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+-]{2,}|\d{4,7}|[\u3400-\u9fff]{2,}")
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid"}
TITLE_SUFFIX_RE = re.compile(r"\s[-–—|]\s[^-–—|]+$")
STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "into", "over",
    "new", "news", "update", "updates", "launch", "launches", "release",
    "releases", "released", "announces", "says", "report", "reports",
    "security", "cybersecurity", "vulnerability", "vulnerabilities",
}
ANCHOR_TOKENS = {
    "openai", "chatgpt", "gpt", "anthropic", "claude", "google", "gemini",
    "deepseek", "microsoft", "windows", "apple", "linux", "kernel",
    "cisco", "fortinet", "ivanti", "palo", "zscaler", "sap", "github",
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
            if _same_title_story(tokens[i], tokens[j]):
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
    tokens = {token for token in TOKEN_RE.findall(title) if token not in STOPWORDS}
    tokens.update(_extract_cves(entry))
    return tokens


def _same_title_story(left: set[str], right: set[str]) -> bool:
    if not left or not right:
        return False
    shared = left & right
    if len(shared) < 3:
        return False
    shared_anchors = shared & ANCHOR_TOKENS
    if not shared_anchors:
        return False
    left_without_anchor = left - shared_anchors
    right_without_anchor = right - shared_anchors
    if len(left_without_anchor & right_without_anchor) < 2:
        return False
    union = left | right
    return len(shared) / len(union) >= 0.45


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

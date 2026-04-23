"""Post-fetch filtering: WAF detection, blacklist, CVE-based semantic dedup.

Applied after fetch_feeds.py returns raw entries, before writing latest.json.
Keeps entries widely (breadth-first philosophy) but flags/drops obvious noise.
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from fetch_feeds import FeedEntry

# --- WAF / verification-page markers ------------------------------------

WAF_MARKERS = (
    "CF_APP_WAF",
    "sceneId",
    "traceid",
    "captcha",
    "Just a moment",
    "请完成验证",
    "请开启JavaScript",
    "Please enable JavaScript",
    "appkey",
    "requestInfo",
)

# --- Title blacklist: recruiting / weekly-thread / Q&A chatter ----------

TITLE_BLACKLIST_SUBSTR = (
    # Recruiting / career
    "招聘",
    "实习生",
    "招人",
    "求职",
    "内推",
    "Horror stories",
    "Job Market",
    "Career Advice",
    "Mentorship",
    "Salary",
    "Billing Ratio",
    "how to become",
    "entering pentesting",
    "enter pentesting",
    "first pentest",
    # Forum chatter / asking for help
    "Questions about",
    "AMA",
    "Weekly Thread",
    "Weekend Thread",
    "Mod Q&A",
    "Looking for teammates",
    "Looking for Pre-",
    "Looking for affordable",
    "Best laptop",
    "Best tool for",
    "Best X for",
    "affordable/free alternatives",
    "Pre-Pentest Document Templates",
    "Digital prank",
    "wildest shadow IT",
    "projects should I build",
    "struggle with this",
    "What's your",
    "What is your current workflow",
    "wild west stories",
    "beginner",
    "Beginner",
    # Aggregator meta-posts (SecWiki daily digest)
    "合集",
    " Review",
    # Reddit removed content
    "[ Removed by Reddit ]",
    "[removed]",
    "[deleted]",
    # Claude / Anthropic help-center docs (surface via site:claude.com query)
    "Claude Help Center",
)

# --- Title regex blacklist (for patterns that need more flexibility) ----

TITLE_REGEX_BLACKLIST = (
    re.compile(r"^\s*(What|How|Is it|Are there|Why|Where|Do|Does|Should|Can|Could)\b.*\?\s*$", re.IGNORECASE),
    re.compile(r"^\s*Tips? for\b", re.IGNORECASE),
    re.compile(r"^\s*Help with\b", re.IGNORECASE),
    # CTF/HTB walkthroughs: training content, not news
    re.compile(r"(HTB|Hack The Box|HackTheBox).+(Walkthrough|Machine)", re.IGNORECASE),
    re.compile(r"Walkthrough\s*[–—|]", re.IGNORECASE),
    # Image/audio generation tutorials from mixed-content blogs
    re.compile(r"\b(photorealistic|non-photographic|ComfyUI|stable diffusion)\b", re.IGNORECASE),
    # Vague opinion titles that end in "?"
    re.compile(r"\bSkynet\b", re.IGNORECASE),
    # Numbered table-of-contents entries (miloserdov pattern "11. Foo")
    re.compile(r"^\s*\d+\.\s+[A-Z]"),
)

# --- Source-level blacklist (host substring match) ----------------------

SOURCE_BLACKLIST_SUBSTR = (
    # Reddit help/career subs — high-volume forum chatter
    "reddit.com/r/AskNetsec",
    "reddit.com/r/cybersecurity_help",
    # Off-topic aggregators
    "buaq.net",                 # coffee tutorials, lifestyle content
    # Dev personal blogs miscategorized as security research
    "lucumr.pocoo.org",         # Armin Ronacher (Flask author) — Python/compiler opinions
    "maskray.me",               # Fangrui Song — LLVM/linker deep dives, not security
)

# --- Thresholds ---------------------------------------------------------

MIN_SUMMARY_LEN = 30  # below this, mark as title_only

CVE_RE = re.compile(r"CVE[-–—]\d{4}[-–—]\d{4,7}", re.IGNORECASE)
PATCH_TUESDAY_RE = re.compile(r"(微软|Microsoft).*补丁日", re.IGNORECASE)

# Title-normalized dedup: strip punctuation, lowercase ASCII, collapse whitespace.
TITLE_NORMALIZE_RE = re.compile(r"[^\w\u3400-\u4dbf\u4e00-\u9fff]+", re.UNICODE)
# Google News RSS appends " - SourceName" to every headline; Yahoo/MSN similar.
# Strip this suffix before normalizing so cross-publisher duplicates collapse.
TITLE_SUFFIX_SEP_RE = re.compile(r"\s[-–—|]\s[^-–—|]+$")
TITLE_STOPWORDS = frozenset((
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "of", "to", "in", "on", "at", "by", "for", "with", "from", "as",
    "and", "or", "but", "if", "then", "than", "that", "this", "these", "those",
    "it", "its", "has", "have", "had", "will", "would", "can", "could",
    "new", "live", "now", "update", "updated", "report", "reports",
    # Generic news verbs/adjectives that contribute no story identity
    "launches", "launch", "launched", "launching",
    "announces", "announce", "announced", "announcement",
    "says", "said", "saying",
    "expands", "expand", "expanded", "expansion",
    "introduces", "introduce", "introduced",
    "enables", "enable", "enabled",
    "offers", "offer", "offered",
    "releases", "release", "released",
    "reveals", "reveal", "revealed",
    "among", "across", "where", "when", "how", "why", "after", "before",
    "into", "onto", "upon", "out", "off", "over", "under",
    "make", "makes", "made", "complete", "completes",
))
# Domain-specific "anchor tokens" — proper-noun-ish terms that strongly identify
# what a story is about. Two headlines sharing ≥1 anchor + ≥2 other tokens are
# treated as the same story even if phrased very differently.
# We match via substring on normalized tokens so "alipay" catches "Alipay", etc.
ANCHOR_TOKENS = frozenset((
    # Payments / finance
    "alipay", "ant", "wechat", "weixin", "tenpay", "tencent",
    "visa", "mastercard", "paypal", "jcb", "amex", "americanexpress",
    "stripe", "adyen", "cfpb", "genius",
    # AI labs / products
    "anthropic", "claude", "openai", "gpt", "sora", "chatgpt",
    "deepmind", "gemini", "google", "meta", "llama", "mistral",
    "cohere", "xai", "grok", "nvidia", "huggingface", "perplexity",
    # Security
    "microsoft", "windows", "apple", "ios", "macos", "android",
    "cisco", "fortinet", "ivanti", "palo", "zscaler", "crowdstrike",
    "cve", "0day", "ransomware", "apt",
))
# Crude plural stem: strip trailing 's' on tokens len>=4 so "agent"/"agents",
# "country"/"countries" normalize to the same form.
def _stem(tok: str) -> str:
    if len(tok) >= 5 and tok.endswith("ies"):
        return tok[:-3] + "y"
    if len(tok) >= 4 and tok.endswith("s") and not tok.endswith("ss"):
        return tok[:-1]
    return tok

# Normalize small digit tokens to word form so "5 countries" and "five countries"
# cluster. Only 0-10 — larger numbers are usually identifying (years, dollar amounts).
DIGIT_WORD = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
    "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten",
}

# Clustering thresholds. Same anchor is a strong signal, so we allow a more
# permissive Jaccard. Require at least one shared content token of length >=5
# to avoid merging on short generic words like "code"/"user".
CLUSTER_SHARED_MIN = 2
CLUSTER_JACCARD_ANCHOR = 0.22   # when both sides share an anchor token
CLUSTER_JACCARD_NOANCHOR = 0.4  # when neither side has an anchor
CLUSTER_LONG_TOKEN_MIN = 5      # at least one shared token must be this long

# For Reddit URLs: require at least one hard security indicator to keep.
# Forum subs are high-volume but mostly chatter; the few real posts always
# carry one of these markers.
REDDIT_KEEP_MARKERS = (
    "CVE-", "CVE–", "CVE—",
    "0day", "0-day", "zero-day", "zero day",
    "RCE", "LPE", "LFI", "SSRF", "XXE", "XSS", "SQLi",
    "exploit", "Exploit", "EXPLOIT",
    "vulnerab", "Vulnerab",
    "disclosure", "Disclosure",
    "writeup", "Writeup", "WriteUp",
    "malware", "Malware",
    "phishing", "Phishing",
    "ransomware", "Ransomware",
    "APT",
    "backdoor", "Backdoor",
    "botnet", "Botnet",
    "privilege escalation", "Privilege Escalation",
    "bypass", "Bypass",
)


@dataclass
class FilteredEntry:
    title: str
    url: str
    summary: str
    category: str
    published: str
    fetch_status: str  # "full" | "rss_only" | "title_only" | "blocked"
    cve_ids: list[str]
    related_urls: list[str]
    quality_score: int


def _is_waf_polluted(text: str) -> bool:
    if not text:
        return False
    return any(marker in text for marker in WAF_MARKERS)


def _matches_title_blacklist(title: str) -> bool:
    if not title:
        return True
    if any(bad in title for bad in TITLE_BLACKLIST_SUBSTR):
        return True
    return any(r.search(title) for r in TITLE_REGEX_BLACKLIST)


def _matches_source_blacklist(url: str) -> bool:
    return any(bad in url for bad in SOURCE_BLACKLIST_SUBSTR)


def _reddit_lacks_security_marker(url: str, title: str, summary: str) -> bool:
    """Reddit-only gate: without a hard security marker, treat as forum chatter."""
    if "reddit.com" not in url:
        return False
    text = f"{title}\n{summary}"
    return not any(m in text for m in REDDIT_KEEP_MARKERS)


def _extract_cves(title: str, summary: str) -> list[str]:
    text = f"{title}\n{summary}"
    # Normalize fancy dashes to ASCII hyphen for consistent IDs.
    return sorted({
        m.upper().replace("–", "-").replace("—", "-")
        for m in CVE_RE.findall(text)
    })


def _title_tokens(title: str) -> tuple[frozenset[str], frozenset[str]]:
    """Return (anchor_tokens, content_tokens) extracted from a title.

    anchor_tokens: brand/product identifiers (Alipay, WeChat, Visa, Claude, ...).
    content_tokens: other non-stopword tokens of length >=4, plural-stemmed,
                    used to measure topical overlap via Jaccard.
    CJK chars are kept intact but contribute to content_tokens as the whole
    contiguous run.
    """
    if not title:
        return frozenset(), frozenset()
    stripped = TITLE_SUFFIX_SEP_RE.sub("", title).strip().lower()
    raw = [t for t in TITLE_NORMALIZE_RE.split(stripped) if t]
    anchors: set[str] = set()
    content: set[str] = set()
    for tok in raw:
        if tok in ANCHOR_TOKENS:
            anchors.add(tok)
            continue
        # Check substring anchor (e.g. "americanexpress" embedded)
        if any(a in tok for a in ANCHOR_TOKENS if len(a) >= 5):
            anchors.add(next(a for a in ANCHOR_TOKENS if len(a) >= 5 and a in tok))
        if tok in TITLE_STOPWORDS:
            continue
        # CJK: keep as-is, length >= 2 is meaningful
        if any("\u3400" <= c <= "\u9fff" for c in tok):
            if len(tok) >= 2:
                content.add(tok)
            continue
        if tok.isdigit():
            content.add(DIGIT_WORD.get(tok, tok))
            continue
        if len(tok) < 4:
            continue
        content.add(_stem(tok))
    return frozenset(anchors), frozenset(content)


def _same_story(
    a_anchors: frozenset[str], a_content: frozenset[str],
    b_anchors: frozenset[str], b_content: frozenset[str],
) -> bool:
    """Two titles describe the same story iff:
      - Anchor constraint: both have ≥1 common anchor, OR neither has an anchor.
        (Asymmetric anchors mean different subjects.)
      - Content: share ≥CLUSTER_SHARED_MIN tokens, at least one of length ≥
        CLUSTER_LONG_TOKEN_MIN (rules out matches on only generic shorts).
      - Jaccard ≥ threshold (permissive when anchors match, strict otherwise).
    """
    has_anchor_match = bool(a_anchors and b_anchors and (a_anchors & b_anchors))
    if (a_anchors and b_anchors) and not has_anchor_match:
        return False
    if a_anchors != b_anchors and not (a_anchors and b_anchors):
        # One side has an anchor, the other doesn't — different subjects.
        return False
    shared = a_content & b_content
    if len(shared) < CLUSTER_SHARED_MIN:
        return False
    if not any(len(t) >= CLUSTER_LONG_TOKEN_MIN for t in shared):
        return False
    union = a_content | b_content
    if not union:
        return False
    threshold = CLUSTER_JACCARD_ANCHOR if has_anchor_match else CLUSTER_JACCARD_NOANCHOR
    return len(shared) / len(union) >= threshold


def _dedup_key_static(title: str, cves: list[str]) -> str | None:
    """Strong static dedup keys (CVE / Patch Tuesday). Returns None otherwise,
    in which case cluster-based dedup handles the entry.
    """
    if cves:
        return "cve:" + "|".join(cves)
    if PATCH_TUESDAY_RE.search(title):
        return "PATCH_TUESDAY"
    return None


class _UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def _score(entry: FeedEntry, cves: list[str], status: str) -> int:
    score = 0
    title = entry.title or ""
    summary = entry.summary or ""

    if cves:
        score += 2
    if any(kw in title for kw in ("在野利用", "0day", "零日", "PoC", "EXP", "Exploited in the Wild")):
        score += 2
    if any(kw in title for kw in ("APT", "供应链", "勒索", "Ransomware", "Supply chain")):
        score += 2
    if any(kw in title for kw in ("AI", "LLM", "MCP", "Agent", "Prompt")):
        score += 1
    if "Daily Threat Briefing" in title or "Daily Briefing" in title:
        score += 1
    if len(summary) >= 200:
        score += 1
    if status == "title_only":
        score -= 1
    if status == "blocked":
        score -= 5
    return score


def filter_and_dedup(entries: Iterable[FeedEntry]) -> tuple[list[FilteredEntry], dict[str, int]]:
    """Apply blacklist, WAF detection, CVE dedup.

    Returns:
        (kept entries, stats dict).
    """
    stats: dict[str, int] = defaultdict(int)
    stats["input"] = 0

    staged: list[FilteredEntry] = []

    for e in entries:
        stats["input"] += 1
        title = (e.title or "").strip()
        summary = (e.summary or "").strip()

        if _matches_source_blacklist(e.url):
            stats["dropped_source_blacklist"] += 1
            continue

        if _matches_title_blacklist(title):
            stats["dropped_title_blacklist"] += 1
            continue

        if _reddit_lacks_security_marker(e.url, title, summary):
            stats["dropped_reddit_chatter"] += 1
            continue

        # WAF pollution: don't drop the entry, but blank the summary so
        # downstream consumers don't feed Claude garbage.
        if _is_waf_polluted(summary):
            stats["waf_scrubbed"] += 1
            summary = ""

        if len(summary) >= MIN_SUMMARY_LEN:
            status = "full" if len(summary) >= 200 else "rss_only"
        elif title:
            status = "title_only"
        else:
            stats["dropped_empty"] += 1
            continue

        cves = _extract_cves(title, summary)
        score = _score(e, cves, status)

        staged.append(
            FilteredEntry(
                title=title,
                url=e.url,
                summary=summary,
                category=e.category,
                published=e.published.isoformat(),
                fetch_status=status,
                cve_ids=cves,
                related_urls=[],
                quality_score=score,
            )
        )

    # --- Semantic dedup ---------------------------------------------------
    # Pass 1: strong static keys (CVE IDs, Patch Tuesday bucket).
    # Pass 2: cluster remaining entries by (anchor token, content Jaccard)
    #         so cross-publisher paraphrases of the same story collapse.
    n = len(staged)
    uf = _UnionFind(n)
    static_group: dict[str, int] = {}  # static_key -> representative idx
    tokens: list[tuple[frozenset[str], frozenset[str]]] = [
        _title_tokens(fe.title) for fe in staged
    ]

    for i, fe in enumerate(staged):
        key = _dedup_key_static(fe.title, fe.cve_ids)
        if key is not None:
            if key in static_group:
                uf.union(static_group[key], i)
            else:
                static_group[key] = i

    # Pass 2: pairwise cluster via anchor+Jaccard. O(N^2) acceptable at ~100.
    for i in range(n):
        a_anchors, a_content = tokens[i]
        if not a_content:
            continue
        for j in range(i + 1, n):
            if uf.find(i) == uf.find(j):
                continue
            b_anchors, b_content = tokens[j]
            if not b_content:
                continue
            if _same_story(a_anchors, a_content, b_anchors, b_content):
                uf.union(i, j)

    clusters: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        clusters[uf.find(i)].append(i)

    kept_indices: set[int] = set()
    for root, idxs in clusters.items():
        if len(idxs) == 1:
            kept_indices.add(idxs[0])
            continue
        # Pick the one with longest summary; ties broken by quality_score.
        best = max(idxs, key=lambda i: (len(staged[i].summary), staged[i].quality_score))
        kept_indices.add(best)
        related = [staged[i].url for i in idxs if i != best]
        staged[best].related_urls = related
        stats["dedup_merged"] += len(related)

    kept = [staged[i] for i in sorted(kept_indices)]
    kept.sort(key=lambda fe: (fe.quality_score, fe.published), reverse=True)

    stats["output"] = len(kept)
    return kept, dict(stats)

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
# English stopwords dropped so "OpenAI launches GPT-5.4" and "OpenAI Launches GPT5.4 — live now"
# collapse to the same key.
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
))
TITLE_DEDUP_PREFIX_LEN = 50

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


def _normalize_title_for_dedup(title: str) -> str:
    """Lowercase, strip ' - SourceName' suffix, drop stopwords, keep CJK intact."""
    if not title:
        return ""
    # Google News / Yahoo style: "Real Headline - Publisher". Drop the tail.
    stripped = TITLE_SUFFIX_SEP_RE.sub("", title).strip()
    tokens = TITLE_NORMALIZE_RE.split(stripped.lower())
    kept = [t for t in tokens if t and t not in TITLE_STOPWORDS]
    return "".join(kept)[:TITLE_DEDUP_PREFIX_LEN]


def _dedup_key(title: str, cves: list[str]) -> str | None:
    """Return a semantic dedup key, or None if entry has no obvious group.

    Priority:
      1. CVE IDs — strongest signal (same vuln reported by multiple sources).
      2. Patch Tuesday — constant bucket.
      3. Normalized title prefix — catches cross-source duplicates for non-CVE
         news (especially AI / finance where the same event is reported by
         multiple outlets on the same day).
    """
    if cves:
        return "cve:" + "|".join(cves)
    if PATCH_TUESDAY_RE.search(title):
        return "PATCH_TUESDAY"
    norm = _normalize_title_for_dedup(title)
    if len(norm) >= 12:  # avoid clustering on tiny fragments
        return "t:" + norm
    return None


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

    # Semantic dedup: group by CVE-id set (or Patch-Tuesday bucket).
    # Keep the richest entry per group; fold the rest into related_urls.
    groups: dict[str, list[int]] = defaultdict(list)
    singletons: list[int] = []
    for i, fe in enumerate(staged):
        key = _dedup_key(fe.title, fe.cve_ids)
        if key is None:
            singletons.append(i)
        else:
            groups[key].append(i)

    kept_indices: set[int] = set(singletons)
    for key, idxs in groups.items():
        # Pick the one with longest summary; ties broken by quality_score.
        best = max(idxs, key=lambda i: (len(staged[i].summary), staged[i].quality_score))
        kept_indices.add(best)
        related = [staged[i].url for i in idxs if i != best]
        if related:
            staged[best].related_urls = related
            stats["dedup_merged"] += len(related)

    kept = [staged[i] for i in sorted(kept_indices)]
    kept.sort(key=lambda fe: (fe.quality_score, fe.published), reverse=True)

    stats["output"] = len(kept)
    return kept, dict(stats)

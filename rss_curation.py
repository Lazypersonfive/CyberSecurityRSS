from collections import Counter
from typing import Any, Iterable
from urllib.parse import urlparse


def normalize_source(url: str) -> str:
    try:
        return urlparse(url).netloc.removeprefix("www.")
    except Exception:
        return ""


def curate_entries(entries: Iterable[Any], board_cfg: dict[str, Any]) -> tuple[list[Any], dict[str, int]]:
    stats = Counter()
    curated = list(entries)

    source_blacklist = [s.lower() for s in board_cfg.get("source_blacklist", [])]
    title_blacklist = [s.lower() for s in board_cfg.get("title_blacklist", [])]
    if source_blacklist or title_blacklist:
        kept = []
        for entry in curated:
            source = normalize_source(getattr(entry, "url", ""))
            title = (getattr(entry, "title", "") or "").lower()
            if any(bad in source for bad in source_blacklist):
                stats["dropped_source_blacklist"] += 1
                continue
            if any(bad in title for bad in title_blacklist):
                stats["dropped_title_blacklist"] += 1
                continue
            kept.append(entry)
        curated = kept

    source_caps = {
        key.removeprefix("www.").lower(): int(value)
        for key, value in (board_cfg.get("source_caps") or {}).items()
    }
    if source_caps:
        kept = []
        source_counts: Counter[str] = Counter()
        for entry in curated:
            source = normalize_source(getattr(entry, "url", "")).lower()
            cap = source_caps.get(source)
            if cap is not None and source_counts[source] >= cap:
                stats["dropped_source_cap"] += 1
                continue
            kept.append(entry)
            source_counts[source] += 1
        curated = kept

    max_entries = int(board_cfg.get("max_entries", 0) or 0)
    if max_entries > 0 and len(curated) > max_entries:
        stats["dropped_max_entries"] += len(curated) - max_entries
        curated = curated[:max_entries]

    return curated, dict(stats)

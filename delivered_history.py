"""Track stories already published without discarding unselected feed entries."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable

from story_clustering import story_id_for_entry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeliveredHistory:
    urls: set[str]
    story_ids: set[str]


def load_delivered_history(
    board: str,
    as_of: date,
    *,
    lookback_days: int = 7,
    digest_dir: Path,
) -> DeliveredHistory:
    """Load URLs and story IDs from prior published digests for one board."""
    urls: set[str] = set()
    story_ids: set[str] = set()
    for offset in range(1, max(0, lookback_days) + 1):
        day = as_of - timedelta(days=offset)
        path = digest_dir / f"{board}_{day.isoformat()}.json"
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("delivered history %s unreadable: %s", path.name, exc)
            continue
        for item in data.get("items") or []:
            url = str(item.get("url") or "")
            if url:
                urls.add(url)
            urls.update(str(value) for value in item.get("related_urls") or [] if value)
            story_id = str(item.get("story_id") or "")
            if story_id:
                story_ids.add(story_id)
                story_ids.update(_individual_cve_story_ids(story_id))
            for cve in item.get("cve_ids") or []:
                story_ids.add(f"cve:{str(cve).lower()}")
    return DeliveredHistory(urls=urls, story_ids=story_ids)


def filter_delivered_candidates(
    candidates: Iterable[dict[str, Any]],
    history: DeliveredHistory,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Drop prior published URLs/events while leaving unseen candidates eligible."""
    kept: list[dict[str, Any]] = []
    stats = {"url": 0, "story": 0, "total": 0}
    for entry in candidates:
        url = str(entry.get("url") or "")
        if url and url in history.urls:
            stats["url"] += 1
            stats["total"] += 1
            continue
        story_id = str(entry.get("story_id") or story_id_for_entry(entry))
        story_keys = {story_id, *_individual_cve_story_ids(story_id)}
        if story_keys & history.story_ids:
            stats["story"] += 1
            stats["total"] += 1
            continue
        kept.append(entry)
    return kept, stats


def _individual_cve_story_ids(story_id: str) -> set[str]:
    if not story_id.startswith("cve:"):
        return set()
    return {f"cve:{value.strip()}" for value in story_id.removeprefix("cve:").split(",") if value.strip()}

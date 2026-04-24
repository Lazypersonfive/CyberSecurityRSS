"""Parse an OPML file into a category -> feed URL mapping.

Supports either a local path or an HTTP(S) URL. For local files under
``feeds/`` no network access is required.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

import httpx

LEGACY_OPML_URL = "https://raw.githubusercontent.com/zer0yu/CyberSecurityRSS/master/tiny.opml"
LEGACY_OPML_CACHE = Path(__file__).parent / ".cache" / "tiny.opml"


def fetch_opml(source: str | Path | None = None, use_cache: bool = True) -> dict[str, list[str]]:
    """Load and parse an OPML document.

    Args:
        source: Local path (preferred) or http(s) URL. When ``None`` falls
            back to the legacy zer0yu/CyberSecurityRSS tiny.opml cache (for
            backward compat with older scripts).
        use_cache: Only relevant for the legacy URL path; ignored for local
            files.

    Returns:
        Mapping of category label -> list of feed XML URLs.
    """
    return _parse_opml(_load_raw(source, use_cache))


def fetch_opml_metadata(
    source: str | Path | None = None, use_cache: bool = True
) -> dict[str, dict[str, str]]:
    """Load OPML feed metadata keyed by feed URL.

    ``fetch_opml`` intentionally keeps its historical category -> URL-list
    shape. This helper preserves feed-level labels for source-quality reports.
    """
    return _parse_opml_metadata(_load_raw(source, use_cache))


def _load_raw(source: str | Path | None, use_cache: bool) -> str:
    if source is None:
        return _load_legacy(use_cache)

    if isinstance(source, (str, Path)) and _looks_like_url(str(source)):
        return _fetch_remote(str(source))
    return Path(source).read_text(encoding="utf-8")


def _looks_like_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def _fetch_remote(url: str) -> str:
    response = httpx.get(url, timeout=30, follow_redirects=True)
    response.raise_for_status()
    return response.text


def _load_legacy(use_cache: bool) -> str:
    if use_cache and LEGACY_OPML_CACHE.exists():
        return LEGACY_OPML_CACHE.read_text(encoding="utf-8")
    raw = _fetch_remote(LEGACY_OPML_URL)
    LEGACY_OPML_CACHE.parent.mkdir(parents=True, exist_ok=True)
    LEGACY_OPML_CACHE.write_text(raw, encoding="utf-8")
    return raw


def _parse_opml(raw: str) -> dict[str, list[str]]:
    root = ET.fromstring(raw)
    body = root.find("body")
    if body is None:
        raise ValueError("OPML missing <body>")

    feeds: dict[str, list[str]] = {}
    for category_node in body:
        category = category_node.get("text", "Uncategorized")
        urls: list[str] = []
        for outline in category_node:
            xml_url = outline.get("xmlUrl")
            if xml_url:
                urls.append(xml_url)
        # Allow category nodes that carry xmlUrl directly (flat OPMLs).
        if not urls and category_node.get("xmlUrl"):
            urls.append(category_node.get("xmlUrl"))
        if urls:
            feeds[category] = feeds.get(category, []) + urls

    return feeds


def _parse_opml_metadata(raw: str) -> dict[str, dict[str, str]]:
    root = ET.fromstring(raw)
    body = root.find("body")
    if body is None:
        raise ValueError("OPML missing <body>")

    metadata: dict[str, dict[str, str]] = {}
    for category_node in body:
        category = category_node.get("text", "Uncategorized")
        outlines = list(category_node)
        if not outlines and category_node.get("xmlUrl"):
            outlines = [category_node]
        for outline in outlines:
            xml_url = outline.get("xmlUrl")
            if not xml_url:
                continue
            title = outline.get("title") or outline.get("text") or xml_url
            metadata[xml_url] = {"feed_title": title, "category": category}
    return metadata

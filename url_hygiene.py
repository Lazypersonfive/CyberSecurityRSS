"""Guards against non-routable item URLs leaking into public digests.

Some upstream feeds ship misconfigured RSS generators whose <link> elements
point at the generator's bind address (e.g. hackernews.cc emits
``http://0.0.0.0:8080/post/<id>``). Two-layer defence:

- ``repair_entry_url`` recovers the real article URL by grafting the item's
  path onto the feed's public host — generic, so the next misconfigured feed
  is fixed too, not just the one we found.
- ``is_public_http_url`` is the final filter gate; anything still pointing at
  a non-routable host is dropped before it can reach output/digest/site.
"""

from __future__ import annotations

import ipaddress
from urllib.parse import urlparse, urlunparse

_LOCAL_HOSTNAMES = {"localhost", "localhost.localdomain", "ip6-localhost"}


def _host_is_public(hostname: str | None) -> bool:
    if not hostname:
        return False
    host = hostname.strip().lower().rstrip(".")
    if not host or host in _LOCAL_HOSTNAMES or host.endswith(".localhost") or host.endswith(".local"):
        return False
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        return True  # regular DNS name
    return addr.is_global and not addr.is_multicast


def is_public_http_url(url: str) -> bool:
    """True only for http(s) URLs whose host is publicly routable."""
    if not url:
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    try:
        hostname = parsed.hostname
    except ValueError:
        return False
    return _host_is_public(hostname)


def repair_entry_url(link: str, feed_url: str) -> str:
    """Rewrite a non-routable item link onto the feed's public host.

    ``http://0.0.0.0:8080/post/64413`` from ``http://hackernews.cc/feed``
    becomes ``https://hackernews.cc/post/64413`` (path + query preserved,
    scheme forced to https). Returns the link unchanged when it is already
    public or when the feed host is itself non-routable.
    """
    if not link or is_public_http_url(link):
        return link
    try:
        feed_host = urlparse(feed_url).hostname
    except ValueError:
        return link
    if not _host_is_public(feed_host):
        return link
    try:
        parsed = urlparse(link)
    except ValueError:
        return link
    if parsed.scheme not in ("http", "https"):
        return link
    return urlunparse(("https", feed_host, parsed.path or "/", parsed.params, parsed.query, ""))

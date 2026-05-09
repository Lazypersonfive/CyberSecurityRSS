"""Legacy Discord digest generator placeholder.

The maintained digest route is ``fetch_and_save.py`` plus
``digest_pipeline_gemini.py`` and ``site_builder.py``. This module is kept only
for import compatibility with older local scripts.
"""

from __future__ import annotations

from datetime import date
from typing import Any


def generate_digest(_entries: list[Any], _today: date | None = None) -> str:
    raise RuntimeError(
        "Legacy Discord digest generation has been removed; use digest_pipeline_gemini.py."
    )

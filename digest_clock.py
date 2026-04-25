"""Shared date helpers for daily digest generation."""

import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

DIGEST_TIMEZONE = ZoneInfo("Asia/Shanghai")
DIGEST_DATE_ENV = "DIGEST_DATE"


def digest_today() -> date:
    override = os.environ.get(DIGEST_DATE_ENV)
    if override:
        return date.fromisoformat(override)
    return datetime.now(DIGEST_TIMEZONE).date()

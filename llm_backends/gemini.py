"""Gemini implementation of the digest LLM backend."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

try:
    from google import genai
    from google.genai import errors as genai_errors
    from google.genai import types
except ImportError as exc:  # allow importing pure helpers in lean test environments
    genai = None
    genai_errors = None
    types = None
    GOOGLE_GENAI_IMPORT_ERROR: ImportError | None = exc
else:
    GOOGLE_GENAI_IMPORT_ERROR = None

DEFAULT_GEMINI_MODEL = "gemini-3-flash-preview"
MAX_RETRIES = 3
RETRY_BACKOFF_SEC = 4


@dataclass(frozen=True)
class GeminiBackend:
    """Gemini backend used by current production runs."""

    client: object
    score_model: str = DEFAULT_GEMINI_MODEL
    summarize_model: str = DEFAULT_GEMINI_MODEL
    name: str = "gemini"

    @classmethod
    def from_env(cls) -> "GeminiBackend":
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise SystemExit("GEMINI_API_KEY (or GOOGLE_API_KEY) env var is required")
        if genai is None:
            raise SystemExit(f"google-genai is required to run Gemini backend: {GOOGLE_GENAI_IMPORT_ERROR}")
        model = os.environ.get("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL
        return cls(client=genai.Client(api_key=api_key), score_model=model, summarize_model=model)

    def generate_json(
        self,
        model: str,
        system: str,
        user_prompt: str,
        max_output_tokens: int,
    ) -> str:
        cfg = types.GenerateContentConfig(
            system_instruction=system,
            temperature=0.2,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )
        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                resp = self.client.models.generate_content(
                    model=model,
                    contents=user_prompt,
                    config=cfg,
                )
                text = resp.text or ""
                if not text.strip():
                    raise RuntimeError("empty response text")
                return text
            except (genai_errors.APIError, RuntimeError) as exc:
                last_exc = exc
                wait = RETRY_BACKOFF_SEC * (attempt + 1)
                import logging

                logging.getLogger(__name__).warning(
                    "gemini call failed (attempt %d/%d): %s — retry in %ds",
                    attempt + 1,
                    MAX_RETRIES,
                    exc,
                    wait,
                )
                time.sleep(wait)
        raise RuntimeError(f"gemini call exhausted retries: {last_exc}")

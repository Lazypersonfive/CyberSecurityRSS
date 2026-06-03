"""Gemini implementation of the digest LLM backend."""

from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
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

DEFAULT_GEMINI_MODEL = "gemini-3.5-flash"
MAX_RETRIES = 3
RETRY_BACKOFF_SEC = 4
DEFAULT_REQUEST_TIMEOUT_SEC = 90


@dataclass(frozen=True)
class GeminiBackend:
    """Gemini backend used by current production runs."""

    client: object
    score_model: str = DEFAULT_GEMINI_MODEL
    summarize_model: str = DEFAULT_GEMINI_MODEL
    name: str = "gemini"
    request_timeout_sec: int = DEFAULT_REQUEST_TIMEOUT_SEC

    @classmethod
    def from_env(cls) -> "GeminiBackend":
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise SystemExit("GEMINI_API_KEY (or GOOGLE_API_KEY) env var is required")
        if genai is None:
            raise SystemExit(f"google-genai is required to run Gemini backend: {GOOGLE_GENAI_IMPORT_ERROR}")
        model = os.environ.get("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL
        request_timeout_sec = int(
            os.environ.get("GEMINI_REQUEST_TIMEOUT_SEC") or DEFAULT_REQUEST_TIMEOUT_SEC
        )
        return cls(
            client=genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(timeout=request_timeout_sec * 1000),
            ),
            score_model=model,
            summarize_model=model,
            request_timeout_sec=request_timeout_sec,
        )

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
                resp = self._generate_content_with_timeout(model, user_prompt, cfg)
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

    def _generate_content_with_timeout(self, model: str, user_prompt: str, cfg: object) -> object:
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(
            self.client.models.generate_content,
            model=model,
            contents=user_prompt,
            config=cfg,
        )
        try:
            return future.result(timeout=self.request_timeout_sec)
        except FutureTimeoutError as exc:
            future.cancel()
            raise RuntimeError(
                f"gemini request timed out after {self.request_timeout_sec}s"
            ) from exc
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

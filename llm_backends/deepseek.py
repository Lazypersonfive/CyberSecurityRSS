"""DeepSeek implementation reserved as the next replaceable digest backend."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

import httpx

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-flash"
DEPRECATED_MODELS = {"deepseek-chat", "deepseek-reasoner"}
MAX_RETRIES = 3
RETRY_BACKOFF_SEC = 2


@dataclass(frozen=True)
class DeepSeekBackend:
    """OpenAI-compatible DeepSeek backend.

    This is production-shaped but opt-in only: current production remains Gemini
    unless LLM_BACKEND=deepseek is set explicitly.
    """

    api_key: str
    base_url: str = DEFAULT_BASE_URL
    score_model: str = DEFAULT_MODEL
    summarize_model: str = DEFAULT_MODEL
    name: str = "deepseek"

    @classmethod
    def from_env(cls) -> "DeepSeekBackend":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise SystemExit("DEEPSEEK_API_KEY env var is required when LLM_BACKEND=deepseek")
        model = os.environ.get("DEEPSEEK_MODEL") or DEFAULT_MODEL
        if model in DEPRECATED_MODELS:
            raise SystemExit(
                f"DEEPSEEK_MODEL={model} is deprecated; use deepseek-v4-flash or deepseek-v4-pro"
            )
        base_url = (os.environ.get("DEEPSEEK_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        return cls(api_key=api_key, base_url=base_url, score_model=model, summarize_model=model)

    def generate_json(
        self,
        model: str,
        system: str,
        user_prompt: str,
        max_output_tokens: int,
    ) -> str:
        payload = {
            "model": model or self.score_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": max_output_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                with httpx.Client(timeout=90) as client:
                    resp = client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                content = data["choices"][0]["message"].get("content") or ""
                if not content.strip():
                    raise RuntimeError("empty response content")
                return content
            except (httpx.HTTPError, KeyError, IndexError, RuntimeError) as exc:
                last_exc = exc
                if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
                    raise RuntimeError(f"deepseek call failed: {exc}") from exc
                if attempt == MAX_RETRIES - 1:
                    break
                time.sleep(RETRY_BACKOFF_SEC * (attempt + 1))
        raise RuntimeError(f"deepseek call exhausted retries: {last_exc}")

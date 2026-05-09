"""Common interface for digest LLM backends."""

from __future__ import annotations

import os
from typing import Protocol


class LLMBackend(Protocol):
    """Minimal JSON-generation contract used by the digest pipeline."""

    name: str
    score_model: str
    summarize_model: str

    def generate_json(
        self,
        model: str,
        system: str,
        user_prompt: str,
        max_output_tokens: int,
    ) -> str:
        """Return a JSON string from the configured backend."""


def backend_name_from_env() -> str:
    return (os.environ.get("LLM_BACKEND") or "gemini").strip().lower()


def get_backend() -> LLMBackend:
    """Load the configured backend lazily so optional SDK imports stay isolated."""
    name = backend_name_from_env()
    if name == "gemini":
        from llm_backends.gemini import GeminiBackend

        return GeminiBackend.from_env()
    if name == "deepseek":
        from llm_backends.deepseek import DeepSeekBackend

        return DeepSeekBackend.from_env()
    raise SystemExit("Unsupported LLM_BACKEND=%s; expected 'gemini' or 'deepseek'" % name)

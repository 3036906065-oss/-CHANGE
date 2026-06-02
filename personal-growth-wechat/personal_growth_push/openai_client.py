from __future__ import annotations

import json
import logging
import re
from typing import Any, Callable

from .config import Settings

logger = logging.getLogger(__name__)


class AIClient:
    """Small wrapper around the OpenAI Responses API with deterministic fallback."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._client = None
        if settings.openai_enabled:
            from openai import OpenAI

            self._client = OpenAI(
                api_key=settings.openai_api_key,
                timeout=settings.openai_timeout_seconds,
            )

    @property
    def enabled(self) -> bool:
        return self._client is not None

    def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        fallback: Callable[[], dict[str, Any]],
    ) -> dict[str, Any]:
        if not self.enabled:
            return fallback()

        try:
            response = self._client.responses.create(
                model=self.settings.openai_model,
                instructions=system_prompt,
                input=user_prompt,
            )
            text = getattr(response, "output_text", "") or ""
            return _loads_json(text)
        except Exception:
            logger.exception("OpenAI generation failed; using fallback content.")
            return fallback()


def _loads_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", cleaned, flags=re.DOTALL)
    if fence:
        cleaned = fence.group(1).strip()
    return json.loads(cleaned)

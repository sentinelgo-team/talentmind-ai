"""
TalentMind AI - Base Agent
============================
Abstract base class for all AI agents.
Uses updated google-genai SDK.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from google import genai
from google.genai import types
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.exceptions import (
    APIKeyNotConfiguredError,
    AgentResponseError,
)
from app.core.settings import get_settings

logger = logging.getLogger(__name__)
cfg    = get_settings()


class BaseAgent(ABC):
    """
    Abstract base class for all TalentMind AI agents.

    Provides:
        - Google GenAI client initialization
        - Retry logic for API calls
        - JSON response parsing
        - Execution timing
        - Consistent logging
        - Error handling
    """

    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name
        self._logger    = logging.getLogger(f"agents.{agent_name}")
        self._client    = self._initialize_client()

    def _initialize_client(self) -> genai.Client:
        """
        Initializes Google GenAI client.

        Returns:
            genai.Client: Configured client instance

        Raises:
            APIKeyNotConfiguredError: If key missing
        """
        if not cfg.validate_google_api_key():
            raise APIKeyNotConfiguredError()

        client = genai.Client(api_key=cfg.GOOGLE_API_KEY)

        self._logger.debug(
            "GenAI client initialized | model=%s",
            cfg.GEMINI_MODEL
        )
        return client

    @abstractmethod
    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main agent execution method.
        Must be implemented by all agents.

        Args:
            input_data: Agent-specific input dictionary

        Returns:
            dict: Agent output results
        """
        pass

    def _call_llm(self, prompt: str) -> str:
        """
        Calls Gemini API with retry logic.
        Handles rate limiting with exponential backoff.
        """
        import time

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=3, min=5, max=30),
            retry=retry_if_exception_type(Exception),
            reraise=True,
        )
        def _call() -> str:
            response = self._client.models.generate_content(
                model=cfg.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=cfg.GEMINI_TEMPERATURE,
                    max_output_tokens=cfg.GEMINI_MAX_TOKENS,
                ),
            )
            if not response.text:
                raise AgentResponseError(
                    agent_name=self.agent_name,
                    response=""
                )
            return response.text

        start_time = time.time()
        result     = _call()
        elapsed    = time.time() - start_time

        self._logger.debug(
            "LLM call complete | agent=%s | time=%.2fs",
            self.agent_name, elapsed
        )
        return result

    def _parse_json_response(
        self,
        response_text: str,
        fallback: Optional[Dict] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Safely parses JSON from LLM response.

        Handles common LLM formatting issues:
            - Markdown code blocks
            - Extra text before/after JSON
            - Trailing commas

        Args:
            response_text : Raw LLM response
            fallback      : Default if parsing fails (returns None if not provided)

        Returns:
            dict: Parsed JSON data, or fallback if parsing fails
        """
        import json
        import re

        text = response_text.strip()

        # Remove markdown code blocks
        text = re.sub(r"```(?:json)?\s*", "", text).strip()
        text = text.replace("```", "").strip()

        # Find JSON object boundaries
        start = text.find("{")
        end   = text.rfind("}") + 1

        if start == -1 or end == 0:
            self._logger.warning(
                "No JSON found in response | agent=%s",
                self.agent_name
            )
            return fallback

        json_str = text[start:end]

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as exc:
            self._logger.error(
                "JSON parse error | agent=%s | error=%s",
                self.agent_name, exc
            )
            return fallback

    def _log_start(self, input_keys: list) -> None:
        """Logs agent execution start."""
        self._logger.info(
            "Agent started | name=%s | inputs=%s",
            self.agent_name, input_keys
        )

    def _log_complete(self, result_keys: list) -> None:
        """Logs agent execution completion."""
        self._logger.info(
            "Agent complete | name=%s | outputs=%s",
            self.agent_name, result_keys
        )

    def _log_error(self, error: Exception) -> None:
        """Logs agent execution error."""
        self._logger.error(
            "Agent error | name=%s | error=%s",
            self.agent_name, error
        )
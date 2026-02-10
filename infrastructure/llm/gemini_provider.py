"""
Gemini LLM Provider implementation.

Implements the LLMProvider protocol for Google's Gemini models.
"""

from typing import Optional, Any

from google import genai
from google.genai import types

from infrastructure.llm.base import BaseLLMProvider


class GeminiLLMProvider(BaseLLMProvider):
    """LLM Provider implementation for Google Gemini."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-3.0-flash-preview",
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 4096,
    ):
        """
        Initialize Gemini provider.

        Args:
            api_key: Google API key
            model_name: Gemini model to use
            max_retries: Maximum retry attempts
            initial_delay: Initial delay for retry
            max_output_tokens: Maximum output tokens
        """
        super().__init__(
            model_name=model_name,
            max_retries=max_retries,
            initial_delay=initial_delay,
            max_output_tokens=max_output_tokens,
        )
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "Gemini"

    def _init_client(self) -> Any:
        """Initialize the Gemini client."""
        return genai.Client(api_key=self._api_key)

    def _call_api(
        self,
        messages: list[dict],
        system_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Make the actual Gemini API call.

        Args:
            messages: List of conversation messages
            system_prompt: System prompt to use
            temperature: Sampling temperature

        Returns:
            Text response from Gemini
        """
        client = self._get_client()

        # Convert messages to Gemini Content format
        contents = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            # Gemini uses "user" and "model" roles
            if role == "assistant":
                role = "model"
            parts = [types.Part.from_text(text=content)]
            contents.append(types.Content(role=role, parts=parts))

        response = client.models.generate_content(
            model=self._model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=self._max_output_tokens,
                system_instruction=system_prompt,
            )
        )

        # Check for empty response
        if not response.text:
            finish_reason = "unknown"
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    finish_reason = candidate.finish_reason
            raise Exception(f"Gemini n'a pas généré de réponse (finish_reason={finish_reason}).")

        return response.text

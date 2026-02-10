"""
Kimi (Moonshot AI) LLM Provider implementation.

Implements the LLMProvider protocol for Kimi K2.5 via OpenAI-compatible API.
"""

from typing import Optional, Any

from infrastructure.llm.base import BaseLLMProvider


class KimiLLMProvider(BaseLLMProvider):
    """LLM Provider implementation for Kimi K2.5 (Moonshot AI)."""

    KIMI_BASE_URL = "https://api.moonshot.ai/v1"

    def __init__(
        self,
        api_key: str,
        model_name: str = "kimi-k2.5",
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 4096,
    ):
        """
        Initialize Kimi provider.

        Args:
            api_key: Kimi (Moonshot) API key
            model_name: Kimi model to use
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
        return "Kimi"

    def _init_client(self) -> Any:
        """Initialize the OpenAI-compatible client for Kimi."""
        from openai import OpenAI
        return OpenAI(
            api_key=self._api_key,
            base_url=self.KIMI_BASE_URL,
        )

    def _call_api(
        self,
        messages: list[dict],
        system_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Make the Kimi API call via OpenAI-compatible endpoint.

        Args:
            messages: List of conversation messages
            system_prompt: System prompt to use
            temperature: Sampling temperature

        Returns:
            Text response from Kimi
        """
        client = self._get_client()

        # Kimi uses OpenAI message format with system as first message
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = client.chat.completions.create(
            model=self._model_name,
            messages=formatted_messages,
            max_completion_tokens=self._max_output_tokens,
            temperature=0.6,  # Kimi K2.5 only accepts 0.6
            extra_body={"thinking": {"type": "disabled"}},
        )

        # Extract text from response
        if not response.choices or not response.choices[0].message.content:
            raise Exception("Kimi n'a pas genere de reponse.")

        return response.choices[0].message.content

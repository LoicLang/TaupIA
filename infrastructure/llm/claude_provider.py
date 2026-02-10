"""
Claude LLM Provider implementation.

Implements the LLMProvider protocol for Anthropic's Claude models.
"""

from typing import Optional, Any

import anthropic

from infrastructure.llm.base import BaseLLMProvider


class ClaudeLLMProvider(BaseLLMProvider):
    """LLM Provider implementation for Anthropic Claude."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "claude-sonnet-4-20250514",
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 4096,
    ):
        """
        Initialize Claude provider.

        Args:
            api_key: Anthropic API key
            model_name: Claude model to use
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
        return "Claude"

    def _init_client(self) -> Any:
        """Initialize the Anthropic client."""
        return anthropic.Anthropic(api_key=self._api_key)

    def _call_api(
        self,
        messages: list[dict],
        system_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Make the actual Claude API call.

        Args:
            messages: List of conversation messages
            system_prompt: System prompt to use
            temperature: Sampling temperature

        Returns:
            Text response from Claude
        """
        client = self._get_client()

        # Claude uses messages directly (role: user/assistant)
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = client.messages.create(
            model=self._model_name,
            max_tokens=self._max_output_tokens,
            temperature=temperature,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=formatted_messages
        )

        # Extract text from response
        if not response.content or len(response.content) == 0:
            raise Exception("Claude n'a pas généré de réponse.")

        return response.content[0].text

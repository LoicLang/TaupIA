"""
DeepSeek LLM Provider implementation.

Implements the LLMProvider protocol for DeepSeek via OpenAI-compatible API.
"""

import json
from typing import Optional, Any

from core.entities.agent import AgentResponse, ToolCall
from infrastructure.llm.base import BaseLLMProvider


class DeepSeekLLMProvider(BaseLLMProvider):
    """LLM Provider implementation for DeepSeek."""

    DEEPSEEK_BASE_URL = "https://api.deepseek.com"

    def __init__(
        self,
        api_key: str,
        model_name: str = "deepseek-chat",
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 4096,
    ):
        """
        Initialize DeepSeek provider.

        Args:
            api_key: DeepSeek API key
            model_name: DeepSeek model to use
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
        return "DeepSeek"

    def _init_client(self) -> Any:
        """Initialize the OpenAI-compatible client for DeepSeek."""
        from openai import OpenAI
        return OpenAI(
            api_key=self._api_key,
            base_url=self.DEEPSEEK_BASE_URL,
        )

    def _call_api(
        self,
        messages: list[dict],
        system_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Make the DeepSeek API call via OpenAI-compatible endpoint.

        Args:
            messages: List of conversation messages
            system_prompt: System prompt to use
            temperature: Sampling temperature

        Returns:
            Text response from DeepSeek
        """
        client = self._get_client()

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
            temperature=temperature,
        )

        if not response.choices or not response.choices[0].message.content:
            raise Exception("DeepSeek n'a pas genere de reponse.")

        return response.choices[0].message.content

    def _call_api_with_tools(
        self,
        messages: list[dict],
        system_prompt: str,
        tools: list[dict],
        temperature: float = 0.7,
    ) -> AgentResponse:
        """Make a DeepSeek API call with tool definitions."""
        client = self._get_client()

        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            role = msg["role"]
            if role == "tool":
                formatted_messages.append({
                    "role": "tool",
                    "tool_call_id": msg.get("tool_call_id", ""),
                    "content": msg.get("content", ""),
                })
            elif role == "assistant" and "tool_calls" in msg:
                formatted_messages.append({
                    "role": "assistant",
                    "content": msg.get("content") or "",
                    "tool_calls": msg["tool_calls"],
                })
            else:
                formatted_messages.append({
                    "role": role,
                    "content": msg.get("content", ""),
                })

        response = client.chat.completions.create(
            model=self._model_name,
            messages=formatted_messages,
            max_completion_tokens=self._max_output_tokens,
            temperature=temperature,
            tools=tools,
            tool_choice="auto",
        )

        choice = response.choices[0]
        message = choice.message

        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    args = {}
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=args,
                ))

        return AgentResponse(
            text=message.content,
            tool_calls=tool_calls,
            stop_reason="tool_use" if tool_calls else "end_turn",
        )

"""
Claude LLM Provider implementation.

Implements the LLMProvider protocol for Anthropic's Claude models.
"""

import json
from typing import Optional, Any

import anthropic

from core.entities.agent import AgentResponse, ToolCall
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

    def _call_api_with_tools(
        self,
        messages: list[dict],
        system_prompt: str,
        tools: list[dict],
        temperature: float = 0.7,
    ) -> AgentResponse:
        """Make a Claude API call with tool definitions."""
        client = self._get_client()

        # Convert OpenAI tool format to Claude tool format
        claude_tools = []
        for tool in tools:
            func = tool.get("function", {})
            claude_tools.append({
                "name": func["name"],
                "description": func.get("description", ""),
                "input_schema": func.get("parameters", {"type": "object", "properties": {}}),
            })

        # Convert messages to Claude format
        formatted_messages = []
        for msg in messages:
            role = msg["role"]
            if role == "assistant" and "tool_calls" in msg:
                # Assistant message with tool use
                content = []
                if msg.get("content"):
                    content.append({"type": "text", "text": msg["content"]})
                for tc in msg["tool_calls"]:
                    func = tc.get("function", {})
                    args = func.get("arguments", "{}")
                    if isinstance(args, str):
                        args = json.loads(args)
                    content.append({
                        "type": "tool_use",
                        "id": tc["id"],
                        "name": func["name"],
                        "input": args,
                    })
                formatted_messages.append({"role": "assistant", "content": content})
            elif role == "tool":
                # Tool result — Claude expects these in a user message
                tool_result = {
                    "type": "tool_result",
                    "tool_use_id": msg.get("tool_call_id", ""),
                    "content": msg.get("content", ""),
                }
                # Merge consecutive tool results into one user message
                if formatted_messages and formatted_messages[-1].get("role") == "user":
                    last = formatted_messages[-1]
                    if isinstance(last["content"], list):
                        last["content"].append(tool_result)
                    else:
                        formatted_messages[-1] = {
                            "role": "user",
                            "content": [tool_result],
                        }
                else:
                    formatted_messages.append({
                        "role": "user",
                        "content": [tool_result],
                    })
            else:
                formatted_messages.append({
                    "role": role,
                    "content": msg.get("content", ""),
                })

        response = client.messages.create(
            model=self._model_name,
            max_tokens=self._max_output_tokens,
            temperature=temperature,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=formatted_messages,
            tools=claude_tools,
        )

        # Parse response
        text_parts = []
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    id=block.id,
                    name=block.name,
                    arguments=block.input if isinstance(block.input, dict) else {},
                ))

        stop = "tool_use" if response.stop_reason == "tool_use" else "end_turn"

        return AgentResponse(
            text="\n".join(text_parts) if text_parts else None,
            tool_calls=tool_calls,
            stop_reason=stop,
        )

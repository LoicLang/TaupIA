"""
Gemini LLM Provider implementation.

Implements the LLMProvider protocol for Google's Gemini models.
"""

import json
import uuid
from typing import Optional, Any

from google import genai
from google.genai import types

from core.entities.agent import AgentResponse, ToolCall
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

    def _call_api_with_tools(
        self,
        messages: list[dict],
        system_prompt: str,
        tools: list[dict],
        temperature: float = 0.7,
    ) -> AgentResponse:
        """Make a Gemini API call with tool definitions."""
        client = self._get_client()

        # Convert OpenAI tool format to Gemini function declarations
        function_declarations = []
        for tool in tools:
            func = tool.get("function", {})
            function_declarations.append(types.FunctionDeclaration(
                name=func["name"],
                description=func.get("description", ""),
                parameters=func.get("parameters"),
            ))

        # Convert messages to Gemini Content format
        contents = []
        for msg in messages:
            role = msg["role"]
            if role == "assistant":
                # Check if this is a tool-call message
                if "tool_calls" in msg:
                    parts = []
                    if msg.get("content"):
                        parts.append(types.Part.from_text(text=msg["content"]))
                    for tc in msg["tool_calls"]:
                        func = tc.get("function", {})
                        args = func.get("arguments", "{}")
                        if isinstance(args, str):
                            args = json.loads(args)
                        parts.append(types.Part.from_function_call(
                            name=func["name"],
                            args=args,
                        ))
                    contents.append(types.Content(role="model", parts=parts))
                else:
                    parts = [types.Part.from_text(text=msg.get("content", ""))]
                    contents.append(types.Content(role="model", parts=parts))
            elif role == "tool":
                # Tool result → Gemini function response
                content_str = msg.get("content", "{}")
                try:
                    result_data = json.loads(content_str)
                except json.JSONDecodeError:
                    result_data = {"result": content_str}
                # Find the tool name from the previous assistant message
                tool_name = self._find_tool_name_for_id(messages, msg.get("tool_call_id", ""))
                parts = [types.Part.from_function_response(
                    name=tool_name,
                    response=result_data,
                )]
                contents.append(types.Content(role="user", parts=parts))
            else:
                parts = [types.Part.from_text(text=msg.get("content", ""))]
                contents.append(types.Content(role="user", parts=parts))

        response = client.models.generate_content(
            model=self._model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=self._max_output_tokens,
                system_instruction=system_prompt,
                tools=[types.Tool(function_declarations=function_declarations)],
            )
        )

        # Parse response for text and/or function calls
        text_parts = []
        tool_calls = []

        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if part.text:
                    text_parts.append(part.text)
                elif part.function_call:
                    fc = part.function_call
                    tool_calls.append(ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        name=fc.name,
                        arguments=dict(fc.args) if fc.args else {},
                    ))

        return AgentResponse(
            text="\n".join(text_parts) if text_parts else None,
            tool_calls=tool_calls,
            stop_reason="tool_use" if tool_calls else "end_turn",
        )

    def _find_tool_name_for_id(self, messages: list[dict], tool_call_id: str) -> str:
        """Find the tool name associated with a tool_call_id in message history."""
        for msg in reversed(messages):
            if msg.get("role") == "assistant" and "tool_calls" in msg:
                for tc in msg["tool_calls"]:
                    if tc.get("id") == tool_call_id:
                        return tc.get("function", {}).get("name", "unknown")
        return "unknown"

    def _format_tool_calls_message(self, response: AgentResponse) -> dict:
        """Gemini uses the same OpenAI format for our internal message passing."""
        return super()._format_tool_calls_message(response)

    def _format_tool_result_message(self, tool_call: ToolCall, result: str) -> dict:
        """Gemini tool results are mapped in _call_api_with_tools."""
        return super()._format_tool_result_message(tool_call, result)

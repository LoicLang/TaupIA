"""Agent domain entities for tool-calling LLM interactions."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ToolCall:
    """Represents a tool call requested by the LLM."""

    id: str
    name: str
    arguments: dict = field(default_factory=dict)


@dataclass
class ToolResult:
    """Result of executing a tool call."""

    tool_call_id: str
    name: str
    content: str  # JSON string


@dataclass
class AgentResponse:
    """Response from an LLM that may include tool calls."""

    text: Optional[str] = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    stop_reason: str = "end_turn"  # "end_turn" | "tool_use" | "max_tokens"

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)

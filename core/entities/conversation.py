"""Conversation domain entities."""

from dataclasses import dataclass, field
from typing import Literal, Optional
from datetime import datetime


MessageRole = Literal["user", "assistant"]


@dataclass
class Message:
    """A single message in a conversation."""

    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dict format for API calls."""
        return {
            "role": self.role,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Create from dict."""
        return cls(
            role=data["role"],
            content=data["content"],
        )

    def __len__(self) -> int:
        """Return content length for truncation calculations."""
        return len(self.content)


@dataclass
class ConversationHistory:
    """Manages conversation history with truncation support."""

    messages: list[Message] = field(default_factory=list)
    max_messages: int = 30
    max_chars: int = 6000

    def add(self, role: MessageRole, content: str) -> None:
        """Add a message to the history."""
        self.messages.append(Message(role=role, content=content))

    def add_user(self, content: str) -> None:
        """Add a user message."""
        self.add("user", content)

    def add_assistant(self, content: str) -> None:
        """Add an assistant message."""
        self.add("assistant", content)

    def get_truncated(self, max_chars: Optional[int] = None) -> list[Message]:
        """Get recent messages within character limit."""
        limit = max_chars or self.max_chars
        recent = self.messages[-self.max_messages:] if len(self.messages) > self.max_messages else self.messages

        total_chars = 0
        result = []
        for msg in reversed(recent):
            msg_length = len(msg.content)
            if total_chars + msg_length > limit:
                break
            result.insert(0, msg)
            total_chars += msg_length

        return result

    def to_dict_list(self, max_chars: Optional[int] = None) -> list[dict]:
        """Get truncated history as list of dicts."""
        return [msg.to_dict() for msg in self.get_truncated(max_chars)]

    def clear(self) -> None:
        """Clear all messages."""
        self.messages = []

    def __len__(self) -> int:
        return len(self.messages)

    def __bool__(self) -> bool:
        return bool(self.messages)

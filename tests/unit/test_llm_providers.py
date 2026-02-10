"""Tests for LLM provider infrastructure."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from core.entities import EvaluationResult, Score
from infrastructure.llm.base import BaseLLMProvider
from infrastructure.llm.gemini_provider import GeminiLLMProvider
from infrastructure.llm.claude_provider import ClaudeLLMProvider


class TestBaseLLMProvider:
    """Tests for BaseLLMProvider shared functionality."""

    def test_truncate_history_empty(self):
        """Test truncation with empty history."""

        class DummyProvider(BaseLLMProvider):
            @property
            def name(self):
                return "Dummy"

            def _init_client(self):
                return None

            def _call_api(self, messages, system_prompt, temperature=0.7):
                return "test"

        provider = DummyProvider(model_name="test")
        result = provider._truncate_history(None)
        assert result == []

        result = provider._truncate_history([])
        assert result == []

    def test_truncate_history_within_limits(self):
        """Test truncation when history fits within limits."""

        class DummyProvider(BaseLLMProvider):
            @property
            def name(self):
                return "Dummy"

            def _init_client(self):
                return None

            def _call_api(self, messages, system_prompt, temperature=0.7):
                return "test"

        provider = DummyProvider(model_name="test")
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ]
        result = provider._truncate_history(history, max_chars=1000, max_messages=10)
        assert len(result) == 2
        assert result[0]["content"] == "Hello"

    def test_truncate_history_exceeds_char_limit(self):
        """Test truncation when history exceeds character limit."""

        class DummyProvider(BaseLLMProvider):
            @property
            def name(self):
                return "Dummy"

            def _init_client(self):
                return None

            def _call_api(self, messages, system_prompt, temperature=0.7):
                return "test"

        provider = DummyProvider(model_name="test")
        history = [
            {"role": "user", "content": "A" * 100},
            {"role": "assistant", "content": "B" * 100},
            {"role": "user", "content": "C" * 100},
        ]
        result = provider._truncate_history(history, max_chars=150, max_messages=10)
        # Should keep only the most recent messages that fit
        assert len(result) == 1
        assert result[0]["content"] == "C" * 100

    def test_parse_evaluation_response_complete(self):
        """Test parsing a complete evaluation response."""

        class DummyProvider(BaseLLMProvider):
            @property
            def name(self):
                return "Dummy"

            def _init_client(self):
                return None

            def _call_api(self, messages, system_prompt, temperature=0.7):
                return "test"

        provider = DummyProvider(model_name="test")
        text = """Très bien ! Tu as montré une bonne compréhension.

SCORE: 85/100
COMPLET: OUI
MANQUE: rien"""

        result = provider._parse_evaluation_response(text)
        assert isinstance(result, EvaluationResult)
        assert result.score.value == 85
        assert result.is_complete is True
        assert result.missing_points == []
        assert "Très bien" in result.feedback

    def test_parse_evaluation_response_incomplete(self):
        """Test parsing an incomplete evaluation response."""

        class DummyProvider(BaseLLMProvider):
            @property
            def name(self):
                return "Dummy"

            def _init_client(self):
                return None

            def _call_api(self, messages, system_prompt, temperature=0.7):
                return "test"

        provider = DummyProvider(model_name="test")
        text = """Il manque quelques points importants.

SCORE: 60/100
COMPLET: NON
MANQUE: définition précise, exemple"""

        result = provider._parse_evaluation_response(text)
        assert result.score.value == 60
        assert result.is_complete is False
        assert "définition précise" in result.missing_points
        assert "exemple" in result.missing_points


class TestGeminiProvider:
    """Tests for GeminiLLMProvider."""

    def test_initialization(self):
        """Test provider initialization."""
        provider = GeminiLLMProvider(
            api_key="test-key",
            model_name="gemini-2.0-flash",
        )
        assert provider.name == "Gemini"
        assert provider.model_name == "gemini-2.0-flash"

    @patch("infrastructure.llm.gemini_provider.genai")
    def test_init_client(self, mock_genai):
        """Test client initialization."""
        mock_client = Mock()
        mock_genai.Client.return_value = mock_client

        provider = GeminiLLMProvider(api_key="test-key")
        client = provider._init_client()

        mock_genai.Client.assert_called_once_with(api_key="test-key")
        assert client == mock_client


class TestClaudeProvider:
    """Tests for ClaudeLLMProvider."""

    def test_initialization(self):
        """Test provider initialization."""
        provider = ClaudeLLMProvider(
            api_key="test-key",
            model_name="claude-sonnet-4-20250514",
        )
        assert provider.name == "Claude"
        assert provider.model_name == "claude-sonnet-4-20250514"

    @patch("infrastructure.llm.claude_provider.anthropic")
    def test_init_client(self, mock_anthropic):
        """Test client initialization."""
        mock_client = Mock()
        mock_anthropic.Anthropic.return_value = mock_client

        provider = ClaudeLLMProvider(api_key="test-key")
        client = provider._init_client()

        mock_anthropic.Anthropic.assert_called_once_with(api_key="test-key")
        assert client == mock_client


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""Tests for DI Container."""

import os
import pytest
from unittest.mock import patch, MagicMock

from application.container import Container, get_container, reset_container
from application.settings import Settings


class TestContainer:
    """Tests for the DI Container."""

    def setup_method(self):
        """Reset container before each test."""
        reset_container()

    def test_container_initialization(self):
        """Test container initializes with settings."""
        container = Container()
        assert container.settings is not None
        assert isinstance(container.settings, Settings)

    @patch.dict(os.environ, {
        "GOOGLE_API_KEY": "test-google-key",
        "CLAUDE_API_KEY": "test-claude-key",
    }, clear=False)
    def test_container_with_env_settings(self):
        """Test container loads from environment."""
        # Create settings after patching env
        settings = Settings(_env_file=None)
        container = Container(settings=settings)
        assert container.settings.google_api_key == "test-google-key"
        assert container.settings.claude_api_key == "test-claude-key"

    @patch.dict(os.environ, {
        "GOOGLE_API_KEY": "",
        "CLAUDE_API_KEY": "",
    }, clear=False)
    def test_get_available_providers_none(self):
        """Test available providers when no keys configured."""
        settings = Settings(_env_file=None)
        container = Container(settings=settings)
        providers = container.get_available_providers()
        assert providers == []

    @patch.dict(os.environ, {
        "GOOGLE_API_KEY": "test-google",
        "CLAUDE_API_KEY": "test-claude",
    }, clear=False)
    def test_get_available_providers_with_keys(self):
        """Test available providers with configured keys."""
        settings = Settings(_env_file=None)
        container = Container(settings=settings)
        providers = container.get_available_providers()
        assert "gemini" in providers
        assert "claude" in providers

    def test_get_llm_provider_unknown(self):
        """Test error for unknown provider."""
        container = Container()
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            container.get_llm_provider("unknown")

    @patch.dict(os.environ, {
        "GOOGLE_API_KEY": "",
    }, clear=False)
    def test_get_llm_provider_missing_api_key(self):
        """Test error when API key is missing."""
        settings = Settings(_env_file=None)
        container = Container(settings=settings)
        with pytest.raises(ValueError, match="non configurée"):
            container.get_llm_provider("gemini")

    @patch("application.container.Container._create_gemini_llm")
    def test_get_llm_provider_caching(self, mock_create):
        """Test that providers are cached."""
        mock_provider = MagicMock()
        mock_create.return_value = mock_provider

        container = Container()
        # Force a key to exist for the test
        container._settings.google_api_key = "test-key"

        # First call creates provider
        provider1 = container.get_llm_provider("gemini")
        assert mock_create.call_count == 1

        # Second call returns cached
        provider2 = container.get_llm_provider("gemini")
        assert mock_create.call_count == 1  # Not called again
        assert provider1 is provider2


class TestGlobalContainer:
    """Tests for global container functions."""

    def setup_method(self):
        """Reset container before each test."""
        reset_container()

    def test_get_container_singleton(self):
        """Test that get_container returns same instance."""
        container1 = get_container()
        container2 = get_container()
        assert container1 is container2

    def test_reset_container(self):
        """Test that reset_container creates new instance."""
        container1 = get_container()
        reset_container()
        container2 = get_container()
        assert container1 is not container2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

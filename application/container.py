"""
Dependency Injection Container.

Provides centralized creation and management of service instances.
"""

from typing import Optional

from core.interfaces import LLMProvider, OCRProvider
from application.settings import Settings


class Container:
    """
    Dependency Injection Container for Khôlleur AI.

    Manages creation and caching of service instances.
    """

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize container with settings.

        Args:
            settings: Application settings (loads from env if not provided)
        """
        self._settings = settings or Settings()
        self._llm_providers: dict[str, LLMProvider] = {}
        self._ocr_providers: dict[str, OCRProvider] = {}

    @property
    def settings(self) -> Settings:
        """Get application settings."""
        return self._settings

    # =========================================================================
    # LLM Providers
    # =========================================================================

    def get_llm_provider(self, provider_name: Optional[str] = None) -> LLMProvider:
        """
        Get or create an LLM provider by name.

        Args:
            provider_name: Provider name (gemini, claude, kimi, deepseek).
                          Uses default from settings if not specified.

        Returns:
            LLMProvider instance

        Raises:
            ValueError: If provider is not configured or API key missing
        """
        name = (provider_name or self._settings.default_llm_provider).lower()

        # Return cached provider if exists
        if name in self._llm_providers:
            return self._llm_providers[name]

        # Create new provider
        provider = self._create_llm_provider(name)
        self._llm_providers[name] = provider
        return provider

    def _create_llm_provider(self, name: str) -> LLMProvider:
        """Create a new LLM provider instance."""
        if name == "gemini":
            return self._create_gemini_llm()
        elif name == "claude":
            return self._create_claude_llm()
        elif name == "kimi":
            return self._create_kimi_llm()
        elif name == "deepseek":
            return self._create_deepseek_llm()
        else:
            raise ValueError(f"Unknown LLM provider: {name}")

    def _create_gemini_llm(self) -> LLMProvider:
        """Create Gemini LLM provider."""
        if not self._settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY non configurée dans le fichier .env")

        from infrastructure.llm import GeminiLLMProvider
        return GeminiLLMProvider(
            api_key=self._settings.google_api_key,
            model_name=self._settings.gemini_model,
        )

    def _create_claude_llm(self) -> LLMProvider:
        """Create Claude LLM provider."""
        if not self._settings.claude_api_key:
            raise ValueError("CLAUDE_API_KEY non configurée dans le fichier .env")

        from infrastructure.llm import ClaudeLLMProvider
        return ClaudeLLMProvider(
            api_key=self._settings.claude_api_key,
            model_name=self._settings.claude_model,
        )

    def _create_kimi_llm(self) -> LLMProvider:
        """Create Kimi LLM provider."""
        if not self._settings.kimi_api_key:
            raise ValueError("KIMI_API_KEY non configuree dans le fichier .env")

        from infrastructure.llm import KimiLLMProvider
        return KimiLLMProvider(
            api_key=self._settings.kimi_api_key,
            model_name=self._settings.kimi_model,
        )

    def _create_deepseek_llm(self) -> LLMProvider:
        """Create DeepSeek LLM provider."""
        if not self._settings.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY non configuree dans le fichier .env")

        from infrastructure.llm import DeepSeekLLMProvider
        return DeepSeekLLMProvider(
            api_key=self._settings.deepseek_api_key,
            model_name=self._settings.deepseek_model,
        )

    def get_available_llm_providers(self) -> list[str]:
        """
        Get list of available (configured) LLM providers.

        Returns:
            List of provider names that have API keys configured
        """
        available = []
        if self._settings.google_api_key:
            available.append("gemini")
        if self._settings.claude_api_key:
            available.append("claude")
        if self._settings.deepseek_api_key:
            available.append("deepseek")
        if self._settings.kimi_api_key:
            available.append("kimi")
        return available

    # Alias for backwards compatibility
    def get_available_providers(self) -> list[str]:
        """Alias for get_available_llm_providers()."""
        return self.get_available_llm_providers()

    # =========================================================================
    # OCR Providers
    # =========================================================================

    def get_ocr_provider(self, provider_name: Optional[str] = None) -> OCRProvider:
        """
        Get or create an OCR provider by name.

        Args:
            provider_name: Provider name (gemini, kimi).
                          Uses default from settings if not specified.

        Returns:
            OCRProvider instance

        Raises:
            ValueError: If provider is not configured or API key missing
        """
        name = (provider_name or self._settings.ocr_provider).lower()

        # Return cached provider if exists
        if name in self._ocr_providers:
            return self._ocr_providers[name]

        # Create new provider
        provider = self._create_ocr_provider(name)
        self._ocr_providers[name] = provider
        return provider

    def _create_ocr_provider(self, name: str) -> OCRProvider:
        """Create a new OCR provider instance."""
        if name == "gemini":
            return self._create_gemini_ocr()
        elif name == "kimi":
            return self._create_kimi_ocr()
        else:
            raise ValueError(f"Unknown OCR provider: {name}")

    def _create_gemini_ocr(self) -> OCRProvider:
        """Create Gemini OCR provider."""
        if not self._settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY non configurée dans le fichier .env")

        from infrastructure.ocr import GeminiOCRProvider
        return GeminiOCRProvider(
            api_key=self._settings.google_api_key,
            model_name=self._settings.gemini_ocr_model,
        )

    def _create_kimi_ocr(self) -> OCRProvider:
        """Create Kimi OCR provider."""
        if not self._settings.kimi_api_key:
            raise ValueError("KIMI_API_KEY non configuree dans le fichier .env")

        from infrastructure.ocr import KimiOCRProvider
        return KimiOCRProvider(
            api_key=self._settings.kimi_api_key,
            model_name=self._settings.kimi_ocr_model,
        )

    def get_available_ocr_providers(self) -> list[str]:
        """
        Get list of available (configured) OCR providers.

        Returns:
            List of provider names that have API keys configured
        """
        available = []
        if self._settings.google_api_key:
            available.append("gemini")
        if self._settings.kimi_api_key:
            available.append("kimi")
        return available


# Global container instance (lazy initialization)
_container: Optional[Container] = None


def get_container() -> Container:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container():
    """Reset the global container (useful for testing)."""
    global _container
    _container = None

"""Application settings using Pydantic."""

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Keys
    google_api_key: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")
    claude_api_key: Optional[str] = Field(default=None, alias="CLAUDE_API_KEY")
    kimi_api_key: Optional[str] = Field(default=None, alias="KIMI_API_KEY")
    deepseek_api_key: Optional[str] = Field(default=None, alias="DEEPSEEK_API_KEY")

    # LLM Model Names
    gemini_model: str = Field(default="gemini-3-flash-preview", alias="GEMINI_MODEL")
    claude_model: str = Field(default="claude-sonnet-4-5-20250929", alias="CLAUDE_MODEL")
    kimi_model: str = Field(default="kimi-k2.5", alias="KIMI_MODEL")
    deepseek_model: str = Field(default="deepseek-chat", alias="DEEPSEEK_MODEL")

    # OCR Model Names (can differ from LLM models)
    gemini_ocr_model: str = Field(default="gemini-3-flash-preview", alias="GEMINI_OCR_MODEL")
    kimi_ocr_model: str = Field(default="kimi-k2.5", alias="KIMI_OCR_MODEL")

    # Provider Selection
    default_llm_provider: Literal["gemini", "claude", "kimi", "deepseek"] = Field(
        default="kimi", alias="DEFAULT_AI_PROVIDER"
    )
    ocr_provider: Literal["gemini", "kimi"] = Field(
        default="kimi", alias="OCR_PROVIDER"
    )

    # Enforced providers for regular users
    fixed_ai_provider: Literal["gemini", "claude", "kimi", "deepseek"] = Field(
        default="deepseek", alias="FIXED_AI_PROVIDER"
    )
    fixed_ocr_provider: Literal["gemini", "kimi"] = Field(
        default="kimi", alias="FIXED_OCR_PROVIDER"
    )

    # Users allowed to override fixed providers (comma-separated allowlists)
    provider_override_user_ids: str = Field(
        default="", alias="PROVIDER_OVERRIDE_USER_IDS"
    )
    provider_override_emails: str = Field(
        default="", alias="PROVIDER_OVERRIDE_EMAILS"
    )

    # Showcase feature flag: let the agent navigate (change exercise on demand) and
    # use the student mastery profile. Off in production.
    allow_deviation: bool = Field(default=False, alias="ALLOW_DEVIATION")

    # Paths (computed from BASE_DIR)
    @property
    def base_dir(self) -> Path:
        return Path(__file__).parent.parent

    @property
    def data_dir(self) -> Path:
        return self.base_dir / "data"

    @property
    def knowledge_graph_file(self) -> Path:
        return self.data_dir / "knowledge_graph.json"

    @property
    def questions_kholle_file(self) -> Path:
        return self.data_dir / "questions_kholle.json"

    @property
    def programme_file(self) -> Path:
        return self.data_dir / "programme.json"

    @property
    def cours_json_dir(self) -> Path:
        return self.data_dir / "cours"

    @property
    def exo_json_dir(self) -> Path:
        return self.data_dir / "exercices"

    @property
    def prompts_dir(self) -> Path:
        return self.base_dir / "prompts"

    # Helper methods
    def has_gemini(self) -> bool:
        return bool(self.google_api_key)

    def has_claude(self) -> bool:
        return bool(self.claude_api_key)

    def has_kimi(self) -> bool:
        return bool(self.kimi_api_key)

    def has_deepseek(self) -> bool:
        return bool(self.deepseek_api_key)

    def get_available_llm_providers(self) -> list[str]:
        """Return list of available LLM providers based on API keys."""
        providers = []
        if self.has_kimi():
            providers.append("kimi")
        if self.has_gemini():
            providers.append("gemini")
        if self.has_claude():
            providers.append("claude")
        if self.has_deepseek():
            providers.append("deepseek")
        return providers

    def get_available_ocr_providers(self) -> list[str]:
        """Return list of available OCR providers based on API keys."""
        providers = []
        if self.has_kimi():
            providers.append("kimi")
        if self.has_gemini():
            providers.append("gemini")
        return providers

    @staticmethod
    def _parse_csv(raw: str) -> set[str]:
        return {v.strip().lower() for v in raw.split(",") if v.strip()}

    @property
    def provider_override_user_ids_set(self) -> set[str]:
        """Allowlisted user IDs that can override providers."""
        return self._parse_csv(self.provider_override_user_ids)

    @property
    def provider_override_emails_set(self) -> set[str]:
        """Allowlisted emails that can override providers."""
        return self._parse_csv(self.provider_override_emails)

    def load_prompt(self, prompt_name: str) -> str:
        """Load a prompt from the prompts directory."""
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        return prompt_file.read_text(encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

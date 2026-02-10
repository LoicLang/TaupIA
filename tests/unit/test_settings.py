"""Tests for application settings."""

import pytest
from pathlib import Path


class TestSettings:
    def test_settings_load(self):
        from application.settings import Settings

        settings = Settings()
        assert settings.base_dir.exists()

    def test_paths(self):
        from application.settings import get_settings

        settings = get_settings()
        assert settings.data_dir.name == "data"
        assert settings.prompts_dir.name == "prompts"
        assert settings.knowledge_graph_file.name == "knowledge_graph.json"
        assert settings.questions_kholle_file.name == "questions_kholle.json"
        assert settings.programme_file.name == "programme.json"
        assert settings.cours_json_dir.name == "cours"
        assert settings.exo_json_dir.name == "exercices"

    def test_load_prompt(self):
        from application.settings import get_settings

        settings = get_settings()
        prompt = settings.load_prompt("kholleur_system")
        assert "khôlleur" in prompt.lower()
        assert "COMPLET" in prompt

    def test_available_providers(self):
        from application.settings import Settings

        settings = Settings()
        # At minimum, should return empty lists if no keys
        llm_providers = settings.get_available_llm_providers()
        ocr_providers = settings.get_available_ocr_providers()
        assert isinstance(llm_providers, list)
        assert isinstance(ocr_providers, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

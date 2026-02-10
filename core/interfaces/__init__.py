"""Interfaces (Protocols) for dependency injection."""

from .llm_provider import LLMProvider
from .ocr_provider import OCRProvider
from .embedding_provider import EmbeddingProvider

__all__ = [
    "LLMProvider",
    "OCRProvider",
    "EmbeddingProvider",
]

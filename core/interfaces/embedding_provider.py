"""Embedding Provider interface."""

from typing import Protocol


class EmbeddingProvider(Protocol):
    """Interface for embedding providers (text to vector)."""

    @property
    def name(self) -> str:
        """Provider name for display."""
        ...

    @property
    def model_name(self) -> str:
        """Model identifier."""
        ...

    @property
    def dimension(self) -> int:
        """Embedding dimension."""
        ...

    def embed(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        ...

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        ...

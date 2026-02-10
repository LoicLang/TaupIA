"""OCR Provider interface."""

from typing import Protocol


class OCRProvider(Protocol):
    """Interface for OCR providers (image to LaTeX transcription)."""

    @property
    def name(self) -> str:
        """Provider name for display."""
        ...

    @property
    def model_name(self) -> str:
        """Model identifier."""
        ...

    def transcribe(
        self,
        image_data: bytes,
        mime_type: str = "image/jpeg",
    ) -> str:
        """
        Transcribe an image of handwritten math to LaTeX.

        Args:
            image_data: Raw image bytes
            mime_type: Image MIME type

        Returns:
            LaTeX transcription of the image content
        """
        ...

"""
Gemini OCR Provider implementation.

Implements the OCRProvider protocol for Google's Gemini models.
"""

from typing import Any

from google import genai
from google.genai import types

from infrastructure.ocr.base import BaseOCRProvider


class GeminiOCRProvider(BaseOCRProvider):
    """OCR Provider implementation for Google Gemini."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-3.0-flash-preview",
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 8192,
    ):
        """
        Initialize Gemini OCR provider.

        Args:
            api_key: Google API key
            model_name: Gemini model to use
            max_retries: Maximum retry attempts
            initial_delay: Initial delay for retry
            max_output_tokens: Maximum output tokens
        """
        super().__init__(
            model_name=model_name,
            max_retries=max_retries,
            initial_delay=initial_delay,
            max_output_tokens=max_output_tokens,
        )
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "Gemini"

    def _init_client(self) -> Any:
        """Initialize the Gemini client."""
        return genai.Client(api_key=self._api_key)

    def _call_api(self, image_data: bytes, mime_type: str, prompt: str) -> str:
        """
        Make the Gemini API call for OCR.

        Args:
            image_data: Raw image bytes
            mime_type: Image MIME type
            prompt: System prompt for OCR

        Returns:
            Transcribed text
        """
        client = self._get_client()

        response = client.models.generate_content(
            model=self._model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt + "\n\nTranscris ce brouillon mathématique en LaTeX."),
                        types.Part.from_bytes(data=image_data, mime_type=mime_type),
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=self._max_output_tokens,
            )
        )

        if not response.text:
            finish_reason = "unknown"
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    finish_reason = candidate.finish_reason
            raise Exception(f"Gemini n'a pas pu transcrire l'image (finish_reason={finish_reason}).")

        return response.text

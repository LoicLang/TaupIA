"""
Kimi (Moonshot AI) OCR Provider implementation.

Implements the OCRProvider protocol for Kimi K2.5 vision via OpenAI-compatible API.
"""

import base64
from typing import Any

from infrastructure.ocr.base import BaseOCRProvider


class KimiOCRProvider(BaseOCRProvider):
    """OCR Provider implementation for Kimi K2.5 Vision (Moonshot AI)."""

    KIMI_BASE_URL = "https://api.moonshot.ai/v1"

    def __init__(
        self,
        api_key: str,
        model_name: str = "kimi-k2.5",
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 8192,
    ):
        """
        Initialize Kimi OCR provider.

        Args:
            api_key: Kimi (Moonshot) API key
            model_name: Kimi model to use (must support vision)
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
        return "Kimi"

    def _init_client(self) -> Any:
        """Initialize the OpenAI-compatible client for Kimi."""
        from openai import OpenAI
        return OpenAI(
            api_key=self._api_key,
            base_url=self.KIMI_BASE_URL,
        )

    def _call_api(self, image_data: bytes, mime_type: str, prompt: str) -> str:
        """
        Make the Kimi API call for OCR via OpenAI-compatible endpoint.

        Args:
            image_data: Raw image bytes
            mime_type: Image MIME type
            prompt: System prompt for OCR

        Returns:
            Transcribed text
        """
        client = self._get_client()

        # Encode image to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        response = client.chat.completions.create(
            model=self._model_name,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Transcris ce brouillon mathematique en LaTeX."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_completion_tokens=self._max_output_tokens,
            temperature=0.6,  # Kimi K2.5 only accepts 0.6
            extra_body={"thinking": {"type": "disabled"}},
        )

        if not response.choices or not response.choices[0].message.content:
            raise Exception("Kimi n'a pas pu transcrire l'image.")

        return response.choices[0].message.content

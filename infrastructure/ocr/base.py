"""
Base OCR Provider with shared functionality.

This module provides common functionality for all OCR providers,
including image processing, retry logic, and prompt loading.
"""

import io
import time
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from pathlib import Path


class BaseOCRProvider(ABC):
    """Abstract base class for OCR providers with shared functionality."""

    def __init__(
        self,
        model_name: str,
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 8192,
        prompts_dir: Optional[Path] = None,
    ):
        """
        Initialize the base OCR provider.

        Args:
            model_name: Model identifier
            max_retries: Maximum retry attempts
            initial_delay: Initial delay in seconds for retry
            max_output_tokens: Maximum output tokens
            prompts_dir: Directory containing prompt files
        """
        self._model_name = model_name
        self._max_retries = max_retries
        self._initial_delay = initial_delay
        self._max_output_tokens = max_output_tokens
        self._prompts_dir = prompts_dir or Path(__file__).parent.parent.parent / "prompts"
        self._client = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name for display."""
        ...

    @property
    def model_name(self) -> str:
        """Model identifier."""
        return self._model_name

    @abstractmethod
    def _init_client(self) -> Any:
        """Initialize the API client. Called lazily."""
        ...

    @abstractmethod
    def _call_api(self, image_data: bytes, mime_type: str, prompt: str) -> str:
        """
        Make the actual API call for OCR.

        Args:
            image_data: Raw image bytes
            mime_type: Image MIME type
            prompt: System prompt for OCR

        Returns:
            Transcribed text
        """
        ...

    def _get_client(self) -> Any:
        """Get or initialize the API client."""
        if self._client is None:
            self._client = self._init_client()
        return self._client

    def _load_prompt(self) -> str:
        """Load the OCR system prompt."""
        prompt_file = self._prompts_dir / "ocr_system.txt"
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8")
        raise FileNotFoundError(f"OCR prompt file not found: {prompt_file}")

    def _call_with_retry(
        self,
        func: Callable[[], str],
        retryable_errors: tuple[str, ...] = ("503", "500", "overloaded", "rate_limit"),
    ) -> str:
        """
        Call a function with retry and exponential backoff.

        Args:
            func: Function to call (should return response text)
            retryable_errors: Error substrings that should trigger retry

        Returns:
            Response text from the successful call

        Raises:
            Exception: If all retries fail
        """
        delay = self._initial_delay
        last_exception = None

        for attempt in range(self._max_retries):
            try:
                response = func()

                # Check for empty response
                if not response or not response.strip():
                    if attempt < self._max_retries - 1:
                        print(f"[{self.name} OCR] Réponse vide, nouvelle tentative dans {delay}s...")
                        time.sleep(delay)
                        delay *= 2
                        continue
                    else:
                        raise Exception("Réponse vide après plusieurs tentatives.")

                return response

            except Exception as e:
                last_exception = e
                error_str = str(e).lower()

                # Check if error is retryable
                is_retryable = any(err in error_str for err in retryable_errors)

                if is_retryable and attempt < self._max_retries - 1:
                    print(f"[{self.name} OCR] Erreur, nouvelle tentative dans {delay}s... ({attempt + 1}/{self._max_retries})")
                    time.sleep(delay)
                    delay *= 2
                    continue
                elif is_retryable:
                    raise Exception(
                        f"{self.name} OCR a rencontré des erreurs après {self._max_retries} tentatives. "
                        f"Réessaie dans quelques minutes."
                    ) from e
                else:
                    raise e

        raise last_exception

    def _detect_mime_type(self, image_data: bytes) -> str:
        """Detect the actual MIME type from image bytes."""
        if image_data[:8] == b'\x89PNG\r\n\x1a\n':
            return "image/png"
        elif image_data[:2] == b'\xff\xd8':
            return "image/jpeg"
        elif image_data[:4] == b'RIFF' and image_data[8:12] == b'WEBP':
            return "image/webp"
        else:
            return "image/jpeg"  # Fallback

    def _resize_image_if_needed(
        self,
        image_data: bytes,
        mime_type: str,
        max_dimension: int = 4096,
    ) -> bytes:
        """
        Resize image if necessary, preserving quality for OCR.

        Args:
            image_data: Original image bytes
            mime_type: MIME type
            max_dimension: Maximum dimension (width or height) in pixels

        Returns:
            Optimized image bytes
        """
        try:
            from PIL import Image
        except ImportError:
            # PIL not available, return original
            return image_data

        img = Image.open(io.BytesIO(image_data))

        # Check if resize needed
        if img.width <= max_dimension and img.height <= max_dimension:
            # For PNG, convert RGBA to RGB if needed
            if mime_type == "image/png" and img.mode in ('RGBA', 'LA', 'P'):
                buffer = io.BytesIO()
                img_rgb = img.convert('RGB')
                img_rgb.save(buffer, format="PNG", optimize=True)
                return buffer.getvalue()
            return image_data

        # Calculate ratio to respect max_dimension
        ratio = min(max_dimension / img.width, max_dimension / img.height)
        new_width = int(img.width * ratio)
        new_height = int(img.height * ratio)

        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to RGB if necessary
        if img_resized.mode in ('RGBA', 'LA', 'P'):
            img_resized = img_resized.convert('RGB')

        # Save as PNG for text quality or JPEG for large images
        buffer = io.BytesIO()
        if new_width * new_height > 8_000_000:  # > 8 megapixels
            img_resized.save(buffer, format="JPEG", quality=95, optimize=True)
        else:
            img_resized.save(buffer, format="PNG", optimize=True)

        return buffer.getvalue()

    def transcribe(self, image_data: bytes, mime_type: str = "image/jpeg") -> str:
        """
        Transcribe an image of handwritten math to LaTeX.

        Args:
            image_data: Raw image bytes
            mime_type: Image MIME type

        Returns:
            LaTeX transcription of the image content
        """
        # Detect actual MIME type
        actual_mime = self._detect_mime_type(image_data)

        # Resize/optimize image
        optimized_data = self._resize_image_if_needed(image_data, actual_mime)

        # Load prompt
        prompt = self._load_prompt()

        def _call() -> str:
            return self._call_api(optimized_data, actual_mime, prompt)

        return self._call_with_retry(_call)

"""Endpoint OCR (transcription d'images)."""

from fastapi import APIRouter, Depends, File, Form, UploadFile

from application.container import Container
from backend.dependencies import get_di_container

router = APIRouter(tags=["ocr"])


@router.post("/ocr/transcribe")
async def transcribe_image(
    file: UploadFile = File(...),
    ocr_provider: str = Form("kimi"),
    container: Container = Depends(get_di_container),
):
    """Transcrit une image manuscrite en LaTeX via OCR."""
    image_data = await file.read()
    mime_type = file.content_type or "image/jpeg"

    provider = container.get_ocr_provider(ocr_provider)
    text = provider.transcribe(image_data, mime_type)

    return {"text": text}

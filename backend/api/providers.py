"""Endpoints providers LLM et OCR."""

from fastapi import APIRouter, Depends

from application.container import Container
from backend.dependencies import get_di_container

router = APIRouter(tags=["providers"])


@router.get("/providers/llm")
async def list_llm_providers(
    container: Container = Depends(get_di_container),
):
    """Liste les providers LLM disponibles (cles API configurees)."""
    return container.get_available_providers()


@router.get("/providers/ocr")
async def list_ocr_providers(
    container: Container = Depends(get_di_container),
):
    """Liste les providers OCR disponibles."""
    return container.get_available_ocr_providers()

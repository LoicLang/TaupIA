"""Endpoints providers LLM et OCR."""

from typing import Optional

from fastapi import APIRouter, Depends

from application.container import Container
from application.settings import get_settings
from backend.auth import get_current_user_optional
from backend.dependencies import get_di_container
from backend.provider_policy import allowed_llm_providers, allowed_ocr_providers

router = APIRouter(tags=["providers"])


@router.get("/providers/llm")
async def list_llm_providers(
    container: Container = Depends(get_di_container),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Liste les providers LLM disponibles (cles API configurees)."""
    settings = get_settings()
    return allowed_llm_providers(container, settings, current_user)


@router.get("/providers/ocr")
async def list_ocr_providers(
    container: Container = Depends(get_di_container),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Liste les providers OCR disponibles."""
    settings = get_settings()
    return allowed_ocr_providers(container, settings, current_user)

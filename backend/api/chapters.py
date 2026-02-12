"""Endpoints chapitres et stats."""

from fastapi import APIRouter, Depends

from services.knowledge_service import KnowledgeService
from backend.dependencies import get_knowledge_service

router = APIRouter(tags=["chapters"])


@router.get("/chapters")
async def list_chapters(
    ks: KnowledgeService = Depends(get_knowledge_service),
):
    """Liste les chapitres disponibles avec stats."""
    return ks.get_chapters()


@router.get("/stats")
async def get_stats(
    ks: KnowledgeService = Depends(get_knowledge_service),
):
    """Stats des collections (questions, exercices, concepts)."""
    return ks.get_collection_stats()

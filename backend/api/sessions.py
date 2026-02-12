"""Endpoints CRUD sessions."""

from fastapi import APIRouter, Depends

from backend.session_store import SessionStore, SessionState
from backend.dependencies import get_session_store, get_session
from backend.schemas.session import SessionResponse

router = APIRouter(tags=["sessions"])


@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    store: SessionStore = Depends(get_session_store),
):
    """Cree une nouvelle session de kholle."""
    session = store.create()
    return session.to_dict()


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session_state(
    session: SessionState = Depends(get_session),
):
    """Recupere l'etat d'une session."""
    return session.to_dict()


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    store: SessionStore = Depends(get_session_store),
):
    """Supprime une session (reset)."""
    deleted = store.delete(session_id)
    if not deleted:
        return {"detail": "Session not found"}
    return {"detail": "Session deleted"}

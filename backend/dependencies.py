"""
FastAPI dependencies.

Fournit KnowledgeService et Container via Depends().
"""

from typing import Optional

from services.knowledge_service import KnowledgeService
from application.container import get_container, Container
from backend.session_store import SessionStore, SessionState
from fastapi import HTTPException

# Singletons initialises au demarrage (lifespan)
_knowledge_service: Optional[KnowledgeService] = None
_session_store: Optional[SessionStore] = None


def init_services():
    """Initialise les services au demarrage de l'app."""
    global _knowledge_service, _session_store
    _knowledge_service = KnowledgeService()
    _session_store = SessionStore(ttl_hours=2)


def get_knowledge_service() -> KnowledgeService:
    """Dependency: KnowledgeService."""
    if _knowledge_service is None:
        raise RuntimeError("KnowledgeService not initialized")
    return _knowledge_service


def get_session_store() -> SessionStore:
    """Dependency: SessionStore."""
    if _session_store is None:
        raise RuntimeError("SessionStore not initialized")
    return _session_store


def get_di_container() -> Container:
    """Dependency: DI Container."""
    return get_container()


def get_session(session_id: str) -> SessionState:
    """Recupere une session ou leve 404."""
    store = get_session_store()
    session = store.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return session

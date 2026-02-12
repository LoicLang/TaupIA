"""
Session store in-memory.

Remplace st.session_state par un dict Python {uuid: SessionState}.
Les sessions expirent apres SESSION_TTL_HOURS d'inactivite.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class SessionState:
    """Etat d'une session de kholle (equivalent de st.session_state)."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    phase: str = "setup"
    chapter_id: Optional[str] = None
    difficulty: int = 3
    ai_provider: str = "kimi"
    ocr_provider: str = "kimi"
    format: str = "full"  # "full" ou "exercise_only"
    current_question: Optional[dict] = None
    current_exercise: Optional[dict] = None
    conversation_history: list[dict] = field(default_factory=list)
    question_validated: bool = False
    asked_questions: list[str] = field(default_factory=list)
    done_exercises: list[str] = field(default_factory=list)
    scores: list[int] = field(default_factory=list)
    debug_prompt_data: Optional[dict] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)

    def touch(self):
        """Met a jour le timestamp d'activite."""
        self.last_activity = datetime.utcnow()

    def to_dict(self) -> dict:
        """Serialise l'etat pour la reponse API."""
        return {
            "id": self.id,
            "phase": self.phase,
            "chapter_id": self.chapter_id,
            "difficulty": self.difficulty,
            "ai_provider": self.ai_provider,
            "ocr_provider": self.ocr_provider,
            "format": self.format,
            "current_question": self.current_question,
            "current_exercise": self.current_exercise,
            "conversation_history": self.conversation_history,
            "question_validated": self.question_validated,
            "scores": self.scores,
        }


class SessionStore:
    """Store in-memory pour les sessions de kholle."""

    def __init__(self, ttl_hours: int = 2):
        self._sessions: dict[str, SessionState] = {}
        self._ttl = timedelta(hours=ttl_hours)

    def create(self) -> SessionState:
        """Cree une nouvelle session."""
        session = SessionState()
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> Optional[SessionState]:
        """Recupere une session par son ID."""
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if datetime.utcnow() - session.last_activity > self._ttl:
            del self._sessions[session_id]
            return None
        session.touch()
        return session

    def delete(self, session_id: str) -> bool:
        """Supprime une session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def cleanup_expired(self):
        """Supprime les sessions expirees."""
        now = datetime.utcnow()
        expired = [
            sid for sid, s in self._sessions.items()
            if now - s.last_activity > self._ttl
        ]
        for sid in expired:
            del self._sessions[sid]

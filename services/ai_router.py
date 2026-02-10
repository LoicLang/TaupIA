"""
Router pour les services AI (LLM et OCR).

Ce module est une façade qui délègue à application.ai_service
et application.container pour les appels LLM et OCR.
Supporte le changement dynamique de provider via session_state.
"""

from pathlib import Path
from typing import Optional

# Import du nouveau service
from application import ai_service

# Repertoire des prompts
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(name: str) -> str:
    """Charge un fichier prompt depuis prompts/."""
    return (_PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")

# Import pour Streamlit (lazy pour éviter import error si pas de streamlit)
_streamlit_initialized = False


def _init_streamlit_provider():
    """Configure le provider getter pour Streamlit."""
    global _streamlit_initialized
    if _streamlit_initialized:
        return

    try:
        import streamlit as st

        def get_provider_from_session() -> str:
            return st.session_state.get("ai_provider", "gemini")

        ai_service.set_provider_getter(get_provider_from_session)
        _streamlit_initialized = True
    except ImportError:
        # Streamlit pas disponible, utiliser le default
        pass


def get_ai_provider() -> str:
    """Retourne le provider AI choisi (claude ou gemini)."""
    _init_streamlit_provider()
    return ai_service.get_current_provider_name()


def get_available_providers() -> list[str]:
    """Retourne la liste des providers disponibles."""
    return ai_service.get_available_providers()


def evaluate_answer(
    question: str,
    expected: list[str],
    student_answer: str,
    common_errors: list[str] = None,
    follow_up_questions: list[str] = None,
    conversation_history: list[dict] = None,
    question_id: str = None,
    chapter_id: str = None,
) -> dict:
    """
    Route l'evaluation vers le provider configure.

    Utilise le knowledge graph pour construire le contexte structure
    (definitions/theoremes exacts + programme officiel).
    """
    _init_streamlit_provider()

    # Construire le contexte via le knowledge graph
    if question_id and chapter_id:
        from services.knowledge_service import get_structured_context
        context = get_structured_context(question_id, chapter_id, max_chars=4000)
    else:
        context = ""

    result = ai_service.evaluate_answer(
        question=question,
        expected=expected,
        student_answer=student_answer,
        rag_context=context,
        common_errors=common_errors,
        follow_up_questions=follow_up_questions,
        conversation_history=conversation_history,
    )

    # Ajouter les prompts pour le mode debug
    try:
        result["_debug_system_prompt"] = _load_prompt("kholleur_system")
        template = _load_prompt("evaluation")
        result["_debug_user_prompt"] = template.format(
            question=question,
            expected_points=chr(10).join("- " + e for e in expected),
            common_errors=chr(10).join("- " + e for e in (common_errors or [])) or "Aucune erreur specifique.",
            rag_context=context,
            student_answer=student_answer,
        )
    except Exception:
        result["_debug_system_prompt"] = ""
        result["_debug_user_prompt"] = ""

    return result


def guide_exercise(
    exercise_statement: str,
    student_message: str,
    hints: str = "",
    solution: str = "",
    conversation_history: list[dict] = None,
) -> str:
    """
    Route le guidage d'exercice vers le provider configuré.
    """
    _init_streamlit_provider()
    return ai_service.guide_exercise(
        exercise_statement=exercise_statement,
        student_message=student_message,
        hints=hints,
        solution=solution,
        conversation_history=conversation_history,
    )


def chat(
    user_message: str,
    context: str = "",
    conversation_history: list[dict] = None,
) -> str:
    """
    Route le chat libre vers le provider configuré.
    """
    _init_streamlit_provider()
    return ai_service.chat(
        user_message=user_message,
        context=context,
        conversation_history=conversation_history,
    )


# =============================================================================
# OCR - Utilise le provider configuré (modulaire)
# =============================================================================


def get_ocr_provider_name() -> str:
    """Retourne le nom du provider OCR actuellement configuré."""
    try:
        import streamlit as st
        return st.session_state.get("ocr_provider", "gemini")
    except ImportError:
        from application.container import get_container
        return get_container().settings.ocr_provider


def get_available_ocr_providers() -> list[str]:
    """Retourne la liste des providers OCR disponibles."""
    from application.container import get_container
    return get_container().get_available_ocr_providers()


def transcribe_image(image_data: bytes, mime_type: str = "image/jpeg") -> str:
    """
    Transcrit une image via le provider OCR configuré.

    Le provider est déterminé par session_state.ocr_provider ou settings.
    """
    from application.container import get_container

    # Récupérer le provider OCR configuré
    provider_name = get_ocr_provider_name()
    container = get_container()
    ocr_provider = container.get_ocr_provider(provider_name)

    return ocr_provider.transcribe(image_data, mime_type)

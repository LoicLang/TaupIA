"""
Endpoints kholle : start, answer, next-exercise, exercise/message, finish.
"""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from application import ai_service
from application.settings import get_settings
from application.container import Container
from services.knowledge_service import KnowledgeService
from core.tools.executor import ToolExecutor
from backend.auth import get_current_user_optional
from backend.provider_policy import effective_llm_provider, effective_ocr_provider
from backend.session_store import SessionState
from backend.dependencies import (
    get_knowledge_service,
    get_di_container,
    get_session,
)
from backend.schemas.session import (
    StartKholleRequest,
    StartKholleResponse,
    AnswerRequest,
    AnswerResponse,
    ExerciseMessageRequest,
    ExerciseMessageResponse,
    NextExerciseResponse,
    SkipResponse,
    FinishResponse,
)

router = APIRouter(tags=["kholle"])

_PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


def _load_prompt(name: str) -> str:
    return (_PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")


def _get_tool_executor(ks: KnowledgeService) -> ToolExecutor:
    """Create a tool executor bound to the knowledge service."""
    return ToolExecutor(ks)


# =========================================================================
# POST /api/sessions/{session_id}/start
# =========================================================================

@router.post(
    "/sessions/{session_id}/start",
    response_model=StartKholleResponse,
)
async def start_kholle(
    session_id: str,
    req: StartKholleRequest,
    session: SessionState = Depends(get_session),
    ks: KnowledgeService = Depends(get_knowledge_service),
    container: Container = Depends(get_di_container),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Demarre une kholle : configure la session et tire une question ou un exercice."""
    settings = get_settings()

    try:
        session.ai_provider = effective_llm_provider(
            requested_provider=req.ai_provider,
            container=container,
            settings=settings,
            user_payload=current_user,
        )
        session.ocr_provider = effective_ocr_provider(
            requested_provider=req.ocr_provider,
            container=container,
            settings=settings,
            user_payload=current_user,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    session.chapter_id = req.chapter_id
    session.difficulty = req.difficulty
    session.format = req.format

    # Configurer le provider getter pour cette requete
    ai_service.set_provider_getter(lambda: session.ai_provider)

    if req.format == "exercise_only":
        # Mode exercice seul : on passe directement a un exercice
        exercise = ks.get_exercise_by_difficulty(
            chapter_id=session.chapter_id,
            difficulty=session.difficulty,
            exclude_ids=session.done_exercises,
        )
        if not exercise:
            raise HTTPException(
                status_code=404,
                detail="Aucun exercice disponible pour ce chapitre et cette difficulte.",
            )
        session.current_exercise = exercise
        session.done_exercises.append(exercise["id"])
        session.phase = "exercice"
        session.conversation_history = []
        return StartKholleResponse(phase="exercice", exercise=exercise)

    # Mode complet : question de cours + exercice
    question = ks.get_random_question(
        chapter_id=session.chapter_id,
        difficulty=session.difficulty,
        exclude_ids=session.asked_questions,
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Plus de questions disponibles pour ce chapitre et cette difficulte.",
        )

    session.current_question = question
    session.asked_questions.append(question["id"])
    session.phase = "question_cours"
    session.conversation_history = []
    session.question_validated = False

    return StartKholleResponse(phase=session.phase, question=question)


# =========================================================================
# POST /api/sessions/{session_id}/answer
# =========================================================================

@router.post(
    "/sessions/{session_id}/answer",
    response_model=AnswerResponse,
)
async def submit_answer(
    session_id: str,
    req: AnswerRequest,
    session: SessionState = Depends(get_session),
    ks: KnowledgeService = Depends(get_knowledge_service),
):
    """Soumet une reponse a la question en cours et recoit l'evaluation via agent."""
    if session.phase != "question_cours":
        raise HTTPException(status_code=400, detail="Pas en phase question")

    q = session.current_question
    if not q:
        raise HTTPException(status_code=400, detail="Aucune question en cours")

    # Configurer le provider getter
    ai_service.set_provider_getter(lambda: session.ai_provider)

    # Ajouter la reponse a l'historique
    session.conversation_history.append({
        "role": "user",
        "content": req.answer,
    })

    # Build agent system prompt with evaluation context
    system_prompt = _load_prompt("kholleur_system")
    answer_latex = q.get("answer_latex", "")

    # Inject evaluation instructions into the agent prompt
    eval_context = f"""
## Contexte de cette evaluation
Question posee : {q["question_raw"]}
Reponse de reference : {answer_latex or "Non disponible."}

## Instructions
Evalue la reponse de l'etudiant. Tu peux utiliser tes outils pour verifier les definitions
et theoremes exacts. A la fin de ta reponse, indique sur des lignes separees :
SCORE: X/100
COMPLET: OUI/NON
MANQUE: liste des points manquants (ou "rien")
"""
    full_system_prompt = system_prompt + "\n\n" + eval_context

    # Create tool executor
    tool_executor = _get_tool_executor(ks)

    try:
        response_text = ai_service.agent_respond(
            user_message=req.answer,
            system_prompt=full_system_prompt,
            tool_executor=tool_executor.execute,
            conversation_history=session.conversation_history[:-1],
            temperature=0.7,
        )
    except Exception as e:
        session.conversation_history.pop()
        raise HTTPException(status_code=500, detail=f"Erreur LLM: {e}")

    if not response_text or not response_text.strip():
        session.conversation_history.pop()
        raise HTTPException(status_code=500, detail="Aucune reponse generee par le LLM")

    # Parse the evaluation from the agent's response
    from infrastructure.llm.base import BaseLLMProvider
    result = BaseLLMProvider._parse_evaluation_response(None, response_text)

    feedback = result.feedback
    session.conversation_history.append({
        "role": "assistant",
        "content": feedback,
    })

    score = result.score.value
    session.scores.append(score)

    is_complete = result.is_complete
    question_validated = is_complete and score >= 75
    if question_validated:
        session.question_validated = True

    # Debug data
    debug_data = {
        "system_prompt": full_system_prompt,
        "mode": "agent",
    }
    session.debug_prompt_data = debug_data

    return AnswerResponse(
        feedback=feedback,
        is_complete=is_complete,
        score=score,
        missing_points=result.missing_points,
        question_validated=session.question_validated,
        conversation_history=session.conversation_history,
        debug_prompt_data=debug_data,
    )


# =========================================================================
# POST /api/sessions/{session_id}/force-validate
# =========================================================================

@router.post("/sessions/{session_id}/force-validate")
async def force_validate(
    session_id: str,
    session: SessionState = Depends(get_session),
):
    """Force la validation de la question (bypass auto-validation)."""
    if session.phase != "question_cours":
        raise HTTPException(status_code=400, detail="Pas en phase question")
    session.question_validated = True
    return {"question_validated": True}


# =========================================================================
# POST /api/sessions/{session_id}/next-exercise
# =========================================================================

@router.post(
    "/sessions/{session_id}/next-exercise",
    response_model=NextExerciseResponse,
)
async def next_exercise(
    session_id: str,
    session: SessionState = Depends(get_session),
    ks: KnowledgeService = Depends(get_knowledge_service),
):
    """Passe a la phase exercice. Trouve un exercice testant les memes concepts."""
    q = session.current_question
    exercise = None

    # Matching par concepts si une question a ete posee
    if q and q.get("id"):
        concepts = ks.get_concepts_for_question(q["id"])
        concept_ids = [c["id"] for c in concepts]
        if concept_ids:
            exercise = ks.get_exercise_for_concepts(
                concept_ids=concept_ids,
                difficulty=session.difficulty,
                chapter_id=session.chapter_id,
                exclude_ids=session.done_exercises,
            )

    # Fallback sur chapitre + difficulte
    if not exercise:
        exercise = ks.get_exercise_by_difficulty(
            chapter_id=session.chapter_id,
            difficulty=session.difficulty,
            exclude_ids=session.done_exercises,
        )

    if exercise:
        session.current_exercise = exercise
        session.done_exercises.append(exercise["id"])
        session.phase = "exercice"
        session.conversation_history = []
        return NextExerciseResponse(phase="exercice", exercise=exercise)
    else:
        session.phase = "finished"
        return NextExerciseResponse(phase="finished", exercise=None)


# =========================================================================
# POST /api/sessions/{session_id}/exercise/message
# =========================================================================

@router.post(
    "/sessions/{session_id}/exercise/message",
    response_model=ExerciseMessageResponse,
)
async def exercise_message(
    session_id: str,
    req: ExerciseMessageRequest,
    session: SessionState = Depends(get_session),
    ks: KnowledgeService = Depends(get_knowledge_service),
):
    """Envoie un message pendant la phase exercice (guidage socratique via agent)."""
    if session.phase != "exercice":
        raise HTTPException(status_code=400, detail="Pas en phase exercice")

    ex = session.current_exercise
    if not ex:
        raise HTTPException(status_code=400, detail="Aucun exercice en cours")

    # Configurer le provider getter
    ai_service.set_provider_getter(lambda: session.ai_provider)

    # Ajouter le message a l'historique
    session.conversation_history.append({
        "role": "user",
        "content": req.message,
    })

    # Build agent system prompt with exercise context
    system_prompt = _load_prompt("kholleur_system")
    exercise_context = f"""
## Contexte de cet exercice
Enonce : {ex.get("enonce", "")}

## Indices disponibles (a distiller progressivement, NE PAS tout donner)
{ex.get("indications", "Aucun indice specifique.")}

## Solution de reference (NE JAMAIS donner directement)
{ex.get("correction", "Non disponible.")}

## Instructions
Guide l'etudiant sans donner la solution. Tu peux utiliser tes outils pour
consulter les definitions et theoremes pertinents quand l'etudiant est bloque.
Pose des questions pour le faire reflechir. Si l'etudiant est bloque,
cherche les prerequis du concept concerne pour identifier ce qui lui manque.
"""
    full_system_prompt = system_prompt + "\n\n" + exercise_context

    # Create tool executor
    tool_executor = _get_tool_executor(ks)

    try:
        guidance = ai_service.agent_respond(
            user_message=req.message,
            system_prompt=full_system_prompt,
            tool_executor=tool_executor.execute,
            conversation_history=session.conversation_history[:-1],
            temperature=0.8,
        )
    except Exception as e:
        session.conversation_history.pop()
        raise HTTPException(status_code=500, detail=f"Erreur LLM: {e}")

    session.conversation_history.append({
        "role": "assistant",
        "content": guidance,
    })

    return ExerciseMessageResponse(
        guidance=guidance,
        conversation_history=session.conversation_history,
    )


# =========================================================================
# POST /api/sessions/{session_id}/finish
# =========================================================================

@router.post(
    "/sessions/{session_id}/finish",
    response_model=FinishResponse,
)
async def finish_kholle(
    session_id: str,
    session: SessionState = Depends(get_session),
):
    """Termine la kholle et retourne les resultats."""
    session.phase = "finished"

    scores = session.scores
    avg = sum(scores) / len(scores) if scores else 0

    return FinishResponse(
        phase="finished",
        scores=scores,
        average_score=round(avg, 1),
        question_count=len(session.asked_questions),
        exercise_count=len(session.done_exercises),
    )


# =========================================================================
# POST /api/sessions/{session_id}/skip
# =========================================================================

@router.post(
    "/sessions/{session_id}/skip",
    response_model=SkipResponse,
)
async def skip_current(
    session_id: str,
    session: SessionState = Depends(get_session),
    ks: KnowledgeService = Depends(get_knowledge_service),
):
    """Passe a un nouveau contenu (question ou exercice) dans la meme phase."""
    if session.phase == "question_cours":
        question = ks.get_random_question(
            chapter_id=session.chapter_id,
            difficulty=session.difficulty,
            exclude_ids=session.asked_questions,
        )
        if not question:
            session.phase = "finished"
            return SkipResponse(phase="finished")
        session.current_question = question
        session.asked_questions.append(question["id"])
        session.conversation_history = []
        session.question_validated = False
        return SkipResponse(phase="question_cours", question=question)

    elif session.phase == "exercice":
        exercise = ks.get_exercise_by_difficulty(
            chapter_id=session.chapter_id,
            difficulty=session.difficulty,
            exclude_ids=session.done_exercises,
        )
        if not exercise:
            session.phase = "finished"
            return SkipResponse(phase="finished")
        session.current_exercise = exercise
        session.done_exercises.append(exercise["id"])
        session.conversation_history = []
        return SkipResponse(phase="exercice", exercise=exercise)

    else:
        raise HTTPException(
            status_code=400,
            detail="Impossible de passer dans cette phase.",
        )

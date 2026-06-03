"""Schemas Pydantic pour les sessions et kholles."""

from pydantic import BaseModel
from typing import Optional


class SessionResponse(BaseModel):
    id: str
    phase: str
    chapter_id: Optional[str] = None
    difficulty: int = 3
    ai_provider: str = "kimi"
    ocr_provider: str = "kimi"
    format: str = "full"
    current_question: Optional[dict] = None
    current_exercise: Optional[dict] = None
    conversation_history: list[dict] = []
    question_validated: bool = False
    scores: list[int] = []


class StartKholleRequest(BaseModel):
    chapter_id: str
    difficulty: int = 3
    ai_provider: str = "kimi"
    ocr_provider: str = "kimi"
    format: str = "full"  # "full" ou "exercise_only"


class StartKholleResponse(BaseModel):
    phase: str
    question: Optional[dict] = None
    exercise: Optional[dict] = None


class AnswerRequest(BaseModel):
    answer: str


class AnswerResponse(BaseModel):
    feedback: str
    is_complete: bool
    score: int
    missing_points: list[str]
    question_validated: bool
    conversation_history: list[dict]
    debug_prompt_data: Optional[dict] = None


class ExerciseMessageRequest(BaseModel):
    message: str


class ExerciseMessageResponse(BaseModel):
    guidance: str
    conversation_history: list[dict]
    # Set when the agent switched the exercise mid-conversation (deviation).
    exercise: Optional[dict] = None


class NextExerciseResponse(BaseModel):
    phase: str
    exercise: Optional[dict] = None


class SkipResponse(BaseModel):
    phase: str
    question: Optional[dict] = None
    exercise: Optional[dict] = None


class FinishResponse(BaseModel):
    phase: str
    scores: list[int]
    average_score: float
    question_count: int
    exercise_count: int

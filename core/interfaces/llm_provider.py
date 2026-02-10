"""LLM Provider interface."""

from typing import Protocol, Optional
from core.entities import EvaluationResult, Message


class LLMProvider(Protocol):
    """Interface for LLM providers (Gemini, Claude, DeepSeek, Kimi)."""

    @property
    def name(self) -> str:
        """Provider name for display."""
        ...

    @property
    def model_name(self) -> str:
        """Model identifier."""
        ...

    def evaluate(
        self,
        question: str,
        expected_answers: list[str],
        student_answer: str,
        rag_context: str,
        conversation_history: Optional[list[dict]] = None,
        common_errors: Optional[list[str]] = None,
    ) -> EvaluationResult:
        """
        Evaluate a student's answer to a course question.

        Args:
            question: The question asked
            expected_answers: List of expected points in the answer
            student_answer: Student's response
            rag_context: RAG context from course materials
            conversation_history: Previous messages
            common_errors: Common mistakes to watch for

        Returns:
            EvaluationResult with feedback, score, and completion status
        """
        ...

    def guide(
        self,
        exercise_statement: str,
        student_message: str,
        hints: str,
        solution: str,
        conversation_history: Optional[list[dict]] = None,
    ) -> str:
        """
        Guide a student through an exercise using Socratic method.

        Args:
            exercise_statement: The exercise problem
            student_message: Student's question or attempt
            hints: Available hints (to give progressively)
            solution: Reference solution (never to be given directly)
            conversation_history: Previous messages

        Returns:
            Guidance response (questions, not answers)
        """
        ...

    def chat(
        self,
        user_message: str,
        context: str = "",
        conversation_history: Optional[list[dict]] = None,
    ) -> str:
        """
        Free-form chat with the kholleur.

        Args:
            user_message: User's message
            context: Optional context
            conversation_history: Previous messages

        Returns:
            Assistant response
        """
        ...

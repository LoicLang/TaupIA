"""
AI Service - Facade for LLM operations.

This module provides a clean interface to AI capabilities,
abstracting away provider selection and dependency injection.
"""

from typing import Optional, Callable

from core.entities import EvaluationResult
from core.interfaces import LLMProvider
from core.tools.definitions import get_tool_definitions
from application.container import get_container


# Provider getter function - can be overridden per request/session context
_provider_getter: Optional[Callable[[], str]] = None


def set_provider_getter(getter: Callable[[], str]):
    """
    Set a custom function to get the current provider name.

    This allows callers to inject request/session-based provider selection.

    Args:
        getter: Function that returns the current provider name
    """
    global _provider_getter
    _provider_getter = getter


def get_current_provider_name() -> str:
    """Get the current provider name."""
    if _provider_getter is not None:
        return _provider_getter()
    return get_container().settings.default_llm_provider


def get_provider() -> LLMProvider:
    """Get the current LLM provider based on configuration."""
    provider_name = get_current_provider_name()
    return get_container().get_llm_provider(provider_name)


def get_available_providers() -> list[str]:
    """Get list of available (configured) LLM providers."""
    return get_container().get_available_providers()


def evaluate_answer(
    question: str,
    expected: list[str],
    student_answer: str,
    rag_context: str,
    common_errors: Optional[list[str]] = None,
    follow_up_questions: Optional[list[str]] = None,
    conversation_history: Optional[list[dict]] = None,
) -> dict:
    """
    Evaluate a student's answer using the configured LLM provider.

    Args:
        question: The question asked
        expected: List of expected points in the answer
        student_answer: Student's response
        rag_context: RAG context from course materials
        common_errors: Common mistakes to watch for
        follow_up_questions: Possible follow-up questions (unused currently)
        conversation_history: Previous messages

    Returns:
        dict with feedback, is_complete, missing_points, score
    """
    provider = get_provider()
    result = provider.evaluate(
        question=question,
        expected_answers=expected,
        student_answer=student_answer,
        rag_context=rag_context,
        conversation_history=conversation_history,
        common_errors=common_errors,
    )
    return result.to_dict()


def guide_exercise(
    exercise_statement: str,
    student_message: str,
    context: str = "",
    hints: str = "",
    solution: str = "",
    conversation_history: Optional[list[dict]] = None,
) -> str:
    """
    Guide a student through an exercise using Socratic method.

    Args:
        exercise_statement: The exercise problem
        student_message: Student's question or attempt
        context: Structured context for the exercise
        hints: Available hints
        solution: Reference solution
        conversation_history: Previous messages

    Returns:
        Guidance response
    """
    provider = get_provider()
    return provider.guide(
        exercise_statement=exercise_statement,
        student_message=student_message,
        context=context,
        hints=hints,
        solution=solution,
        conversation_history=conversation_history,
    )


def chat(
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
    provider = get_provider()
    return provider.chat(
        user_message=user_message,
        context=context,
        conversation_history=conversation_history,
    )


def agent_respond(
    user_message: str,
    system_prompt: str,
    tool_executor: Callable[[str, dict], str],
    conversation_history: Optional[list[dict]] = None,
    temperature: float = 0.7,
    include_actions: bool = False,
) -> str:
    """
    Run an agent turn with knowledge graph tool calling.

    The agent dynamically queries the knowledge graph as needed,
    then produces a response to the student.

    Args:
        user_message: Student's message
        system_prompt: System prompt (kholleur + tool instructions)
        tool_executor: Function to execute tool calls
        conversation_history: Previous messages
        temperature: Sampling temperature

    Returns:
        Agent's text response
    """
    provider = get_provider()
    tools = get_tool_definitions(include_actions=include_actions)
    return provider.run_agent_turn(
        user_message=user_message,
        system_prompt=system_prompt,
        tools=tools,
        tool_executor=tool_executor,
        conversation_history=conversation_history,
        temperature=temperature,
    )

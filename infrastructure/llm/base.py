"""
Base LLM Provider with shared retry logic.

This module provides common functionality for all LLM providers,
including retry logic with exponential backoff and response parsing.
"""

import time
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from pathlib import Path

from core.entities import EvaluationResult, Score


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers with shared functionality."""

    def __init__(
        self,
        model_name: str,
        max_retries: int = 3,
        initial_delay: float = 2.0,
        max_output_tokens: int = 4096,
        prompts_dir: Optional[Path] = None,
    ):
        """
        Initialize the base provider.

        Args:
            model_name: Model identifier
            max_retries: Maximum retry attempts
            initial_delay: Initial delay in seconds for retry
            max_output_tokens: Maximum output tokens
            prompts_dir: Directory containing prompt files
        """
        self._model_name = model_name
        self._max_retries = max_retries
        self._initial_delay = initial_delay
        self._max_output_tokens = max_output_tokens
        self._prompts_dir = prompts_dir or Path(__file__).parent.parent.parent / "prompts"
        self._client = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name for display."""
        ...

    @property
    def model_name(self) -> str:
        """Model identifier."""
        return self._model_name

    @abstractmethod
    def _init_client(self) -> Any:
        """Initialize the API client. Called lazily."""
        ...

    @abstractmethod
    def _call_api(
        self,
        messages: list[dict],
        system_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Make the actual API call.

        Args:
            messages: List of conversation messages
            system_prompt: System prompt to use
            temperature: Sampling temperature

        Returns:
            Text response from the model
        """
        ...

    def _get_client(self) -> Any:
        """Get or initialize the API client."""
        if self._client is None:
            self._client = self._init_client()
        return self._client

    def _load_prompt(self, prompt_name: str) -> str:
        """Load a prompt from file."""
        prompt_file = self._prompts_dir / f"{prompt_name}.txt"
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    def _call_with_retry(
        self,
        func: Callable[[], str],
        retryable_errors: tuple[str, ...] = ("503", "500", "overloaded", "rate_limit"),
    ) -> str:
        """
        Call a function with retry and exponential backoff.

        Args:
            func: Function to call (should return response text)
            retryable_errors: Error substrings that should trigger retry

        Returns:
            Response text from the successful call

        Raises:
            Exception: If all retries fail
        """
        delay = self._initial_delay
        last_exception = None

        for attempt in range(self._max_retries):
            try:
                response = func()

                # Check for empty response
                if not response or not response.strip():
                    if attempt < self._max_retries - 1:
                        print(f"[{self.name}] Réponse vide, nouvelle tentative dans {delay}s...")
                        time.sleep(delay)
                        delay *= 2
                        continue
                    else:
                        raise Exception("Réponse vide après plusieurs tentatives.")

                return response

            except Exception as e:
                last_exception = e
                error_str = str(e).lower()

                # Check if error is retryable
                is_retryable = any(err in error_str for err in retryable_errors)

                if is_retryable and attempt < self._max_retries - 1:
                    print(f"[{self.name}] Erreur, nouvelle tentative dans {delay}s... ({attempt + 1}/{self._max_retries})")
                    time.sleep(delay)
                    delay *= 2
                    continue
                elif is_retryable:
                    raise Exception(
                        f"{self.name} a rencontré des erreurs après {self._max_retries} tentatives. "
                        f"Réessaie dans quelques minutes."
                    ) from e
                else:
                    raise e

        raise last_exception

    def _truncate_history(
        self,
        conversation_history: Optional[list[dict]],
        max_chars: int = 4000,
        max_messages: int = 20,
    ) -> list[dict]:
        """
        Truncate conversation history to fit within limits.

        Args:
            conversation_history: Full conversation history
            max_chars: Maximum total characters
            max_messages: Maximum number of messages

        Returns:
            Truncated history (most recent messages that fit)
        """
        if not conversation_history:
            return []

        # Take most recent messages
        recent = conversation_history[-max_messages:]

        # Truncate by character count (from most recent)
        total_chars = 0
        result = []
        for msg in reversed(recent):
            msg_length = len(msg.get("content", ""))
            if total_chars + msg_length > max_chars:
                break
            result.insert(0, msg)
            total_chars += msg_length

        return result

    def _parse_evaluation_response(self, text: str) -> EvaluationResult:
        """
        Parse the evaluation response to extract score, completion status, and missing points.

        Args:
            text: Raw response text from the model

        Returns:
            EvaluationResult with parsed values
        """
        score = 50
        is_complete = False
        missing_points = []
        feedback = text

        lines = text.strip().split("\n")
        for line in lines[-10:]:  # Look in last lines
            # Clean markdown formatting for parsing
            line_clean = line.replace("**", "").strip()
            line_upper = line_clean.upper()

            if "SCORE:" in line_upper or "SCORE :" in line_upper:
                try:
                    parts = line_clean.split(":", 1)[1] if ":" in line_clean else line_clean.split()[-1]
                    score = int(parts.strip().split("/")[0].split()[0])
                    feedback = feedback.replace(line, "").strip()
                except Exception:
                    pass

            elif "COMPLET:" in line_upper or "COMPLET :" in line_upper:
                is_complete = "OUI" in line_upper or "YES" in line_upper
                feedback = feedback.replace(line, "").strip()

            elif "MANQUE:" in line_upper or "MANQUE :" in line_upper:
                try:
                    missing = line_clean.split(":", 1)[1].strip()
                    if missing.lower() not in ["rien", "nothing", "none"]:
                        missing_points = [m.strip() for m in missing.split(",")]
                    feedback = feedback.replace(line, "").strip()
                except Exception:
                    pass

        return EvaluationResult(
            feedback=feedback.strip(),
            is_complete=is_complete,
            score=Score(score),
            missing_points=missing_points,
        )

    def _build_evaluation_prompt(
        self,
        question: str,
        expected_answers: list[str],
        student_answer: str,
        rag_context: str,
        common_errors: Optional[list[str]] = None,
    ) -> str:
        """Build the evaluation prompt."""
        # V3: expected_answers contient la reponse de reference en LaTeX
        reference_answer = chr(10).join(expected_answers) if expected_answers else "Non disponible."
        try:
            template = self._load_prompt("evaluation")
            return template.format(
                question=question,
                reference_answer=reference_answer,
                rag_context=rag_context,
                student_answer=student_answer,
            )
        except FileNotFoundError:
            return f"""## Question posée
{question}

## Réponse de référence (définition/théorème/démonstration attendue)
{reference_answer}

## Référentiel mathématique (définitions et théorèmes exacts)
{rag_context}

## Réponse de l'étudiant
{student_answer}

---

Évalue cette réponse. Donne un feedback constructif en suivant ton rôle de khôlleur.
Compare la réponse de l'étudiant avec la réponse de référence ci-dessus.
À la fin, indique sur une ligne séparée :
- SCORE: X/100 (estimation)
- COMPLET: OUI/NON
- MANQUE: liste des points manquants séparés par des virgules (ou "rien" si complet)"""

    def _build_exercise_prompt(
        self,
        exercise_statement: str,
        student_message: str,
        hints: str,
        solution: str,
    ) -> str:
        """Build the exercise guidance prompt."""
        try:
            template = self._load_prompt("exercise_guide")
            return template.format(
                exercise_statement=exercise_statement,
                hints=hints or "Aucun indice spécifique.",
                solution=solution or "Non disponible.",
                student_message=student_message,
            )
        except FileNotFoundError:
            # Fallback to inline prompt
            return f"""## Exercice
{exercise_statement}

## Indices disponibles (à distiller progressivement)
{hints if hints else "Aucun indice spécifique."}

## Solution de référence (NE PAS DONNER, juste pour vérifier)
{solution if solution else "Non disponible."}

## Message de l'étudiant
{student_message}

---

Guide l'étudiant sans donner la solution. Pose des questions pour le faire réfléchir.
Si l'étudiant est bloqué, donne UN indice parmi ceux disponibles."""

    def _get_system_prompt(self) -> str:
        """Get the kholleur system prompt."""
        try:
            return self._load_prompt("kholleur_system")
        except FileNotFoundError:
            raise FileNotFoundError(
                "System prompt 'kholleur_system.txt' not found in prompts directory. "
                "Please ensure prompts are properly set up."
            )

    def evaluate(
        self,
        question: str,
        expected_answers: list[str],
        student_answer: str,
        rag_context: str,
        conversation_history: Optional[list[dict]] = None,
        common_errors: Optional[list[str]] = None,
    ) -> EvaluationResult:
        """Evaluate a student's answer to a course question."""
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_evaluation_prompt(
            question=question,
            expected_answers=expected_answers,
            student_answer=student_answer,
            rag_context=rag_context,
            common_errors=common_errors,
        )

        # Build messages with truncated history
        messages = self._truncate_history(conversation_history, max_chars=4000, max_messages=20)
        messages.append({"role": "user", "content": user_prompt})

        def _call() -> str:
            return self._call_api(messages, system_prompt, temperature=0.7)

        try:
            response_text = self._call_with_retry(_call)
            return self._parse_evaluation_response(response_text)
        except Exception as e:
            return EvaluationResult(
                feedback=f"Désolé, je n'ai pas pu générer de réponse ({e}). Peux-tu reformuler ta réponse ?",
                is_complete=False,
                score=Score(0),
                missing_points=[],
            )

    def guide(
        self,
        exercise_statement: str,
        student_message: str,
        hints: str = "",
        solution: str = "",
        conversation_history: Optional[list[dict]] = None,
    ) -> str:
        """Guide a student through an exercise using Socratic method."""
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_exercise_prompt(
            exercise_statement=exercise_statement,
            student_message=student_message,
            hints=hints,
            solution=solution,
        )

        # Build messages with truncated history
        messages = self._truncate_history(conversation_history, max_chars=6000, max_messages=30)
        messages.append({"role": "user", "content": user_prompt})

        def _call() -> str:
            return self._call_api(messages, system_prompt, temperature=0.8)

        try:
            return self._call_with_retry(_call)
        except Exception as e:
            return f"Désolé, je n'ai pas pu générer de réponse ({e}). Peux-tu reformuler ta question ?"

    def chat(
        self,
        user_message: str,
        context: str = "",
        conversation_history: Optional[list[dict]] = None,
    ) -> str:
        """Free-form chat with the kholleur."""
        system_prompt = self._get_system_prompt()
        prompt = user_message
        if context:
            prompt = f"Contexte: {context}\n\n{user_message}"

        # Build messages with truncated history
        messages = self._truncate_history(conversation_history, max_chars=6000, max_messages=30)
        messages.append({"role": "user", "content": prompt})

        def _call() -> str:
            return self._call_api(messages, system_prompt, temperature=0.8)

        try:
            return self._call_with_retry(_call)
        except Exception as e:
            return f"Désolé, je n'ai pas pu générer de réponse ({e}). Peux-tu reformuler ?"

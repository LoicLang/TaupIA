"""Question and Exercise domain entities."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chapter:
    """Represents a course chapter."""

    id: str
    title: str
    semestre: int
    importance: int = 1
    question_count: int = 0
    difficulties: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.difficulties:
            self.difficulties = []


@dataclass
class Question:
    """Represents a course question (question de cours)."""

    id: str
    question: str
    expected_answers: list[str]
    chapter_id: str
    chapter_title: str
    difficulty: int
    importance: int = 1
    common_errors: list[str] = field(default_factory=list)
    follow_up_questions: list[str] = field(default_factory=list)
    semestre: int = 1

    def __post_init__(self):
        if not self.common_errors:
            self.common_errors = []
        if not self.follow_up_questions:
            self.follow_up_questions = []


@dataclass
class Exercise:
    """Represents a math exercise."""

    id: str
    title: str
    statement: str
    chapter: str
    difficulty: int
    hints: str = ""
    solution: str = ""
    chapter_id: str = ""
    source: str = ""

    @classmethod
    def from_metadata(cls, doc_id: str, content: str, metadata: dict) -> "Exercise":
        """Create Exercise from ChromaDB document."""
        return cls(
            id=doc_id,
            title=metadata.get("title", "Exercice"),
            statement=content,
            chapter=metadata.get("chapter", ""),
            difficulty=metadata.get("difficulty", 2),
            hints=metadata.get("hints", ""),
            solution=metadata.get("solution", ""),
            chapter_id=metadata.get("chapter_id", ""),
            source=metadata.get("source", ""),
        )

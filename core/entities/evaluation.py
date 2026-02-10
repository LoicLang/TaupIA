"""Evaluation domain entities."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Score:
    """Represents an evaluation score."""

    value: int
    max_value: int = 100

    def __post_init__(self):
        self.value = max(0, min(self.value, self.max_value))

    @property
    def percentage(self) -> float:
        return (self.value / self.max_value) * 100

    @property
    def is_passing(self) -> bool:
        return self.value >= 60

    @property
    def is_good(self) -> bool:
        return self.value >= 75

    def __str__(self) -> str:
        return f"{self.value}/{self.max_value}"


@dataclass
class EvaluationResult:
    """Result of evaluating a student's answer."""

    feedback: str
    is_complete: bool
    score: Score
    missing_points: list[str] = field(default_factory=list)
    raw_response: str = ""

    def __post_init__(self):
        if not self.missing_points:
            self.missing_points = []
        if isinstance(self.score, int):
            self.score = Score(self.score)

    @classmethod
    def from_dict(cls, data: dict) -> "EvaluationResult":
        """Create from legacy dict format."""
        return cls(
            feedback=data.get("feedback", ""),
            is_complete=data.get("is_complete", False),
            score=Score(data.get("score", 0)),
            missing_points=data.get("missing_points", []),
        )

    def to_dict(self) -> dict:
        """Convert to legacy dict format for backward compatibility."""
        return {
            "feedback": self.feedback,
            "is_complete": self.is_complete,
            "score": self.score.value,
            "missing_points": self.missing_points,
        }

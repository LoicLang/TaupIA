"""Tests for core entities."""

import pytest
from core.entities import (
    Question,
    Exercise,
    Chapter,
    EvaluationResult,
    Score,
    Message,
    ConversationHistory,
)


class TestScore:
    def test_score_creation(self):
        score = Score(85)
        assert score.value == 85
        assert score.max_value == 100
        assert str(score) == "85/100"

    def test_score_clamping(self):
        assert Score(150).value == 100
        assert Score(-10).value == 0

    def test_score_properties(self):
        assert Score(75).is_passing
        assert Score(75).is_good
        assert not Score(50).is_passing
        assert Score(60).is_passing
        assert not Score(60).is_good


class TestEvaluationResult:
    def test_from_dict(self):
        data = {
            "feedback": "Bonne réponse",
            "is_complete": True,
            "score": 85,
            "missing_points": [],
        }
        result = EvaluationResult.from_dict(data)
        assert result.feedback == "Bonne réponse"
        assert result.is_complete
        assert result.score.value == 85

    def test_to_dict(self):
        result = EvaluationResult(
            feedback="Test",
            is_complete=True,
            score=Score(90),
            missing_points=["point1"],
        )
        d = result.to_dict()
        assert d["score"] == 90
        assert d["is_complete"]


class TestConversationHistory:
    def test_add_messages(self):
        history = ConversationHistory()
        history.add_user("Hello")
        history.add_assistant("Hi there")
        assert len(history) == 2
        assert history.messages[0].role == "user"
        assert history.messages[1].role == "assistant"

    def test_truncation(self):
        history = ConversationHistory(max_chars=50)
        history.add_user("A" * 30)
        history.add_user("B" * 30)
        history.add_user("C" * 30)

        truncated = history.get_truncated()
        total_chars = sum(len(m.content) for m in truncated)
        assert total_chars <= 50

    def test_to_dict_list(self):
        history = ConversationHistory()
        history.add_user("Test")
        dicts = history.to_dict_list()
        assert dicts == [{"role": "user", "content": "Test"}]


class TestQuestion:
    def test_question_creation(self):
        q = Question(
            id="q1",
            question="What is a group?",
            expected_answers=["A set with operation"],
            chapter_id="ch1",
            chapter_title="Groups",
            difficulty=2,
        )
        assert q.id == "q1"
        assert q.difficulty == 2
        assert q.common_errors == []


class TestExercise:
    def test_from_metadata(self):
        ex = Exercise.from_metadata(
            doc_id="ex1",
            content="Prove that...",
            metadata={
                "title": "Exercise 1",
                "chapter": "Algebra",
                "difficulty": 3,
            },
        )
        assert ex.id == "ex1"
        assert ex.statement == "Prove that..."
        assert ex.difficulty == 3


class TestChapter:
    def test_chapter_creation(self):
        ch = Chapter(
            id="ch1",
            title="Groups",
            semestre=1,
            importance=2,
        )
        assert ch.id == "ch1"
        assert ch.difficulties == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

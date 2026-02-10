"""Tests for knowledge service."""

import pytest
from pathlib import Path

from services.knowledge_service import KnowledgeService


class TestKnowledgeService:
    """Tests for KnowledgeService with real data."""

    @pytest.fixture(scope="class")
    def service(self):
        return KnowledgeService()

    def test_loads_data(self, service):
        """Test that all data files load correctly."""
        assert len(service._graph_nodes) > 0
        assert len(service._graph_edges) > 0
        assert len(service._raw_questions) > 0
        assert len(service._course_nodes_by_id) > 0
        assert len(service._td_exercises_by_id) > 0

    def test_get_chapters(self, service):
        """Test get_chapters returns chapters with questions and exercises."""
        chapters = service.get_chapters()
        assert len(chapters) > 0

        for ch in chapters:
            assert "id" in ch
            assert "title" in ch
            assert "semestre" in ch
            assert "importance" in ch
            assert "question_count" in ch
            assert ch["question_count"] > 0
            assert "difficulties" in ch
            assert len(ch["difficulties"]) > 0

    def test_get_chapters_sorted(self, service):
        """Test that chapters are sorted by semestre then title."""
        chapters = service.get_chapters()
        for i in range(len(chapters) - 1):
            assert (chapters[i]["semestre"], chapters[i]["title"]) <= (
                chapters[i + 1]["semestre"],
                chapters[i + 1]["title"],
            )

    def test_get_random_question(self, service):
        """Test getting a random question."""
        chapters = service.get_chapters()
        ch = chapters[0]
        q = service.get_random_question(ch["id"])

        assert q is not None
        assert "id" in q
        assert "question_raw" in q
        assert "chapter_id" in q
        assert "difficulty" in q
        assert "attendus_json" in q
        assert "erreurs_frequentes_json" in q
        assert "relances_prof_json" in q

    def test_get_random_question_exclude(self, service):
        """Test that exclude_ids works."""
        chapters = service.get_chapters()
        ch = chapters[0]

        # Get all question IDs for this chapter
        questions, _ = service._find_questions_for_chapter(ch["id"])
        all_ids = [q["id"] for q in questions]

        # Exclude all but potentially one
        q = service.get_random_question(ch["id"], exclude_ids=all_ids)
        assert q is None

    def test_get_exercise_by_difficulty(self, service):
        """Test getting an exercise by difficulty."""
        chapters = service.get_chapters()
        ch = chapters[0]
        ex = service.get_exercise_by_difficulty(ch["id"], difficulty=3)

        assert ex is not None
        assert "id" in ex
        assert "enonce" in ex
        assert "correction" in ex
        assert "chapter_id" in ex

    def test_get_concepts_for_question(self, service):
        """Test graph traversal from kholle to concepts."""
        # Find a question that has TESTS edges
        for q_id, concepts in service._kholle_to_concepts.items():
            if concepts:
                result = service.get_concepts_for_question(q_id)
                assert len(result) > 0
                for c in result:
                    assert "id" in c
                    assert "type" in c
                    assert "title" in c
                    assert "confidence" in c
                break

    def test_get_structured_context(self, service):
        """Test structured context generation."""
        # Find a question with concepts
        for q_id in service._kholle_to_concepts:
            concepts = service._kholle_to_concepts[q_id]
            if concepts:
                ch_id = service._concept_to_chapter.get(concepts[0][0], "")
                if ch_id:
                    context = service.get_structured_context(q_id, ch_id)
                    assert isinstance(context, str)
                    assert len(context) > 0
                    assert "Concepts testes" in context
                    break

    def test_get_collection_stats(self, service):
        """Test collection stats."""
        stats = service.get_collection_stats()
        assert "questions_cours" in stats
        assert "exercices" in stats
        assert "concepts" in stats
        assert stats["questions_cours"]["count"] > 0
        assert stats["exercices"]["count"] > 0

    def test_chapter_id_alias(self, service):
        """Test that chapter ID aliases work (EV -> EV_AL)."""
        canonical = service._normalize_chapter_id("EV")
        assert canonical == "EV_AL"
        # Non-aliased IDs pass through
        assert service._normalize_chapter_id("LOGIQUE_ENS") == "LOGIQUE_ENS"

    def test_get_programme_for_chapter(self, service):
        """Test programme data retrieval."""
        chapters = service.get_chapters()
        ch = chapters[0]
        prog = service.get_programme_for_chapter(ch["id"])
        assert "notions" in prog
        assert "prerequis" in prog
        assert "vigilance" in prog
        assert "capacites_exigibles" in prog

    def test_get_rag_context_by_question_id(self, service):
        """Test rag_context with question_id uses graph."""
        for q_id in service._kholle_to_concepts:
            result = service.get_rag_context("", question_id=q_id)
            assert isinstance(result, list)
            if result:
                assert "chunk_id" in result[0]
                assert "content" in result[0]
                assert "score" in result[0]
            break


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

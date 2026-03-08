"""Tests for knowledge service (V3 data format, 29 course chapters)."""

import pytest
from pathlib import Path

from services.knowledge_service import KnowledgeService


class TestKnowledgeService:
    """Tests for KnowledgeService with V3 data."""

    @pytest.fixture(scope="class")
    def service(self):
        return KnowledgeService()

    # =========================================================================
    # Data loading
    # =========================================================================

    def test_loads_data(self, service):
        """Test that all V3 data files load correctly."""
        assert len(service._graph_nodes) > 0
        assert len(service._graph_edges) > 0
        assert len(service._questions_by_course_chapter) > 0
        assert len(service._course_nodes_by_id) > 0
        assert len(service._td_exercises_by_id) > 0

    def test_v3_data_counts(self, service):
        """Test V3 data scale."""
        stats = service.get_collection_stats()
        assert stats["exercices"]["count"] >= 1500
        assert stats["concepts"]["count"] >= 1900

    def test_29_course_chapters_loaded(self, service):
        """Test that all 29 course chapters are loaded from cours/."""
        assert len(service._course_chapters) == 29

    def test_programme_to_course_mapping(self, service):
        """Test that programme-to-course chapter mapping is loaded."""
        assert len(service._prog_to_course_chapters) > 0
        assert len(service._course_to_prog) > 0

        for prog_id, course_ids in service._prog_to_course_chapters.items():
            assert len(course_ids) >= 1, f"{prog_id} has no linked course chapters"

        for course_id, prog_id in service._course_to_prog.items():
            assert course_id in service._prog_to_course_chapters[prog_id]

    def test_exercise_id_normalization(self, service):
        """Test that exercise chapter IDs are normalized to match cours IDs."""
        # These 3 exercises had different IDs, should be normalized
        for canonical_id in [
            "calculs_algebriques_dans_R",
            "representation_matricielle_applications_lineaires",
            "arithmetique_des_polynomes_et_fractions_rationnelles",
        ]:
            exercises = service._td_exercises_by_chapter.get(canonical_id, [])
            assert len(exercises) > 0, f"No exercises found for {canonical_id}"

    # =========================================================================
    # Chapters (29 course chapters user-facing)
    # =========================================================================

    def test_get_chapters_returns_29(self, service):
        """Test that get_chapters returns all 29 course chapters."""
        chapters = service.get_chapters()
        assert len(chapters) == 29

    def test_get_chapters_fields(self, service):
        """Test get_chapters returns chapters with all expected fields."""
        chapters = service.get_chapters()
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

    def test_chapter_ids_are_course_ids(self, service):
        """Test that chapter IDs are course chapter IDs (not programme IDs)."""
        chapters = service.get_chapters()
        course_ids = set(service._course_chapters.keys())
        for ch in chapters:
            assert ch["id"] in course_ids, f"{ch['id']} is not a course chapter ID"

    # =========================================================================
    # Questions
    # =========================================================================

    def test_get_random_question(self, service):
        """Test getting a random question (V3 fields)."""
        chapters = service.get_chapters()
        ch = chapters[0]
        q = service.get_random_question(ch["id"])

        assert q is not None
        assert "id" in q
        assert "question_raw" in q
        assert "chapter_id" in q
        assert "difficulty" in q
        assert "answer_latex" in q
        assert "answer_node_id" in q
        # Old V2 fields should NOT be present
        assert "attendus_json" not in q
        assert "erreurs_frequentes_json" not in q
        assert "relances_prof_json" not in q

    def test_get_random_question_exclude(self, service):
        """Test that exclude_ids works."""
        chapters = service.get_chapters()
        ch = chapters[0]

        questions = service._questions_by_course_chapter.get(ch["id"], [])
        all_ids = [q["id"] for q in questions]

        q = service.get_random_question(ch["id"], exclude_ids=all_ids)
        assert q is None

    def test_get_random_question_difficulty_filter(self, service):
        """Test difficulty filter on questions."""
        chapters = service.get_chapters()
        ch = chapters[0]
        q = service.get_random_question(ch["id"], difficulty=3)
        if q:
            assert abs(q["difficulty"] - 3) <= 1

    # =========================================================================
    # Exercises
    # =========================================================================

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

    def test_exercise_format_v3(self, service):
        """Test that V3 exercise formatting handles sub_questions."""
        chapters = service.get_chapters()
        ch = chapters[0]
        ex = service.get_exercise_by_difficulty(ch["id"], difficulty=3)

        assert ex is not None
        assert ex["enonce"].strip()
        assert isinstance(ex["indications"], str)
        assert isinstance(ex["correction"], str)

    def test_exercise_for_concepts(self, service):
        """Test concept-based exercise matching."""
        for q_id, concepts in service._kholle_to_concepts.items():
            if concepts:
                concept_ids = [c_id for c_id, _ in concepts]
                ex = service.get_exercise_for_concepts(concept_ids=concept_ids)
                if ex:
                    assert "id" in ex
                    assert "enonce" in ex
                    break

    # =========================================================================
    # Graph traversal
    # =========================================================================

    def test_get_concepts_for_question(self, service):
        """Test graph traversal from kholle to concepts."""
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
        for q_id in service._kholle_to_concepts:
            concepts = service._kholle_to_concepts[q_id]
            if concepts:
                # Use the course chapter ID directly
                ch_id = service._concept_to_chapter.get(concepts[0][0], "")
                if ch_id:
                    context = service.get_structured_context(q_id, ch_id)
                    assert isinstance(context, str)
                    assert len(context) > 0
                    assert "Concepts testes" in context
                    break

    # =========================================================================
    # Stats and programme
    # =========================================================================

    def test_get_collection_stats(self, service):
        """Test collection stats."""
        stats = service.get_collection_stats()
        assert "questions_cours" in stats
        assert "exercices" in stats
        assert "concepts" in stats
        assert stats["questions_cours"]["count"] > 0
        assert stats["exercices"]["count"] > 0

    def test_get_programme_for_chapter(self, service):
        """Test programme data retrieval for a course chapter."""
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

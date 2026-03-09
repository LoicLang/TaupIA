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
        assert stats["exercices"]["count"] >= 1490
        assert stats["exercices"]["invalid_count"] > 0
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

    def test_exercise_text_artifacts_are_normalized(self, service):
        """OCR/text artifacts should be normalized during loading."""
        raw = "Une borne \\u00e0 calculer et un r\\éel \\à fixer."
        assert service._normalize_text_artifacts(raw) == "Une borne à calculer et un réel à fixer."

    def test_placeholder_exercises_are_filtered_out(self, service):
        """Known placeholder exercises should not be served to users."""
        ex_id = "rappels_et_complements_sur_les_fonctions_reelles__ex_025"
        assert ex_id not in service._td_exercises_by_id
        assert "placeholder_tag" in service._invalid_exercises_by_id[ex_id]

    def test_self_confessed_invalid_exercises_are_filtered_out(self, service):
        """Exercises whose solutions admit an error should be excluded from selection."""
        ex_id = "matrices_et_systemes_lineaires__ex_002"
        assert ex_id not in service._td_exercises_by_id
        assert service._invalid_exercises_by_id[ex_id]

    def test_manually_blacklisted_exercises_are_filtered_out(self, service):
        """Manually reviewed low-quality exercises should not be served."""
        for ex_id in [
            "calculs_algebriques_dans_r__ex_007",
            "calculs_algebriques_dans_r__champo_024",
            "calculs_algebriques_dans_r__champo_025",
            "arithmetique_des_entiers__champo_028",
            "groupes_et_anneaux__ex_004",
            "derivabilite_et_convexite__ex_032",
            "determinants__ex_020",
            "groupes_et_anneaux__champo_017",
            "nombres_complexes__ex_020",
            "nombres_complexes__ex_028",
            "nombres_complexes__champo_029",
            "rappels_et_complements_sur_les_fonctions_reelles__champo_024",
            "rappels_et_complements_sur_les_fonctions_reelles__champo_025",
            "rappels_et_complements_sur_les_fonctions_reelles__champo_027",
            "rappels_et_complements_sur_les_fonctions_reelles__champo_030",
            "rappels_et_complements_sur_les_fonctions_reelles__champo_031",
            "relations_binaires_et_applications__champo_027",
        ]:
            assert ex_id not in service._td_exercises_by_id
            assert service._invalid_exercises_by_id[ex_id]

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

    def test_curated_question_bank_covers_all_course_chapters(self, service):
        """Each course chapter should have its own curated questions."""
        assert set(service._questions_by_course_chapter) == set(service._course_chapters)
        for course_id, questions in service._questions_by_course_chapter.items():
            assert len(questions) >= 6, f"{course_id} should expose at least 6 curated questions"
            for question in questions:
                assert question["id"].startswith(f"{course_id}__")

    def test_curated_questions_expose_structured_concepts(self, service):
        """Curated questions should provide exact linked concepts or a curated fallback."""
        exact_links = 0
        total = 0
        seen_ids = set()

        for questions in service._questions_by_course_chapter.values():
            for question in questions:
                if question["id"] in seen_ids:
                    continue
                seen_ids.add(question["id"])
                total += 1
                if question.get("tested_concept_ids"):
                    exact_links += 1
                concepts = service.get_concepts_for_question(question["id"])
                assert concepts, f"{question['id']} has no structured concept context"

        assert total == 176
        assert exact_links >= 90

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

    def test_exercise_format_deduplicates_repeated_main_statement(self, service):
        """A repeated statement should not appear twice in the final exercise text."""
        duplicate_exercise = None

        for raw_exercise in service._td_exercises_by_id.values():
            main_statement = (raw_exercise.get("statement_latex") or "").strip()
            if not main_statement:
                continue

            for sub_question in raw_exercise.get("sub_questions", []):
                label = (sub_question.get("label") or "").strip()
                stmt = (sub_question.get("statement_latex") or "").strip()
                if not label and stmt == main_statement:
                    duplicate_exercise = raw_exercise
                    break

            if duplicate_exercise:
                break

        assert duplicate_exercise is not None

        chapter_id = duplicate_exercise["_chapter_id"]
        chapter_title = service._course_chapters.get(chapter_id, {}).get("title", "")
        formatted = service._format_exercise(duplicate_exercise, chapter_title, chapter_id)
        repeated_statement = duplicate_exercise["statement_latex"].strip()

        assert formatted["enonce"].count(repeated_statement) == 1

    def test_exercise_format_numbers_unlabeled_sub_questions(self, service):
        """Multiple unlabeled sub-questions should be separated explicitly."""
        raw_exercise = {
            "id": "dummy_multi_subq",
            "difficulty": 2,
            "statement_latex": "Résoudre dans $\\mathbb{R}$.",
            "sub_questions": [
                {
                    "label": "",
                    "statement_latex": "Montrer que $f$ est injective.",
                    "solution_latex": "On raisonne par l'absurde.",
                    "hints": [{"level": 1, "content_latex": "Partir de $f(x)=f(y)$."}],
                },
                {
                    "label": "",
                    "statement_latex": "Calculer l'image de $f$.",
                    "solution_latex": "On explicite les valeurs atteintes.",
                    "hints": [{"level": 1, "content_latex": "Chercher un antécédent de $y$."}],
                },
            ],
            "hints": [],
            "global_solution_latex": "",
        }

        formatted = service._format_exercise(raw_exercise, "Test", "test")

        assert "**1.** Montrer que $f$ est injective." in formatted["enonce"]
        assert "**2.** Calculer l'image de $f$." in formatted["enonce"]
        assert "**1.** Montrer que $f$ est injective." in formatted["indications"]
        assert "**Indice 1.** Partir de $f(x)=f(y)$." in formatted["indications"]
        assert "**2.** Calculer l'image de $f$." in formatted["correction"]
        assert "On explicite les valeurs atteintes." in formatted["correction"]

    def test_exercise_format_splits_embedded_numbered_statement(self, service):
        """A main statement containing inline numbered parts should be separated."""
        raw_exercise = {
            "id": "dummy_embedded_numbering",
            "difficulty": 2,
            "statement_latex": (
                "Ordre d'un element : "
                "1. Montrer que $G=\\langle x \\rangle$. "
                "2. Calculer le cardinal de $\\langle a \\rangle$."
            ),
            "sub_questions": [],
            "hints": [],
            "global_solution_latex": "",
        }

        formatted = service._format_exercise(raw_exercise, "Test", "test")

        assert "Ordre d'un element :" in formatted["enonce"]
        assert "**1.** Montrer que $G=\\langle x \\rangle$." in formatted["enonce"]
        assert "**2.** Calculer le cardinal de $\\langle a \\rangle$." in formatted["enonce"]

    def test_exercise_format_preserves_multi_question_hint_structure(self, service):
        """Hints for multi-part exercises should stay attached to the right sub-question."""
        raw_exercise = service._td_exercises_by_id["analyse_asymptotique_de_niveau_1__ex_003"]
        chapter_id = raw_exercise["_chapter_id"]
        chapter_title = service._course_chapters[chapter_id]["title"]

        formatted = service._format_exercise(raw_exercise, chapter_title, chapter_id)

        assert "**1)** $(x\\mapsto e^{x}, x\\mapsto x e^{x}, x\\mapsto e^{x+x^{2}})$" in formatted["enonce"]
        assert "**1)** $(x\\mapsto e^{x}, x\\mapsto x e^{x}, x\\mapsto e^{x+x^{2}})$" in formatted["indications"]
        assert "**Indice 1.** Écrire une combinaison linéaire nulle" in formatted["indications"]
        assert "**2)** $(x\\mapsto \\cos x, x\\mapsto x \\cos x, x\\mapsto \\sin x, x\\mapsto x \\sin x)$" in formatted["indications"]
        assert "**Indice 2.** Effectuer un développement limité en $0$ à l'ordre 3" in formatted["indications"]
        assert "**2)** $(x\\mapsto \\cos x, x\\mapsto x \\cos x, x\\mapsto \\sin x, x\\mapsto x \\sin x)$" in formatted["correction"]

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

    def test_get_concepts_for_exercise(self, service):
        """Exercises should expose the structured concepts they test."""
        concepts = service.get_concepts_for_exercise("arithmetique_des_entiers__champo_036")

        assert concepts
        assert any(concept["title"] for concept in concepts)

    def test_get_exercise_structured_context(self, service):
        """A multi-part exercise should expose chapter concepts and sub-question mapping."""
        context = service.get_exercise_structured_context(
            "analyse_asymptotique_de_niveau_1__ex_003",
            "analyse_asymptotique_de_niveau_1",
        )

        assert "Concepts testes par cet exercice" in context
        assert "Repartition par sous-question" in context
        assert "**1)** $(x\\mapsto e^{x}, x\\mapsto x e^{x}, x\\mapsto e^{x+x^{2}})$" in context
        assert "Notions clees" in context

    # =========================================================================
    # Stats and programme
    # =========================================================================

    def test_get_collection_stats(self, service):
        """Test collection stats."""
        stats = service.get_collection_stats()
        assert "questions_cours" in stats
        assert "exercices" in stats
        assert "concepts" in stats
        assert stats["questions_cours"]["count"] == 176
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

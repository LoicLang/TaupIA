"""
Tool executor — dispatches tool calls to KnowledgeService methods.

Returns JSON-serializable dicts. The agent loop converts these to
JSON strings for the LLM.
"""

import json
from typing import Any

from services.knowledge_service import KnowledgeService


class ToolExecutor:
    """Executes tool calls against the knowledge graph."""

    def __init__(self, knowledge_service: KnowledgeService):
        self._ks = knowledge_service

    def execute(self, tool_name: str, arguments: dict) -> str:
        """
        Execute a tool and return the result as a JSON string.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            JSON string with the tool result
        """
        handler = getattr(self, f"_tool_{tool_name}", None)
        if handler is None:
            return json.dumps({"error": f"Outil inconnu: {tool_name}"}, ensure_ascii=False)

        try:
            result = handler(**arguments)
            return json.dumps(result, ensure_ascii=False, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

    # -----------------------------------------------------------------
    # Tool implementations
    # -----------------------------------------------------------------

    def _tool_chercher_concepts(
        self,
        query: str,
        chapter_id: str | None = None,
        max_results: int = 5,
    ) -> dict[str, Any]:
        """Search concepts by keyword."""
        results = self._ks.search_concepts(
            query=query,
            chapter_id=chapter_id,
            max_results=max_results,
        )
        return {"concepts": results, "count": len(results)}

    def _tool_lire_definition(self, concept_id: str) -> dict[str, Any]:
        """Read a concept definition."""
        node = self._ks._course_nodes_by_id.get(concept_id)
        if not node:
            graph_node = self._ks._graph_nodes.get(concept_id, {})
            props = graph_node.get("properties", {})
            if props:
                return {
                    "id": concept_id,
                    "type": props.get("type", "unknown"),
                    "title": props.get("title", concept_id),
                    "content_latex": props.get("content_latex"),
                    "found": True,
                }
            return {"error": f"Concept non trouve: {concept_id}", "found": False}

        return {
            "id": concept_id,
            "type": node.get("type", "unknown"),
            "title": node.get("title", ""),
            "content_latex": node.get("content_latex", ""),
            "proof_latex": node.get("proof_latex"),
            "found": True,
        }

    def _tool_lire_theoreme(self, concept_id: str) -> dict[str, Any]:
        """Read a theorem — same data source as definitions, includes proof."""
        return self._tool_lire_definition(concept_id)

    def _tool_trouver_prerequis(
        self,
        concept_id: str | None = None,
        chapter_id: str | None = None,
    ) -> dict[str, Any]:
        """Find prerequisites — concept-level when the graph is enriched, else chapter-level."""
        # Prefer enriched concept->concept prerequisites (grounded + adversarially verified).
        if concept_id:
            concept_prereqs = self._ks.get_concept_prerequisites(concept_id)
            if concept_prereqs:
                return {
                    "prerequisites": [
                        {
                            "id": p["id"],
                            "type": p["type"],
                            "title": p["title"],
                            "content_latex": p["content_latex"],
                            "confidence": p["confidence"],
                        }
                        for p in concept_prereqs
                    ],
                    "source": "concept_graph",
                }

        # Fallback: coarse chapter-level prerequisites.
        prerequisites: list[dict] = []
        seen: set[str] = set()
        chapters_to_check: list[str] = []
        if chapter_id:
            chapters_to_check.append(chapter_id)
        if concept_id:
            concept_chapter = self._ks._concept_to_chapter.get(concept_id)
            if concept_chapter:
                chapters_to_check.append(concept_chapter)

        for chapter in chapters_to_check:
            for prereq_id in self._ks._chapter_prerequisites.get(chapter, []):
                if prereq_id in seen:
                    continue
                seen.add(prereq_id)
                chapter_info = self._ks._course_chapters.get(prereq_id, {})
                prerequisites.append({
                    "id": prereq_id,
                    "type": "chapter",
                    "title": chapter_info.get("title", prereq_id),
                })

        if not prerequisites:
            return {"prerequisites": [], "message": "Aucun prerequis trouve."}

        return {"prerequisites": prerequisites, "source": "chapter_fallback"}

    def _tool_chercher_exercice(
        self,
        concept_ids: list[str],
        chapter_id: str | None = None,
        difficulty: int = 3,
    ) -> dict[str, Any]:
        """Find an exercise matching concepts."""
        exercise = self._ks.get_exercise_for_concepts(
            concept_ids=concept_ids,
            difficulty=difficulty,
            chapter_id=chapter_id,
        )
        if not exercise:
            return {"found": False, "message": "Aucun exercice trouve pour ces concepts."}

        return {
            "found": True,
            "exercise": {
                "id": exercise["id"],
                "chapter": exercise.get("chapter", ""),
                "chapter_id": exercise.get("chapter_id", ""),
                "difficulty": exercise.get("difficulty", 3),
                "enonce": exercise.get("enonce", ""),
                "indications": exercise.get("indications", ""),
                "correction": exercise.get("correction", ""),
            },
        }

    def _tool_lire_programme(self, chapter_id: str) -> dict[str, Any]:
        """Read official programme constraints for a chapter."""
        prog = self._ks.get_programme_for_chapter(chapter_id)
        chapter_info = self._ks._course_chapters.get(chapter_id, {})
        return {
            "chapter_id": chapter_id,
            "chapter_title": chapter_info.get("title", chapter_id),
            "notions": prog.get("notions", []),
            "prerequis": prog.get("prerequis", []),
            "vigilance": prog.get("vigilance", []),
            "capacites_exigibles": prog.get("capacites_exigibles", []),
        }

    def _tool_choisir_question(
        self,
        chapter_id: str,
        difficulty: int | None = None,
        exclude_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Pick a random question for the student."""
        question = self._ks.get_random_question(
            chapter_id=chapter_id,
            difficulty=difficulty,
            exclude_ids=exclude_ids,
        )
        if not question:
            return {"found": False, "message": "Plus de questions disponibles."}

        # Also get the concepts tested by this question
        concepts = self._ks.get_concepts_for_question(question["id"])
        concept_summaries = [
            {"id": c["id"], "type": c["type"], "title": c["title"]}
            for c in concepts[:5]
        ]

        return {
            "found": True,
            "question": {
                "id": question["id"],
                "chapter_id": question["chapter_id"],
                "difficulty": question["difficulty"],
                "question_raw": question["question_raw"],
                "answer_latex": question.get("answer_latex", ""),
            },
            "tested_concepts": concept_summaries,
        }

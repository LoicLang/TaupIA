"""
Knowledge Service - Acces deterministe aux donnees via le knowledge graph.

Remplace le RAG vectoriel ChromaDB par un lookup en memoire sur les JSON structures.
Charge ~2 Mo de donnees au demarrage, construit des index, et expose les memes
signatures que l'ancien data/query.py pour une integration transparente dans app.py.
"""

import json
import random
from pathlib import Path
from typing import Optional


class KnowledgeService:
    """Base de connaissances en memoire chargee depuis les fichiers JSON."""

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        self._base_dir = base_dir

        # Alias de normalisation des chapter IDs
        self._chapter_id_aliases = {"EV": "EV_AL"}

        # Chargement des donnees
        self._load_knowledge_graph()
        self._load_questions_kholle()
        self._load_programme()
        self._load_cours_json()
        self._load_exo_json()
        self._build_indices()

    # =========================================================================
    # Chargement des donnees
    # =========================================================================

    def _load_knowledge_graph(self):
        path = self._base_dir / "data" / "knowledge_graph.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._graph_nodes: dict[str, dict] = {}
        for node in data["nodes"]:
            self._graph_nodes[node["id"]] = node

        self._graph_edges: list[dict] = data["edges"]

    def _load_questions_kholle(self):
        path = self._base_dir / "data" / "questions_kholle.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._raw_questions: dict = data["chapters"]

    def _load_programme(self):
        path = self._base_dir / "data" / "programme.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        ref = data["referentiel_mpsi"]
        # Retirer les metadata du referentiel
        self._raw_programme: dict = {k: v for k, v in ref.items() if k != "metadata"}

    def _load_cours_json(self):
        self._course_nodes_by_id: dict[str, dict] = {}
        self._course_nodes_by_chapter: dict[str, list[dict]] = {}

        cours_dir = self._base_dir / "data" / "cours"
        if not cours_dir.exists():
            return

        for fpath in cours_dir.glob("*.json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            chapter_id = data.get("chapter_official_id", "")
            nodes = data.get("knowledge_nodes", [])

            if chapter_id not in self._course_nodes_by_chapter:
                self._course_nodes_by_chapter[chapter_id] = []

            for node in nodes:
                self._course_nodes_by_id[node["id"]] = node
                self._course_nodes_by_chapter[chapter_id].append(node)

    def _load_exo_json(self):
        self._td_exercises_by_id: dict[str, dict] = {}
        self._td_exercises_by_chapter: dict[str, list[dict]] = {}

        exo_dir = self._base_dir / "data" / "exercices"
        if not exo_dir.exists():
            return

        for fpath in exo_dir.glob("*.json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            chapter_id = data.get("chapter_official_id", "")
            exercises = data.get("exercises", [])

            if chapter_id not in self._td_exercises_by_chapter:
                self._td_exercises_by_chapter[chapter_id] = []

            for ex in exercises:
                ex["_chapter_id"] = chapter_id
                self._td_exercises_by_id[ex["id"]] = ex
                self._td_exercises_by_chapter[chapter_id].append(ex)

    # =========================================================================
    # Construction des index
    # =========================================================================

    def _build_indices(self):
        # Index des chapitres
        self._chapters: dict[str, dict] = {}
        for node in self._graph_nodes.values():
            if "Chapter" in node["labels"]:
                self._chapters[node["id"]] = node["properties"]

        # Index des aretes
        self._kholle_to_concepts: dict[str, list[tuple[str, float]]] = {}
        self._concept_to_kholles: dict[str, list[str]] = {}
        self._exercise_to_concepts: dict[str, list[tuple[str, float]]] = {}
        self._concept_to_exercises: dict[str, list[str]] = {}
        self._concept_to_chapter: dict[str, str] = {}
        self._chapter_to_concepts: dict[str, list[str]] = {}
        self._chapter_prerequisites: dict[str, list[str]] = {}

        for edge in self._graph_edges:
            src, tgt, etype = edge["source"], edge["target"], edge["type"]
            props = edge.get("properties", {})

            if etype == "BELONGS_TO":
                src_node = self._graph_nodes.get(src, {})
                labels = src_node.get("labels", [])
                if "Concept" in labels:
                    self._concept_to_chapter[src] = tgt
                    self._chapter_to_concepts.setdefault(tgt, []).append(src)

            elif etype == "TESTS":
                confidence = props.get("confidence", 0.5)
                src_node = self._graph_nodes.get(src, {})
                labels = src_node.get("labels", [])

                if "Kholle" in labels:
                    self._kholle_to_concepts.setdefault(src, []).append((tgt, confidence))
                    self._concept_to_kholles.setdefault(tgt, []).append(src)
                elif "Exercise" in labels:
                    self._exercise_to_concepts.setdefault(src, []).append((tgt, confidence))
                    self._concept_to_exercises.setdefault(tgt, []).append(src)

            elif etype == "REQUIRES":
                self._chapter_prerequisites.setdefault(src, []).append(tgt)

    # =========================================================================
    # Utilitaires
    # =========================================================================

    def _normalize_chapter_id(self, chapter_id: str) -> str:
        return self._chapter_id_aliases.get(chapter_id, chapter_id)

    def _find_questions_for_chapter(self, chapter_id: str) -> tuple[list[dict], str]:
        """Retourne (questions, chapter_title) pour un chapter_id (avec alias)."""
        canonical = self._normalize_chapter_id(chapter_id)
        # Chercher dans les deux IDs possibles
        for cid in {chapter_id, canonical}:
            if cid in self._raw_questions:
                ch_data = self._raw_questions[cid]
                title = ch_data.get("title", self._chapters.get(canonical, {}).get("title", ""))
                return ch_data["questions_cours"], title
        return [], self._chapters.get(canonical, {}).get("title", "")

    # =========================================================================
    # API publique - Drop-in pour data/query.py
    # =========================================================================

    def get_chapters(self) -> list[dict]:
        """Retourne la liste des chapitres avec stats."""
        result = []
        for chapter_id, props in self._chapters.items():
            questions, _ = self._find_questions_for_chapter(chapter_id)
            has_exercises = chapter_id in self._td_exercises_by_chapter

            if not questions or not has_exercises:
                continue

            difficulties = sorted({q["difficulte"] for q in questions})
            result.append({
                "id": chapter_id,
                "title": props["title"],
                "semestre": props["semestre"],
                "importance": props["importance"],
                "question_count": len(questions),
                "difficulties": difficulties,
            })

        return sorted(result, key=lambda x: (x["semestre"], x["title"]))

    def get_random_question(
        self,
        chapter_id: str,
        difficulty: Optional[int] = None,
        question_type: Optional[str] = None,
        exclude_ids: Optional[list[str]] = None,
    ) -> Optional[dict]:
        """Retourne une question aleatoire correspondant aux criteres."""
        canonical = self._normalize_chapter_id(chapter_id)
        questions, chapter_title = self._find_questions_for_chapter(chapter_id)

        if not questions:
            return None

        candidates = list(questions)

        # Filtrer par difficulte (+/- 1)
        if difficulty is not None:
            filtered = [q for q in candidates if abs(q["difficulte"] - difficulty) <= 1]
            if filtered:
                candidates = filtered

        # Filtrer par type
        if question_type:
            filtered = [q for q in candidates if q["type"] == question_type]
            if filtered:
                candidates = filtered

        # Exclure les deja posees
        if exclude_ids:
            candidates = [q for q in candidates if q["id"] not in exclude_ids]

        if not candidates:
            return None

        q = random.choice(candidates)

        return {
            "id": q["id"],
            "chapter_id": canonical,
            "chapter_title": chapter_title,
            "difficulty": q["difficulte"],
            "question_raw": q["question"],
            "question_type": q["type"],
            "temps_estime_min": q["temps_estime_min"],
            "attendus_json": json.dumps(q["attendus"], ensure_ascii=False),
            "erreurs_frequentes_json": json.dumps(q["erreurs_frequentes"], ensure_ascii=False),
            "relances_prof_json": json.dumps(q["relances_prof"], ensure_ascii=False),
        }

    def get_exercise_by_difficulty(
        self,
        chapter_id: Optional[str] = None,
        difficulty: int = 3,
        exclude_ids: Optional[list[str]] = None,
    ) -> Optional[dict]:
        """Retourne un exercice adapte au niveau."""
        canonical = self._normalize_chapter_id(chapter_id) if chapter_id else None

        candidates = []
        if canonical and canonical in self._td_exercises_by_chapter:
            candidates = list(self._td_exercises_by_chapter[canonical])
        else:
            candidates = list(self._td_exercises_by_id.values())

        if exclude_ids:
            candidates = [ex for ex in candidates if ex["id"] not in exclude_ids]

        if not candidates:
            return None

        def diff_distance(ex):
            return abs(ex.get("metadata", {}).get("difficulty_score", 3) - difficulty)

        candidates.sort(key=diff_distance)
        best = diff_distance(candidates[0])
        tier = [ex for ex in candidates if diff_distance(ex) <= best + 1]

        ex = random.choice(tier)
        ch_id = ex.get("_chapter_id", canonical or "")
        chapter_title = self._chapters.get(ch_id, {}).get("title", "")

        return self._format_exercise(ex, chapter_title, ch_id)

    def get_exercise_for_concepts(
        self,
        concept_ids: list[str],
        difficulty: int = 3,
        chapter_id: Optional[str] = None,
        exclude_ids: Optional[list[str]] = None,
    ) -> Optional[dict]:
        """
        Trouve un exercice TD testant les memes concepts que la question validee.
        Utilise les aretes TESTS du knowledge graph. Fallback sur chapter + difficulty.
        """
        candidate_ids: set[str] = set()
        for concept_id in concept_ids:
            for ex_id in self._concept_to_exercises.get(concept_id, []):
                candidate_ids.add(ex_id)

        candidates = []
        for ex_id in candidate_ids:
            if ex_id in self._td_exercises_by_id:
                if exclude_ids and ex_id in exclude_ids:
                    continue
                candidates.append(self._td_exercises_by_id[ex_id])

        if not candidates:
            return self.get_exercise_by_difficulty(chapter_id, difficulty, exclude_ids)

        concept_set = set(concept_ids)

        def score_exercise(ex):
            ex_concepts = {c_id for c_id, _ in self._exercise_to_concepts.get(ex["id"], [])}
            overlap = len(ex_concepts & concept_set)
            ex_diff = ex.get("metadata", {}).get("difficulty_score", 3)
            diff_penalty = abs(ex_diff - difficulty)
            return (overlap, -diff_penalty)

        candidates.sort(key=score_exercise, reverse=True)
        top = candidates[:3]
        ex = random.choice(top)

        ch_id = ex.get("_chapter_id", "")
        chapter_title = self._chapters.get(ch_id, {}).get("title", "")

        return self._format_exercise(ex, chapter_title, ch_id)

    def _format_exercise(self, ex: dict, chapter_title: str, chapter_id: str) -> dict:
        content = ex.get("content", {})
        return {
            "id": ex["id"],
            "chapter": chapter_title,
            "chapter_id": chapter_id,
            "difficulty": ex.get("metadata", {}).get("difficulty_score", 3),
            "enonce": content.get("statement_latex", ""),
            "indications": content.get("hint_latex", "") or "",
            "correction": content.get("solution_latex", ""),
        }

    # =========================================================================
    # Contexte structure pour le LLM (remplace le RAG)
    # =========================================================================

    def get_concepts_for_question(self, question_id: str) -> list[dict]:
        """
        Traverse les aretes TESTS pour trouver les concepts testes par une question.
        Retourne le contenu LaTeX complet depuis les Cours JSON.
        """
        tested = self._kholle_to_concepts.get(question_id, [])
        if not tested:
            return []

        tested_sorted = sorted(tested, key=lambda x: x[1], reverse=True)

        result = []
        for concept_id, confidence in tested_sorted:
            course_node = self._course_nodes_by_id.get(concept_id)

            if course_node:
                result.append({
                    "id": concept_id,
                    "type": course_node.get("type", "unknown"),
                    "title": course_node.get("title", ""),
                    "content_latex": course_node.get("content_latex", ""),
                    "proof_latex": course_node.get("proof_latex"),
                    "confidence": confidence,
                })
            else:
                graph_node = self._graph_nodes.get(concept_id, {})
                props = graph_node.get("properties", {})
                result.append({
                    "id": concept_id,
                    "type": props.get("type", "unknown"),
                    "title": props.get("title", concept_id),
                    "content_latex": None,
                    "proof_latex": None,
                    "confidence": confidence,
                })

        return result

    def get_programme_for_chapter(self, chapter_id: str) -> dict:
        """Retourne les contraintes du programme officiel pour un chapitre."""
        canonical = self._normalize_chapter_id(chapter_id)
        prog = self._raw_programme.get(canonical, {})
        return {
            "notions": prog.get("notions", []),
            "prerequis": prog.get("prerequis", []),
            "vigilance": prog.get("vigilance", []),
            "capacites_exigibles": prog.get("capacites_exigibles", []),
        }

    def get_structured_context(
        self,
        question_id: str,
        chapter_id: str,
        max_chars: int = 4000,
    ) -> str:
        """
        Construit le contexte structure pour le LLM.
        Remplace get_context_for_evaluation() de l'ancien data/query.py.

        Au lieu de 3 chunks RAG aleatoires, fournit :
        1. Definitions/theoremes exacts testes par la question (via aretes TESTS)
        2. Points de vigilance du programme officiel
        3. Capacites exigibles
        """
        parts = []
        total_chars = 0

        # 1. Concepts testes par cette question
        concepts = self.get_concepts_for_question(question_id)
        if concepts:
            parts.append("### Concepts testes par cette question")
            for c in concepts:
                if total_chars >= max_chars:
                    break

                type_label = {
                    "definition": "Definition",
                    "theorem": "Theoreme",
                    "property": "Propriete",
                    "method": "Methode",
                }.get(c["type"], c["type"].capitalize())

                entry = f"**{type_label} : {c['title']}**"
                if c.get("content_latex"):
                    entry += f"\n{c['content_latex']}"
                if c.get("proof_latex"):
                    entry += f"\n*Demonstration :* {c['proof_latex']}"

                parts.append(entry)
                total_chars += len(entry)

        # 2. Programme officiel
        canonical = self._normalize_chapter_id(chapter_id)
        prog = self.get_programme_for_chapter(canonical)

        if prog["vigilance"] and total_chars < max_chars:
            vigilance_text = "### Points de vigilance (programme officiel)\n"
            vigilance_text += "\n".join(f"- {v}" for v in prog["vigilance"][:5])
            parts.append(vigilance_text)
            total_chars += len(vigilance_text)

        if prog["capacites_exigibles"] and total_chars < max_chars:
            cap_text = "### Capacites exigibles\n"
            cap_text += "\n".join(f"- {c}" for c in prog["capacites_exigibles"][:5])
            parts.append(cap_text)
            total_chars += len(cap_text)

        if not parts:
            return "Contexte non disponible pour ce chapitre."

        return "\n\n".join(parts)

    def get_rag_context(
        self,
        question: str,
        chapter_id: Optional[str] = None,
        top_k: int = 3,
        question_id: Optional[str] = None,
    ) -> list[dict]:
        """
        Retourne le contexte au format compatible avec le debug panel.
        Utilise le graphe au lieu de ChromaDB.
        """
        if question_id:
            concepts = self.get_concepts_for_question(question_id)
        elif chapter_id:
            canonical = self._normalize_chapter_id(chapter_id)
            concept_ids = self._chapter_to_concepts.get(canonical, [])[:top_k]
            concepts = []
            for concept_id in concept_ids:
                node = self._course_nodes_by_id.get(concept_id, {})
                concepts.append({
                    "id": concept_id,
                    "type": node.get("type", "unknown"),
                    "title": node.get("title", concept_id),
                    "content_latex": node.get("content_latex", ""),
                    "confidence": 0.5,
                })
        else:
            return []

        result = []
        for c in concepts[:top_k]:
            content = c.get("content_latex", "") or ""
            ch_id = self._concept_to_chapter.get(c["id"], "")
            result.append({
                "chunk_id": c["id"],
                "content": content,
                "score": c.get("confidence", 0.5) * 100,
                "metadata": {
                    "chapter": self._chapters.get(ch_id, {}).get("title", ""),
                    "section": c.get("type", ""),
                    "subsection": c.get("title", ""),
                },
            })

        return result

    def get_collection_stats(self) -> dict:
        """Retourne les stats des collections de donnees."""
        total_questions = sum(
            len(ch["questions_cours"]) for ch in self._raw_questions.values()
        )
        return {
            "questions_cours": {"count": total_questions},
            "exercices": {"count": len(self._td_exercises_by_id)},
            "concepts": {"count": len(self._course_nodes_by_id)},
        }


# =============================================================================
# Singleton et fonctions module-level (drop-in pour app.py)
# =============================================================================

_service: Optional[KnowledgeService] = None


def _get_service() -> KnowledgeService:
    global _service
    if _service is None:
        _service = KnowledgeService()
    return _service


def get_chapters() -> list[dict]:
    return _get_service().get_chapters()


def get_random_question(
    chapter_id: str,
    difficulty: Optional[int] = None,
    question_type: Optional[str] = None,
    exclude_ids: Optional[list[str]] = None,
) -> Optional[dict]:
    return _get_service().get_random_question(chapter_id, difficulty, question_type, exclude_ids)


def get_exercise_by_difficulty(
    chapter_id: Optional[str] = None,
    difficulty: int = 3,
    exclude_ids: Optional[list[str]] = None,
) -> Optional[dict]:
    return _get_service().get_exercise_by_difficulty(chapter_id, difficulty, exclude_ids)


def get_exercise_for_concepts(
    concept_ids: list[str],
    difficulty: int = 3,
    chapter_id: Optional[str] = None,
    exclude_ids: Optional[list[str]] = None,
) -> Optional[dict]:
    return _get_service().get_exercise_for_concepts(concept_ids, difficulty, chapter_id, exclude_ids)


def get_structured_context(
    question_id: str,
    chapter_id: str,
    max_chars: int = 4000,
) -> str:
    return _get_service().get_structured_context(question_id, chapter_id, max_chars)


def get_concepts_for_question(question_id: str) -> list[dict]:
    return _get_service().get_concepts_for_question(question_id)


def get_rag_context(
    question: str,
    chapter_id: Optional[str] = None,
    top_k: int = 3,
    question_id: Optional[str] = None,
) -> list[dict]:
    return _get_service().get_rag_context(question, chapter_id, top_k, question_id)


def get_collection_stats() -> dict:
    return _get_service().get_collection_stats()

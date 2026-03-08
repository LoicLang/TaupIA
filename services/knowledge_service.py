"""
Knowledge Service - Acces deterministe aux donnees via le knowledge graph V3.

Charge les donnees JSON V3 au demarrage, construit des index en memoire,
et expose l'API publique pour les chapitres, questions, exercices et contexte LLM.

Architecture: 29 chapitres cours (user-facing) sont la reference.
Les questions (groupees par programme) sont distribuees aux chapitres cours
via le mapping linked_course_chapters.
"""

import json
import random
import re
from pathlib import Path
from typing import Optional


class KnowledgeService:
    """Base de connaissances en memoire chargee depuis les fichiers JSON V3."""

    _TEXT_UNICODE_ESCAPE = re.compile(r"\\u([0-9a-fA-F]{4})")
    _TEXT_ACCENT_ESCAPE = re.compile(r"\\(?=[À-ÖØ-öø-ÿ])")
    _KNOWN_INVALID_EXERCISE_IDS: dict[str, str] = {
        "calculs_algebriques_dans_r__ex_007": "incomplete_solution",
        "calculs_algebriques_dans_r__champo_024": "thin_solution",
        "calculs_algebriques_dans_r__champo_025": "thin_solution",
        "arithmetique_des_entiers__champo_028": "thin_solution",
        "groupes_et_anneaux__ex_004": "incorrect_solution",
        "derivabilite_et_convexite__ex_032": "truncated_source",
        "determinants__ex_020": "incomplete_solution",
        "groupes_et_anneaux__champo_017": "incomplete_solution",
        "nombres_complexes__ex_020": "incorrect_solution",
        "nombres_complexes__ex_028": "incorrect_solution",
        "nombres_complexes__champo_029": "incomplete_solution",
        "rappels_et_complements_sur_les_fonctions_reelles__champo_024": "thin_solution",
        "rappels_et_complements_sur_les_fonctions_reelles__champo_025": "thin_solution",
        "rappels_et_complements_sur_les_fonctions_reelles__champo_027": "thin_solution",
        "rappels_et_complements_sur_les_fonctions_reelles__champo_030": "thin_solution",
        "rappels_et_complements_sur_les_fonctions_reelles__champo_031": "thin_solution",
        "relations_binaires_et_applications__champo_027": "thin_solution",
    }
    _INVALID_EXERCISE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
        ("placeholder_tag", re.compile(r"\bplaceholder\b", re.IGNORECASE)),
        (
            "missing_statement",
            re.compile(
                r"\[texte manquant dans le pdf\]|\[exercise statement not provided in source",
                re.IGNORECASE,
            ),
        ),
        (
            "truncated_source",
            re.compile(
                r"énoncé (?:tronqué|source)|question semble tronquée|fragments manquants",
                re.IGNORECASE,
            ),
        ),
        (
            "incomplete_solution",
            re.compile(r"solution incomp|correction probable|faux\s*:\s*recalcul", re.IGNORECASE),
        ),
        (
            "unknown_bound",
            re.compile(r"\\text\{\?\}|\[\s*1\s*,\s*\\text\{\?\}\s*\[", re.IGNORECASE),
        ),
    )

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        self._base_dir = base_dir

        # Normalisation des exercise chapter IDs vers les IDs cours (reference)
        # Corrige les mismatches entre exercices/ et cours/
        self._exercise_id_to_cours_id = {
            "calculs_algebriques_dans_r": "calculs_algebriques_dans_R",
            "representation_matricielle": "representation_matricielle_applications_lineaires",
            "arithmetique_polynomes_fractions": "arithmetique_des_polynomes_et_fractions_rationnelles",
        }

        # Chargement des donnees
        self._load_knowledge_graph()
        self._load_programme()
        self._load_cours_json()
        self._load_exo_json()
        self._load_questions_de_cours()
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

    def _load_programme(self):
        """Charge programme.json pour les metadonnees (semestre, importance, vigilance, etc.)."""
        path = self._base_dir / "data" / "programme.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        ref = data["referentiel_mpsi"]
        self._raw_programme: dict = {k: v for k, v in ref.items() if k != "metadata"}

        # Mapping programme_id -> course chapter IDs (pour distribuer les questions)
        self._prog_to_course_chapters: dict[str, list[str]] = {}
        # Mapping course_id -> programme_id (pour retrouver semestre/importance)
        self._course_to_prog: dict[str, str] = {}
        for prog_id, prog_data in self._raw_programme.items():
            linked = prog_data.get("linked_course_chapters", [])
            self._prog_to_course_chapters[prog_id] = linked
            for course_id in linked:
                self._course_to_prog[course_id] = prog_id

    def _load_cours_json(self):
        """Charge les 29 fichiers cours. Les chapter_official_id sont la reference."""
        self._course_chapters: dict[str, dict] = {}  # chapter_id -> metadata
        self._course_nodes_by_id: dict[str, dict] = {}
        self._course_nodes_by_chapter: dict[str, list[dict]] = {}

        cours_dir = self._base_dir / "data" / "cours"
        if not cours_dir.exists():
            return

        for fpath in cours_dir.glob("*.json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            chapter_id = data.get("chapter_official_id", "")
            chapter_name = data.get("chapter_name", "")
            nodes = data.get("knowledge_nodes", [])

            # Stocker les metadonnees du chapitre
            prog_id = self._course_to_prog.get(chapter_id, "")
            prog_data = self._raw_programme.get(prog_id, {})
            self._course_chapters[chapter_id] = {
                "title": chapter_name,
                "semestre": prog_data.get("semestre", 1),
                "importance": prog_data.get("importance", 3),
                "programme_id": prog_id,
            }

            self._course_nodes_by_chapter[chapter_id] = []
            for node in nodes:
                self._course_nodes_by_id[node["id"]] = node
                self._course_nodes_by_chapter[chapter_id].append(node)

    def _load_exo_json(self):
        """Charge les exercices et normalise les chapter_official_id vers les IDs cours."""
        self._td_exercises_by_id: dict[str, dict] = {}
        self._td_exercises_by_chapter: dict[str, list[dict]] = {}
        self._invalid_exercises_by_id: dict[str, list[str]] = {}

        exo_dir = self._base_dir / "data" / "exercices"
        if not exo_dir.exists():
            return

        for fpath in exo_dir.glob("*.json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            raw_chapter_id = data.get("chapter_official_id", "")
            # Normaliser vers l'ID cours de reference
            chapter_id = self._exercise_id_to_cours_id.get(raw_chapter_id, raw_chapter_id)
            exercises = data.get("exercises", [])

            if chapter_id not in self._td_exercises_by_chapter:
                self._td_exercises_by_chapter[chapter_id] = []

            for ex in exercises:
                ex = self._normalize_exercise_payload(ex)
                ex["_chapter_id"] = chapter_id
                quality_issues = self._exercise_quality_issues(ex)
                if quality_issues:
                    self._invalid_exercises_by_id[ex["id"]] = quality_issues
                    continue
                self._td_exercises_by_id[ex["id"]] = ex
                self._td_exercises_by_chapter[chapter_id].append(ex)

    def _load_questions_de_cours(self):
        """Charge les questions et les distribue aux chapitres cours."""
        # Questions indexees par cours chapter ID
        self._questions_by_course_chapter: dict[str, list[dict]] = {}
        self._questions_by_id: dict[str, dict] = {}
        # Garder les donnees brutes par programme pour get_programme_for_chapter
        self._raw_questions_by_prog: dict[str, dict] = {}

        curated_qdir = self._base_dir / "data" / "questions_de_cours_curated"
        qdir = curated_qdir if curated_qdir.exists() else self._base_dir / "data" / "questions_de_cours"
        if not qdir.exists():
            return

        for fpath in qdir.glob("*.json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            prog_id = data.get("programme_chapter_id", "")
            questions = data.get("questions", [])
            linked = data.get("linked_course_chapters", [])

            self._raw_questions_by_prog[prog_id] = data

            # Distribuer les questions aux chapitres cours lies
            for course_id in linked:
                if course_id not in self._questions_by_course_chapter:
                    self._questions_by_course_chapter[course_id] = []
                self._questions_by_course_chapter[course_id].extend(questions)
            for question in questions:
                self._questions_by_id[question["id"]] = question

    # =========================================================================
    # Construction des index
    # =========================================================================

    def _build_indices(self):
        """Construit les index du knowledge graph."""
        self._kholle_to_concepts: dict[str, list[tuple[str, float]]] = {}
        self._concept_to_kholles: dict[str, list[str]] = {}
        self._exercise_to_concepts: dict[str, list[tuple[str, float]]] = {}
        self._concept_to_exercises: dict[str, list[str]] = {}
        self._concept_to_chapter: dict[str, str] = {}
        self._chapter_to_concepts: dict[str, list[str]] = {}
        self._chapter_prerequisites: dict[str, list[str]] = {}

        for edge in self._graph_edges:
            src, tgt, etype = edge["source"], edge["target"], edge["type"]
            props = edge.get("properties", {}) or {}

            if etype == "BELONGS_TO":
                src_node = self._graph_nodes.get(src, {})
                labels = src_node.get("labels", [])
                if "Concept" in labels:
                    self._concept_to_chapter[src] = tgt
                    self._chapter_to_concepts.setdefault(tgt, []).append(src)

            elif etype == "TESTS":
                confidence = props.get("confidence", 1.0)
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

    def _normalize_text_artifacts(self, text: str) -> str:
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized = self._TEXT_UNICODE_ESCAPE.sub(
            lambda match: chr(int(match.group(1), 16)),
            normalized,
        )
        normalized = self._TEXT_ACCENT_ESCAPE.sub("", normalized)
        return normalized

    def _normalize_exercise_payload(self, value):
        if isinstance(value, str):
            return self._normalize_text_artifacts(value)
        if isinstance(value, list):
            return [self._normalize_exercise_payload(item) for item in value]
        if isinstance(value, dict):
            return {
                key: self._normalize_exercise_payload(item)
                for key, item in value.items()
            }
        return value

    def _exercise_quality_issues(self, ex: dict) -> list[str]:
        issues: list[str] = []
        if ex.get("id") in self._KNOWN_INVALID_EXERCISE_IDS:
            issues.append(self._KNOWN_INVALID_EXERCISE_IDS[ex["id"]])

        tags = [tag.lower() for tag in ex.get("tags", []) if isinstance(tag, str)]
        if "placeholder" in tags:
            issues.append("placeholder_tag")

        texts = [
            ex.get("title", ""),
            ex.get("statement_latex", "") or "",
            ex.get("global_solution_latex", "") or "",
        ]

        for hint in ex.get("hints", []):
            texts.append(hint.get("content_latex", "") or "")

        for sq in ex.get("sub_questions", []):
            texts.append(sq.get("statement_latex", "") or "")
            texts.append(sq.get("solution_latex", "") or "")
            for hint in sq.get("hints", []):
                texts.append(hint.get("content_latex", "") or "")

        blob = "\n".join(texts)
        for name, pattern in self._INVALID_EXERCISE_PATTERNS:
            if pattern.search(blob) and name not in issues:
                issues.append(name)

        has_statement = bool((ex.get("statement_latex") or "").strip()) or any(
            (sq.get("statement_latex") or "").strip()
            for sq in ex.get("sub_questions", [])
        )
        if not has_statement:
            issues.append("empty_statement")

        has_solution = bool((ex.get("global_solution_latex") or "").strip()) or any(
            (sq.get("solution_latex") or "").strip()
            for sq in ex.get("sub_questions", [])
        )
        if not has_solution:
            issues.append("missing_solution")

        return issues

    # =========================================================================
    # API publique
    # =========================================================================

    def get_chapters(self) -> list[dict]:
        """Retourne la liste des 29 chapitres cours avec stats."""
        result = []
        for chapter_id, props in self._course_chapters.items():
            questions = self._questions_by_course_chapter.get(chapter_id, [])
            exercises = self._td_exercises_by_chapter.get(chapter_id, [])

            if not questions or not exercises:
                continue

            difficulties = sorted({q["difficulty"] for q in questions})
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
        """Retourne une question aleatoire pour un chapitre cours."""
        questions = self._questions_by_course_chapter.get(chapter_id, [])
        chapter_title = self._course_chapters.get(chapter_id, {}).get("title", "")

        if not questions:
            return None

        candidates = list(questions)

        if difficulty is not None:
            filtered = [q for q in candidates if abs(q["difficulty"] - difficulty) <= 1]
            if filtered:
                candidates = filtered

        if question_type:
            filtered = [q for q in candidates if q["type"] == question_type]
            if filtered:
                candidates = filtered

        if exclude_ids:
            candidates = [q for q in candidates if q["id"] not in exclude_ids]

        if not candidates:
            return None

        q = random.choice(candidates)

        return {
            "id": q["id"],
            "chapter_id": chapter_id,
            "chapter_title": chapter_title,
            "difficulty": q["difficulty"],
            "question_raw": q["question_latex"],
            "question_type": q["type"],
            "answer_latex": q.get("answer_latex", ""),
            "answer_node_id": q.get("answer_node_id", ""),
            "programme_notion": q.get("programme_notion", ""),
        }

    def get_exercise_by_difficulty(
        self,
        chapter_id: Optional[str] = None,
        difficulty: int = 3,
        exclude_ids: Optional[list[str]] = None,
    ) -> Optional[dict]:
        """Retourne un exercice adapte au niveau pour un chapitre cours."""
        candidates = []
        if chapter_id:
            candidates = list(self._td_exercises_by_chapter.get(chapter_id, []))
        if not candidates:
            candidates = list(self._td_exercises_by_id.values())

        if exclude_ids:
            candidates = [ex for ex in candidates if ex["id"] not in exclude_ids]

        if not candidates:
            return None

        def diff_distance(ex):
            return abs(ex.get("difficulty", 3) - difficulty)

        candidates.sort(key=diff_distance)
        best = diff_distance(candidates[0])
        tier = [ex for ex in candidates if diff_distance(ex) <= best + 1]

        ex = random.choice(tier)
        ch_id = ex.get("_chapter_id", chapter_id or "")
        chapter_title = self._course_chapters.get(ch_id, {}).get("title", "")

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
                ex = self._td_exercises_by_id[ex_id]
                # Si un chapitre est specifie, filtrer
                if chapter_id and ex.get("_chapter_id") != chapter_id:
                    continue
                candidates.append(ex)

        if not candidates:
            return self.get_exercise_by_difficulty(chapter_id, difficulty, exclude_ids)

        concept_set = set(concept_ids)

        def score_exercise(ex):
            ex_concepts = {c_id for c_id, _ in self._exercise_to_concepts.get(ex["id"], [])}
            overlap = len(ex_concepts & concept_set)
            ex_diff = ex.get("difficulty", 3)
            diff_penalty = abs(ex_diff - difficulty)
            return (overlap, -diff_penalty)

        candidates.sort(key=score_exercise, reverse=True)
        top = candidates[:3]
        ex = random.choice(top)

        ch_id = ex.get("_chapter_id", "")
        chapter_title = self._course_chapters.get(ch_id, {}).get("title", "")

        return self._format_exercise(ex, chapter_title, ch_id)

    def _format_exercise(self, ex: dict, chapter_title: str, chapter_id: str) -> dict:
        """Formate un exercice V3 pour l'API."""
        numbered_item_pattern = re.compile(r"(?m)^(?P<label>(?:\d+|[a-zA-Z])[.)])\s+")
        inline_numbered_item_pattern = re.compile(r"(?<![_\\])(?P<label>(?:\d+|[a-zA-Z])[.)])\s+")

        def _normalized_text(value: Optional[str]) -> str:
            return " ".join((value or "").split())

        def _append_unique(parts: list[str], seen: set[str], value: Optional[str]) -> None:
            text = (value or "").strip()
            if not text:
                return

            key = _normalized_text(text)
            if key in seen:
                return

            seen.add(key)
            parts.append(text)

        def _format_labeled_block(text: str, label: Optional[str]) -> str:
            clean = text.strip()
            if not clean:
                return ""
            if not label:
                return clean
            return f"**{label}** {clean}"

        def _label_sort_value(label: str) -> tuple[str, int] | None:
            token = (label or "").strip()[:-1]
            if token.isdigit():
                return ("num", int(token))
            if len(token) == 1 and token.isalpha():
                return ("alpha", ord(token.lower()) - ord("a") + 1)
            return None

        def _looks_like_ordered_sequence(matches: list[re.Match[str]]) -> bool:
            if len(matches) < 2:
                return False

            parsed = [_label_sort_value(match.group("label")) for match in matches]
            if any(value is None for value in parsed):
                return False

            first_kind, first_value = parsed[0]
            if first_value != 1:
                return False

            for expected, parsed_label in enumerate(parsed[: min(len(parsed), 8)], start=1):
                kind, value = parsed_label
                if kind != first_kind or value != expected:
                    return False

            return True

        def _iter_embedded_matches(content: str) -> list[re.Match[str]]:
            line_matches = list(numbered_item_pattern.finditer(content))
            if _looks_like_ordered_sequence(line_matches):
                return line_matches

            inline_matches = list(inline_numbered_item_pattern.finditer(content))
            if _looks_like_ordered_sequence(inline_matches):
                return inline_matches

            return []

        def _split_embedded_numbered_items(text: Optional[str]) -> list[str]:
            content = (text or "").strip()
            if not content:
                return []

            matches = _iter_embedded_matches(content)
            if not matches:
                return [content]

            parts: list[str] = []
            intro = content[:matches[0].start()].strip()
            if intro:
                parts.append(intro)

            for index, match in enumerate(matches):
                start = match.end()
                end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
                block = content[start:end].strip()
                if block:
                    parts.append(_format_labeled_block(block, match.group("label")))

            return parts or [content]

        def _sub_question_display_label(index: int, sq: dict) -> Optional[str]:
            label = (sq.get("label") or "").strip()
            if label:
                return label
            if has_multiple_sub_questions:
                return f"{index}."
            return None

        def _format_hint_blocks() -> str:
            blocks: list[str] = []
            seen_general_hints: set[str] = set()
            general_hints: list[str] = []
            for hint in ex.get("hints", []):
                _append_unique(general_hints, seen_general_hints, hint.get("content_latex", ""))

            if general_hints:
                block = ["Indications générales"]
                block.extend(general_hints)
                blocks.append("\n\n".join(block))

            for index, sq in enumerate(sub_questions, start=1):
                sq_hint_lines: list[str] = []
                sq_seen: set[str] = set()
                for hint_index, hint in enumerate(sq.get("hints", []), start=1):
                    content = (hint.get("content_latex") or "").strip()
                    if not content:
                        continue
                    level = hint.get("level")
                    hint_label = f"Indice {level}" if level else f"Indice {hint_index}"
                    _append_unique(
                        sq_hint_lines,
                        sq_seen,
                        f"**{hint_label}.** {content}",
                    )

                if not sq_hint_lines:
                    continue

                display_label = _sub_question_display_label(index, sq)
                statement = (sq.get("statement_latex") or "").strip()
                header = _format_labeled_block(statement, display_label)
                block = [header] if header else []
                block.extend(sq_hint_lines)
                blocks.append("\n\n".join(block))

            return "\n\n".join(block for block in blocks if block)

        def _format_correction_blocks() -> str:
            correction_parts: list[str] = []
            seen_correction: set[str] = set()
            global_sol = ex.get("global_solution_latex")
            if global_sol:
                _append_unique(correction_parts, seen_correction, global_sol)
                return "\n\n".join(correction_parts)

            for index, sq in enumerate(sub_questions, start=1):
                sol = (sq.get("solution_latex") or "").strip()
                if not sol:
                    continue

                display_label = _sub_question_display_label(index, sq)
                statement = (sq.get("statement_latex") or "").strip()
                if statement:
                    rendered = f"{_format_labeled_block(statement, display_label)}\n{sol}"
                elif display_label:
                    rendered = f"**{display_label}**\n{sol}"
                else:
                    rendered = sol
                _append_unique(correction_parts, seen_correction, rendered)

            return "\n\n".join(correction_parts)

        enonce_parts = []
        seen_enonce: set[str] = set()
        main_statement = ex.get("statement_latex", "")
        for part in _split_embedded_numbered_items(main_statement):
            _append_unique(enonce_parts, seen_enonce, part)

        sub_questions = ex.get("sub_questions", [])
        has_multiple_sub_questions = len([sq for sq in sub_questions if (sq.get("statement_latex") or "").strip()]) > 1
        for index, sq in enumerate(sub_questions, start=1):
            label = _sub_question_display_label(index, sq)
            stmt = (sq.get("statement_latex") or "").strip()
            if not stmt:
                continue
            if not (sq.get("label") or "").strip() and _normalized_text(stmt) == _normalized_text(main_statement):
                continue

            rendered = _format_labeled_block(stmt, label)
            _append_unique(enonce_parts, seen_enonce, rendered)

        enonce = "\n\n".join(enonce_parts)
        indications = _format_hint_blocks()
        correction = _format_correction_blocks()

        return {
            "id": ex["id"],
            "chapter": chapter_title,
            "chapter_id": chapter_id,
            "difficulty": ex.get("difficulty", 3),
            "enonce": enonce,
            "indications": indications,
            "correction": correction,
        }

    # =========================================================================
    # Contexte structure pour le LLM
    # =========================================================================

    def get_concepts_for_question(self, question_id: str) -> list[dict]:
        """Traverse les aretes TESTS pour trouver les concepts testes par une question."""
        tested = self._kholle_to_concepts.get(question_id, [])
        question = self._questions_by_id.get(question_id, {})
        if not tested:
            tested = [
                (concept_id, 1.0)
                for concept_id in question.get("tested_concept_ids", [])
            ]
        if not tested:
            if question.get("answer_latex"):
                inferred_type = {
                    "definition": "definition",
                    "enonce": "theorem",
                }.get(question.get("type"), "theorem")
                return [{
                    "id": question.get("answer_node_id", question_id),
                    "type": inferred_type,
                    "title": question.get("programme_notion", question_id),
                    "content_latex": question.get("answer_latex", ""),
                    "proof_latex": None,
                    "confidence": 1.0,
                }]
            return []

        return self._resolve_concepts(tested)

    def _resolve_concepts(self, tested: list[tuple[str, float]]) -> list[dict]:
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

    def get_concepts_for_exercise(self, exercise_id: str) -> list[dict]:
        """Retourne les concepts testes par un exercice via le graphe, avec fallback JSON."""
        tested = list(self._exercise_to_concepts.get(exercise_id, []))

        raw_exercise = self._td_exercises_by_id.get(exercise_id)
        if raw_exercise and not tested:
            for concept_id in raw_exercise.get("knowledge_nodes_tested", []) or []:
                tested.append((concept_id, 1.0))

            for sq in raw_exercise.get("sub_questions", []):
                for concept_id in sq.get("knowledge_nodes_tested", []) or []:
                    tested.append((concept_id, 1.0))

        if not tested:
            return []

        deduped: dict[str, float] = {}
        for concept_id, confidence in tested:
            deduped[concept_id] = max(confidence, deduped.get(concept_id, 0.0))

        return self._resolve_concepts(list(deduped.items()))

    def get_exercise_structured_context(
        self,
        exercise_id: str,
        chapter_id: str,
        max_chars: int = 4000,
    ) -> str:
        """Construit un contexte structuré pour le guidage d'exercice."""
        parts: list[str] = []
        total_chars = 0

        concepts = self.get_concepts_for_exercise(exercise_id)
        if concepts:
            section_parts = ["### Concepts testes par cet exercice"]
            for concept in concepts[:6]:
                type_label = {
                    "definition": "Definition",
                    "theorem": "Theoreme",
                    "property": "Propriete",
                    "method": "Methode",
                    "example": "Exemple",
                    "remark": "Remarque",
                    "warning": "Attention",
                }.get(concept["type"], concept["type"].capitalize())
                entry = f"**{type_label} : {concept['title']}**"
                if concept.get("content_latex"):
                    entry += f"\n{concept['content_latex']}"
                section_parts.append(entry)
            concept_text = "\n\n".join(section_parts)
            parts.append(concept_text)
            total_chars += len(concept_text)

        raw_exercise = self._td_exercises_by_id.get(exercise_id)
        if raw_exercise and total_chars < max_chars:
            sub_blocks: list[str] = []
            for index, sq in enumerate(raw_exercise.get("sub_questions", []), start=1):
                concept_ids = sq.get("knowledge_nodes_tested", []) or []
                if not concept_ids:
                    continue

                label = (sq.get("label") or "").strip() or f"{index}."
                statement = (sq.get("statement_latex") or "").strip()
                concept_titles = []
                for concept_id in concept_ids[:3]:
                    node = self._course_nodes_by_id.get(concept_id)
                    if node:
                        concept_titles.append(node.get("title", concept_id))
                if not concept_titles:
                    continue

                header = f"**{label}** {statement}".strip() if statement else f"**{label}**"
                sub_blocks.append(f"{header}\nNotions clees : {', '.join(concept_titles)}")

            if sub_blocks:
                sub_text = "### Repartition par sous-question\n" + "\n\n".join(sub_blocks)
                if total_chars + len(sub_text) <= max_chars:
                    parts.append(sub_text)
                    total_chars += len(sub_text)

        prog = self.get_programme_for_chapter(chapter_id)
        if prog["vigilance"] and total_chars < max_chars:
            vigilance_text = "### Points de vigilance (programme officiel)\n"
            vigilance_text += "\n".join(f"- {v}" for v in prog["vigilance"][:4])
            if total_chars + len(vigilance_text) <= max_chars:
                parts.append(vigilance_text)
                total_chars += len(vigilance_text)

        if not parts:
            return "Contexte non disponible pour cet exercice."

        return "\n\n".join(parts)

    def get_programme_for_chapter(self, chapter_id: str) -> dict:
        """Retourne les contraintes du programme officiel pour un chapitre cours."""
        # Retrouver le programme_id depuis le chapitre cours
        prog_id = self._course_to_prog.get(chapter_id, "")
        prog = self._raw_programme.get(prog_id, {})
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
        Fournit les definitions/theoremes exacts + vigilance programme + capacites.
        """
        parts = []
        total_chars = 0

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
                    "example": "Exemple",
                    "remark": "Remarque",
                    "warning": "Attention",
                }.get(c["type"], c["type"].capitalize())

                entry = f"**{type_label} : {c['title']}**"
                if c.get("content_latex"):
                    entry += f"\n{c['content_latex']}"
                if c.get("proof_latex"):
                    entry += f"\n*Demonstration :* {c['proof_latex']}"

                parts.append(entry)
                total_chars += len(entry)

        prog = self.get_programme_for_chapter(chapter_id)

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
        """Retourne le contexte au format debug panel."""
        if question_id:
            concepts = self.get_concepts_for_question(question_id)
        elif chapter_id:
            concept_ids = self._chapter_to_concepts.get(chapter_id, [])[:top_k]
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
            chapter_title = self._course_chapters.get(ch_id, {}).get("title", "")
            result.append({
                "chunk_id": c["id"],
                "content": content,
                "score": c.get("confidence", 0.5) * 100,
                "metadata": {
                    "chapter": chapter_title,
                    "section": c.get("type", ""),
                    "subsection": c.get("title", ""),
                },
            })

        return result

    def get_collection_stats(self) -> dict:
        """Retourne les stats des collections de donnees."""
        total_questions = sum(
            len(qs) for qs in self._questions_by_course_chapter.values()
        )
        return {
            "questions_cours": {"count": total_questions},
            "exercices": {
                "count": len(self._td_exercises_by_id),
                "invalid_count": len(self._invalid_exercises_by_id),
            },
            "concepts": {"count": len(self._course_nodes_by_id)},
        }


# =============================================================================
# Singleton et fonctions module-level
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

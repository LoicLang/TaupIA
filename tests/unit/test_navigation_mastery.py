"""Tests for navigation (deviation) tools and the mastery layer (pillars 2 & 3)."""

import json

import pytest

from services.knowledge_service import KnowledgeService
from core.tools.executor import ToolExecutor
from core.tools.definitions import get_tool_definitions
from backend.session_store import SessionState


@pytest.fixture(scope="module")
def ks():
    return KnowledgeService()


def test_action_tools_gated_by_flag():
    base = {t["function"]["name"] for t in get_tool_definitions()}
    assert "changer_exercice" not in base
    with_actions = get_tool_definitions(include_actions=True)
    names = {t["function"]["name"] for t in with_actions}
    assert "changer_exercice" in names
    assert "consulter_profil_maitrise" in names
    assert len(with_actions) == len(base) + 2


def test_changer_exercice_records_intent(ks):
    executor = ToolExecutor(
        ks,
        session_context={"chapter_id": "applications_lineaires", "difficulty": 3, "done_exercises": []},
    )
    result = json.loads(executor.execute("changer_exercice", {}))
    assert result["found"] is True
    assert result["exercise"]["enonce"]
    assert len(executor.intents) == 1
    assert executor.intents[0]["action"] == "set_exercise"
    assert executor.intents[0]["exercise"]["id"] == result["exercise"]["id"]


def test_consulter_profil_maitrise_returns_weakest_first(ks):
    mastery = {"c_weak": {"score": 0.2, "seen": 2}, "c_strong": {"score": 0.9, "seen": 1}}
    executor = ToolExecutor(ks, mastery=mastery)
    result = json.loads(executor.execute("consulter_profil_maitrise", {}))
    assert result["mastery"][0]["concept_id"] == "c_weak"
    assert result["n_tracked"] == 2


def test_trouver_prerequis_weighted_by_mastery(ks):
    concept = "applications_lineaires__theoreme_du_rang"
    base = ks.get_concept_prerequisites(concept)
    assert len(base) >= 2, "this concept should have several prerequisites"

    mastered_id = base[0]["id"]  # mark the top-confidence prerequisite as well mastered
    executor = ToolExecutor(ks, mastery={mastered_id: {"score": 0.95, "seen": 3}})
    result = json.loads(executor.execute("trouver_prerequis", {"concept_id": concept}))

    assert result["source"] == "concept_graph"
    by_id = {p["id"]: p for p in result["prerequisites"]}
    others = [p["priority"] for p in result["prerequisites"] if p["id"] != mastered_id]
    # A well-mastered prerequisite is deprioritised below at least one unmastered one.
    assert by_id[mastered_id]["priority"] < max(others)
    assert by_id[mastered_id]["mastery"] == 0.95


def test_update_mastery_ema():
    s = SessionState()
    s.update_mastery(["c1"], 100)
    assert s.mastery["c1"]["score"] == 1.0
    assert s.mastery["c1"]["seen"] == 1
    s.update_mastery(["c1"], 0)
    assert abs(s.mastery["c1"]["score"] - 0.6) < 1e-9  # 0.6*1.0 + 0.4*0.0
    assert s.mastery["c1"]["seen"] == 2

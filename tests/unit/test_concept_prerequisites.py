"""Tests for the concept-level prerequisite overlay (enrichment pipeline output).

These verify that the offline-generated overlay is loaded by KnowledgeService and
surfaced by the trouver_prerequis tool, with a graceful fall back to the coarse
chapter-level prerequisites when enrichment is disabled.
"""

import json

import pytest

from services.knowledge_service import KnowledgeService
from core.tools.executor import ToolExecutor

# An edge validated in the applications_lineaires pilot overlay.
CONCEPT = "applications_lineaires__definition_application_lineaire"
PREREQ = "espaces_vectoriels__definition_espace_vectoriel"


@pytest.fixture(scope="module")
def ks():
    return KnowledgeService()


def test_concept_level_prerequisites_loaded(ks):
    prereqs = ks.get_concept_prerequisites(CONCEPT)
    assert prereqs, "expected enriched concept-level prerequisites to be loaded"
    ids = [p["id"] for p in prereqs]
    assert PREREQ in ids
    edge = next(p for p in prereqs if p["id"] == PREREQ)
    assert edge["confidence"] is not None
    assert edge["title"]  # resolved from the graph/course data


def test_enriched_graph_flag_disables_overlay():
    ks_off = KnowledgeService(enriched_graph=False)
    assert ks_off.get_concept_prerequisites(CONCEPT) == []


def test_trouver_prerequis_tool_prefers_concept_graph(ks):
    executor = ToolExecutor(ks)
    result = json.loads(executor.execute("trouver_prerequis", {"concept_id": CONCEPT}))
    assert result["source"] == "concept_graph"
    assert any(p["id"] == PREREQ for p in result["prerequisites"])


def test_trouver_prerequis_tool_falls_back_to_chapter(ks):
    """A concept with no enriched prerequisites still yields chapter-level ones."""
    executor = ToolExecutor(ks)
    # Use only a chapter_id (no concept) -> must use the chapter fallback path.
    result = json.loads(executor.execute("trouver_prerequis", {"chapter_id": "applications_lineaires"}))
    assert result["source"] == "chapter_fallback"
    assert any(p["id"] == "espaces_vectoriels" for p in result["prerequisites"])

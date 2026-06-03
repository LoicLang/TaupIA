"""
Layer 1 of the concept-prerequisite enrichment pipeline: deterministic grounding.

For each "load-bearing" concept (definition / theorem / property / method) in a
chapter, build the list of REAL candidate prerequisites taken straight from the
knowledge graph:
  - same-chapter concepts with a strictly lower `order`
  - load-bearing concepts of the chapter's prerequisite chapters

The LLM extractor (next layer) only ever *selects* from these grounded
candidates, so it can never invent an edge to a node that does not exist.

Output is compact: a single `catalog` (id -> card) and a `content` table
(id -> statement excerpt) are stored once; each unit only references candidate
IDs. This keeps the payload small enough to pass around cheaply.

Usage:
    python scripts/build_extraction_units.py applications_lineaires
Writes:
    data/derived/extraction_units_<chapter>.json
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DERIVED = os.path.join(DATA, "derived")

# Only these types are nodes in the prerequisite dependency graph.
LOAD_BEARING = {"definition", "theorem", "property", "method"}

# How much statement text to keep (bounds token cost during verification).
STATEMENT_MAX = 600


def _label(node: dict) -> str:
    return node["labels"][0] if node.get("labels") else "?"


def load_graph() -> list[dict]:
    with open(os.path.join(DATA, "knowledge_graph.json"), encoding="utf-8") as f:
        return json.load(f)["nodes"]


def load_course_content(chapter_id: str) -> dict[str, str]:
    """id -> content_latex from data/cours/<chapter>.json (best effort)."""
    path = os.path.join(DATA, "cours", f"{chapter_id}.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        course = json.load(f)
    return {n["id"]: (n.get("content_latex") or "") for n in course.get("knowledge_nodes", [])}


def excerpt(text: str, limit: int) -> str:
    return " ".join(text.split())[:limit]


def build(chapter_id: str) -> dict:
    nodes = load_graph()
    chapters = {n["id"]: n for n in nodes if _label(n) == "Chapter"}
    concepts = [n for n in nodes if _label(n) == "Concept"]

    if chapter_id not in chapters:
        raise SystemExit(f"Unknown chapter '{chapter_id}'. Known: {sorted(chapters)[:5]}...")

    prereq_chapters = chapters[chapter_id]["properties"].get("prerequis", [])

    by_chapter: dict[str, list[dict]] = {}
    for c in concepts:
        by_chapter.setdefault(c["properties"]["chapter_id"], []).append(c)

    raw_content: dict[str, str] = {}
    for ch in [chapter_id, *prereq_chapters]:
        raw_content.update(load_course_content(ch))

    same_chapter = [c for c in by_chapter.get(chapter_id, []) if c["properties"]["type"] in LOAD_BEARING]
    same_chapter.sort(key=lambda c: c["properties"]["order"])

    cross = [
        c
        for ch in prereq_chapters
        for c in by_chapter.get(ch, [])
        if c["properties"]["type"] in LOAD_BEARING
    ]

    # Single catalog + content table, referenced by id everywhere else.
    catalog: dict[str, dict] = {}
    content: dict[str, str] = {}
    for c in same_chapter + cross:
        p = c["properties"]
        catalog[c["id"]] = {
            "title": p["title"],
            "type": p["type"],
            "order": p["order"],
            "chapter_id": p["chapter_id"],
        }
        content[c["id"]] = excerpt(raw_content.get(c["id"], ""), STATEMENT_MAX)

    cross_ids = [c["id"] for c in cross]
    units = []
    for c in same_chapter:
        order_c = c["properties"]["order"]
        same_ids = [d["id"] for d in same_chapter if d["properties"]["order"] < order_c]
        units.append({
            "concept_id": c["id"],
            "candidate_ids": same_ids + cross_ids,
        })

    return {
        "chapter_id": chapter_id,
        "prereq_chapters": prereq_chapters,
        "n_load_bearing": len(same_chapter),
        "catalog": catalog,
        "content": content,
        "units": units,
    }


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python scripts/build_extraction_units.py <chapter_id>")
    chapter_id = sys.argv[1]
    result = build(chapter_id)
    os.makedirs(DERIVED, exist_ok=True)
    out_path = os.path.join(DERIVED, f"extraction_units_{chapter_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    cand = [len(u["candidate_ids"]) for u in result["units"]]
    avg = sum(cand) / len(cand) if cand else 0
    print(f"chapter: {chapter_id}")
    print(f"prereq chapters: {result['prereq_chapters']}")
    print(f"load-bearing concepts (units): {result['n_load_bearing']}")
    print(f"catalog size: {len(result['catalog'])} concepts")
    print(f"candidates per unit: min={min(cand)} avg={avg:.1f} max={max(cand)}")
    print(f"written: {out_path}")


if __name__ == "__main__":
    main()

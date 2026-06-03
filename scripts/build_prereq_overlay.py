"""
Layer 4 of the concept-prerequisite enrichment pipeline: deterministic guardrails
+ overlay writer.

Takes the extraction/verification workflow output, keeps only edges that survived
adversarial verification, then enforces structural guardrails:
  - both endpoints exist as Concept nodes
  - no self-loop
  - same-chapter edge must point to a STRICTLY earlier `order` (a prerequisite
    cannot come after the concept that needs it)
  - no duplicate edges
  - the resulting concept->concept graph stays acyclic (DAG)

Writes data/derived/concept_prerequisites_<chapter>.json — the overlay the runtime
loads behind a flag — plus a stats report and a human-validation sample.

Usage:
    python scripts/build_prereq_overlay.py <workflow_output.json>
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DERIVED = os.path.join(DATA, "derived")


def _label(n: dict) -> str:
    return n["labels"][0] if n.get("labels") else "?"


def load_concepts() -> dict[str, dict]:
    with open(os.path.join(DATA, "knowledge_graph.json"), encoding="utf-8") as f:
        nodes = json.load(f)["nodes"]
    return {
        n["id"]: {"order": n["properties"]["order"], "chapter_id": n["properties"]["chapter_id"],
                  "type": n["properties"]["type"], "title": n["properties"]["title"]}
        for n in nodes if _label(n) == "Concept"
    }


def extract_results(blob) -> list[dict]:
    """Find the per-concept results list inside whatever JSON shape we were given."""
    if isinstance(blob, list):
        return blob
    if isinstance(blob, dict):
        if "results" in blob:
            return blob["results"]
        if "result" in blob and isinstance(blob["result"], dict):
            return blob["result"].get("results", [])
    raise SystemExit("Could not locate a 'results' list in the input JSON.")


def creates_cycle(edges: list[tuple[str, str]], new: tuple[str, str]) -> bool:
    """Would adding `new` (src->dst, meaning src REQUIRES dst) create a cycle?"""
    adj: dict[str, list[str]] = {}
    for s, d in edges + [new]:
        adj.setdefault(s, []).append(d)
    # DFS from new[1] trying to reach new[0]
    target, stack, seen = new[0], [new[1]], set()
    while stack:
        node = stack.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        stack.extend(adj.get(node, []))
    return False


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python scripts/build_prereq_overlay.py <workflow_output.json>")
    with open(sys.argv[1], encoding="utf-8") as f:
        results = extract_results(json.load(f))

    concepts = load_concepts()

    proposed = survived = 0
    edges: list[dict] = []
    edge_pairs: list[tuple[str, str]] = []
    dropped = {"unknown_id": 0, "self_loop": 0, "order": 0, "cycle": 0, "dup": 0}
    seen_pairs: set[tuple[str, str]] = set()

    for r in results:
        cid = r.get("concept_id")
        ex = {p["prereq_id"]: p for p in (r.get("extraction", {}) or {}).get("prerequisites", [])}
        verdicts = (r.get("verification", {}) or {}).get("verdicts", [])
        proposed += len(ex)
        for v in verdicts:
            if not v.get("survives"):
                continue
            survived += 1
            pid = v["prereq_id"]
            pair = (cid, pid)
            if cid not in concepts or pid not in concepts:
                dropped["unknown_id"] += 1; continue
            if cid == pid:
                dropped["self_loop"] += 1; continue
            same_chapter = concepts[cid]["chapter_id"] == concepts[pid]["chapter_id"]
            if same_chapter and concepts[pid]["order"] >= concepts[cid]["order"]:
                dropped["order"] += 1; continue
            if pair in seen_pairs:
                dropped["dup"] += 1; continue
            if creates_cycle(edge_pairs, pair):
                dropped["cycle"] += 1; continue
            seen_pairs.add(pair)
            edge_pairs.append(pair)
            edges.append({
                "source": cid,
                "target": pid,
                "type": "REQUIRES",
                "properties": {
                    "confidence": ex.get(pid, {}).get("confidence"),
                    "source_method": "llm_grounded_verified",
                    "extract_reason": ex.get(pid, {}).get("reason", ""),
                    "verify_reason": v.get("reason", ""),
                    "generated": True,
                },
            })

    out = {
        "schema": "concept_prerequisites_overlay/v1",
        "n_edges": len(edges),
        "edges": edges,
    }
    os.makedirs(DERIVED, exist_ok=True)
    out_path = os.path.join(DERIVED, "concept_prerequisites_applications_lineaires.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"proposed edges (extraction): {proposed}")
    print(f"survived adversarial verify: {survived}")
    print(f"kept after guardrails:       {len(edges)}")
    print(f"dropped: {dropped}")
    print(f"written: {out_path}")
    print()
    print("=== VALIDATION SAMPLE (concept  REQUIRES  prereq) ===")
    for e in edges[:25]:
        s, t = concepts[e["source"]], concepts[e["target"]]
        cross = "" if s["chapter_id"] == t["chapter_id"] else f"  [<-{t['chapter_id']}]"
        print(f"  {s['title'][:46]:46} REQUIRES  {t['title'][:42]}{cross}  (c={e['properties']['confidence']})")


if __name__ == "__main__":
    main()

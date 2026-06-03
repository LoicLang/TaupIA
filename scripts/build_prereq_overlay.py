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

Writes one data/derived/concept_prerequisites_<chapter>.json per chapter. Handles
both a single-chapter output ({chapter, results}) and a multi-chapter output
({chaptersResults: [{chapter, results}, ...]}).

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


def chapter_groups(blob) -> list[dict]:
    """Normalise the workflow output into a list of {chapter, results}."""
    root = blob.get("result", blob) if isinstance(blob, dict) else blob
    if isinstance(root, dict) and "chaptersResults" in root:
        return root["chaptersResults"]
    if isinstance(root, dict) and "results" in root:
        return [{"chapter": root.get("chapter", "unknown"), "results": root["results"]}]
    if isinstance(root, list):
        return [{"chapter": "unknown", "results": root}]
    raise SystemExit("Could not locate chapter results in the input JSON.")


def creates_cycle(edges: list[tuple[str, str]], new: tuple[str, str]) -> bool:
    """Would adding `new` (src->dst, src REQUIRES dst) create a cycle?"""
    adj: dict[str, list[str]] = {}
    for s, d in edges + [new]:
        adj.setdefault(s, []).append(d)
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


def process(chapter: str, results: list[dict], concepts: dict[str, dict]) -> dict:
    proposed = survived = 0
    edges: list[dict] = []
    edge_pairs: list[tuple[str, str]] = []
    refuted: list[tuple[str, str, str]] = []
    dropped = {"unknown_id": 0, "self_loop": 0, "order": 0, "cycle": 0, "dup": 0}
    seen_pairs: set[tuple[str, str]] = set()

    for r in results or []:
        cid = r.get("concept_id")
        ex = {p["prereq_id"]: p for p in (r.get("extraction", {}) or {}).get("prerequisites", [])}
        verdicts = (r.get("verification", {}) or {}).get("verdicts", [])
        proposed += len(ex)
        for v in verdicts:
            pid = v["prereq_id"]
            if not v.get("survives"):
                refuted.append((cid, pid, v.get("reason", "")))
                continue
            survived += 1
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
                "source": cid, "target": pid, "type": "REQUIRES",
                "properties": {
                    "confidence": ex.get(pid, {}).get("confidence"),
                    "source_method": "llm_grounded_verified",
                    "extract_reason": ex.get(pid, {}).get("reason", ""),
                    "verify_reason": v.get("reason", ""),
                    "generated": True,
                },
            })

    out_path = os.path.join(DERIVED, f"concept_prerequisites_{chapter}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"schema": "concept_prerequisites_overlay/v1", "n_edges": len(edges), "edges": edges},
                  f, ensure_ascii=False, indent=1)
    _write_validation_doc(chapter, edges, refuted, proposed, concepts)
    print(f"[{chapter}] proposed={proposed} survived={survived} kept={len(edges)} dropped={dropped} -> {os.path.basename(out_path)}")
    return {"chapter": chapter, "proposed": proposed, "survived": survived, "kept": len(edges)}


def _write_validation_doc(chapter, edges, refuted, proposed, concepts):
    """Emit a human-reviewable markdown: kept edges (precision) + refuted edges (recall)."""
    def title(i): return concepts.get(i, {}).get("title", i)
    def chap(i): return concepts.get(i, {}).get("chapter_id", "")
    def order(i): return concepts.get(i, {}).get("order", 0)

    kept_by_src: dict[str, list[dict]] = {}
    for e in edges:
        kept_by_src.setdefault(e["source"], []).append(e)
    refuted_by_src: dict[str, list[tuple[str, str]]] = {}
    for c, p, why in refuted:
        refuted_by_src.setdefault(c, []).append((p, why))

    md = [f"# Validation des prérequis — {chapter}", "",
          f"**{len(edges)} arêtes retenues** (proposées {proposed}, réfutées {len(refuted)}). "
          "`[<-chapitre]` = prérequis amont d'un autre chapitre.", "",
          "## Arêtes RETENUES (vérifier la précision)"]
    for s in sorted(kept_by_src, key=order):
        md.append(f"\n### {title(s)}")
        for e in sorted(kept_by_src[s], key=lambda x: -(x["properties"]["confidence"] or 0)):
            cross = "" if chap(e["target"]) == chapter else f"  [<-{chap(e['target'])}]"
            md.append(f"- **{title(e['target'])}**{cross} · conf {e['properties']['confidence']}")
            md.append(f"      {e['properties']['extract_reason']}")
    md.append("\n## Arêtes RÉFUTÉES (vérifier si le filtre est trop strict)")
    for s in refuted_by_src:
        md.append(f"\n### {title(s)}")
        for p, why in refuted_by_src[s]:
            md.append(f"- ~~{title(p)}~~ — {why}")

    with open(os.path.join(DERIVED, f"validation_{chapter}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python scripts/build_prereq_overlay.py <workflow_output.json>")
    with open(sys.argv[1], encoding="utf-8") as f:
        blob = json.load(f)
    concepts = load_concepts()
    os.makedirs(DERIVED, exist_ok=True)
    totals = [process(g["chapter"], g.get("results", []), concepts) for g in chapter_groups(blob)]
    if len(totals) > 1:
        print(f"TOTAL kept: {sum(t['kept'] for t in totals)} edges across {len(totals)} chapters")


if __name__ == "__main__":
    main()

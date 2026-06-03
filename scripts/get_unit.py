"""
Helper for the enrichment workflow: serve one concept's grounded slice on demand,
so each sub-agent fetches only what it needs (no giant payloads in any context).

Reads data/derived/extraction_units_<chapter>.json (produced by
build_extraction_units.py) and prints compact JSON.

Modes:
  list
      -> ["concept_id", ...]            (all load-bearing concept ids of the chapter)
  extract <concept_id>
      -> {"concept": {id,title,type,statement}, "candidates": [{id,title,type,chapter_id,order}, ...]}
  batch <id1,id2,...>
      -> [ {"concept": ..., "candidates": ...}, ... ]   (several extract units at once)
  statements <id1,id2,...>
      -> {id: statement_excerpt, ...}   (for the adversarial verifier)
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DERIVED = os.path.join(ROOT, "data", "derived")


def load(chapter_id: str) -> dict:
    with open(os.path.join(DERIVED, f"extraction_units_{chapter_id}.json"), encoding="utf-8") as f:
        return json.load(f)


def main():
    chapter_id, mode = sys.argv[1], sys.argv[2]
    data = load(chapter_id)
    catalog, content = data["catalog"], data["content"]

    units = {u["concept_id"]: u for u in data["units"]}

    def build_unit(cid: str) -> dict:
        concept = {"id": cid, **catalog[cid], "statement": content.get(cid, "")}
        candidates = [{"id": c, **catalog[c]} for c in units[cid]["candidate_ids"]]
        return {"concept": concept, "candidates": candidates}

    if mode == "list":
        print(json.dumps([u["concept_id"] for u in data["units"]]))

    elif mode == "extract":
        print(json.dumps(build_unit(sys.argv[3]), ensure_ascii=False))

    elif mode == "batch":
        print(json.dumps([build_unit(c) for c in sys.argv[3].split(",")], ensure_ascii=False))

    elif mode == "statements":
        ids = sys.argv[3].split(",")
        print(json.dumps({i: content.get(i, "") for i in ids}, ensure_ascii=False))

    else:
        raise SystemExit(f"unknown mode '{mode}'")


if __name__ == "__main__":
    main()

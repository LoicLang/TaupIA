"""
Helper for the enrichment workflow: serve one concept's grounded slice on demand,
so each sub-agent fetches only what it needs (no giant payloads in any context).

Reads data/derived/extraction_units_<chapter>.json (produced by
build_extraction_units.py) and prints compact JSON.

Modes:
  extract <concept_id>
      -> {"concept": {id,title,type,statement}, "candidates": [{id,title,type,chapter_id,order}, ...]}
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

    if mode == "extract":
        cid = sys.argv[3]
        unit = next(u for u in data["units"] if u["concept_id"] == cid)
        concept = {"id": cid, **catalog[cid], "statement": content.get(cid, "")}
        candidates = [{"id": c, **catalog[c]} for c in unit["candidate_ids"]]
        print(json.dumps({"concept": concept, "candidates": candidates}, ensure_ascii=False))

    elif mode == "statements":
        ids = sys.argv[3].split(",")
        print(json.dumps({i: content.get(i, "") for i in ids}, ensure_ascii=False))

    else:
        raise SystemExit(f"unknown mode '{mode}'")


if __name__ == "__main__":
    main()

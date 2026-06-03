# ADR 0001 — Concept-level prerequisite enrichment

- **Status:** Accepted (showcase / not yet in production)
- **Date:** 2026-06-03

## Context

TaupIA's examiner is an agent with tools over a knowledge graph. One tool,
`trouver_prerequis`, is meant to power *remediation* — when a student is stuck,
the agent walks "upstream" to find the missing notion ("you're blocked on the
rank theorem because the image/kernel notions aren't solid").

Auditing the graph showed this was not real:

- The graph has **49 `REQUIRES` edges, all chapter→chapter** (e.g.
  `applications_lineaires` → `espaces_vectoriels`). There are **zero
  concept→concept** prerequisites.
- The branch of `trouver_prerequis` that traversed concept-level `REQUIRES`
  edges was therefore **dead code** — it could never return anything.

So the agent could only say "review the whole *espaces vectoriels* chapter",
never "review *this specific definition*". Remediation needs concept-level
prerequisites, which did not exist.

A naive fix (heuristics over the `order` field + `TESTS` co-occurrence) produces
a *plausible* graph but not a *reliable* one: `order` is presentation order, not
logical dependency; co-occurrence is correlation, not causation. Equally, asking
an LLM "what are the prerequisites of X?" in the open hallucinates concepts that
don't exist as nodes.

## Decision

Generate concept→concept prerequisites with a **hybrid, grounded pipeline** —
deterministic structure where it earns reliability, LLM judgment where it earns
precision — and keep the output **separate from the source graph**, behind a flag,
with per-edge provenance.

Five layers (see `docs/design/graph-enrichment.md` for detail):

1. **Grounding (deterministic).** For each "load-bearing" concept (definition /
   theorem / property / method), build the candidate set from *real graph nodes*:
   same-chapter concepts of lower `order`, plus load-bearing concepts of the
   prerequisite chapters. The LLM only ever **selects** from this list, so it can
   never invent an edge to a non-existent node.
2. **Extraction (LLM).** A sub-agent judges which candidates are *direct*
   prerequisites, returning `{prereq_id, reason, confidence}`.
3. **Adversarial verification (independent LLM).** A separate skeptic sub-agent
   tries to **refute** each proposed edge. Only edges that survive are kept. This
   is where precision comes from — not a multi-vendor vote, but an independent
   "prove it's *not* a prerequisite" pass.
4. **Guardrails (deterministic).** Reject unknown ids, self-loops, same-chapter
   edges that point to a later `order`, duplicates, and any edge that would create
   a cycle (the result must stay a DAG).
5. **Human validation.** A domain expert validates a sample → a *measured*
   precision, not a promise.

Every kept edge carries `confidence`, `source_method`, and the extraction +
verification reasons, so the agent can weight or ignore weak edges and nothing is
ever presented as certified truth.

**Storage & control.** Edges are written to `data/derived/concept_prerequisites_*.json`
— never mutating `data/knowledge_graph.json`. `KnowledgeService` loads them behind
`enriched_graph` (default on; `enriched_graph=False` disables). `trouver_prerequis`
prefers concept-level prerequisites and falls back to chapter-level when none exist.

## Consequences

- `trouver_prerequis` becomes a real capability instead of dead code; remediation
  can target a specific upstream concept.
- The overlay is the **substrate for the future student-mastery layer**: a mastery
  score per concept, propagated along these `REQUIRES` edges, lets the agent say
  "structurally required *and* weakly mastered → review this first".
- Cost is a **one-time offline capex**, not a runtime cost: once generated and
  committed, lookups are free in-memory. The pilot was deliberately unoptimised
  (~2.5M tokens for 53 concepts); batching concepts per agent and using a cheaper
  Claude tier for extraction (Haiku) reduce this ~4–6×.
- Prerequisites are **probabilistic, not pedagogically certified**. The
  `confidence`/`source`/`reason` metadata and the flag make this explicit and
  reversible.

## Alternatives considered

- **Pure deterministic (order + co-occurrence).** Cheapest, but produces a
  plausible-not-reliable graph (false positives from presentation order). Kept only
  as the *grounding* and *guardrail* layers, not as the edge source.
- **Naive LLM ("list the prerequisites of X").** Hallucinates non-existent nodes;
  rejected in favour of grounded *selection* over real candidates.
- **Multi-vendor ensemble** (Claude + DeepSeek agree). Viable given the existing
  provider abstraction, but the **independent adversarial verifier** gives stronger
  precision than identical-model voting and keeps the pipeline single-model. Cross-
  vendor agreement remains an optional later cross-check.

## Open question (pedagogical, owner's call)

The verifier currently keeps a prerequisite only if it is needed to understand the
**statement** of a concept. A looser criterion — needed to **master** it (statement
*or* proof) — yields a richer graph better suited to remediation, at the cost of
more edges. The pilot uses the strict "statement" criterion; switching is a prompt
change + re-run.

# ADR 0002 — Agent navigation (deviation) and the mastery layer

- **Status:** Accepted (showcase / behind `ALLOW_DEVIATION`, not in production)
- **Date:** 2026-06-03

## Context

After [ADR 0001](0001-concept-prerequisite-enrichment.md), the examiner agent could
*read* the knowledge graph (definitions, theorems, concept-level prerequisites) but
could not *act* on the session, and it knew nothing about the individual student:

- The session was a rigid phase machine; an exercise was server-selected and fixed.
  A student could not say "give me a harder one / a different topic" and have it
  honoured — the only escape was a random same-difficulty skip.
- Prerequisites came back in a fixed order, blind to what the student had already
  shown they understood. Remediation pointed at *a* missing notion, not *their*
  missing notion.

## Decision

**Pillar 2 — navigation as intention-recording action tools.** Add `changer_exercice`
(and `consulter_profil_maitrise`) to the tool set, enabled only when `ALLOW_DEVIATION`
is set. Crucially, action tools do **not** mutate session state directly — that would
couple `core/tools/` to the backend. Instead they perform the lookup (via
`KnowledgeService`) and record an **intention** (`{"action": "set_exercise", ...}`) in
`ToolExecutor.intents`. The endpoint applies the intention to the session *after* the
agent turn. So the agent stays a pure function of (message, tools); the backend owns
state changes and remains auditable.

**Pillar 3 — an in-session mastery layer.** `SessionState.mastery` maps each concept
to `{score, seen}`, updated after every evaluation by blending the score (EMA) into
the concepts the question tested (`TESTS` edges). `trouver_prerequis` then ranks
prerequisites by **confidence × (1 − mastery)** — the gap that is *both* structurally
required *and* weakly mastered surfaces first. This is exactly where the enriched
concept→concept graph (ADR 0001) and the student profile meet.

## Consequences

- The agent is **steerable by the student** — verified live: "give me a harder one" →
  the agent calls `changer_exercice({"difficulty": 4})` and the active exercise
  switches. (This also confirmed real tool-calling on a non-Claude provider.)
- Remediation is **personalised** — a mastered prerequisite drops to the bottom of the
  list (priority ≈ 0.05) while unmastered ones rise.
- The intention pattern keeps `core/tools/` free of backend imports.
- Mastery is **in-session only** (lost at the 2h TTL). Durable per-user mastery
  (keyed on the Clerk identity, in a real store) is the aspirational next step toward
  cross-session personalisation.

## Alternatives considered

- **Tools mutate session state directly.** Simpler, but couples the domain tools to the
  backend session and hides side effects inside `core/`. Rejected.
- **Full agent-first `/turn` endpoint** replacing the phase machine entirely (the agent
  drives every transition). More capable but a large, riskier rewrite touching the
  frontend. Deferred — the action-tool + flag approach delivers the deviation
  capability incrementally without disturbing the production path.

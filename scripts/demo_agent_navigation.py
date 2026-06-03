"""Live end-to-end demo of pillars 2 (navigation) & 3 (mastery).

Runs the real agent against the configured LLM provider (default: DeepSeek),
so it needs a working key in .env. Two scenarios:

  1. Mastery-weighted remediation (no LLM): prerequisites are reordered so the
     gap that is BOTH required and weakly mastered surfaces first.
  2. Deviation (live LLM): the student asks for a different exercise and the
     agent calls the changer_exercice action tool, switching the active exercise.

Run: python scripts/demo_agent_navigation.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from services.knowledge_service import KnowledgeService
from core.tools.executor import ToolExecutor
from application import ai_service


def main():
    ks = KnowledgeService()

    print("=" * 70)
    print("PILIER 3 — Remédiation pondérée par la maîtrise")
    print("=" * 70)
    concept = "applications_lineaires__theoreme_du_rang"
    prs = ks.get_concept_prerequisites(concept)
    mastered_id = prs[0]["id"]  # pretend the student has mastered this one
    print(f"Concept travaillé : Théorème du rang")
    print(f"Élève suppose maîtriser : {prs[0]['title']} (score 0.95)\n")

    executor = ToolExecutor(ks, mastery={mastered_id: {"score": 0.95, "seen": 3}})
    res = json.loads(executor.execute("trouver_prerequis", {"concept_id": concept}))
    print("Remédiation priorisée (le maîtrisé tombe en bas) :")
    for p in res["prerequisites"]:
        flag = "  <- maîtrisé" if p["mastery"] is not None else ""
        print(f"  priorité {p['priority']:.2f}   {p['title']}{flag}")

    print()
    print("=" * 70)
    print("PILIER 2 — L'agent change d'exercice à la demande (LLM réel)")
    print("=" * 70)
    provider = ai_service.get_current_provider_name()
    print(f"Provider LLM : {provider}\n")

    executor = ToolExecutor(
        ks,
        session_context={"chapter_id": "applications_lineaires", "difficulty": 3, "done_exercises": []},
    )
    system = (
        "Tu es un khôlleur de maths MPSI, exigeant mais bienveillant. "
        "Tu disposes d'un outil changer_exercice : appelle-le quand l'étudiant "
        "demande un autre exercice (plus dur, plus facile, autre thème)."
    )
    student = "Cet exercice est un peu facile pour moi, donne-m'en un plus difficile."
    print(f"Élève : {student}\n")

    guidance = ai_service.agent_respond(
        user_message=student,
        system_prompt=system,
        tool_executor=executor.execute,
        include_actions=True,
    )
    print(f"Agent : {guidance[:280]}\n")
    print(f"Intentions enregistrées : {[i['action'] for i in executor.intents]}")
    if executor.intents:
        new_ex = executor.intents[-1]["exercise"]
        print(f"-> Nouvel exercice actif : {new_ex['id']} (difficulté {new_ex.get('difficulty')})")
        print(f"   Énoncé : {new_ex.get('enonce', '')[:180]}")
    else:
        print("-> L'agent n'a pas appelé l'outil (réponse en texte seul).")


if __name__ == "__main__":
    main()

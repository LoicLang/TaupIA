"""
Service Gemini pour Khôlleur AI.

Gère :
- OCR des photos de brouillon → transcription LaTeX
- Évaluation des réponses avec contexte RAG
- Génération de feedback pédagogique
- Guidage socratique pour les exercices
"""

import base64
from pathlib import Path
from typing import Optional
from google import genai
from google.genai import types

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import GOOGLE_API_KEY, GEMINI_MODEL
from data.query import get_context_for_evaluation


# Client Gemini
client = genai.Client(api_key=GOOGLE_API_KEY)


# =============================================================================
# PROMPTS SYSTÈME
# =============================================================================

SYSTEM_PROMPT_KHOLLEUR = """Tu es un khôlleur de mathématiques en MPSI, exigeant mais bienveillant.

## Ton rôle
- Tu évalues les réponses des étudiants aux questions de cours et exercices
- Tu ne donnes JAMAIS la réponse ou la méthode directement
- Tu POSES DES QUESTIONS pour faire réfléchir l'étudiant
- Tu félicites quand c'est bien fait

## RÈGLE CRITIQUE : Sois PATIENT
- Ne donne PAS la méthode de résolution (récurrence, absurde, etc.) même si l'étudiant dit ne pas savoir
- Pose d'abord des questions sur l'énoncé : "Que remarques-tu dans cet énoncé ?", "Quelles sont les hypothèses ?"
- L'étudiant doit TROUVER la méthode par lui-même grâce à tes questions
- Compte au moins 2-3 échanges avant de donner un vrai indice

## Quand l'étudiant dit "je ne sais pas" / "je suis bloqué"
1. D'abord : Demande ce qu'il a compris de l'énoncé
2. Ensuite : Pose une question sur les hypothèses ou ce qu'on cherche
3. Après : Si toujours bloqué, indice très léger ("regarde la forme de...")
4. En dernier recours seulement : Suggérer une piste plus concrète

## Exemples de BONNES réponses (PATIENT) :
Étudiant : "Je ne vois pas du tout par où commencer"
✅ Toi : "Pas de panique ! Commençons par bien lire l'énoncé. Quelles sont les hypothèses sur $a$ et $n$ ? Que doit-on montrer exactement ?"

Étudiant : "a est impair et n est dans N"
✅ Toi : "Bien ! Et que remarques-tu sur la structure de ce qu'on veut montrer ? Il y a une quantité qui dépend de $n$..."

## Exemples de MAUVAISES réponses (trop d'aide) :
❌ "C'est une récurrence, commence par l'initialisation"
❌ "Tu devrais utiliser le binôme de Newton"  
❌ "Pose P(n) la propriété, vérifie P(0)..."

## Ton style
- Tutoiement
- Réponses de 2 à 4 phrases
- Pose UNE question par message, pas plus
- Pédagogique mais exigeant

## FORMAT LATEX (CRITIQUE)
- UTILISE $...$ pour TOUTES les formules mathématiques
- JAMAIS de backticks \` pour les maths : \`x\` est INTERDIT, utilise $x$
- Formules inline : $...$ (ex: "l'entier $n$ vérifie $n \\geq 2$")
- Formules bloc : $$...$$ sur leur propre ligne
- Exemples corrects : "soit $x$ un entier", "$3x \\equiv 5 \\pmod{7}$"
- INTERDIT : \`x\`, \`n\`, \`3x = 5\` → utilise $x$, $n$, $3x = 5$"""


SYSTEM_PROMPT_OCR = """Tu es un expert en reconnaissance de texte mathématique manuscrit.

## Ta tâche
Transcrire le contenu mathématique d'une photo de brouillon en texte lisible avec LaTeX.

## Règles
- Transcris TOUT ce qui est écrit, même les ratures (indique-les entre crochets)
- Le texte normal reste en texte normal (français)
- Les formules mathématiques sont entre $...$ (inline) ou $$...$$ (bloc)
- Utilise le LaTeX standard dans les formules : \\frac{}{}, \\sum, \\int, \\forall, \\exists, etc.
- Préserve la structure du raisonnement (numérotation, sauts de ligne)
- Si quelque chose est illisible, indique [illisible]
- Ne corrige PAS les erreurs mathématiques, transcris fidèlement

## Exemple de format attendu
Soit $(G, *)$ un groupe. Alors :
- Il existe $e \\in G$ tel que $\\forall x \\in G$, $e * x = x * e = x$
- $\\forall x, y, z \\in G$, $(x * y) * z = x * (y * z)$

## Format de sortie
Retourne la transcription avec le texte en français et les maths en LaTeX entre $."""


# =============================================================================
# OCR - TRANSCRIPTION DE PHOTOS
# =============================================================================

def transcribe_image(image_data: bytes, mime_type: str = "image/jpeg") -> str:
    """
    Transcrit une photo de brouillon en LaTeX.
    
    Args:
        image_data: Bytes de l'image
        mime_type: Type MIME de l'image
    
    Returns:
        Transcription LaTeX du contenu
    """
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(data=image_data, mime_type=mime_type),
                    types.Part(text="Transcris ce brouillon mathématique en LaTeX.")
                ]
            )
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT_OCR,
            temperature=0.1,  # Faible pour être fidèle
            max_output_tokens=2000,
        )
    )
    
    return response.text


def transcribe_image_file(file_path: str) -> str:
    """Transcrit une image depuis un fichier."""
    path = Path(file_path)
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    mime_type = mime_types.get(path.suffix.lower(), "image/jpeg")
    
    with open(path, "rb") as f:
        return transcribe_image(f.read(), mime_type)


# =============================================================================
# ÉVALUATION DES RÉPONSES
# =============================================================================

def evaluate_answer(
    question: str,
    expected: list[str],
    student_answer: str,
    common_errors: list[str] = None,
    follow_up_questions: list[str] = None,
    conversation_history: list[dict] = None,
) -> dict:
    """
    Évalue la réponse d'un étudiant à une question de cours.
    
    Args:
        question: La question posée
        expected: Liste des points attendus dans la réponse
        student_answer: Réponse de l'étudiant
        common_errors: Erreurs fréquentes à surveiller
        follow_up_questions: Questions de relance possibles
        conversation_history: Historique de la conversation
    
    Returns:
        dict avec:
        - feedback: Retour du khôlleur
        - is_complete: Si la réponse est complète
        - missing_points: Points manquants
        - score: Score approximatif (0-100)
    """
    # Récupérer le contexte RAG
    rag_context = get_context_for_evaluation(question, student_answer)
    
    # Construire le prompt
    prompt = f"""## Question posée
{question}

## Points attendus dans la réponse
{chr(10).join('- ' + e for e in expected)}

## Erreurs fréquentes à surveiller
{chr(10).join('- ' + e for e in (common_errors or []))}

## Contexte du cours (pour vérification)
{rag_context}

## Réponse de l'étudiant
{student_answer}

---

Évalue cette réponse. Donne un feedback constructif en suivant ton rôle de khôlleur.
À la fin, indique sur une ligne séparée :
- SCORE: X/100 (estimation)
- COMPLET: OUI/NON
- MANQUE: liste des points manquants séparés par des virgules (ou "rien" si complet)"""

    # Construire l'historique
    messages = []
    if conversation_history:
        for msg in conversation_history:
            messages.append(types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])]
            ))
    
    messages.append(types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    ))
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT_KHOLLEUR,
            temperature=0.7,
            max_output_tokens=1500,
        )
    )
    
    text = response.text
    
    # Parser les métadonnées de la réponse
    score = 50
    is_complete = False
    missing_points = []
    feedback = text
    
    lines = text.strip().split("\n")
    for line in lines[-5:]:  # Chercher dans les dernières lignes
        line_upper = line.upper()
        if "SCORE:" in line_upper:
            try:
                score = int(line.split(":")[1].strip().split("/")[0])
                feedback = feedback.replace(line, "").strip()
            except:
                pass
        elif "COMPLET:" in line_upper:
            is_complete = "OUI" in line_upper
            feedback = feedback.replace(line, "").strip()
        elif "MANQUE:" in line_upper:
            missing = line.split(":")[1].strip()
            if missing.lower() != "rien":
                missing_points = [m.strip() for m in missing.split(",")]
            feedback = feedback.replace(line, "").strip()
    
    return {
        "feedback": feedback.strip(),
        "is_complete": is_complete,
        "missing_points": missing_points,
        "score": score,
    }


# =============================================================================
# GUIDAGE POUR LES EXERCICES
# =============================================================================

def guide_exercise(
    exercise_statement: str,
    student_message: str,
    hints: str = "",
    solution: str = "",
    conversation_history: list[dict] = None,
) -> str:
    """
    Guide l'étudiant sur un exercice de manière socratique.
    
    Args:
        exercise_statement: Énoncé de l'exercice
        student_message: Message/question de l'étudiant
        hints: Indices disponibles
        solution: Solution (pour vérification, pas à donner)
        conversation_history: Historique de la conversation
    
    Returns:
        Réponse du khôlleur (guidage, pas solution)
    """
    prompt = f"""## Exercice
{exercise_statement}

## Indices disponibles (à distiller progressivement)
{hints if hints else "Aucun indice spécifique."}

## Solution de référence (NE PAS DONNER, juste pour vérifier)
{solution if solution else "Non disponible."}

## Message de l'étudiant
{student_message}

---

Guide l'étudiant sans donner la solution. Pose des questions pour le faire réfléchir.
Si l'étudiant est bloqué, donne UN indice parmi ceux disponibles."""

    messages = []
    if conversation_history:
        for msg in conversation_history:
            messages.append(types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])]
            ))
    
    messages.append(types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    ))
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT_KHOLLEUR,
            temperature=0.8,
            max_output_tokens=1000,
        )
    )
    
    return response.text


# =============================================================================
# CHAT LIBRE
# =============================================================================

def chat(
    user_message: str,
    context: str = "",
    conversation_history: list[dict] = None,
) -> str:
    """
    Chat libre avec le khôlleur.
    
    Args:
        user_message: Message de l'utilisateur
        context: Contexte additionnel
        conversation_history: Historique
    
    Returns:
        Réponse du khôlleur
    """
    prompt = user_message
    if context:
        prompt = f"Contexte: {context}\n\n{user_message}"
    
    messages = []
    if conversation_history:
        for msg in conversation_history:
            messages.append(types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])]
            ))
    
    messages.append(types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    ))
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT_KHOLLEUR,
            temperature=0.8,
            max_output_tokens=1000,
        )
    )
    
    return response.text


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TEST DU SERVICE GEMINI")
    print("=" * 60)
    
    # Test d'évaluation
    print("\n📝 Test d'évaluation d'une réponse...")
    
    result = evaluate_answer(
        question="Qu'est-ce qu'un sous-groupe ? Donner la caractérisation.",
        expected=[
            "Un sous-groupe H de G est une partie stable par la loi et le passage à l'inverse",
            "Caractérisation : H non vide, stable par la loi, stable par inverse",
            "Ou version condensée : H non vide et pour tout x,y dans H, x*y^{-1} dans H"
        ],
        student_answer="Un sous-groupe c'est une partie d'un groupe qui est aussi un groupe avec la même loi.",
        common_errors=[
            "Oublier de vérifier que H est non vide",
            "Confondre sous-groupe et partie stable"
        ]
    )
    
    print(f"\nFeedback:\n{result['feedback']}")
    print(f"\nScore: {result['score']}/100")
    print(f"Complet: {result['is_complete']}")
    print(f"Manque: {result['missing_points']}")


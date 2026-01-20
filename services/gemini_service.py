"""
Service Gemini pour Khôlleur AI.

Gère :
- OCR des photos de brouillon → transcription LaTeX
- Évaluation des réponses avec contexte RAG
- Génération de feedback pédagogique
- Guidage socratique pour les exercices
"""

import base64
import time
from pathlib import Path
from typing import Optional
from google import genai
from google.genai import types
from google.api_core import exceptions as google_exceptions

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import GOOGLE_API_KEY, GEMINI_MODEL
from data.query import get_context_for_evaluation


# Client Gemini
client = genai.Client(api_key=GOOGLE_API_KEY)


# =============================================================================
# RETRY LOGIC POUR GÉRER LES ERREURS 503
# =============================================================================

def call_gemini_with_retry(func, max_retries=3, initial_delay=2):
    """
    Wrapper pour appeler Gemini avec retry et backoff exponentiel.

    Args:
        func: Fonction lambda qui fait l'appel à Gemini
        max_retries: Nombre maximum de tentatives
        initial_delay: Délai initial en secondes (doublé à chaque retry)

    Returns:
        Réponse de l'API Gemini

    Raises:
        Exception: Si toutes les tentatives échouent
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            error_str = str(e)

            # Vérifier si c'est une erreur temporaire (503 ou 500)
            is_retryable = (
                "503" in error_str or
                "500" in error_str or
                "overloaded" in error_str.lower() or
                "internal" in error_str.lower()
            )

            if is_retryable:
                if attempt < max_retries - 1:
                    # Message adapté selon le type d'erreur
                    if "503" in error_str or "overloaded" in error_str.lower():
                        msg = f"⚠️ Gemini surchargé, nouvelle tentative dans {delay}s... (tentative {attempt + 1}/{max_retries})"
                    else:
                        msg = f"⚠️ Erreur serveur Gemini, nouvelle tentative dans {delay}s... (tentative {attempt + 1}/{max_retries})"
                    print(msg)
                    time.sleep(delay)
                    delay *= 2  # Backoff exponentiel
                    continue
                else:
                    # Dernière tentative échouée
                    raise Exception(
                        f"Gemini a rencontré des erreurs après {max_retries} tentatives. "
                        f"Réessaie dans quelques minutes."
                    ) from e
            else:
                # Autre type d'erreur, ne pas retry
                raise e

    # Si on arrive ici, toutes les tentatives ont échoué
    raise last_exception


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

## VALIDATION RÉALISTE (COMME EN KHÔLLE RÉELLE)
En khôlle, on ne rédige pas tout au tableau ! Tu dois marquer COMPLET: OUI si l'étudiant a :
1. Montré qu'il COMPREND le raisonnement (même si pas tout rédigé)
2. Donné les ÉTAPES CLÉS et la STRUCTURE de la démonstration
3. Utilisé les BONS OUTILS mathématiques (théorèmes, définitions)
4. Pas d'erreur conceptuelle grave

IMPORTANT : Si le raisonnement est BON et que l'étudiant sait QUOI FAIRE, même sans tout rédiger → COMPLET: OUI

Tu dois marquer COMPLET: NON seulement si :
- Raisonnement faux ou incomplet
- Confusion sur les concepts clés
- Ne sait pas quelle méthode utiliser

IMPORTANT : Si tu marques COMPLET: OUI, termine par une FÉLICITATION et dis "Tu peux passer à l'exercice." SANS poser de nouvelle question.

Score :
- 85-100 : Raisonnement solide, comprend bien → COMPLET: OUI
- 70-84 : Raisonnement correct mais lacunes mineures → COMPLET: OUI si >75
- 60-69 : Raisonnement incomplet ou confus → COMPLET: NON
- <60 : Raisonnement faux ou manque de base → COMPLET: NON

## Ton style
- Tutoiement
- Réponses de 2 à 4 phrases
- Pose UNE question par message, pas plus
- Pédagogique mais exigeant

## FORMAT LATEX (ABSOLUMENT CRITIQUE - AUCUNE EXCEPTION)
RÈGLE ABSOLUE : TOUT symbole mathématique DOIT être entre $...$ ou $$...$$

✅ CORRECT :
- "soit $n$ un entier"
- "on a $p_1 \\mid n$"
- "l'entier $n \\geq 2$"
- "$3x \\equiv 5 \\pmod{7}$"
- "$$n = p_1 p_2 \\cdots p_m$$"

❌ INTERDIT (tu dois TOUJOURS corriger) :
- "soit n un entier" → FAUX, écris "soit $n$ un entier"
- "p_1 divise n" → FAUX, écris "$p_1$ divise $n$"
- "\mid" seul → FAUX, écris "$\\mid$"
- Backticks \`n\` → INTERDIT, utilise $n$

VÉRIFIE CHAQUE LIGNE : Si tu vois une variable ou symbole math SANS $, c'est une ERREUR.
Relis ta réponse avant de l'envoyer et entoure TOUS les symboles de $...$"""


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

def _resize_image_if_needed(image_data: bytes, mime_type: str, max_size_mb: float = 4.0) -> bytes:
    """
    Redimensionne l'image si elle dépasse la taille max (pour éviter erreurs API).

    Args:
        image_data: Bytes de l'image originale
        mime_type: Type MIME
        max_size_mb: Taille max en MB (default: 4MB, limite safe pour Gemini)

    Returns:
        Bytes de l'image (redimensionnée si nécessaire)
    """
    from PIL import Image
    import io

    size_mb = len(image_data) / (1024 * 1024)
    if size_mb <= max_size_mb:
        return image_data

    # Image trop grande, la redimensionner
    img = Image.open(io.BytesIO(image_data))

    # Calculer le ratio de réduction nécessaire
    reduction_ratio = (max_size_mb / size_mb) ** 0.5  # Racine carrée car surface

    new_width = int(img.width * reduction_ratio)
    new_height = int(img.height * reduction_ratio)

    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Sauvegarder dans un buffer
    buffer = io.BytesIO()
    if mime_type == "image/png":
        img_resized.save(buffer, format="PNG", optimize=True)
    else:
        img_resized.save(buffer, format="JPEG", quality=85, optimize=True)

    return buffer.getvalue()


def transcribe_image(image_data: bytes, mime_type: str = "image/jpeg") -> str:
    """
    Transcrit une photo de brouillon en LaTeX.

    Args:
        image_data: Bytes de l'image
        mime_type: Type MIME de l'image

    Returns:
        Transcription LaTeX du contenu
    """
    # Redimensionner si nécessaire pour éviter erreurs API
    image_data = _resize_image_if_needed(image_data, mime_type)

    def _call():
        return client.models.generate_content(
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

    response = call_gemini_with_retry(_call)
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

    # Construire l'historique (limité pour éviter de surcharger l'API)
    messages = []
    if conversation_history:
        # Limiter en nombre de messages ET en tokens approximatifs
        max_history_chars = 4000  # ~1000 tokens
        recent_history = conversation_history[-20:] if len(conversation_history) > 20 else conversation_history

        # Compter les caractères et prendre uniquement ce qui rentre
        total_chars = 0
        messages_to_add = []
        for msg in reversed(recent_history):  # Partir de la fin (plus récent)
            msg_length = len(msg["content"])
            if total_chars + msg_length > max_history_chars:
                break
            messages_to_add.insert(0, msg)  # Insérer au début pour garder l'ordre
            total_chars += msg_length

        for msg in messages_to_add:
            messages.append(types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])]
            ))

    messages.append(types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    ))

    def _call():
        return client.models.generate_content(
            model=GEMINI_MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT_KHOLLEUR,
                temperature=0.7,
                max_output_tokens=4096,  # Maximum pour éviter troncature
            )
        )

    response = call_gemini_with_retry(_call)

    # Vérifier que la réponse n'est pas vide
    if not response.text:
        return {
            "feedback": "Désolé, je n'ai pas pu générer de réponse. Peux-tu reformuler ta réponse ?",
            "is_complete": False,
            "missing_points": [],
            "score": 0,
        }

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
        # Limiter en nombre de messages ET en tokens approximatifs
        max_history_chars = 6000  # ~1500 tokens (exercices peuvent être plus longs)
        recent_history = conversation_history[-30:] if len(conversation_history) > 30 else conversation_history

        # Compter les caractères et prendre uniquement ce qui rentre
        total_chars = 0
        messages_to_add = []
        for msg in reversed(recent_history):  # Partir de la fin (plus récent)
            msg_length = len(msg["content"])
            if total_chars + msg_length > max_history_chars:
                break
            messages_to_add.insert(0, msg)  # Insérer au début pour garder l'ordre
            total_chars += msg_length

        for msg in messages_to_add:
            messages.append(types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])]
            ))

    messages.append(types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    ))

    def _call():
        return client.models.generate_content(
            model=GEMINI_MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT_KHOLLEUR,
                temperature=0.8,
                max_output_tokens=4096,  # Maximum pour éviter troncature
            )
        )

    response = call_gemini_with_retry(_call)

    # Vérifier que la réponse n'est pas vide
    if not response.text:
        return "Désolé, je n'ai pas pu générer de réponse. Peux-tu reformuler ta question ?"

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
        # Limiter en nombre de messages ET en tokens approximatifs
        max_history_chars = 6000  # ~1500 tokens (exercices peuvent être plus longs)
        recent_history = conversation_history[-30:] if len(conversation_history) > 30 else conversation_history

        # Compter les caractères et prendre uniquement ce qui rentre
        total_chars = 0
        messages_to_add = []
        for msg in reversed(recent_history):  # Partir de la fin (plus récent)
            msg_length = len(msg["content"])
            if total_chars + msg_length > max_history_chars:
                break
            messages_to_add.insert(0, msg)  # Insérer au début pour garder l'ordre
            total_chars += msg_length

        for msg in messages_to_add:
            messages.append(types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])]
            ))

    messages.append(types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    ))

    def _call():
        return client.models.generate_content(
            model=GEMINI_MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT_KHOLLEUR,
                temperature=0.8,
                max_output_tokens=4096,  # Maximum pour éviter troncature
            )
        )

    response = call_gemini_with_retry(_call)

    # Vérifier que la réponse n'est pas vide
    if not response.text:
        return "Désolé, je n'ai pas pu générer de réponse. Peux-tu reformuler ?"

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


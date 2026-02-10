"""
Khôlleur AI - Application Streamlit

Simule des khôlles de maths MPSI avec :
- Questions de cours
- Exercices adaptés au niveau
- Feedback pédagogique via Gemini
- OCR pour les photos de brouillon
"""

import streamlit as st
import json
from typing import Optional

# Configuration de la page (DOIT être en premier)
st.set_page_config(
    page_title="TaupIA - Khôlleur AI",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "TaupIA - Simulateur de khôlles MPSI"
    }
)

from services.knowledge_service import (
    get_chapters,
    get_random_question,
    get_exercise_by_difficulty,
    get_collection_stats,
    get_exercise_for_concepts,
    get_concepts_for_question,
)
# Import du router AI qui gère Claude/Gemini
from services.ai_router import (
    evaluate_answer,
    guide_exercise,
    transcribe_image,
    chat,
    get_available_providers,
    get_available_ocr_providers,
)
from application.settings import get_settings
from pathlib import Path


# =============================================================================
# STYLES CSS (chargé depuis fichier externe)
# =============================================================================

def load_css():
    """Charge le CSS depuis le fichier externe."""
    css_path = Path(__file__).parent / "ui" / "streamlit" / "styles.css"
    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

load_css()


# CSS a été déplacé vers ui/streamlit/styles.css


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_base64_image(image_path: str) -> str:
    """Encode une image en base64 pour l'afficher en HTML."""
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# =============================================================================
# ÉTAT DE LA SESSION
# =============================================================================

# Phases de la khôlle (strings simples pour éviter les problèmes avec Enum)
PHASE_SETUP = "setup"
PHASE_QUESTION = "question_cours"
PHASE_EXERCICE = "exercice"
PHASE_FINISHED = "finished"


def init_session_state():
    """Initialise l'état de la session."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.phase = PHASE_SETUP
        st.session_state.chapter_id = None
        st.session_state.difficulty = 3
        st.session_state.ai_provider = "gemini"  # "claude" ou "gemini"
        st.session_state.current_question = None
        st.session_state.current_exercise = None
        st.session_state.conversation_history = []
        st.session_state.question_validated = False
        st.session_state.asked_questions = []
        st.session_state.done_exercises = []
        st.session_state.scores = []
        # Debug mode
        st.session_state.debug_prompt_mode = False
        st.session_state.debug_prompt_data = {}
        # UI state management pour éviter doubles soumissions
        st.session_state.is_processing = False


init_session_state()


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar():
    """Affiche la sidebar avec les options."""
    with st.sidebar:
        st.markdown("## Configuration")
        
        # Stats
        try:
            stats = get_collection_stats()
            st.caption(f"{stats['questions_cours']['count']} questions · {stats['exercices']['count']} exercices")
        except:
            pass
        
        st.divider()
        
        # Choix du chapitre
        chapters = get_chapters()
        chapter_options = {ch['title']: ch['id'] for ch in chapters}
        chapter_ids = list(chapter_options.values())

        # Calculer l'index courant depuis session_state
        current_idx = 0
        if st.session_state.chapter_id in chapter_ids:
            current_idx = chapter_ids.index(st.session_state.chapter_id)

        selected_chapter = st.selectbox(
            "Chapitre",
            options=list(chapter_options.keys()),
            index=current_idx if chapter_options else None,
            help="Sélectionner le chapitre"
        )

        if selected_chapter:
            st.session_state.chapter_id = chapter_options[selected_chapter]
        
        st.divider()
        
        # Difficulté
        st.session_state.difficulty = st.slider(
            "Niveau",
            min_value=1,
            max_value=5,
            value=st.session_state.difficulty,
            help="1 = Facile, 5 = Expert"
        )
        
        # Afficher les étoiles
        stars = "★" * st.session_state.difficulty + "☆" * (5 - st.session_state.difficulty)
        st.markdown(f"<p class='difficulty'>{stars}</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # Actions
        if st.button("Nouvelle session", use_container_width=True, type="primary"):
            start_new_kholle()

        if st.session_state.phase != PHASE_SETUP:
            if st.button("Reset", use_container_width=True):
                reset_kholle()
        
        # Scores
        if st.session_state.scores:
            st.divider()
            st.markdown("### Statistiques")
            avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
            st.metric("Score moyen", f"{avg_score:.0f}/100")
        
        # Providers AI et OCR
        st.divider()
        st.markdown("### Modèles")

        # Sélecteur AI Provider (Khôlleur) - désactivé pendant une khôlle
        available_ai = get_available_providers()
        ai_labels = {
            "gemini": "Gemini",
            "claude": "Claude",
            "deepseek": "DeepSeek (V3.2)",
            "kimi": "Kimi (K2.5)",
        }

        # Désactiver si khôlle en cours (pas en phase setup)
        is_kholle_in_progress = st.session_state.phase != PHASE_SETUP

        if len(available_ai) > 1:
            options_ai = [ai_labels.get(p, p) for p in available_ai]
            current_ai = st.session_state.get("ai_provider", "gemini")
            current_ai_index = available_ai.index(current_ai) if current_ai in available_ai else 0

            selected_ai_label = st.selectbox(
                "Khôlleur",
                options=options_ai,
                index=current_ai_index,
                help="Changer avant de démarrer" if is_kholle_in_progress else "Modèle IA pour les interactions",
                disabled=is_kholle_in_progress
            )

            # Mettre à jour le provider si changé (seulement si pas désactivé)
            if not is_kholle_in_progress:
                selected_ai = available_ai[options_ai.index(selected_ai_label)]
                if selected_ai != st.session_state.get("ai_provider"):
                    st.session_state.ai_provider = selected_ai

        # Sélecteur OCR Provider
        available_ocr = get_available_ocr_providers()
        ocr_labels = {
            "gemini": "Gemini",
            "kimi": "Kimi (K2.5)",
        }

        if len(available_ocr) > 1:
            # Initialiser le provider dans session_state si pas déjà fait
            if "ocr_provider" not in st.session_state:
                st.session_state.ocr_provider = get_settings().ocr_provider

            options_ocr = [ocr_labels.get(p, p) for p in available_ocr]
            current_ocr = st.session_state.ocr_provider
            current_ocr_index = available_ocr.index(current_ocr) if current_ocr in available_ocr else 0

            selected_ocr_label = st.selectbox(
                "OCR",
                options=options_ocr,
                index=current_ocr_index,
                help="Modèle pour la lecture des photos"
            )

            # Mettre à jour le provider si changé
            selected_ocr = available_ocr[options_ocr.index(selected_ocr_label)]
            if selected_ocr != st.session_state.ocr_provider:
                st.session_state.ocr_provider = selected_ocr

        # Debug Prompt Mode
        st.divider()
        st.markdown("### Avance")
        st.session_state.debug_prompt_mode = st.toggle(
            "Mode Debug Prompt",
            value=st.session_state.debug_prompt_mode,
            help="Affiche le prompt enrichi envoye au LLM"
        )


def start_new_kholle():
    """Démarre une nouvelle khôlle."""
    if not st.session_state.chapter_id:
        st.error("Choisis d'abord un chapitre !")
        return
    
    # Tirer une question
    question = get_random_question(
        chapter_id=st.session_state.chapter_id,
        difficulty=st.session_state.difficulty,
        exclude_ids=st.session_state.asked_questions
    )
    
    if not question:
        st.error("Plus de questions disponibles pour ce chapitre !")
        return
    
    st.session_state.current_question = question
    st.session_state.asked_questions.append(question["id"])
    st.session_state.phase = PHASE_QUESTION
    st.session_state.conversation_history = []
    st.session_state.question_validated = False


def reset_kholle():
    """Remet à zéro la khôlle en cours."""
    st.session_state.phase = PHASE_SETUP
    st.session_state.current_question = None
    st.session_state.current_exercise = None
    st.session_state.conversation_history = []
    st.session_state.question_validated = False


# =============================================================================
# PHASE: SETUP MOBILE-FIRST
# =============================================================================

def render_setup_mobile():
    """Écran d'accueil optimisé mobile avec sélection chapitre/difficulté."""
    
    # Message d'accueil compact
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <p style="font-size: 0.8rem; color: #888; margin: 0; text-transform: uppercase; letter-spacing: 0.1em; font-family: 'Inter', sans-serif;">
            Initialiser une session
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sélection du chapitre (synchronise avec la sidebar)
    chapters = get_chapters()
    chapter_options = {ch['title']: ch['id'] for ch in chapters}
    chapter_ids = list(chapter_options.values())

    # Calculer l'index courant depuis session_state
    current_idx = 0
    if st.session_state.chapter_id in chapter_ids:
        current_idx = chapter_ids.index(st.session_state.chapter_id)

    selected_chapter = st.selectbox(
        "Chapitre",
        options=list(chapter_options.keys()),
        index=current_idx if chapter_options else None,
        key="mobile_chapter_select"
    )

    if selected_chapter:
        st.session_state.chapter_id = chapter_options[selected_chapter]

    # Sélection de la difficulté avec boutons radio visuels
    st.markdown("##### Niveau")

    difficulty_labels = {
        1: "01 · Facile",
        2: "02 · Accessible",
        3: "03 · Standard",
        4: "04 · Difficile",
        5: "05 · Expert"
    }

    selected_difficulty = st.radio(
        "Niveau",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: difficulty_labels[x],
        index=st.session_state.difficulty - 1,
        horizontal=True,
        label_visibility="collapsed",
        key="mobile_difficulty_select"
    )
    st.session_state.difficulty = selected_difficulty
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grand bouton de lancement
    if st.button(
        "Démarrer",
        type="primary",
        use_container_width=True,
        key="mobile_start_btn"
    ):
        start_new_kholle()
        st.rerun()
    
    # Info discrète
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 0 0;">
        <small style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #aaa; text-transform: uppercase; letter-spacing: 0.1em;">
            Question → Exercice → Résultats
        </small>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PHASE: QUESTION DE COURS
# =============================================================================

def render_progress_bar(current_phase: str):
    """Affiche la progress bar visuelle selon la phase actuelle."""
    phases = [
        ("setup", "Configuration", "01"),
        ("question_cours", "Question", "02"),
        ("exercice", "Exercice", "03"),
        ("finished", "Résultats", "04")
    ]
    
    phase_order = [p[0] for p in phases]
    current_idx = phase_order.index(current_phase) if current_phase in phase_order else 0
    
    html_parts = ['<div class="progress-container">']
    
    for i, (phase_id, label, icon) in enumerate(phases):
        if i > 0:
            # Connecteur
            connector_class = "completed" if i <= current_idx else ""
            html_parts.append(f'<div class="progress-connector {connector_class}"></div>')
        
        # Étape
        if i < current_idx:
            step_class = "completed"
            step_icon = "✓"
        elif i == current_idx:
            step_class = "active"
            step_icon = str(i + 1)
        else:
            step_class = ""
            step_icon = str(i + 1)
        
        html_parts.append(f'''
            <div class="progress-step {step_class}">
                <span class="step-number">{step_icon}</span>
                <span>{label}</span>
            </div>
        ''')
    
    html_parts.append('</div>')
    st.markdown(''.join(html_parts), unsafe_allow_html=True)


def render_question_cours():
    """Affiche la phase de question de cours."""
    q = st.session_state.current_question

    # Progress bar
    render_progress_bar(PHASE_QUESTION)

    # Question avec rendu LaTeX supporté (st.container + marker CSS)
    with st.container(border=True):
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <p style="color: #888; margin-bottom: 0.75rem; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.05em;">
            {q['chapter_title']} · Niveau {q['difficulty']}/5 · {q['temps_estime_min']} min
        </p>
        <h3 style="margin: 0 0 1.5rem 0; color: #000; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Question de cours</h3>
        """, unsafe_allow_html=True)

        # Le texte de la question est rendu par st.markdown pour supporter LaTeX
        st.markdown(q['question_raw'])

    st.divider()

    # Historique de conversation avec séquencement
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg['content'], unsafe_allow_html=True)
        else:
            # Message assistant s'affiche après le message user
            with st.chat_message("assistant", avatar="📐"):
                st.markdown(msg['content'], unsafe_allow_html=True)

    # Panneau debug prompt (si active et donnees disponibles)
    if st.session_state.debug_prompt_mode and st.session_state.debug_prompt_data:
        with st.expander("Prompt envoye au LLM", expanded=False):
            st.markdown("**System prompt**")
            st.code(st.session_state.debug_prompt_data.get("system_prompt", ""), language="markdown")
            st.markdown("**User prompt (enrichi)**")
            st.code(st.session_state.debug_prompt_data.get("user_prompt", ""), language="markdown")

    # ÉTAPE 2 : Spinner pour génération de réponse (AVANT zone de formulaire)
    if (not st.session_state.question_validated and
        st.session_state.is_processing and
        st.session_state.conversation_history and
        st.session_state.conversation_history[-1]["role"] == "user"):

        # Évaluer avec spinner visible
        with st.spinner("Le khôlleur analyse votre réponse..."):
            try:
                final_answer = st.session_state.conversation_history[-1]["content"]
                attendus = json.loads(q.get("attendus_json", "[]"))
                erreurs = json.loads(q.get("erreurs_frequentes_json", "[]"))
                relances = json.loads(q.get("relances_prof_json", "[]"))

                result = evaluate_answer(
                    question=q["question_raw"],
                    expected=attendus,
                    student_answer=final_answer,
                    common_errors=erreurs,
                    follow_up_questions=relances,
                    conversation_history=st.session_state.conversation_history[:-1],
                    question_id=q["id"],
                    chapter_id=st.session_state.chapter_id,
                )

                # Stocker les prompts debug (et les retirer du result)
                st.session_state.debug_prompt_data = {
                    "system_prompt": result.pop("_debug_system_prompt", ""),
                    "user_prompt": result.pop("_debug_user_prompt", ""),
                }

                # Vérifier que le feedback n'est pas vide
                feedback = result.get("feedback", "")
                if not feedback or not feedback.strip():
                    st.error("Erreur: aucune réponse générée. Réessayer.")
                    st.session_state.conversation_history.pop()
                    st.session_state.is_processing = False
                    st.stop()

                # Ajouter le feedback à l'historique
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": feedback
                })

                # Stocker le score et les détails de validation
                st.session_state.scores.append(result["score"])

                # Debug: Afficher les valeurs retournées
                print(f"DEBUG - is_complete: {result['is_complete']}, score: {result['score']}")

                # Validation réaliste (comme en khôlle)
                if (result["is_complete"] and result["score"] >= 75):
                    st.session_state.question_validated = True
                    st.session_state.validation_score = result["score"]
                    st.session_state.validation_details = {
                        "score": result["score"],
                        "missing_points": result["missing_points"]
                    }
                    print(f"DEBUG - Question validée !")

                st.session_state.is_processing = False

            except Exception as e:
                st.error(f"Erreur: {e}")
                if st.session_state.conversation_history and st.session_state.conversation_history[-1]["role"] == "user":
                    st.session_state.conversation_history.pop()
                st.session_state.is_processing = False
                st.stop()

        st.rerun()

    # Affichage de la validation si question validée
    if st.session_state.question_validated:
        # Récapitulatif de validation avec style moderne
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-left: 4px solid #10b981; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
            <h3 style="margin: 0 0 1rem 0; color: #10b981; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1rem;">✓ Question validée</h3>
        </div>
        """, unsafe_allow_html=True)

        # Afficher le score
        score = st.session_state.get("validation_score", 0)
        col_score, col_status = st.columns([1, 2])
        with col_score:
            st.metric("Score", f"{score}/100")
        with col_status:
            st.markdown(f"""
            <p style="color: var(--color-text); font-size: 0.9rem; padding-top: 1rem;">
                Réponse complète et rigoureuse
            </p>
            """, unsafe_allow_html=True)

        # Bouton pour passer à l'exercice
        if st.button("Passer à l'exercice", type="primary", use_container_width=True, key="btn_pass_exercise"):
            start_exercise()
            st.rerun()
        st.divider()

    # Zone de réponse (désactivée si question validée)
    if not st.session_state.question_validated:
        # Bouton de déblocage manuel (au cas où la validation automatique bug)
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("⚡ Forcer le passage", help="Passer à l'exercice sans validation automatique", key="force_exercise"):
                st.session_state.question_validated = True
                st.session_state.validation_score = 100
                st.rerun()

        st.markdown("### Ta réponse")

        # Layout text-first (texte prioritaire sur photo)
        with st.form(key="question_form", clear_on_submit=True):
            # 1. Textarea PRINCIPALE en premier
            answer = st.text_area(
                "Écris ta réponse",
                height=120,
                placeholder="Si tu es bloqué, décris où tu en es...",
                label_visibility="collapsed",
                key="question_answer_input",
                disabled=st.session_state.is_processing
            )

            # 2. Séparateur visuel
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 1.5rem 0;">
                <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
                <span style="padding: 0 1rem; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #aaa;">ou</span>
                <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
            </div>
            """, unsafe_allow_html=True)

            # 3. Zone photo SECONDAIRE
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem 0;">
                <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #888;">Upload brouillon</span>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Prends en photo ton brouillon",
                type=["jpg", "jpeg", "png", "heic"],
                help="Clique pour prendre une photo ou sélectionner depuis ta galerie",
                label_visibility="collapsed",
                key="question_photo_input"
            )

            # IMAGE MASQUÉE dans un expander collapsed
            if uploaded_file:
                with st.expander("📎 Image uploadée (cliquer pour voir)", expanded=False):
                    st.image(uploaded_file, width=300)

            # 4. Bouton de validation
            submitted = st.form_submit_button(
                "Valider",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.is_processing
            )
        
        if submitted:
            if st.session_state.is_processing:
                st.warning("Traitement en cours, veuillez patienter...")
                st.stop()

            st.session_state.is_processing = True
            final_answer = answer.strip() if answer else ""

            # Transcrire l'image si présente et pas de texte
            if uploaded_file and not final_answer:
                with st.spinner("Lecture de votre écriture..."):
                    try:
                        image_bytes = uploaded_file.getvalue()
                        transcription = transcribe_image(image_bytes, uploaded_file.type)
                        final_answer = transcription
                    except Exception as e:
                        st.error(f"Erreur de transcription : {e}")
                        st.session_state.is_processing = False
                        st.stop()

            if not final_answer:
                st.warning("Écris une réponse ou upload une photo.")
                st.session_state.is_processing = False
                st.stop()

            # ÉTAPE 1 : Afficher d'abord le message utilisateur seul
            st.session_state.conversation_history.append({
                "role": "user",
                "content": final_answer
            })

            # Forcer le rerun pour afficher le message user AVANT la génération
            st.rerun()


def start_exercise():
    """Demarre la phase exercice. Trouve un exercice testant les memes concepts."""
    q = st.session_state.current_question
    exercise = None

    # Matching par concepts si une question a ete posee
    if q and q.get("id"):
        concepts = get_concepts_for_question(q["id"])
        concept_ids = [c["id"] for c in concepts]
        if concept_ids:
            exercise = get_exercise_for_concepts(
                concept_ids=concept_ids,
                difficulty=st.session_state.difficulty,
                chapter_id=st.session_state.chapter_id,
                exclude_ids=st.session_state.done_exercises,
            )

    # Fallback sur chapitre + difficulte
    if not exercise:
        exercise = get_exercise_by_difficulty(
            chapter_id=st.session_state.chapter_id,
            difficulty=st.session_state.difficulty,
            exclude_ids=st.session_state.done_exercises,
        )
    
    if exercise:
        st.session_state.current_exercise = exercise
        st.session_state.done_exercises.append(exercise["id"])
        st.session_state.phase = PHASE_EXERCICE
        st.session_state.conversation_history = []
    else:
        st.warning("Pas d'exercice disponible, fin de la khôlle !")
        st.session_state.phase = PHASE_FINISHED


# =============================================================================
# PHASE: EXERCICE
# =============================================================================

def render_exercice():
    """Affiche la phase exercice."""
    ex = st.session_state.current_exercise
    
    # Progress bar
    render_progress_bar(PHASE_EXERCICE)
    
    # Exercice avec rendu LaTeX supporté (st.container + marker CSS)
    with st.container(border=True):
        st.markdown('<div class="exercise-marker"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <p style="color: #888; margin-bottom: 0.75rem; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.05em;">
            {ex['chapter']} · Niveau {ex['difficulty']}/5
        </p>
        <h3 style="margin: 0 0 1.5rem 0; color: #000; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Exercice</h3>
        """, unsafe_allow_html=True)

        # Enoncé rendu par st.markdown pour supporter LaTeX
        st.markdown(ex.get("enonce", "Énoncé non disponible"))
    
    st.divider()
    
    # Historique de conversation
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg['content'], unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="📐"):
                st.markdown(msg['content'], unsafe_allow_html=True)

    # ÉTAPE 2 : Spinner pour génération de réponse (AVANT zone de formulaire)
    if (st.session_state.is_processing and
        st.session_state.conversation_history and
        st.session_state.conversation_history[-1]["role"] == "user"):

        with st.spinner("Le khôlleur réfléchit..."):
            try:
                final_message = st.session_state.conversation_history[-1]["content"]
                response = guide_exercise(
                    exercise_statement=ex.get("enonce", ""),
                    student_message=final_message,
                    hints=ex.get("indications", ""),
                    solution=ex.get("correction", ""),
                    conversation_history=st.session_state.conversation_history[:-1]
                )

                # Vérifier que la réponse n'est pas vide
                if not response or not response.strip():
                    st.error("Erreur: aucune réponse générée. Réessayer.")
                    st.session_state.conversation_history.pop()
                    st.session_state.is_processing = False
                    st.stop()

                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })

                st.session_state.is_processing = False

            except Exception as e:
                st.error(f"Erreur: {e}")
                if st.session_state.conversation_history and st.session_state.conversation_history[-1]["role"] == "user":
                    st.session_state.conversation_history.pop()
                st.session_state.is_processing = False
                st.stop()

        st.rerun()

    # Zone de réponse photo-first
    st.markdown("### Ton travail")

    with st.form(key="exercise_form", clear_on_submit=True):
        # 1. Textarea PRINCIPALE en premier
        message = st.text_area(
            "Écris ici",
            height=120,
            placeholder="Décris ton approche, pose une question, ou montre ton avancement...",
            label_visibility="collapsed",
            key="exercise_input_form",
            disabled=st.session_state.is_processing
        )

        # 2. Séparateur visuel
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 1.5rem 0;">
            <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
            <span style="padding: 0 1rem; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #aaa;">ou</span>
            <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Zone photo SECONDAIRE
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0;">
            <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #888;">Upload travail</span>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Prends en photo ton travail",
            type=["jpg", "jpeg", "png", "heic"],
            help="Clique pour prendre une photo ou sélectionner depuis ta galerie",
            label_visibility="collapsed",
            key="exercise_photo_form"
        )

        # IMAGE MASQUÉE dans un expander collapsed
        if uploaded_file:
            with st.expander("📎 Image uploadée (cliquer pour voir)", expanded=False):
                st.image(uploaded_file, width=300)

        # 4. Boutons d'action
        col_send, col_end = st.columns([3, 1])
        with col_send:
            submitted = st.form_submit_button(
                "Envoyer",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.is_processing
            )
        with col_end:
            end_clicked = st.form_submit_button(
                "Fin",
                use_container_width=True,
                disabled=st.session_state.is_processing
            )
    
    if end_clicked:
        st.session_state.phase = PHASE_FINISHED
        st.session_state.is_processing = False
        st.rerun()

    if submitted:
        if st.session_state.is_processing:
            st.warning("Traitement en cours, veuillez patienter...")
            st.stop()

        st.session_state.is_processing = True
        final_message = message.strip() if message else ""

        # Transcrire l'image si présente et pas de texte
        if uploaded_file and not final_message:
            with st.spinner("Lecture de votre écriture..."):
                try:
                    image_bytes = uploaded_file.getvalue()
                    transcription = transcribe_image(image_bytes, uploaded_file.type)
                    final_message = transcription
                except Exception as e:
                    st.error(f"Erreur de transcription : {e}")
                    st.session_state.is_processing = False
                    st.stop()

        if not final_message:
            st.warning("Écris un message ou upload une photo.")
            st.session_state.is_processing = False
            st.stop()

        # ÉTAPE 1 : Afficher d'abord le message utilisateur seul
        st.session_state.conversation_history.append({
            "role": "user",
            "content": final_message
        })

        # Forcer le rerun pour afficher le message user AVANT la génération
        st.rerun()


# =============================================================================
# PHASE: TERMINÉ
# =============================================================================

def render_finished():
    """Affiche l'écran de fin."""
    # Progress bar
    render_progress_bar(PHASE_FINISHED)

    st.markdown("## Session terminée")
    
    if st.session_state.scores:
        avg = sum(st.session_state.scores) / len(st.session_state.scores)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score moyen", f"{avg:.0f}/100")
        with col2:
            st.metric("Questions", len(st.session_state.asked_questions))
        with col3:
            st.metric("Exercices", len(st.session_state.done_exercises))
        
        # Feedback global
        if avg >= 80:
            st.success("Performance excellente. Maîtrise confirmée.")
        elif avg >= 60:
            st.info("Performance correcte. Points d'amélioration identifiés.")
        else:
            st.warning("Performance insuffisante. Révision recommandée.")

    if st.button("Nouvelle session", type="primary"):
        reset_kholle()
        st.rerun()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Point d'entrée principal."""

    # Header avec logo TaupIA
    import os
    logo_path = "Logo.png"

    if os.path.exists(logo_path):
        col_logo, col_title = st.columns([1, 6], gap="medium")

        with col_logo:
            st.markdown(f"""
            <img src="data:image/png;base64,{get_base64_image(logo_path)}"
                 style="width: 100px; height: auto;
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges;
                        image-rendering: high-quality;
                        -ms-interpolation-mode: nearest-neighbor;"
                 alt="Logo TaupIA">
            """, unsafe_allow_html=True)

        with col_title:
            st.markdown("""
            <div style="padding-top: 0.5rem;">
                <h1 style="font-size: 2.5rem; margin: 0; font-weight: 700; letter-spacing: 0.05em; color: #000;">TAUP<span style="font-weight: 400; color: #666;">IA</span></h1>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.1em; font-family: 'JetBrains Mono', monospace;">MPSI · Oral Mathematics Training System</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <h1 style="font-size: 2.5rem; margin: 0; font-weight: 700; letter-spacing: 0.05em; color: #000;">TaupIA</h1>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.1em; font-family: 'JetBrains Mono', monospace;">MPSI · Oral Mathematics Training System</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Sidebar
    render_sidebar()
    
    # Contenu principal selon la phase
    if st.session_state.phase == PHASE_SETUP:
        render_setup_mobile()
        
    elif st.session_state.phase == PHASE_QUESTION:
        render_question_cours()
        
    elif st.session_state.phase == PHASE_EXERCICE:
        render_exercice()
        
    elif st.session_state.phase == PHASE_FINISHED:
        render_finished()


if __name__ == "__main__":
    main()


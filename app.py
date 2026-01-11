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
    page_title="Khôlleur AI",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from data.query import (
    get_chapters,
    get_random_question,
    get_exercise_by_difficulty,
    get_collection_stats,
    get_rag_context,
)
from services.gemini_service import (
    evaluate_answer,
    guide_exercise,
    transcribe_image,
    chat,
)
from components.rag_debug import render_rag_debug_panel


def format_latex_text(text: str) -> str:
    """
    Formate le texte pour l'affichage.
    Le JSON est maintenant propre, cette fonction fait juste un nettoyage basique.
    """
    if not text:
        return text
    return text.strip()


# =============================================================================
# STYLES CSS
# =============================================================================

st.markdown("""
<style>
    /* =================================================================
       KHÔLLEUR AI - STYLES CSS v2.0
       Palette: Bleu académique (#2C3E87) + Orange chaleureux (#FF6B35)
       ================================================================= */
    
    /* Variables CSS */
    :root {
        --color-primary: #2C3E87;
        --color-accent: #FF6B35;
        --color-success: #2E7D32;
        --color-warning: #F57C00;
        --color-error: #c62828;
        --color-bg-dark: #1a1a2e;
        --color-bg-light: #f8f9fa;
        --color-text: #1a1a1a;
        --color-text-muted: #666;
        --shadow-sm: 0 2px 4px rgba(0,0,0,0.08);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.12);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.16);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-full: 9999px;
    }
    
    /* Police principale */
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Source Serif 4', Georgia, serif;
    }
    
    code, pre, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* =================================================================
       HEADER PRINCIPAL
       ================================================================= */
    .main-header {
        background: linear-gradient(135deg, var(--color-primary) 0%, #1a2a5e 100%);
        padding: 1.75rem 2rem;
        border-radius: var(--radius-lg);
        margin-bottom: 2rem;
        border-left: 5px solid var(--color-accent);
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,107,53,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .main-header h1 {
        color: #fff;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.8);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* =================================================================
       PROGRESS BAR (Setup → Question → Exercice → Résultats)
       ================================================================= */
    .progress-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin: 1.5rem 0 2rem 0;
        padding: 1rem;
        background: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }
    
    .progress-step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        color: var(--color-text-muted);
        transition: all 0.3s ease;
    }
    
    .progress-step .step-number {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 600;
        background: #e0e0e0;
        color: #999;
        transition: all 0.3s ease;
    }
    
    .progress-step.active .step-number {
        background: var(--color-primary);
        color: white;
        box-shadow: 0 0 0 4px rgba(44, 62, 135, 0.2);
    }
    
    .progress-step.completed .step-number {
        background: var(--color-success);
        color: white;
    }
    
    .progress-step.active {
        color: var(--color-primary);
        font-weight: 600;
    }
    
    .progress-step.completed {
        color: var(--color-success);
    }
    
    .progress-connector {
        width: 40px;
        height: 3px;
        background: #e0e0e0;
        border-radius: 2px;
        transition: background 0.3s ease;
    }
    
    .progress-connector.completed {
        background: var(--color-success);
    }
    
    /* =================================================================
       CARDS DE CONTENU
       ================================================================= */
    .question-card, .styled-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid var(--color-primary);
        box-shadow: var(--shadow-sm);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: var(--color-text) !important;
    }
    
    /* Ciblage du conteneur Streamlit via le marker (Question) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker) {
        background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
        border-radius: var(--radius-md);
        border-left: 5px solid var(--color-primary) !important;
        box-shadow: var(--shadow-sm);
        color: var(--color-text) !important;
    }

    /* Ciblage du conteneur Streamlit via le marker (Exercice) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker) {
        background: linear-gradient(135deg, #fff8f0 0%, #fff 100%);
        border-radius: var(--radius-md);
        border-left: 5px solid var(--color-accent) !important;
        box-shadow: var(--shadow-sm);
        color: var(--color-text) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker) [data-testid="stMarkdownContainer"] p,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker) [data-testid="stMarkdownContainer"] p {
        color: var(--color-text) !important;
        font-size: 1.25rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    .question-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker):hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .exercise-card {
        background: linear-gradient(135deg, #fff8f0 0%, #fff 100%);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid var(--color-accent);
        box-shadow: var(--shadow-sm);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: var(--color-text);
    }
    
    .exercise-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .feedback-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #fff 100%);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid var(--color-success);
        box-shadow: var(--shadow-sm);
        color: var(--color-text);
    }
    
    .feedback-card.warning {
        background: linear-gradient(135deg, #fff3e0 0%, #fff 100%);
        border-left-color: var(--color-warning);
        color: var(--color-text);
    }
    
    /* =================================================================
       MESSAGES CHAT (Kholleur & Étudiant)
       ================================================================= */
    .kholleur-msg {
        background: linear-gradient(135deg, var(--color-primary) 0%, #1a2a5e 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 16px 16px 16px 4px;
        margin: 0.75rem 0;
        max-width: 85%;
        box-shadow: var(--shadow-md);
        position: relative;
    }
    
    .kholleur-msg::before {
        content: '📐';
        position: absolute;
        left: -35px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
    }
    
    .student-msg {
        background: linear-gradient(135deg, #e3f2fd 0%, #fff 100%);
        color: var(--color-text);
        padding: 1.25rem 1.5rem;
        border-radius: 16px 16px 4px 16px;
        margin: 0.75rem 0;
        margin-left: auto;
        max-width: 85%;
        box-shadow: var(--shadow-sm);
        border: 1px solid rgba(44, 62, 135, 0.1);
    }
    
    /* =================================================================
       SCORE GAUGE CIRCULAIRE
       ================================================================= */
    .score-gauge-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    .score-gauge-circle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: conic-gradient(
            var(--gauge-color, var(--color-primary)) calc(var(--score, 0) * 3.6deg),
            #e0e0e0 0deg
        );
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        animation: gaugeAnimation 1s ease-out forwards;
    }
    
    .score-gauge-circle::before {
        content: '';
        position: absolute;
        width: 80px;
        height: 80px;
        background: white;
        border-radius: 50%;
    }
    
    .score-gauge-value {
        position: relative;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--gauge-color, var(--color-primary));
        font-family: 'Inter', sans-serif;
    }
    
    .score-gauge-label {
        font-size: 0.85rem;
        color: var(--color-text-muted);
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gaugeAnimation {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* =================================================================
       SCORE BADGE INLINE
       ================================================================= */
    .score-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.85rem;
        border-radius: var(--radius-full);
        font-weight: 600;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
    }
    
    .score-high { 
        background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%); 
        color: var(--color-success); 
    }
    .score-medium { 
        background: linear-gradient(135deg, #ffe0b2 0%, #ffcc80 100%); 
        color: var(--color-warning); 
    }
    .score-low { 
        background: linear-gradient(135deg, #ffcdd2 0%, #ef9a9a 100%); 
        color: var(--color-error); 
    }
    
    /* =================================================================
       PHASE INDICATOR (legacy, gardé pour compatibilité)
       ================================================================= */
    .phase-indicator {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    
    .phase {
        padding: 0.5rem 1rem;
        border-radius: var(--radius-full);
        font-size: 0.85rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .phase.active {
        background: var(--color-primary);
        color: white;
        box-shadow: 0 2px 8px rgba(44, 62, 135, 0.3);
    }
    
    .phase.completed {
        background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
        color: var(--color-success);
    }
    
    .phase.pending {
        background: #e0e0e0;
        color: #757575;
    }
    
    /* =================================================================
       SIDEBAR
       ================================================================= */
    .difficulty {
        color: var(--color-accent);
        font-size: 1.3rem;
        letter-spacing: 2px;
    }
    
    /* =================================================================
       ANIMATIONS
       ================================================================= */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .question-card, .exercise-card, .feedback-card {
        animation: fadeInUp 0.4s ease forwards;
    }
    
    /* =================================================================
       RESPONSIVE
       ================================================================= */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.2rem;
            margin: 0;
        }
        
        .main-header p {
            display: none; /* Masquer la description sur mobile pour gagner de la place */
        }
        
        /* Progress bar compacte - icônes seulement */
        .progress-container {
            flex-wrap: nowrap;
            gap: 0.25rem;
            padding: 0.5rem;
            justify-content: space-around;
        }
        
        .progress-connector {
            width: 20px;
        }
        
        .progress-step {
            padding: 0.4rem 0.6rem;
            font-size: 0.75rem;
        }
        
        .progress-step span:last-child {
            display: none; /* Masque le texte, garde le numéro */
        }
        
        .kholleur-msg, .student-msg {
            max-width: 95%;
            padding: 1rem;
            font-size: 0.95rem;
        }
        
        .kholleur-msg::before {
            display: none;
        }
        
        /* Touch targets améliorés */
        .stSelectbox > div > div {
            min-height: 52px !important;
            font-size: 1rem !important;
        }
        
        .stButton > button {
            min-height: 52px !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }
        
        /* File uploader PROÉMINENT pour mobile */
        .stFileUploader {
            min-height: 140px !important;
            border: 3px dashed var(--color-primary) !important;
            border-radius: 16px !important;
            background: rgba(44, 62, 135, 0.05) !important;
        }
        
        .stFileUploader section {
            padding: 1.5rem !important;
            min-height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
        }
        
        .stFileUploader section > div {
            font-size: 1rem !important;
        }
        
        .stFileUploader small {
            font-size: 0.9rem !important;
        }
        
        /* Radio buttons de difficulté */
        .stRadio > div {
            flex-wrap: wrap !important;
            gap: 0.5rem !important;
        }
        
        .stRadio label {
            padding: 0.6rem 0.8rem !important;
            font-size: 0.85rem !important;
        }
        
        /* Textarea adapté mobile */
        .stTextArea textarea {
            font-size: 16px !important; /* Empêche le zoom iOS */
            min-height: 80px !important;
        }
        
        /* Cards plus compactes */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker) {
            padding: 1rem !important;
        }
        
        /* Form submit button full width et proéminent */
        .stForm [data-testid="baseButton-primary"] {
            width: 100% !important;
            min-height: 52px !important;
            font-size: 1.1rem !important;
        }
        
        /* Réduire l'espace des diviseurs */
        hr {
            margin: 1rem 0 !important;
        }
    }
    
    /* Améliorer le dropdown pour éviter les bugs de clic */
    .stSelectbox {
        z-index: 100;
    }
    
    .stSelectbox > div > div {
        cursor: pointer;
    }
    
    /* Assurer que le formulaire est bien visible */
    .stForm {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)


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
        st.session_state.current_question = None
        st.session_state.current_exercise = None
        st.session_state.conversation_history = []
        st.session_state.question_validated = False
        st.session_state.asked_questions = []
        st.session_state.done_exercises = []
        st.session_state.scores = []
        # RAG Debug mode
        st.session_state.rag_debug_mode = False
        st.session_state.rag_chunks = []


init_session_state()


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar():
    """Affiche la sidebar avec les options."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Stats
        try:
            stats = get_collection_stats()
            st.caption(f"📚 {stats['questions_cours']['count']} questions · {stats['exercices']['count']} exercices")
        except:
            pass
        
        st.divider()
        
        # Choix du chapitre
        chapters = get_chapters()
        chapter_options = {f"{ch['title']} ({ch['question_count']}q)": ch['id'] for ch in chapters}
        
        selected_chapter = st.selectbox(
            "📖 Chapitre",
            options=list(chapter_options.keys()),
            index=0 if chapter_options else None,
            help="Choisis le chapitre sur lequel tu veux être interrogé"
        )
        
        if selected_chapter:
            st.session_state.chapter_id = chapter_options[selected_chapter]
        
        st.divider()
        
        # Difficulté
        st.session_state.difficulty = st.slider(
            "📊 Difficulté",
            min_value=1,
            max_value=5,
            value=st.session_state.difficulty,
            help="1 = Facile, 5 = Très difficile"
        )
        
        # Afficher les étoiles
        stars = "★" * st.session_state.difficulty + "☆" * (5 - st.session_state.difficulty)
        st.markdown(f"<p class='difficulty'>{stars}</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # Actions
        if st.button("🎯 Nouvelle khôlle", use_container_width=True, type="primary"):
            start_new_kholle()
        
        if st.session_state.phase != PHASE_SETUP:
            if st.button("🔄 Recommencer", use_container_width=True):
                reset_kholle()
        
        # Scores
        if st.session_state.scores:
            st.divider()
            st.markdown("### 📈 Tes scores")
            avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
            st.metric("Moyenne", f"{avg_score:.0f}/100")
        
        # RAG Debug Mode
        st.divider()
        st.markdown("### 🔧 Options avancées")
        st.session_state.rag_debug_mode = st.toggle(
            "🔍 Mode Debug RAG",
            value=st.session_state.rag_debug_mode,
            help="Affiche les chunks de contexte utilisés pour générer les réponses"
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
    <div style="text-align: center; padding: 1rem 0;">
        <p style="font-size: 1.1rem; color: var(--color-text-muted); margin: 0;">
            Prêt pour ta khôlle ? 🎯
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sélection du chapitre
    chapters = get_chapters()
    chapter_options = {f"{ch['title']} ({ch['question_count']}q)": ch['id'] for ch in chapters}
    
    selected_chapter = st.selectbox(
        "📖 Choisis ton chapitre",
        options=list(chapter_options.keys()),
        index=0 if chapter_options else None,
        key="mobile_chapter_select"
    )
    
    if selected_chapter:
        st.session_state.chapter_id = chapter_options[selected_chapter]
    
    # Sélection de la difficulté avec boutons radio visuels
    st.markdown("##### 📊 Difficulté")
    
    difficulty_labels = {
        1: "⭐ Facile",
        2: "⭐⭐ Accessible", 
        3: "⭐⭐⭐ Standard",
        4: "⭐⭐⭐⭐ Difficile",
        5: "⭐⭐⭐⭐⭐ Expert"
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
        "🚀 Lancer la khôlle",
        type="primary",
        use_container_width=True,
        key="mobile_start_btn"
    ):
        start_new_kholle()
        st.rerun()
    
    # Info discrète
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 0 0; opacity: 0.6;">
        <small>📝 Question de cours → 📐 Exercice → 🎉 Résultats</small>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PHASE: QUESTION DE COURS
# =============================================================================

def render_progress_bar(current_phase: str):
    """Affiche la progress bar visuelle selon la phase actuelle."""
    phases = [
        ("setup", "Configuration", "⚙️"),
        ("question_cours", "Question", "📝"),
        ("exercice", "Exercice", "📐"),
        ("finished", "Résultats", "🎉")
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
    question_text = format_latex_text(q['question_raw'])
    
    with st.container(border=True):
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <p style="color: #666; margin-bottom: 0.5rem; font-size: 0.85rem; font-family: 'Inter', sans-serif;">
            {q['chapter_title']} · Difficulté {q['difficulty']}/5 · ~{q['temps_estime_min']} min
        </p>
        <h3 style="margin: 0 0 1rem 0; color: var(--color-primary); font-family: 'Source Serif 4', serif;">📝 Question de cours</h3>
        """, unsafe_allow_html=True)
        
        # Le texte de la question est rendu par st.markdown pour supporter LaTeX
        st.markdown(question_text)
    
    st.divider()
    
    # Historique de conversation
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("assistant", avatar="📐"):
                st.markdown(msg['content'])
    
    # Panneau RAG Debug (si activé et chunks disponibles)
    if st.session_state.rag_debug_mode and st.session_state.rag_chunks:
        with st.expander("🔍 Contexte RAG utilisé", expanded=False):
            render_rag_debug_panel(st.session_state.rag_chunks)
    
    # Bouton pour passer à l'exercice (affiché en premier si validé)
    if st.session_state.question_validated:
        st.success("🎉 Question validée ! Tu peux passer à l'exercice.")
        if st.button("➡️ Passer à l'exercice", type="primary", key="btn_pass_exercise"):
            start_exercise()
            st.rerun()
        st.divider()
    
    # Zone de réponse (désactivée si question validée)
    if not st.session_state.question_validated:
        st.markdown("### Ta réponse")
        
        # Layout photo-first pour mobile
        with st.form(key="question_form", clear_on_submit=True):
            # 1. Zone photo proéminente
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem 0;">
                <span style="font-size: 1.2rem;">📷 Photo de ton brouillon</span>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Prends en photo ton brouillon",
                type=["jpg", "jpeg", "png", "heic"],
                help="Clique pour prendre une photo ou sélectionner depuis ta galerie",
                label_visibility="collapsed",
                key="question_photo_input"
            )
            
            if uploaded_file:
                st.image(uploaded_file, use_container_width=True)
                st.success("📸 Photo prête !")
            
            # 2. Séparateur visuel
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 1rem 0; opacity: 0.5;">
                <div style="flex: 1; height: 1px; background: currentColor;"></div>
                <span style="padding: 0 1rem; font-size: 0.85rem;">ou écris ta réponse</span>
                <div style="flex: 1; height: 1px; background: currentColor;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # 3. Textarea secondaire
            answer = st.text_area(
                "Écris ta réponse",
                height=100,
                placeholder="Si tu es bloqué, décris où tu en es...",
                label_visibility="collapsed",
                key="question_answer_input"
            )
            
            # 4. Bouton de validation
            submitted = st.form_submit_button(
                "✅ Valider",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            final_answer = answer.strip() if answer else ""
            
            # Transcrire l'image si présente et pas de texte
            if uploaded_file and not final_answer:
                with st.spinner("🔍 Transcription de l'image en cours..."):
                    try:
                        image_bytes = uploaded_file.getvalue()
                        transcription = transcribe_image(image_bytes, uploaded_file.type)
                        final_answer = transcription
                        st.success("✅ Transcription réussie !")
                        with st.expander("📝 Voir la transcription", expanded=True):
                            st.markdown(transcription)
                    except Exception as e:
                        st.error(f"Erreur de transcription : {e}")
                        st.stop()
            
            if not final_answer:
                st.warning("Écris une réponse ou upload une photo.")
                st.stop()
            
            # Ajouter à l'historique
            st.session_state.conversation_history.append({
                "role": "user",
                "content": final_answer
            })
            
            # Évaluer
            with st.spinner("🤔 Le khôlleur réfléchit..."):
                try:
                    attendus = json.loads(q.get("attendus_json", "[]"))
                    erreurs = json.loads(q.get("erreurs_frequentes_json", "[]"))
                    relances = json.loads(q.get("relances_prof_json", "[]"))
                    
                    # Récupérer le contexte RAG pour le debug
                    rag_chunks = get_rag_context(
                        question=q["question_raw"],
                        chapter_id=st.session_state.chapter_id,
                        top_k=3
                    )
                    st.session_state.rag_chunks = rag_chunks
                    
                    result = evaluate_answer(
                        question=q["question_raw"],
                        expected=attendus,
                        student_answer=final_answer,
                        common_errors=erreurs,
                        follow_up_questions=relances,
                        conversation_history=st.session_state.conversation_history[:-1]
                    )
                    
                    # Ajouter le feedback à l'historique
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": result["feedback"]
                    })
                    
                    # Stocker le score
                    st.session_state.scores.append(result["score"])
                    
                    # Si complet, passer à l'exercice
                    if result["is_complete"] or result["score"] >= 80:
                        st.session_state.question_validated = True
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'évaluation : {e}")
            
            st.rerun()


def start_exercise():
    """Démarre la phase exercice."""
    exercise = get_exercise_by_difficulty(
        chapter_id=st.session_state.chapter_id,
        difficulty=st.session_state.difficulty,
        exclude_ids=st.session_state.done_exercises
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
        <p style="color: #666; margin-bottom: 0.5rem; font-size: 0.85rem; font-family: 'Inter', sans-serif;">
            {ex['chapter']} · Difficulté {ex['difficulty']}/5
        </p>
        <h3 style="margin: 0 0 1rem 0; color: var(--color-accent); font-family: 'Source Serif 4', serif;">📐 Exercice</h3>
        """, unsafe_allow_html=True)
        
        # Enoncé rendu par st.markdown pour supporter LaTeX
        st.markdown(ex.get("enonce", "Énoncé non disponible"))
    
    st.divider()
    
    # Historique de conversation
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("assistant", avatar="📐"):
                st.markdown(msg['content'])
    
    # Zone de réponse photo-first
    st.markdown("### Ton travail")
    
    with st.form(key="exercise_form", clear_on_submit=True):
        # 1. Zone photo proéminente
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0;">
            <span style="font-size: 1.2rem;">📷 Photo de ton travail</span>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Prends en photo ton travail",
            type=["jpg", "jpeg", "png", "heic"],
            help="Clique pour prendre une photo ou sélectionner depuis ta galerie",
            label_visibility="collapsed",
            key="exercise_photo_form"
        )
        
        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)
            st.success("� Photo prête !")
        
        # 2. Séparateur visuel
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 1rem 0; opacity: 0.5;">
            <div style="flex: 1; height: 1px; background: currentColor;"></div>
            <span style="padding: 0 1rem; font-size: 0.85rem;">ou écris un message</span>
            <div style="flex: 1; height: 1px; background: currentColor;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Textarea secondaire  
        message = st.text_area(
            "Écris ici",
            height=100,
            placeholder="Décris ton approche, pose une question, ou montre ton avancement...",
            label_visibility="collapsed",
            key="exercise_input_form"
        )
        
        # 4. Boutons d'action
        col_send, col_end = st.columns([3, 1])
        with col_send:
            submitted = st.form_submit_button(
                "💬 Envoyer",
                type="primary",
                use_container_width=True
            )
        with col_end:
            end_clicked = st.form_submit_button(
                "🏁 Fin",
                use_container_width=True
            )
    
    if end_clicked:
        st.session_state.phase = PHASE_FINISHED
        st.rerun()
    
    if submitted:
        final_message = message.strip() if message else ""
        
        # Transcrire l'image si présente et pas de texte
        if uploaded_file and not final_message:
            with st.spinner("🔍 Transcription de l'image..."):
                try:
                    image_bytes = uploaded_file.getvalue()
                    transcription = transcribe_image(image_bytes, uploaded_file.type)
                    final_message = transcription
                    with st.expander("Voir la transcription"):
                        st.markdown(transcription)
                except Exception as e:
                    st.error(f"Erreur de transcription : {e}")
                    st.stop()
        
        if not final_message:
            st.warning("Écris un message ou upload une photo.")
            st.stop()
        
        st.session_state.conversation_history.append({
            "role": "user",
            "content": final_message
        })
        
        with st.spinner("🤔 Le khôlleur réfléchit..."):
            try:
                response = guide_exercise(
                    exercise_statement=ex.get("enonce", ""),
                    student_message=final_message,
                    hints=ex.get("indications", ""),
                    solution=ex.get("correction", ""),
                    conversation_history=st.session_state.conversation_history[:-1]
                )
                
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
            except Exception as e:
                st.error(f"Erreur : {e}")
        
        st.rerun()


# =============================================================================
# PHASE: TERMINÉ
# =============================================================================

def render_finished():
    """Affiche l'écran de fin."""
    # Progress bar
    render_progress_bar(PHASE_FINISHED)
    
    st.markdown("## 🎉 Khôlle terminée !")
    
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
            st.success("Excellent travail ! Tu maîtrises bien ce chapitre. 🌟")
        elif avg >= 60:
            st.info("Bon travail ! Quelques points à revoir mais tu es sur la bonne voie. 📚")
        else:
            st.warning("Il y a encore du travail, mais c'est en forgeant qu'on devient forgeron ! 💪")
    
    if st.button("🔄 Nouvelle khôlle", type="primary"):
        reset_kholle()
        st.rerun()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Point d'entrée principal."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📐 Khôlleur AI</h1>
        <p>Ton sparring partner pour les khôlles de maths MPSI</p>
    </div>
    """, unsafe_allow_html=True)
    
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


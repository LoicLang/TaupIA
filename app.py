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




# =============================================================================
# STYLES CSS
# =============================================================================

st.markdown("""
<style>
    /* =================================================================
       KHÔLLEUR AI - ENGINEERING PRECISION v3.0
       Inspired by SpaceX / Tesla UI
       ================================================================= */

    :root {
        --color-primary: #000000;
        --color-accent: #000000;
        --color-bg: #FFFFFF;
        --color-border: #BFBFBF;
        --color-border-strong: #000000;
        --color-text: #000000;
        --color-text-muted: #555555;
        --radius-refined: 2px;
        --font-main: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: var(--font-main);
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Force light mode on main content */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    .stMainBlockContainer, [data-testid="stVerticalBlock"] {
        background-color: #FFFFFF !important;
    }

    /* =================================================================
       GLOBAL TEXT COLOR RESET (Dark Mode Override)
       ================================================================= */
    p, span, label, div, h1, h2, h3, h4, h5, h6, li, td, th {
        color: #000000;
    }

    /* Streamlit specific text elements */
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stText"],
    .stMarkdown, .stMarkdown p {
        color: #000000 !important;
    }

    code, pre, .stCode, .step-number, .score-gauge-value {
        font-family: var(--font-mono) !important;
    }

    /* =================================================================
       HEADER - MINIMALIST PRECISION
       ================================================================= */
    .main-header {
        background: var(--color-primary);
        padding: 1.25rem 1.5rem;
        border-radius: 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--color-border-strong);
        position: relative;
    }

    .main-header h1 {
        color: #fff;
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .main-header p {
        color: #AAAAAA !important;
        margin: 0.25rem 0 0 0;
        font-size: 0.7rem;
        font-family: var(--font-mono);
        text-transform: uppercase;
    }

    /* =================================================================
       PROGRESS BAR - INSTRUMENT SCALE
       ================================================================= */
    .progress-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 1.5rem 0;
        padding: 0.75rem 0;
        background: transparent;
        border-top: 1px solid var(--color-border);
        border-bottom: 1px solid var(--color-border);
    }

    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.4rem;
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #555555 !important;
        letter-spacing: 0.05em;
    }

    .progress-step span {
        color: #555555 !important;
    }

    .progress-step .step-number {
        font-size: 0.65rem;
        color: #555555 !important;
        padding-bottom: 2px;
        border-bottom: 2px solid transparent;
    }

    .progress-step.active .step-number {
        color: #000000 !important;
        border-bottom-color: #000000;
    }

    .progress-step.active span {
        color: #000000 !important;
    }

    .progress-step.completed .step-number {
        color: #000000 !important;
        border-bottom-color: #DDD;
    }

    .progress-step.completed span {
        color: #000000 !important;
    }

    .progress-connector {
        flex-grow: 1;
        height: 1px;
        background: var(--color-border);
        margin: 0 1rem;
    }

    /* =================================================================
       CARDS - TECHNICAL PANELS
       ================================================================= */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker),
    .question-card, .exercise-card, .feedback-card {
        background: transparent !important;
        border-radius: var(--radius-refined) !important;
        border: 1px solid var(--color-border) !important;
        box-shadow: none !important;
        padding: 1.25rem !important;
        margin: 1rem 0 !important;
        transition: border-color 0.2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker):hover,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker):hover {
        border-color: var(--color-border-strong) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker) [data-testid="stMarkdownContainer"] p,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker) [data-testid="stMarkdownContainer"] p {
        color: var(--color-text) !important;
        font-size: 0.95rem !important;
        line-height: 1.5;
        font-weight: 400;
    }

    /* =================================================================
       MESSAGES - CLEAN LOGS
       ================================================================= */
    .kholleur-msg {
        background: #F5F5F5;
        color: var(--color-text);
        padding: 1rem;
        border-radius: var(--radius-refined);
        border-left: 3px solid var(--color-primary);
        margin: 0.75rem 0;
        max-width: 90%;
        font-size: 0.85rem;
    }

    .kholleur-msg::before { display: none; }

    .student-msg {
        background: transparent;
        color: var(--color-text);
        padding: 1rem;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-refined);
        margin: 0.75rem 0 0.75rem auto;
        max-width: 90%;
        font-size: 0.85rem;
    }

    /* =================================================================
       GAUGE - ANALYTICAL READOUT
       ================================================================= */
    .score-gauge-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .score-gauge-circle {
        width: 80px;
        height: 80px;
        border: 1px solid var(--color-border);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
    }

    .score-gauge-circle::before { display: none; }

    .score-gauge-value {
        font-size: 1.1rem;
        font-weight: 500;
        color: var(--color-primary);
    }

    .score-gauge-label {
        font-size: 0.7rem;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .score-badge {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border: 1px solid var(--color-border-strong);
        border-radius: var(--radius-refined);
        text-transform: uppercase;
    }

    .score-high { background: #000; color: #FFF; }
    .score-medium { background: #555; color: #FFF; }
    .score-low { background: #CCC; color: #000; }

    /* =================================================================
       CONTROLS - PRECISION INPUTS
       ================================================================= */
    .stButton > button,
    .stButton > button[kind="primary"],
    .stButton > button[kind="secondary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="baseButton-primary"],
    [data-testid="baseButton-secondary"] {
        border-radius: 2px !important;
        border: 1px solid #000000 !important;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover,
    [data-testid="stBaseButton-primary"]:hover,
    [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="baseButton-primary"]:hover,
    [data-testid="baseButton-secondary"]:hover {
        background-color: #333333 !important;
        border-color: #333333 !important;
        color: #FFFFFF !important;
    }

    .stButton > button p,
    [data-testid="stBaseButton-primary"] p,
    [data-testid="baseButton-primary"] p {
        color: #FFFFFF !important;
    }

    /* Selectbox - Complete styling */
    .stSelectbox label,
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div {
        color: #000000 !important;
    }

    .stSelectbox > div > div {
        border: 1px solid #BFBFBF !important;
        border-radius: 2px !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 0.8rem !important;
    }

    .stSelectbox [data-baseweb="select"] {
        background-color: #FFFFFF !important;
    }

    .stSelectbox [data-baseweb="popover"],
    .stSelectbox [data-baseweb="menu"],
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [data-baseweb="list"],
    [data-baseweb="listbox"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    /* Dropdown list items */
    .stSelectbox [data-baseweb="menu"] li,
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"],
    [data-baseweb="list"] li,
    [data-baseweb="listbox"] li,
    [role="listbox"] [role="option"],
    [data-baseweb="select"] [role="option"],
    ul[role="listbox"] li {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    /* Dropdown list item text */
    [data-baseweb="menu"] li *,
    [data-baseweb="list"] li *,
    [data-baseweb="listbox"] li *,
    [role="listbox"] [role="option"] *,
    ul[role="listbox"] li * {
        color: #000000 !important;
    }

    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [data-baseweb="list"] li:hover,
    [role="listbox"] [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background-color: #F0F0F0 !important;
        background: #F0F0F0 !important;
    }

    /* Popover container */
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] [data-baseweb="menu"],
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #BFBFBF !important;
    }

    /* Radio buttons */
    .stRadio label,
    .stRadio [data-baseweb="radio"] label,
    .stRadio span,
    .stRadio p {
        color: #000000 !important;
    }

    .stRadio > div {
        background-color: transparent !important;
    }

    .stRadio [data-baseweb="radio"] {
        background-color: #FFFFFF !important;
    }

    /* Textarea - Complete styling */
    .stTextArea label {
        color: #000000 !important;
    }

    .stTextArea textarea {
        border: 1px solid #BFBFBF !important;
        border-radius: 2px !important;
        font-size: 0.85rem !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    .stTextArea textarea::placeholder {
        color: #888888 !important;
    }

    .difficulty {
        font-family: var(--font-mono);
        font-size: 0.9rem;
        letter-spacing: 1px;
        color: var(--color-primary);
    }

    /* =================================================================
       ADDITIONAL COMPONENTS - DARK MODE OVERRIDE
       ================================================================= */

    /* Slider */
    .stSlider label,
    .stSlider [data-baseweb="slider"] div,
    .stSlider span {
        color: #000000 !important;
    }

    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #555555 !important;
    }

    /* Metrics */
    [data-testid="stMetric"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #000000 !important;
    }

    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 600;
    }

    /* Chat messages */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessageContent"],
    .stChatMessage {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #000000 !important;
    }

    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #F5F5F5 !important;
    }

    /* Expander */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary span {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }

    /* File uploader */
    .stFileUploader,
    .stFileUploader label,
    .stFileUploader span,
    .stFileUploader p,
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        color: #000000 !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background-color: #FFFFFF !important;
        border: 1px dashed #BFBFBF !important;
    }

    .stFileUploader small {
        color: #555555 !important;
    }

    /* Captions and small text */
    .stCaption, small, .stCaption p {
        color: #555555 !important;
    }

    /* Alert boxes */
    .stSuccess, .stWarning, .stError, .stInfo,
    [data-testid="stAlert"] {
        color: #000000 !important;
    }

    [data-testid="stAlert"] p {
        color: #000000 !important;
    }

    /* Divider */
    .stDivider, hr {
        border-color: #BFBFBF !important;
        background-color: #BFBFBF !important;
    }

    /* Toggle */
    .stToggle label,
    .stToggle span {
        color: #000000 !important;
    }

    /* =================================================================
       PHASE INDICATOR - LEGACY
       ================================================================= */
    .phase-indicator {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .phase {
        padding: 0.4rem 0.8rem;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 1px solid var(--color-border);
    }

    .phase.active {
        background: var(--color-primary);
        color: white;
        border-color: var(--color-primary);
    }

    .phase.completed {
        background: #F5F5F5;
        color: var(--color-text);
    }

    .phase.pending {
        background: transparent;
        color: var(--color-text-muted);
    }

    /* =================================================================
       SIDEBAR - CLEAN PANEL
       ================================================================= */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"] {
        border-right: 1px solid #BFBFBF;
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        color: var(--color-text) !important;
    }

    [data-testid="stSidebar"] .stCaption {
        color: var(--color-text-muted) !important;
    }

    hr {
        border-color: var(--color-border) !important;
    }

    /* =================================================================
       ANIMATIONS - SUBTLE
       ================================================================= */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .question-card, .exercise-card, .feedback-card {
        animation: fadeIn 0.3s ease forwards;
    }

    /* =================================================================
       RESPONSIVE - MOBILE PRECISION
       ================================================================= */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
        }

        .main-header h1 {
            font-size: 0.9rem;
        }

        .main-header p {
            display: none;
        }

        .progress-container {
            padding: 0.5rem 0;
        }

        .progress-step {
            font-size: 0.6rem;
        }

        .progress-step span:last-child {
            display: none;
        }

        .kholleur-msg, .student-msg {
            max-width: 95%;
            padding: 0.75rem;
            font-size: 0.8rem;
        }

        .stSelectbox > div > div {
            min-height: 48px !important;
        }

        .stButton > button {
            min-height: 48px !important;
            font-size: 0.7rem !important;
        }

        .stFileUploader {
            border: 1px dashed var(--color-border) !important;
            border-radius: var(--radius-refined) !important;
            background: transparent !important;
        }

        .stTextArea textarea {
            font-size: 16px !important;
        }

        .stForm [data-testid="baseButton-primary"] {
            width: 100% !important;
            min-height: 48px !important;
        }
    }

    .stSelectbox {
        z-index: 100;
    }

    .stSelectbox > div > div {
        cursor: pointer;
    }

    .stForm {
        background: transparent;
        border-radius: var(--radius-refined);
        padding: 1rem;
        border: 1px solid var(--color-border);
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
        chapter_options = {f"{ch['title']} ({ch['question_count']}q)": ch['id'] for ch in chapters}
        
        selected_chapter = st.selectbox(
            "Chapitre",
            options=list(chapter_options.keys()),
            index=0 if chapter_options else None,
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
        
        # RAG Debug Mode
        st.divider()
        st.markdown("### Avancé")
        st.session_state.rag_debug_mode = st.toggle(
            "Mode Debug RAG",
            value=st.session_state.rag_debug_mode,
            help="Affiche les chunks de contexte utilisés"
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
    
    # Sélection du chapitre
    chapters = get_chapters()
    chapter_options = {f"{ch['title']} ({ch['question_count']}q)": ch['id'] for ch in chapters}
    
    selected_chapter = st.selectbox(
        "Chapitre",
        options=list(chapter_options.keys()),
        index=0 if chapter_options else None,
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
        <p style="color: #888; margin-bottom: 0.5rem; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.05em;">
            {q['chapter_title']} · Niveau {q['difficulty']}/5 · {q['temps_estime_min']} min
        </p>
        <h3 style="margin: 0 0 1rem 0; color: #000; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Question de cours</h3>
        """, unsafe_allow_html=True)
        
        # Le texte de la question est rendu par st.markdown pour supporter LaTeX
        st.markdown(q['question_raw'])
    
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
        with st.expander("Contexte RAG", expanded=False):
            render_rag_debug_panel(st.session_state.rag_chunks)
    
    # Bouton pour passer à l'exercice (affiché en premier si validé)
    if st.session_state.question_validated:
        st.success("Question validée. Passage à l'exercice disponible.")
        if st.button("Continuer", type="primary", key="btn_pass_exercise"):
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
            
            if uploaded_file:
                st.image(uploaded_file, use_container_width=True)
                st.success("Image chargée")
            
            # 2. Séparateur visuel
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 1.5rem 0;">
                <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
                <span style="padding: 0 1rem; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #aaa;">ou</span>
                <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
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
                "Valider",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            final_answer = answer.strip() if answer else ""
            
            # Transcrire l'image si présente et pas de texte
            if uploaded_file and not final_answer:
                with st.spinner("Transcription en cours..."):
                    try:
                        image_bytes = uploaded_file.getvalue()
                        transcription = transcribe_image(image_bytes, uploaded_file.type)
                        final_answer = transcription
                        st.success("Transcription terminée")
                        with st.expander("Voir la transcription", expanded=True):
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
            with st.spinner("Analyse en cours..."):
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
                    
                    # Vérifier que le feedback n'est pas vide
                    feedback = result.get("feedback", "")
                    if not feedback or not feedback.strip():
                        st.error("Erreur: aucune réponse générée. Réessayer.")
                        if st.session_state.conversation_history and st.session_state.conversation_history[-1]["role"] == "user":
                            st.session_state.conversation_history.pop()
                        st.stop()
                    
                    # Ajouter le feedback à l'historique
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": feedback
                    })
                    
                    # Stocker le score
                    st.session_state.scores.append(result["score"])
                    
                    # Si complet, passer à l'exercice
                    if result["is_complete"] or result["score"] >= 80:
                        st.session_state.question_validated = True
                    
                except Exception as e:
                    st.error(f"Erreur: {e}")
                    if st.session_state.conversation_history and st.session_state.conversation_history[-1]["role"] == "user":
                        st.session_state.conversation_history.pop()
                    st.stop()
            
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
        <p style="color: #888; margin-bottom: 0.5rem; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.05em;">
            {ex['chapter']} · Niveau {ex['difficulty']}/5
        </p>
        <h3 style="margin: 0 0 1rem 0; color: #000; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">Exercice</h3>
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
        
        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)
            st.success("Image chargée")
        
        # 2. Séparateur visuel
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 1.5rem 0;">
            <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
            <span style="padding: 0 1rem; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #aaa;">ou</span>
            <div style="flex: 1; height: 1px; background: #E5E5E5;"></div>
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
                "Envoyer",
                type="primary",
                use_container_width=True
            )
        with col_end:
            end_clicked = st.form_submit_button(
                "Fin",
                use_container_width=True
            )
    
    if end_clicked:
        st.session_state.phase = PHASE_FINISHED
        st.rerun()
    
    if submitted:
        final_message = message.strip() if message else ""
        
        # Transcrire l'image si présente et pas de texte
        if uploaded_file and not final_message:
            with st.spinner("Transcription en cours..."):
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
        
        with st.spinner("Analyse en cours..."):
            try:
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
                    # Retirer le message utilisateur qui n'a pas eu de réponse
                    if st.session_state.conversation_history and st.session_state.conversation_history[-1]["role"] == "user":
                        st.session_state.conversation_history.pop()
                    st.stop()
                
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
            except Exception as e:
                st.error(f"Erreur: {e}")
                # Retirer le message utilisateur qui n'a pas eu de réponse
                if st.session_state.conversation_history and st.session_state.conversation_history[-1]["role"] == "user":
                    st.session_state.conversation_history.pop()
                st.stop()
        
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
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Khôlleur AI</h1>
        <p>MPSI · Oral Mathematics Training System</p>
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


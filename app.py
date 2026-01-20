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
        /* EdTech Modern Palette */
        --color-primary: #4f46e5;
        --color-primary-hover: #4338ca;
        --color-accent: #8b5cf6;
        --color-success: #10b981;
        --color-bg: #f8fafc;
        --color-card-bg: #ffffff;
        --color-border: #e2e8f0;
        --color-border-strong: #4f46e5;
        --color-text: #1e293b;
        --color-text-main: #1e293b;
        --color-text-muted: #64748b;
        --color-user-bubble: #4f46e5;
        --color-tutor-bubble: #ffffff;

        /* Spacing & Radii */
        --radius-refined: 8px;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 20px;

        /* Shadows */
        --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);

        /* Transitions */
        --transition-fast: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

        /* Fonts */
        --font-main: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: var(--font-main);
        background-color: var(--color-bg) !important;
        color: var(--color-text) !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Modern light mode with subtle gradient */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: var(--color-bg) !important;
        color: var(--color-text) !important;
    }

    .stMainBlockContainer, [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }

    /* =================================================================
       GLOBAL TEXT COLOR - Modern Edtech
       ================================================================= */
    p, span, label, div, li, td, th {
        color: var(--color-text);
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--color-text-main);
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Streamlit specific text elements */
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stText"],
    .stMarkdown, .stMarkdown p {
        color: var(--color-text) !important;
    }

    code, pre, .stCode, .step-number, .score-gauge-value {
        font-family: var(--font-mono) !important;
    }

    /* =================================================================
       HEADER - Modern & Clean
       ================================================================= */
    .main-header {
        background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
        padding: 1.5rem 2rem;
        border-radius: 0;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-md);
        position: relative;
    }

    .main-header h1 {
        color: #fff;
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
        text-transform: none;
        letter-spacing: -0.02em;
    }

    .main-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        margin: 0.5rem 0 0 0;
        font-size: 0.875rem;
        font-family: var(--font-main);
        text-transform: none;
    }

    .logo-header {
        height: 32px;
        width: auto;
        margin-right: 1rem;
        filter: brightness(0) invert(1);
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }

    /* Logo dans le main content (pas dans header) */
    img[alt="Logo"] {
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
        image-rendering: high-quality;
    }

    /* =================================================================
       PROGRESS BAR - Visual & Progressive
       ================================================================= */
    .progress-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 1.5rem 0;
        padding: 1rem;
        background: var(--color-card-bg);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }

    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        color: var(--color-text-muted) !important;
        letter-spacing: 0.05em;
        transition: var(--transition-fast);
    }

    .progress-step span {
        color: var(--color-text-muted) !important;
    }

    .progress-step .step-number {
        font-size: 0.7rem;
        color: var(--color-text-muted) !important;
        padding: 4px 8px;
        border-radius: 6px;
        background: var(--color-bg);
        transition: var(--transition-fast);
    }

    .progress-step.active .step-number {
        color: #FFFFFF !important;
        background: var(--color-primary);
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
    }

    .progress-step.active span {
        color: var(--color-primary) !important;
    }

    .progress-step.completed .step-number {
        color: #FFFFFF !important;
        background: var(--color-success);
    }

    .progress-step.completed span {
        color: var(--color-text) !important;
    }

    .progress-connector {
        flex-grow: 1;
        height: 2px;
        background: var(--color-border);
        margin: 0 1rem;
        border-radius: 2px;
        transition: var(--transition-fast);
    }

    .progress-connector.completed {
        background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
    }

    /* =================================================================
       CARDS - Modern & Elevated
       ================================================================= */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker),
    .question-card, .exercise-card, .feedback-card {
        background: var(--color-card-bg) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--color-border) !important;
        box-shadow: var(--shadow-sm) !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        transition: var(--transition-fast);
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker):hover,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker):hover {
        border-color: var(--color-accent) !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-2px);
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker) [data-testid="stMarkdownContainer"] p,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker) [data-testid="stMarkdownContainer"] p {
        color: var(--color-text) !important;
        font-size: 1.1rem !important;
        line-height: 1.75;
        font-weight: 450;
    }

    /* Style pour le contenu LaTeX dans les questions/exercices */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker) [data-testid="stMarkdownContainer"],
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.exercise-marker) [data-testid="stMarkdownContainer"] {
        font-size: 1.1rem !important;
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
        padding: 0.3rem 0.6rem;
        border: none;
        border-radius: var(--radius-sm);
        text-transform: uppercase;
        font-weight: 600;
    }

    .score-high {
        background: var(--color-success);
        color: #FFF;
    }

    .score-medium {
        background: var(--color-accent);
        color: #FFF;
    }

    .score-low {
        background: var(--color-text-muted);
        color: #FFF;
    }

    /* =================================================================
       BUTTONS - Modern & Tactile
       ================================================================= */
    .stButton > button,
    .stButton > button[kind="primary"],
    .stButton > button[kind="secondary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="baseButton-primary"],
    [data-testid="baseButton-secondary"] {
        border-radius: var(--radius-md) !important;
        border: none !important;
        background-color: var(--color-primary) !important;
        color: #FFFFFF !important;
        text-transform: none;
        letter-spacing: normal;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        padding: 0.625rem 1.5rem !important;
        transition: var(--transition-fast) !important;
    }

    .stButton > button:hover,
    [data-testid="stBaseButton-primary"]:hover,
    [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="baseButton-primary"]:hover,
    [data-testid="baseButton-secondary"]:hover {
        background-color: var(--color-primary-hover) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        transform: translateY(-1px);
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
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        background-color: var(--color-card-bg) !important;
        color: var(--color-text) !important;
        font-size: 0.875rem !important;
        transition: var(--transition-fast) !important;
    }

    .stSelectbox > div > div:hover {
        border-color: var(--color-primary) !important;
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

    /* Textarea - Modern with focus states */
    .stTextArea label {
        color: var(--color-text) !important;
        font-weight: 500;
    }

    .stTextArea textarea {
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        font-size: 0.9rem !important;
        color: var(--color-text) !important;
        background-color: var(--color-card-bg) !important;
        padding: 12px 16px !important;
        transition: var(--transition-fast) !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        outline: none !important;
    }

    .stTextArea textarea::placeholder {
        color: var(--color-text-muted) !important;
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

    /* Chat messages - Modern bubbles */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessageContent"],
    .stChatMessage {
        background-color: transparent !important;
        border-radius: var(--radius-lg) !important;
        padding: 1rem !important;
        margin: 0.75rem 0 !important;
        animation: fadeIn 0.4s ease-out forwards;
        box-shadow: var(--shadow-sm);
        max-height: none !important;
        overflow: visible !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span:not(.katex):not(.katex *),
    [data-testid="stChatMessage"] div:not(.katex-display):not(.katex *) {
        line-height: 1.6;
        max-height: none !important;
        overflow: visible !important;
        white-space: normal !important;
    }

    /* Ne pas casser les formules LaTeX */
    [data-testid="stChatMessage"] .katex,
    [data-testid="stChatMessage"] .katex *,
    [data-testid="stChatMessage"] .katex-display,
    [data-testid="stChatMessage"] code {
        word-wrap: normal !important;
        word-break: normal !important;
        white-space: nowrap !important;
    }

    /* User message styling - À DROITE, couleur indigo */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: var(--color-user-bubble) !important;
        border: none !important;
        border-bottom-right-radius: 4px !important;
        box-shadow: var(--shadow-md) !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        max-width: 85% !important;
    }

    [data-testid="stChatMessage"][data-testid*="user"] p,
    [data-testid="stChatMessage"][data-testid*="user"] span,
    [data-testid="stChatMessage"][data-testid*="user"] div {
        color: #FFFFFF !important;
    }

    /* Assistant message styling - À GAUCHE, fond blanc */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: var(--color-tutor-bubble) !important;
        border: 1px solid var(--color-border) !important;
        border-left: 3px solid var(--color-primary) !important;
        border-bottom-left-radius: 4px !important;
        box-shadow: var(--shadow-sm) !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        max-width: 85% !important;
    }

    [data-testid="stChatMessage"][data-testid*="assistant"] p,
    [data-testid="stChatMessage"][data-testid*="assistant"] span,
    [data-testid="stChatMessage"][data-testid*="assistant"] div {
        color: var(--color-text) !important;
    }

    /* Transcription message - mise en valeur spéciale */
    .transcription-message {
        background: #F8F8F8 !important;
        border: 1px solid #000000 !important;
        border-radius: 2px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }

    .transcription-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #555555 !important;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
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
        background-color: var(--color-card-bg) !important;
        border: 2px dashed var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        transition: var(--transition-fast) !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--color-primary) !important;
        background-color: rgba(79, 70, 229, 0.02) !important;
    }

    .stFileUploader small {
        color: #555555 !important;
    }

    /* Captions and small text */
    .stCaption, small, .stCaption p {
        color: #555555 !important;
    }

    /* Alert boxes - Modern with rounded corners */
    .stSuccess, .stWarning, .stError, .stInfo,
    [data-testid="stAlert"] {
        border-radius: var(--radius-md) !important;
        border: none !important;
        box-shadow: var(--shadow-sm) !important;
    }

    [data-testid="stAlert"] p {
        color: inherit !important;
    }

    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        color: #059669 !important;
    }

    .stInfo {
        background-color: rgba(79, 70, 229, 0.1) !important;
        color: var(--color-primary) !important;
    }

    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important;
        color: #d97706 !important;
    }

    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        color: #dc2626 !important;
    }

    /* Divider - Subtle */
    .stDivider, hr {
        border: 0;
        border-top: 1px solid var(--color-border);
        margin: 2rem 0;
    }

    /* Header Backdrop avec dégradé progressif */
    [data-testid="stHeader"] {
        background: linear-gradient(180deg,
            rgba(248, 250, 252, 0.95) 0%,
            rgba(248, 250, 252, 0.8) 70%,
            rgba(248, 250, 252, 0) 100%) !important;
        backdrop-filter: blur(8px);
        -webkit-mask-image: linear-gradient(180deg, black 0%, black 70%, transparent 100%);
        mask-image: linear-gradient(180deg, black 0%, black 70%, transparent 100%);
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
       SIDEBAR - Modern Panel
       ================================================================= */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"] {
        border-right: 1px solid var(--color-border);
        background: var(--color-card-bg) !important;
        background-color: var(--color-card-bg) !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--color-text) !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background-color: var(--color-primary) !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: var(--color-primary-hover) !important;
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
       ANIMATIONS - Smooth & Engaging
       ================================================================= */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .question-card, .exercise-card, .feedback-card {
        animation: fadeIn 0.4s ease-out forwards;
    }

    /* =================================================================
       LAYOUT OPTIMIZATION - REDUCE WHITESPACE
       ================================================================= */

    /* Réduire l'espace en haut de la page */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Cacher le footer Streamlit */
    footer {
        visibility: hidden;
        height: 0;
    }

    footer:after {
        content: '';
        visibility: visible;
        display: block;
        position: relative;
        padding: 0.5rem;
    }

    /* Cacher le menu hamburger en haut à droite */
    #MainMenu {
        visibility: hidden;
    }

    /* Réduire l'espace au-dessus du header */
    header {
        background: transparent !important;
    }

    .stApp header {
        background-color: transparent !important;
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

    /* Ensure form submit buttons have modern edtech styling */
    .stForm button,
    .stForm button[kind="primary"],
    .stForm [data-testid="baseButton-primary"],
    .stForm [data-testid="baseButton-secondary"],
    .stForm [type="submit"] {
        background-color: var(--color-primary) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.625rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }

    .stForm button:hover,
    .stForm button[kind="primary"]:hover,
    .stForm [data-testid="baseButton-primary"]:hover,
    .stForm [data-testid="baseButton-secondary"]:hover,
    .stForm [type="submit"]:hover {
        background-color: var(--color-primary-hover) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        transform: translateY(-1px);
    }

    .stForm button p,
    .stForm button span,
    .stForm button[kind="primary"] p,
    .stForm button[kind="primary"] span,
    .stForm [data-testid="baseButton-primary"] p,
    .stForm [data-testid="baseButton-primary"] span,
    .stForm [data-testid="baseButton-secondary"] p,
    .stForm [data-testid="baseButton-secondary"] span,
    .stForm [type="submit"] p,
    .stForm [type="submit"] span {
        color: #FFFFFF !important;
    }

    /* Force white text on all form buttons */
    .stForm button *,
    .stForm [data-testid^="baseButton"] * {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)


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
    chapter_options = {ch['title']: ch['id'] for ch in chapters}
    
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

    # Panneau RAG Debug (si activé et chunks disponibles)
    if st.session_state.rag_debug_mode and st.session_state.rag_chunks:
        with st.expander("Contexte RAG", expanded=False):
            render_rag_debug_panel(st.session_state.rag_chunks)

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

                # Validation réaliste (comme en khôlle)
                if (result["is_complete"] and result["score"] >= 75):
                    st.session_state.question_validated = True
                    st.session_state.validation_score = result["score"]
                    st.session_state.validation_details = {
                        "score": result["score"],
                        "missing_points": result["missing_points"]
                    }

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


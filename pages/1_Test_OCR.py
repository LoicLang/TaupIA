"""
Page de test OCR - Transcription d'images mathématiques
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ai_router import transcribe_image, get_available_ocr_providers, get_ocr_provider_name
from application.settings import get_settings

st.set_page_config(
    page_title="Test OCR - TaupIA",
    page_icon="📷",
    layout="wide",
)

# CSS minimal cohérent avec l'app principale
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --color-primary: #4f46e5;
        --color-primary-hover: #4338ca;
        --color-bg: #f8fafc;
        --color-card-bg: #ffffff;
        --color-border: #e2e8f0;
        --color-text: #1e293b;
        --color-text-muted: #64748b;
        --radius-md: 12px;
        --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--color-bg) !important;
    }

    .stButton > button {
        background-color: var(--color-primary) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 500 !important;
    }

    .stButton > button:hover {
        background-color: var(--color-primary-hover) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }

    .result-box {
        background: var(--color-card-bg);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .prompt-box {
        background: #f1f5f9;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        white-space: pre-wrap;
        max-height: 300px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="padding: 1rem 0;">
    <h1 style="font-size: 2rem; margin: 0; font-weight: 700; color: #000;">Test OCR</h1>
    <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #888; font-family: 'JetBrains Mono', monospace;">
        Transcription d'images mathématiques en LaTeX
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar pour configuration OCR
with st.sidebar:
    st.markdown("## Configuration OCR")

    # Récupérer les providers disponibles
    available_providers = get_available_ocr_providers()

    # Map pour les noms d'affichage
    provider_labels = {
        "gemini": "Gemini",
        "kimi": "Kimi (K2.5)",
    }

    if len(available_providers) > 1:
        # Initialiser le provider dans session_state si pas déjà fait
        if "ocr_provider" not in st.session_state:
            st.session_state.ocr_provider = get_settings().ocr_provider

        # Créer les options avec labels
        options = [provider_labels.get(p, p) for p in available_providers]
        current_provider = st.session_state.ocr_provider
        current_index = available_providers.index(current_provider) if current_provider in available_providers else 0

        selected_label = st.selectbox(
            "Provider",
            options=options,
            index=current_index,
        )

        # Récupérer le provider correspondant au label
        selected_provider = available_providers[options.index(selected_label)]

        if selected_provider != st.session_state.ocr_provider:
            st.session_state.ocr_provider = selected_provider
            st.success(f"Provider: {selected_label}")
    elif len(available_providers) == 1:
        st.info(f"Provider: {provider_labels.get(available_providers[0], available_providers[0])}")
        st.session_state.ocr_provider = available_providers[0]
    else:
        st.error("Aucun provider OCR configuré. Vérifie les clés API dans .env")

    st.divider()

    # Afficher le prompt OCR
    with st.expander("Voir le prompt OCR", expanded=False):
        try:
            settings = get_settings()
            prompt = settings.load_prompt("ocr")
            st.markdown(f'<div class="prompt-box">{prompt}</div>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("Prompt OCR non trouvé")

# Zone principale
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### Image")

    uploaded_file = st.file_uploader(
        "Importer une image",
        type=["jpg", "jpeg", "png", "heic", "webp"],
        help="Photo de brouillon, exercice manuscrit, ou formule mathématique",
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Image importée", use_container_width=True)

        if st.button("Transcrire", type="primary", use_container_width=True):
            with st.spinner("Transcription en cours..."):
                try:
                    image_bytes = uploaded_file.getvalue()
                    mime_type = uploaded_file.type or "image/jpeg"

                    transcription = transcribe_image(image_bytes, mime_type)

                    st.session_state.ocr_result = transcription
                    st.session_state.ocr_success = True

                except Exception as e:
                    st.session_state.ocr_result = str(e)
                    st.session_state.ocr_success = False

with col2:
    st.markdown("### Transcription")

    if "ocr_result" in st.session_state and st.session_state.ocr_result:
        if st.session_state.get("ocr_success", False):
            # Afficher le résultat brut
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("**Texte brut :**")
            st.code(st.session_state.ocr_result, language=None)
            st.markdown('</div>', unsafe_allow_html=True)

            # Afficher le rendu LaTeX
            st.markdown("**Rendu LaTeX :**")
            st.markdown(st.session_state.ocr_result)

            # Bouton copier
            st.download_button(
                "Télécharger le texte",
                data=st.session_state.ocr_result,
                file_name="transcription.txt",
                mime="text/plain",
            )
        else:
            st.error(f"Erreur: {st.session_state.ocr_result}")
    else:
        st.info("Importe une image et clique sur 'Transcrire' pour voir le résultat.")

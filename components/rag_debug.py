"""
Composant RAG Debug pour Khôlleur AI.

Affiche un panneau de debug visuel montrant les chunks de contexte
utilisés par le RAG, avec leurs scores de pertinence et métadonnées.
"""

import streamlit as st
from typing import List, Dict


# =============================================================================
# STYLES CSS POUR LE PANNEAU RAG DEBUG
# =============================================================================

RAG_DEBUG_CSS = """
<style>
    /* Container principal du debug RAG */
    .rag-debug-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Card pour chaque chunk */
    .rag-chunk-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #2C3E87;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .rag-chunk-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    /* Score haute pertinence */
    .rag-chunk-card.high-score {
        border-left-color: #2E7D32;
    }
    
    /* Score moyenne pertinence */
    .rag-chunk-card.medium-score {
        border-left-color: #FF6B35;
    }
    
    /* Score faible pertinence */
    .rag-chunk-card.low-score {
        border-left-color: #c62828;
    }
    
    /* Header du chunk */
    .chunk-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .chunk-title {
        font-weight: 600;
        color: #2C3E87;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .chunk-title .icon {
        font-size: 1.1rem;
    }
    
    /* Badge de score */
    .score-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .score-badge.high {
        background: #c8e6c9;
        color: #2E7D32;
    }
    
    .score-badge.medium {
        background: #ffe0b2;
        color: #e65100;
    }
    
    .score-badge.low {
        background: #ffcdd2;
        color: #c62828;
    }
    
    /* Gauge visuelle du score */
    .score-gauge {
        width: 60px;
        height: 6px;
        background: #e0e0e0;
        border-radius: 3px;
        overflow: hidden;
        margin-left: 0.5rem;
    }
    
    .score-gauge-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    
    .score-gauge-fill.high { background: linear-gradient(90deg, #66bb6a, #2E7D32); }
    .score-gauge-fill.medium { background: linear-gradient(90deg, #ffb74d, #FF6B35); }
    .score-gauge-fill.low { background: linear-gradient(90deg, #ef5350, #c62828); }
    
    /* Métadonnées */
    .chunk-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 0.5rem 0;
        font-size: 0.8rem;
        color: #666;
    }
    
    .chunk-meta-item {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    /* Extrait du contenu */
    .chunk-excerpt {
        color: #444;
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0.75rem 0;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 6px;
        font-family: 'Source Serif 4', Georgia, serif;
    }
    
    /* Tags de type */
    .content-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    
    .content-tag {
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .content-tag.definition {
        background: #e3f2fd;
        color: #1565c0;
    }
    
    .content-tag.theorem {
        background: #f3e5f5;
        color: #7b1fa2;
    }
    
    .content-tag.proof {
        background: #fff3e0;
        color: #e65100;
    }
    
    .content-tag.example {
        background: #e8f5e9;
        color: #2e7d32;
    }
    
    /* Animation d'apparition */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .rag-chunk-card {
        animation: fadeInUp 0.3s ease forwards;
    }
    
    .rag-chunk-card:nth-child(1) { animation-delay: 0.1s; }
    .rag-chunk-card:nth-child(2) { animation-delay: 0.2s; }
    .rag-chunk-card:nth-child(3) { animation-delay: 0.3s; }
    .rag-chunk-card:nth-child(4) { animation-delay: 0.4s; }
    .rag-chunk-card:nth-child(5) { animation-delay: 0.5s; }
</style>
"""


def get_score_class(score: float) -> str:
    """Retourne la classe CSS selon le score."""
    if score >= 70:
        return "high"
    elif score >= 40:
        return "medium"
    return "low"


def get_content_icon(metadata: Dict) -> str:
    """Retourne l'icône selon le type de contenu."""
    if metadata.get("has_definition"):
        return "📖"
    elif metadata.get("has_theorem"):
        return "📐"
    elif metadata.get("has_proof"):
        return "✏️"
    elif metadata.get("has_example"):
        return "🔢"
    return "📄"


def truncate_content(content: str, max_length: int = 150) -> str:
    """Tronque le contenu intelligemment."""
    if len(content) <= max_length:
        return content
    
    # Chercher le dernier espace avant la limite
    truncated = content[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:
        truncated = truncated[:last_space]
    
    return truncated.strip() + "..."


def render_rag_debug_panel(rag_context: List[Dict]) -> None:
    """
    Affiche le panneau de debug RAG dans Streamlit avec design soigné.
    
    Args:
        rag_context: Liste des chunks RAG retournés par get_rag_context()
                     Chaque chunk contient: chunk_id, content, score, metadata
    
    Ce panneau affiche:
    - Cards pour chaque chunk avec titre et score
    - Gauge visuelle du score de pertinence
    - Extrait du contenu (150 chars)
    - Tags de type (définition, théorème, preuve, exemple)
    - Expander pour voir le contenu complet
    """
    # Injecter les styles CSS
    st.markdown(RAG_DEBUG_CSS, unsafe_allow_html=True)
    
    # Header du panneau
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
        <span style="font-size: 1.2rem;">🔍</span>
        <span style="font-weight: 600; color: #2C3E87;">Contexte RAG utilisé</span>
        <span style="font-size: 0.8rem; color: #666; margin-left: auto;">
            {} chunk(s) récupéré(s)
        </span>
    </div>
    """.format(len(rag_context)), unsafe_allow_html=True)
    
    if not rag_context:
        st.info("Aucun chunk de contexte disponible pour cette requête.")
        return
    
    # Afficher chaque chunk
    for idx, chunk in enumerate(rag_context):
        chunk_id = chunk.get("chunk_id", f"chunk_{idx}")
        content = chunk.get("content", "")
        score = chunk.get("score", 0)
        metadata = chunk.get("metadata", {})
        
        score_class = get_score_class(score)
        icon = get_content_icon(metadata)
        
        # Construire le titre
        section = metadata.get("section", "")
        subsection = metadata.get("subsection", "")
        title = section
        if subsection and subsection != section:
            title += f" › {subsection}"
        if not title:
            title = f"Chunk #{idx + 1}"
        
        # Construire les tags de contenu
        tags_html = '<div class="content-tags">'
        if metadata.get("has_definition"):
            tags_html += '<span class="content-tag definition">📖 Définition</span>'
        if metadata.get("has_theorem"):
            tags_html += '<span class="content-tag theorem">📐 Théorème</span>'
        if metadata.get("has_proof"):
            tags_html += '<span class="content-tag proof">✏️ Preuve</span>'
        if metadata.get("has_example"):
            tags_html += '<span class="content-tag example">🔢 Exemple</span>'
        tags_html += '</div>'
        
        # Carte HTML du chunk
        card_html = f"""
        <div class="rag-chunk-card {score_class}-score">
            <div class="chunk-header">
                <div class="chunk-title">
                    <span class="icon">{icon}</span>
                    {title}
                </div>
                <div style="display: flex; align-items: center;">
                    <span class="score-badge {score_class}">{score:.0f}%</span>
                    <div class="score-gauge">
                        <div class="score-gauge-fill {score_class}" style="width: {score}%;"></div>
                    </div>
                </div>
            </div>
            
            <div class="chunk-meta">
                <span class="chunk-meta-item">📍 {chunk_id}</span>
                <span class="chunk-meta-item">📏 {metadata.get('char_count', len(content))} chars</span>
                <span class="chunk-meta-item">⭐ Difficulté: {metadata.get('difficulty', '?')}/5</span>
            </div>
            
            <div class="chunk-excerpt">
                {truncate_content(content)}
            </div>
            
            {tags_html}
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Expander pour le contenu complet
        with st.expander(f"📄 Voir le chunk complet ({len(content)} caractères)"):
            st.markdown(content)


def render_rag_debug_toggle() -> bool:
    """
    Affiche le toggle pour activer/désactiver le mode debug RAG.
    À utiliser dans la sidebar.
    
    Returns:
        bool: True si le mode debug est activé
    """
    return st.toggle(
        "🔍 Mode Debug RAG",
        value=st.session_state.get("rag_debug_mode", False),
        help="Affiche les chunks de contexte utilisés par le RAG"
    )


# =============================================================================
# DONNÉES MOCK POUR TESTS
# =============================================================================

MOCK_RAG_CHUNKS = [
    {
        "chunk_id": "cours_chunk_0012",
        "content": """### III.2 Sous-groupes

**Définition (Sous-groupe)** Soit $(G, *)$ un groupe. On dit que $H \\subset G$ est un **sous-groupe** de $G$ si :
1. $H \\neq \\emptyset$
2. $\\forall x, y \\in H$, $x * y \\in H$ (stabilité)
3. $\\forall x \\in H$, $x^{-1} \\in H$ (stabilité par inverse)

**Notation.** On écrit $H \\leq G$ pour dire que $H$ est un sous-groupe de $G$.""",
        "score": 87.5,
        "metadata": {
            "chapter": "Structures algébriques",
            "section": "III Groupes",
            "subsection": "III.2 Sous-groupes",
            "difficulty": 2,
            "has_definition": True,
            "has_theorem": False,
            "has_proof": False,
            "has_example": False,
            "chunk_index": 12,
            "char_count": 456
        }
    },
    {
        "chunk_id": "cours_chunk_0015",
        "content": """**Proposition (Caractérisation des sous-groupes)**
Soit $(G, *)$ un groupe et $H \\subset G$ non vide. Alors :
$$H \\leq G \\Leftrightarrow \\forall x, y \\in H, \\; x * y^{-1} \\in H$$

Cette caractérisation est très utile car elle combine les deux conditions de stabilité en une seule.

*Démonstration.* Voir exercice 3.2.""",
        "score": 72.3,
        "metadata": {
            "chapter": "Structures algébriques",
            "section": "III Groupes",
            "subsection": "III.2 Sous-groupes",
            "difficulty": 3,
            "has_definition": False,
            "has_theorem": True,
            "has_proof": False,
            "has_example": False,
            "chunk_index": 15,
            "char_count": 389
        }
    },
    {
        "chunk_id": "cours_chunk_0018",
        "content": """**Exemples de sous-groupes**

1. $(\\mathbb{Z}, +) \\leq (\\mathbb{Q}, +) \\leq (\\mathbb{R}, +)$
2. Pour tout groupe $G$ : $\\{e\\} \\leq G$ et $G \\leq G$ (sous-groupes triviaux)
3. $n\\mathbb{Z} = \\{kn : k \\in \\mathbb{Z}\\}$ est un sous-groupe de $(\\mathbb{Z}, +)$

**Contre-exemple.** $\\mathbb{N}$ n'est pas un sous-groupe de $(\\mathbb{Z}, +)$ car il ne contient pas les inverses.""",
        "score": 54.8,
        "metadata": {
            "chapter": "Structures algébriques",
            "section": "III Groupes",
            "subsection": "III.2 Sous-groupes",
            "difficulty": 1,
            "has_definition": False,
            "has_theorem": False,
            "has_proof": False,
            "has_example": True,
            "chunk_index": 18,
            "char_count": 412
        }
    }
]


if __name__ == "__main__":
    # Test du composant
    st.set_page_config(page_title="Test RAG Debug", layout="wide")
    st.title("🔍 Test du panneau RAG Debug")
    
    with st.expander("🔍 Contexte RAG", expanded=True):
        render_rag_debug_panel(MOCK_RAG_CHUNKS)

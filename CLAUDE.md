# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Khôlleur AI simulates oral math exams ("khôlles") for French MPSI preparatory school students. It challenges students with questions and provides Socratic feedback—it does NOT teach or explain course material.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Ingest data into ChromaDB (after adding new questions/exercises/courses)
python data/ingest.py
```

## Architecture

```
app.py                  # Main Streamlit app (UI, session state, pages)
config.py               # Centralized configuration (paths, API keys, model names)
data/
  ingest.py            # Load questions/exercises/courses into ChromaDB
  query.py             # Vector search and RAG retrieval from ChromaDB
services/
  gemini_service.py    # Gemini API calls (OCR, evaluation, Socratic feedback)
components/
  rag_debug.py         # Debug panel for RAG context visualization
```

**Data Flow:**
1. Questions (JSON), exercises (Markdown), courses (Markdown) are ingested into ChromaDB with embeddings
2. User selects a chapter → app retrieves random question
3. User answers (text or photo) → Gemini evaluates using RAG context
4. Socratic feedback guides student without revealing answers

**Key Collections in ChromaDB:**
- `questions_cours`: Course questions with metadata (chapter, difficulty)
- `exercices`: Exercises with solutions
- `cours_chunks`: Course reference chunks

## Design System: Engineering Precision

Vibe inspirée de **SpaceX / Tesla UI** — minimaliste, noir et blanc, précision instrumentale.

### Palette de couleurs
```css
--color-primary: #000000      /* Noir pur */
--color-accent: #000000       /* Noir (pas de couleur d'accent) */
--color-bg: #FFFFFF           /* Blanc pur */
--color-border: #E5E5E5       /* Gris clair pour bordures */
--color-border-strong: #000000 /* Noir pour bordures actives */
--color-text: #000000         /* Texte principal */
--color-text-muted: #888888   /* Texte secondaire */
```

### Typographie
- **Police principale**: Inter (sans-serif)
- **Police monospace**: JetBrains Mono
- **Style**: Uppercase avec letter-spacing pour les labels et boutons

### Principes de design
- **Pas d'emojis** dans l'interface
- **Pas d'ombres** — utiliser des bordures fines (1px)
- **Coins quasi-carrés** (border-radius: 2px)
- **Texte sobre et technique** en français
- **Labels uppercase** avec letter-spacing: 0.05em à 0.1em
- **Animations subtiles** (fade uniquement, pas de translate)

### Composants
| Élément | Style |
|---------|-------|
| Header | Fond noir, texte blanc uppercase |
| Boutons | Fond noir, texte blanc, uppercase, letter-spacing |
| Cards | Bordure 1px gris, fond transparent, hover = bordure noire |
| Inputs | Bordure 1px gris, fond transparent |
| Messages | Bordure gauche noire (assistant) ou bordure complète (user) |

### Exemples de texte
- ❌ "🚀 Lancer la khôlle"  →  ✅ "Démarrer"
- ❌ "📝 Question de cours"  →  ✅ "QUESTION DE COURS"
- ❌ "🎉 Khôlle terminée !"  →  ✅ "Session terminée"
- ❌ "🤔 Le khôlleur réfléchit..."  →  ✅ "Analyse en cours..."

## Code Rules (from context.md)

- **Simple > clever**: Prioritize readability
- **One function = one responsibility**
- **Interface in French**: All UI text in French (but technical/sober tone)
- **Feedback explains the error**, not just "wrong"
- **Socratic method**: Never give answers directly; guide through questions
- **No emojis**: Keep interface clean and professional

## Math/LaTeX Formatting

- All math content uses LaTeX
- Streamlit: `st.latex()` for blocks, `$...$` inline in `st.markdown()`
- JSON files contain raw LaTeX—do not escape it

## What This App Does NOT Do

- No course explanations or teaching from scratch
- No user authentication or accounts
- No traditional database (all data in local files + ChromaDB)

## Tech Stack

- Python 3.x + Streamlit
- Google Gemini (`gemini-3-flash-preview` for OCR/evaluation, `text-embedding-004` for embeddings)
- ChromaDB (persistent vector database in `chroma_db/`)
- Environment: API key in `.env` as `GOOGLE_API_KEY`

# MCP Gemini Design - MANDATORY FOR FRONTEND

## ⛔ ABSOLUTE RULE - NEVER IGNORE

**You MUST NEVER write frontend/UI code yourself.**

Gemini is your frontend developer. You are NOT allowed to create visual components, pages, or interfaces without going through Gemini. This is NON-NEGOTIABLE.

### When to use Gemini? ALWAYS for:
- Creating a page (dashboard, landing, settings, etc.)
- Creating a visual component (card, modal, sidebar, form, button, etc.)
- Modifying the design of an existing element
- Anything related to styling/layout

### Exceptions (you can do it yourself):
- Modifying text/copy
- Adding JS logic without changing the UI
- Non-visual bug fixes
- Data wiring (useQuery, useMutation, etc.)

## MANDATORY Workflow

### Current project status: Design ESTABLISHED
The project uses **"Engineering Precision"** vibe (SpaceX/Tesla inspired).
See "Design System: Engineering Precision" section above for guidelines.

### When modifying UI:
```
ALWAYS pass the CSS from app.py (lines 45-250) in the `context` parameter
ALWAYS follow the Engineering Precision guidelines
```

### For new projects without existing design
```
STEP 1: generate_vibes → show options to the user
STEP 2: User chooses their vibe
STEP 3: create_frontend with the chosen vibe
```

### 3. After Gemini's response
```
Gemini returns code → YOU write it to disk with Write/Edit
```

## Checklist before coding frontend

- [ ] Am I creating/modifying something visual?
- [ ] If YES → STOP → Use Gemini
- [ ] If NO (pure logic) → You can continue

## ❌ WHAT IS FORBIDDEN

- Writing a React component with styling without Gemini
- Creating a page without Gemini
- "Reusing existing styles" as an excuse to not use Gemini
- Doing frontend "quickly" yourself

## ✅ WHAT IS EXPECTED

- Call Gemini BEFORE writing any frontend code
- Ask the user for their vibe choice if new project
- Let Gemini design, you implement
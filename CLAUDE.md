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

## Design System: Modern EdTech

Vibe inspirée de **Duolingo / Khan Academy / Notion** — moderne, coloré mais professionnel, interface accueillante.

### Palette de couleurs
```css
--color-primary: #4f46e5      /* Indigo */
--color-primary-hover: #4338ca
--color-accent: #8b5cf6       /* Purple */
--color-success: #10b981      /* Green */
--color-bg: #f8fafc           /* Light blue-gray */
--color-card-bg: #ffffff
--color-border: #e2e8f0       /* Light gray */
--color-text: #1e293b         /* Dark slate */
--color-text-muted: #888888
--color-user-bubble: #4f46e5  /* Indigo pour messages user */
--color-tutor-bubble: #ffffff /* Blanc pour messages assistant */
```

### Typographie
- **Police principale**: Inter (sans-serif)
- **Police monospace**: JetBrains Mono
- **Style**: Texte normal (pas de uppercase systématique), letter-spacing subtil pour les labels

### Principes de design
- **Pas d'emojis excessifs** (utilisés avec parcimonie uniquement quand pertinent)
- **Ombres douces** — box-shadow subtiles pour profondeur
- **Coins arrondis** (border-radius: 8-20px selon l'élément)
- **Texte sobre et technique** en français
- **Transitions fluides** pour les interactions
- **Glassmorphism subtil** pour le header (backdrop-filter: blur)

### Composants
| Élément | Style |
|---------|-------|
| Header | Fond blanc transparent avec blur, dégradé progressif vers transparent |
| Boutons | Fond indigo, coins arrondis 12px, hover avec ombre indigo + translateY |
| Cards | Bordure légère, coins arrondis, fond blanc, ombres subtiles |
| Inputs | Bordure grise, coins arrondis, fond transparent |
| Messages User | À droite, fond indigo, texte blanc, coins arrondis |
| Messages Assistant | À gauche, fond blanc, bordure gauche indigo, texte noir |

### UX/UI Rules
- **Temporal sequencing**: Message user apparaît d'abord, puis spinner, puis réponse AI
- **Image upload**: Cachée dans expander collapsed après upload (max 300px width)
- **Form order**: Textarea FIRST (prioritaire), puis photo upload SECOND
- **Spinner location**: Entre le chat history et le formulaire (pas en dessous du form)
- **No message truncation**: max-height: none, overflow: visible pour tous les messages

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

## API Error Handling

**Gemini 503 Errors (Overloaded):**
- All Gemini API calls use `call_gemini_with_retry()` wrapper
- Automatic retry with exponential backoff: 2s → 4s → 8s
- Max 3 attempts before showing error to user
- `max_output_tokens` set to 4096 to prevent response truncation
- Located in `services/gemini_service.py`

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
The project uses **"Modern EdTech"** vibe (Duolingo/Khan Academy/Notion inspired).
See "Design System: Modern EdTech" section above for guidelines.

### When modifying UI:
```
ALWAYS pass the CSS from app.py (lines 45-1000) in the `context` parameter
ALWAYS follow the Modern EdTech guidelines
Respect indigo color scheme and rounded corners
Ensure temporal sequencing and proper message display
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
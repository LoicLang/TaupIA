# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kholleur AI simulates oral math exams ("kholles") for French MPSI preparatory school students. It challenges students with questions and provides Socratic feedback—it does NOT teach or explain course material.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run tests
python -m pytest tests/unit/ -v
```

## Architecture

```
kholleur/
├── core/                           # Domain layer (no external dependencies)
│   ├── entities/                   # Domain objects
│   │   ├── question.py             # Question, Exercise, Chapter dataclasses
│   │   ├── evaluation.py           # EvaluationResult, Score dataclasses
│   │   └── conversation.py         # Message, ConversationHistory
│   ├── interfaces/                 # Protocols (abstractions)
│   │   ├── llm_provider.py         # Protocol: LLMProvider
│   │   ├── ocr_provider.py         # Protocol: OCRProvider
│   │   └── embedding_provider.py   # Protocol: EmbeddingProvider
│   └── services/                   # (future) Domain services
│
├── infrastructure/                 # Concrete implementations
│   ├── llm/                        # LLM Providers
│   │   ├── base.py                 # BaseLLMProvider (shared retry logic)
│   │   ├── gemini_provider.py      # GeminiLLMProvider
│   │   ├── claude_provider.py      # ClaudeLLMProvider
│   │   ├── deepseek_provider.py    # DeepSeekLLMProvider
│   │   └── kimi_provider.py        # KimiLLMProvider
│   └── ocr/                        # OCR Providers
│       ├── base.py                 # BaseOCRProvider (shared retry, image processing)
│       ├── gemini_ocr.py           # GeminiOCRProvider
│       └── kimi_ocr.py             # KimiOCRProvider
│
├── application/                    # Application services
│   ├── settings.py                 # Pydantic Settings (env vars)
│   ├── container.py                # DI Container / Factory
│   └── ai_service.py               # AI facade (no Streamlit dependency)
│
├── services/                       # Application layer (Streamlit bridge)
│   ├── ai_router.py                # Routes to ai_service and OCR providers
│   └── knowledge_service.py        # Knowledge graph + data access (replaces ChromaDB)
│
├── prompts/                        # Externalized prompts
│   ├── kholleur_system.txt         # Main system prompt
│   ├── evaluation.txt              # Evaluation prompt template
│   ├── exercise_guide.txt          # Exercise guidance template
│   └── ocr.txt                     # OCR system prompt
│
├── ui/streamlit/                   # UI layer
│   └── styles.css                  # Externalized CSS (960+ lines)
│
├── data/                           # Structured data (JSON)
│   ├── knowledge_graph.json        # 928 nodes, 2236 edges (Chapter/Concept/Exercise/Kholle)
│   ├── questions_kholle.json       # 127 kholle questions with attendus/erreurs/relances
│   ├── programme.json              # Programme officiel MPSI (20 chapitres)
│   ├── cours/                      # 17 course JSON files (1+ per chapter)
│   │   ├── logique_ens.json
│   │   └── ...
│   └── exercices/                  # 17 exercise JSON files (1 per chapter)
│       ├── logique_ens.json
│       └── ...
│
├── tests/                          # Tests
│   └── unit/
│       ├── test_entities.py
│       ├── test_settings.py
│       ├── test_container.py
│       ├── test_llm_providers.py
│       └── test_knowledge_service.py
│
└── app.py                          # Main Streamlit app
```

**Data Flow:**
1. All data is loaded from JSON files at startup into `KnowledgeService` (~2 Mo in memory)
2. User selects a chapter → app retrieves random question from `questions_kholle.json`
3. User answers (text or photo) → LLM evaluates using structured context from the knowledge graph
4. Structured context = exact definitions/theorems tested (via TESTS edges) + programme constraints
5. After validation, exercise is matched by shared concepts (via graph traversal), not just chapter/difficulty

**Knowledge Graph:**
- **Nodes**: Chapter (20), Concept (338), Exercise (443), Kholle (127)
- **Edges**: BELONGS_TO, REQUIRES, TESTS (links questions/exercises to concepts), APPLIES_METHOD
- Deterministic lookup replaces probabilistic RAG: for each kholle question, traverse TESTS edges to find exact concepts tested, then load their LaTeX content from Cours JSON

**Key Abstractions:**
- `KnowledgeService`: In-memory JSON database with graph traversal (replaces ChromaDB)
- `LLMProvider` Protocol: Common interface for Gemini, Claude, DeepSeek, Kimi
- `OCRProvider` Protocol: Common interface for image transcription
- `BaseLLMProvider` / `BaseOCRProvider`: Shared retry logic, prompt loading
- `Container`: Dependency injection for provider creation
- `Settings`: Pydantic-based configuration from `.env`

## Adding a New LLM Provider

1. Create `infrastructure/llm/new_provider.py` extending `BaseLLMProvider`
2. Implement `_init_client()` and `_call_api()` methods
3. Add factory method in `application/container.py`
4. Add API key to `application/settings.py`

## Adding a New OCR Provider

1. Create `infrastructure/ocr/new_ocr.py` extending `BaseOCRProvider`
2. Implement `_init_client()` and `_call_api()` methods
3. Add factory method `_create_new_ocr()` in `application/container.py`
4. Add model name to `application/settings.py`

## Design System: Modern EdTech

Vibe inspired by **Duolingo / Khan Academy / Notion** — modern, colorful but professional.

### Color Palette
```css
--color-primary: #4f46e5      /* Indigo */
--color-primary-hover: #4338ca
--color-accent: #8b5cf6       /* Purple */
--color-success: #10b981      /* Green */
--color-bg: #f8fafc           /* Light blue-gray */
--color-card-bg: #ffffff
--color-border: #e2e8f0       /* Light gray */
--color-text: #1e293b         /* Dark slate */
```

### Typography
- **Main font**: Inter (sans-serif)
- **Monospace**: JetBrains Mono

### Design Principles
- No excessive emojis
- Soft shadows for depth
- Rounded corners (8-20px)
- Sober technical text in French
- Smooth transitions
- Subtle glassmorphism for header

## Code Rules

- **Simple > clever**: Prioritize readability
- **One function = one responsibility**
- **Interface in French**: All UI text in French
- **Feedback explains the error**, not just "wrong"
- **Socratic method**: Never give answers directly; guide through questions
- **No emojis** in code or interface

## Math/LaTeX Formatting

- All math content uses LaTeX
- Streamlit: `st.latex()` for blocks, `$...$` inline in `st.markdown()`
- JSON files contain raw LaTeX—do not escape it

## What This App Does NOT Do

- No course explanations or teaching from scratch
- No user authentication or accounts
- No traditional database (all data in local JSON files)

## Tech Stack

- Python 3.11+ with type hints
- Streamlit for UI
- Multiple LLM providers: Gemini, Claude, DeepSeek (V3.2), Kimi (K2.5)
- Multiple OCR providers: Gemini, Kimi (K2.5)
- In-memory JSON with knowledge graph (deterministic lookup, no vector DB)
- Pydantic for settings validation
- Environment: API keys in `.env`

## API Error Handling

All LLM and OCR providers use shared retry logic in base classes:
- Automatic retry with exponential backoff: 2s → 4s → 8s
- Max 3 attempts before showing error to user
- Handles 503/500 errors and rate limits
- Empty response detection and retry

## Environment Variables

```bash
# Required
GOOGLE_API_KEY=...          # For Gemini

# Optional (for additional providers)
CLAUDE_API_KEY=...          # For Claude
DEEPSEEK_API_KEY=...        # For DeepSeek
KIMI_API_KEY=...            # For Kimi (Moonshot AI)

# LLM Model configuration (optional, has defaults)
GEMINI_MODEL=gemini-3-flash-preview
CLAUDE_MODEL=claude-sonnet-4-5-20250929
DEEPSEEK_MODEL=deepseek-chat
KIMI_MODEL=kimi-k2.5
DEFAULT_AI_PROVIDER=gemini  # or claude, deepseek, kimi

# OCR Model configuration (optional, has defaults)
GEMINI_OCR_MODEL=gemini-2.0-flash
KIMI_OCR_MODEL=kimi-k2.5
OCR_PROVIDER=gemini         # or kimi
```

## MCP Gemini Design - MANDATORY FOR FRONTEND

### When to use Gemini MCP for UI:
- Creating a page (dashboard, landing, settings, etc.)
- Creating a visual component (card, modal, sidebar, form, etc.)
- Modifying the design of an existing element
- Anything related to styling/layout

### Exceptions (you can do it yourself):
- Modifying text/copy
- Adding logic without changing the UI
- Non-visual bug fixes
- Data wiring

### Workflow
```
1. ALWAYS pass CSS from ui/streamlit/styles.css in the `context` parameter
2. ALWAYS follow the Modern EdTech guidelines
3. Respect indigo color scheme and rounded corners
4. Gemini returns code → YOU write it to disk
```

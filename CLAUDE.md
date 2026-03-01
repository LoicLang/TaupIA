# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kholleur AI (TaupIA) simulates oral math exams ("kholles") for French MPSI preparatory school students. It challenges students with questions and provides Socratic feedback—it does NOT teach or explain course material.

## Commands

```bash
# Install backend dependencies
pip install -r requirements.txt

# Run backend (FastAPI)
uvicorn backend.main:app --reload

# Run frontend (Next.js)
cd frontend && npm run dev

# Run tests
python -m pytest tests/unit/ -v

# Build frontend
cd frontend && npx next build
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
│   └── ai_service.py               # AI facade (no framework dependency)
│
├── services/                       # Application layer
│   └── knowledge_service.py        # Knowledge graph + data access (replaces ChromaDB)
│
├── backend/                        # FastAPI backend
│   ├── main.py                     # FastAPI app, CORS, lifespan, routers
│   ├── auth.py                     # Clerk JWT verification (conditional)
│   ├── dependencies.py             # DI: init_services(), get_knowledge_service()
│   ├── session_store.py            # In-memory session store (2h TTL)
│   ├── api/                        # API endpoints
│   │   ├── chapters.py             # GET /api/chapters
│   │   ├── providers.py            # GET /api/providers/llm, /api/providers/ocr
│   │   ├── sessions.py             # POST/GET/DELETE /api/sessions
│   │   ├── kholle.py               # POST /api/sessions/{id}/start, /answer, /skip, etc.
│   │   └── ocr.py                  # POST /api/ocr/transcribe
│   └── schemas/
│       └── session.py              # Pydantic request/response models
│
├── frontend/                       # Next.js 16 App Router
│   ├── src/app/
│   │   ├── layout.tsx              # Root layout (ClerkWrapper + AuthProvider)
│   │   ├── page.tsx                # Setup page (chapter, difficulty, format, providers)
│   │   ├── session/[id]/page.tsx   # Session page (question → exercise → results)
│   │   ├── sign-in/                # Clerk sign-in page
│   │   └── sign-up/                # Clerk sign-up page
│   ├── src/components/
│   │   ├── question/QuestionPhase.tsx    # Question phase with OCR + chat
│   │   ├── exercise/ExercisePhase.tsx    # Exercise phase with OCR + chat
│   │   ├── finished/FinishedPhase.tsx    # Results display
│   │   └── shared/                       # GridBackground, LatexRenderer, ClerkWrapper, AuthProvider
│   ├── src/lib/
│   │   ├── api.ts                  # Typed API client (auto-injects Clerk token)
│   │   ├── types.ts                # TypeScript interfaces
│   │   └── utils.ts                # cn() helper
│   └── src/proxy.ts                # Clerk route protection middleware
│
├── prompts/                        # Externalized prompts
│   ├── kholleur_system.txt         # Main system prompt
│   ├── evaluation.txt              # Evaluation prompt template
│   ├── exercise_guide.txt          # Exercise guidance template
│   └── ocr.txt                     # OCR system prompt
│
├── data/                           # Structured data (JSON)
│   ├── knowledge_graph.json        # 928 nodes, 2236 edges
│   ├── questions_kholle.json       # 127 kholle questions
│   ├── programme.json              # Programme officiel MPSI (20 chapters)
│   ├── cours/                      # 17 course JSON files
│   └── exercices/                  # 17 exercise JSON files
│
├── tests/unit/                     # Tests
│
├── railway.toml                    # Railway deployment config
├── .python-version                 # Python 3.12 (for Railway)
├── .railwayignore                  # Excludes frontend/venv from Railway
├── .env.example                    # All env vars documented
│
```

**Data Flow:**
1. All data is loaded from JSON files at startup into `KnowledgeService` (~2 Mo in memory)
2. User selects a chapter + format (full or exercise-only) → app retrieves random question/exercise
3. User answers (text or photo via OCR) → LLM evaluates using structured context from the knowledge graph
4. Structured context = exact definitions/theorems tested (via TESTS edges) + programme constraints
5. After validation, exercise is matched by shared concepts (via graph traversal)

**Knowledge Graph:**
- **Nodes**: Chapter (20), Concept (338), Exercise (443), Kholle (127)
- **Edges**: BELONGS_TO, REQUIRES, TESTS (links questions/exercises to concepts), APPLIES_METHOD
- Deterministic lookup replaces probabilistic RAG

**Key Abstractions:**
- `KnowledgeService`: In-memory JSON database with graph traversal (replaces ChromaDB)
- `LLMProvider` Protocol: Common interface for Gemini, Claude, DeepSeek, Kimi
- `OCRProvider` Protocol: Common interface for image transcription
- `BaseLLMProvider` / `BaseOCRProvider`: Shared retry logic, prompt loading
- `Container`: Dependency injection for provider creation
- `Settings`: Pydantic-based configuration from `.env`

## Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Backend (FastAPI) | Railway | https://kholleur-ai-production.up.railway.app |
| Frontend (Next.js) | Vercel | https://taupia.vercel.app |
| Auth | Clerk | Waitlist mode (invitation-only) |

**Auto-deploy**: Push to `main` on GitHub triggers automatic redeploy on both Vercel and Railway.

**CORS**: Railway env var `CORS_ORIGINS` must include the Vercel domain.

## Authentication (Clerk)

- **Frontend**: `@clerk/nextjs` with `ClerkProvider` in layout, `proxy.ts` for route protection
- **Backend**: `backend/auth.py` verifies JWT via Clerk's JWKS endpoint (PyJWT + RS256)
- **Conditional**: If `CLERK_PUBLISHABLE_KEY` is not set, auth is disabled (local dev)
- **Protected routes**: `/api/sessions/*`, `/api/kholle/*`, `/api/ocr/*`
- **Public routes**: `/api/health`, `/api/chapters`, `/api/providers/*`
- **Token injection**: `AuthProvider` component registers `getToken()` in `api.ts` module

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

## Design System: Dark Modern EdTech

Dark theme with indigo accents, inspired by terminal/developer aesthetic.

### Color Palette
```css
--bg: #0a0a0a                /* Near-black background */
--card-bg: #0f0f0f           /* Slightly lighter cards */
--primary: #4f46e5           /* Indigo */
--accent: #8b5cf6            /* Purple (exercise phase) */
--success: #10b981           /* Green */
--border: white/10           /* Subtle borders */
--text: white/90             /* Primary text */
```

### Typography
- **Main font**: Inter (sans-serif)
- **Monospace**: JetBrains Mono

### Design Principles
- Dark background with subtle grid pattern
- Glassmorphism cards (backdrop-blur, semi-transparent)
- Indigo for questions, purple for exercises
- Mobile-first responsive
- No emojis in interface
- French UI text

## Code Rules

- **Simple > clever**: Prioritize readability
- **One function = one responsibility**
- **Interface in French**: All UI text in French
- **Feedback explains the error**, not just "wrong"
- **Socratic method**: Never give answers directly; guide through questions
- **No emojis** in code or interface

## Math/LaTeX Formatting

- All math content uses LaTeX
- Frontend: `react-markdown` with `remark-math` + `rehype-katex` for rendering
- JSON files contain raw LaTeX — do not escape it

## What This App Does NOT Do

- No course explanations or teaching from scratch
- No traditional database (all data in local JSON files)
- No payment system (yet)

## Tech Stack

- **Backend**: Python 3.12, FastAPI, Pydantic v2
- **Frontend**: Next.js 16.1.6, React 19, TypeScript 5, TailwindCSS v4
- **Auth**: Clerk (@clerk/nextjs + PyJWT backend verification)
- **LLM**: DeepSeek (default), Gemini, Claude, Kimi
- **OCR**: Kimi (default), Gemini
- **Data**: In-memory JSON with knowledge graph (deterministic lookup, no vector DB)
- **Deployment**: Vercel (frontend) + Railway (backend)

## API Error Handling

All LLM and OCR providers use shared retry logic in base classes:
- Automatic retry with exponential backoff: 2s → 4s → 8s
- Max 3 attempts before showing error to user
- Handles 503/500 errors and rate limits
- Empty response detection and retry

## Environment Variables

```bash
# LLM API Keys (at least one required)
GOOGLE_API_KEY=...          # For Gemini
CLAUDE_API_KEY=...          # For Claude
DEEPSEEK_API_KEY=...        # For DeepSeek
KIMI_API_KEY=...            # For Kimi (Moonshot AI)

# LLM Model configuration (optional, has defaults)
GEMINI_MODEL=gemini-3-flash-preview
CLAUDE_MODEL=claude-sonnet-4-5-20250929
DEEPSEEK_MODEL=deepseek-chat
KIMI_MODEL=kimi-k2.5
DEFAULT_AI_PROVIDER=kimi

# OCR Model configuration (optional, has defaults)
GEMINI_OCR_MODEL=gemini-3-flash-preview
KIMI_OCR_MODEL=kimi-k2.5
OCR_PROVIDER=kimi

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000

# Clerk Auth (required in production)
CLERK_PUBLISHABLE_KEY=pk_live_...
CLERK_SECRET_KEY=sk_live_...
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
1. ALWAYS pass design-system.md content in the `designSystem` parameter
2. ALWAYS follow the Dark Modern EdTech guidelines
3. Respect indigo/purple color scheme and dark background
4. Gemini returns code → YOU write it to disk
```

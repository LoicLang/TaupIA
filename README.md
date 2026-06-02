# Kholleur AI — AI Khôlle Simulator

Kholleur AI is a prototype that helps French preparatory school students train for oral math exams.

The project explores how AI can make high-quality practice more accessible between human teaching sessions.

## Problem

Oral exam practice is one of the best ways to progress in preparatory classes, but individual feedback is limited by time, availability, and cost.

## Product idea

Kholleur AI simulates part of a math khôlle experience:

- select a chapter and difficulty;
- answer a course question or exercise;
- receive a structured challenge;
- use text or image input;
- get feedback focused on reasoning and method.

The goal is not to replace teachers. The goal is to give students more opportunities to practice deliberately.

## What it demonstrates

| Area | What it shows |
| --- | --- |
| Accessible AI | individual practice support for more students |
| Full-stack AI product | FastAPI backend and Next.js frontend |
| Knowledge grounding | structured math knowledge graph instead of only free-form generation |
| Provider abstraction | multiple LLM and OCR providers behind common interfaces |
| Deployment | Railway backend and Vercel frontend setup |

## Architecture direction

```text
Student session
  -> FastAPI backend
  -> knowledge service
  -> LLM and OCR providers
  -> structured feedback
  -> Next.js learning interface
```

## Design philosophy

AI should be useful for learning when it helps the student think, practice, and receive feedback.

A good educational assistant should preserve difficulty, encourage reasoning, and make uncertainty visible rather than giving easy answers too quickly.

## Recommended reading

1. `CLAUDE.md`
2. `backend/`
3. `frontend/`
4. `services/knowledge_service.py`
5. `tests/`

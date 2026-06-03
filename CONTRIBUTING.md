# Contributing

Thanks for your interest in TaupIA. This is a personal project, but issues and pull requests
are welcome.

## Setup

See [Getting started](README.md#getting-started) in the README. In short:

```bash
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add at least one LLM API key
```

## Before opening a pull request

- Run the tests: `python -m pytest tests/unit/ -v` (they must pass; CI runs them too).
- If you change frontend UI, run `cd frontend && npm run build` to confirm it compiles.
- Keep the architecture boundaries intact: `core/` stays free of external dependencies; new LLM
  or OCR providers go under `infrastructure/` (see the steps in the README / `CLAUDE.md`).
- One focused change per PR; describe the _why_, not just the _what_.

## Conventions

- **Branches:** `feat/...`, `fix/...`, `chore/...`, `docs/...`.
- **Commits:** imperative mood, a short subject line, a body explaining the reasoning.
- **UI text is in French**; code, comments, and docs are in English.
- **No secrets in commits** — everything sensitive lives in `.env` (gitignored).

## Reporting issues

Open an issue with steps to reproduce, what you expected, and what happened. Screenshots help
for anything UI-related.

# CareLink — AI-Enhanced Telehealth Triage (Scaffold Only)

**Status:** User Story #2 implemented (AI triage at `/triage/chat/`).

## Quickstart
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. (Optional for live AI) Set `GEMINI_API_KEY` in your environment (e.g., export in shell or a `.env` via your preferred loader). Without a key, the page works but won’t call Gemini.
4. `python manage.py migrate`
5. `python manage.py runserver` (uses `carelink.settings.dev`)

## Project Layout
- Django project in `carelink/`
- Apps: `home`, `accounts`, `profiles`, `triage`, `doctors`, `appointments`
- Templates under `templates/` with a medical theme
- Static assets under `static/` (tokens.css, base.css, components.css)
- Health endpoints: `/healthz/`, `/readyz/`

## Tooling
- Black, isort, Flake8, djLint
- Pytest + pytest-django
- Pre-commit hooks (optional)

## Environment
- `GEMINI_API_KEY` (optional): required to make live Gemini requests for AI triage. The app shows a friendly error without it and tests run offline via monkeypatching.

## Next (later)
- Add further user stories and polish as needed

# CareLink — AI-Enhanced Telehealth Triage (Scaffold Only)

**Status:** Scaffold ready. **No user stories implemented yet.**

## Quickstart
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and edit as needed (keep defaults for now).
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

## Next (later)
- Implement user stories one by one
- Connect OpenAI & Maps via service classes
- Add data models & migrations

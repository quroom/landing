# homepage docs

## Project layout (`landing/` single code root)
- `landing/`: Django application code root
- `landing/project/`: Django project settings/urls/asgi/wsgi
- `landing/templates/`: HTML templates
- `landing/static/`: CSS/JS static assets
- `images/`: image assets used by pages
- `openspec/`: OpenSpec changes/spec history
- `manage.py`: local entrypoint

## Migration map (before -> now)
- `quroom_landing/` -> `landing/project/`
- `templates/` -> `landing/templates/`
- `static/` -> `landing/static/`

## Consolidated documentation location
- All landing / vibe-coding docs have moved to `openspec/changes/consolidate-codex-docs-into-openspec/docs/`.
- `codex-document/` now only contains a pointer README.

## Quick links
- Landing spec: `openspec/changes/consolidate-codex-docs-into-openspec/docs/quroom-landing-spec.md`
- Vibe coding guides & prompt library:
  - `openspec/changes/consolidate-codex-docs-into-openspec/docs/general-vibe-coding-guide-for-beginners.md`
  - `openspec/changes/consolidate-codex-docs-into-openspec/docs/vibe-coding-step-by-step-guide.md`
  - `openspec/changes/consolidate-codex-docs-into-openspec/docs/vibe-coding-prompt-library.md`

## Notes
- Asset paths remain under `images/` (unchanged).
- If you reintroduce `quroom-landing-openspec.md`, place it under the consolidated docs path.

## Run landing page locally (Django)
1. Install dependencies
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`
2. Run server
   - `python manage.py migrate`
   - `python manage.py runserver`
3. Open
   - `http://127.0.0.1:8000/`

## Standard check command (always uses `.venv`)
- Django system check:
  - `./scripts/django-check.sh`
- Direct equivalent:
  - `.venv/bin/python manage.py check`

Use this command as the default before applying or archiving OpenSpec changes.

## Pre-push test commands (before GitHub push)
1. System check
   - `./scripts/django-check.sh`
2. Django test suite
   - `./scripts/django-test.sh`
3. One-shot verification
   - `./scripts/verify.sh`

If both pass, push to GitHub.

### Optional environment variables
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`1` or `0`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `GA4_MEASUREMENT_ID` (if you want GA4 tracking)
- `QUROOM_CONTACT_EMAIL` (defaults to `help@quroom.kr`)

### Contact mail ops check
- Production value should be:
  - `QUROOM_CONTACT_EMAIL=help@quroom.kr`
- Verify in runtime settings before deploy:
  - `.venv/bin/python manage.py shell -c "from django.conf import settings; print(settings.QUROOM_CONTACT_EMAIL)"`

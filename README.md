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
- Dokku deploy runbook: `codex-document/dokku-deploy-runbook.md`
- AX tool stack + diagnosis question source: `landing/ax_tool_stack.py`
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
   - Free diagnosis page: `http://127.0.0.1:8000/free-diagnosis/`

## Standard check command (always uses `.venv`)
- Django system check:
  - `./scripts/django-check.sh`
- Direct equivalent:
  - `.venv/bin/python manage.py check`

Use this command as the default before applying or archiving OpenSpec changes.

## Pre-push test commands (before GitHub push)
1. System check
   - `./scripts/format-check.sh`
2. Django system check
   - `./scripts/django-check.sh`
3. Django test suite
   - `./scripts/django-test.sh`
4. One-shot verification
   - `./scripts/verify.sh`

If both pass, push to GitHub.

## Dokku auto deploy (GitHub Actions)
- Workflow: `.github/workflows/deploy-dokku.yml`
- Trigger: `main` branch push (or manual dispatch)
- Required secret:
  - `DOKKU_SSH_PRIVATE_KEY` (dokku push 권한이 있는 개인키)

## Workspace format standard (`ruff + djlint`)
- Python format/lint:
  - apply: `./scripts/format-apply.sh`
  - check: `./scripts/format-check.sh`
- Django template format:
  - `djlint` is the canonical formatter for `landing/templates/**`
  - avoid formatting template files with generic HTML formatters
- VS Code workspace defaults:
  - Python: Ruff formatter
  - Django template (`django-html`): djLint formatter
  - generic HTML remains separate

### Template guardrails
- If a specific line must keep manual layout, use djLint ignore pragmas around the minimum block.
- Prefer splitting long inline template expressions across tags/elements instead of relying on formatter behavior.

## CSS responsibility split (`site.css` vs Tailwind CDN)
- Tailwind utility classes are the default choice for page-level layout, spacing, color, borders, typography sizing, and one-off visual adjustments inside templates.
- `landing/static/landing/css/site.css` is reserved for:
  - global element defaults (`body`, form fields, anchors/offset behavior)
  - reusable project-specific classes not worth expressing repeatedly in templates
  - font-family hooks like `.font-space`
  - small custom animations/utilities such as `.loading-bar`
- Do not duplicate the same concern in both places.
  - Example: if spacing/color/border can be expressed with template utility classes, keep it in Tailwind classes.
  - Example: if a behavior is global across many templates, keep it in `site.css`.

### Tailwind color rule in this project
- Tailwind is loaded from CDN and extended in [base.html](/home/quroom/workspace/homepage/landing/templates/landing/base.html) with single custom color tokens:
  - `navy`
  - `sky`
  - `fog`
  - `mint`
  - `amber`
- Because `amber` is defined as a single custom token, shade classes like `bg-amber-100` or `border-amber-300` are not reliable in this project.
- Use these forms instead:
  - `bg-amber`
  - `bg-amber/10`
  - `border-amber/30`
  - `text-amber-700` only when relying on Tailwind default palette classes already available
- When in doubt, prefer the custom-token style (`bg-amber/...`, `border-amber/...`) for project-specific colors.

### Known limitations / follow-up
- In network-restricted environments, `ruff`/`djlint` installation can fail until package index access is available.
- Once dependencies are available, run `./scripts/format-apply.sh` then `./scripts/verify.sh` to establish baseline formatting in changed files.

## Django gettext i18n workflow
- Prerequisite:
  - GNU gettext binaries (`msguniq`, `msgfmt`) must be installed on your OS.
  - macOS: `brew install gettext` (then ensure PATH includes gettext bin)
  - Ubuntu/Debian: `sudo apt-get install gettext`
- Generate catalogs:
  - `.venv/bin/python manage.py makemessages -l ko -l en`
- Compile catalogs:
  - `.venv/bin/python manage.py compilemessages`
- Notes:
  - Keep user-facing strings in templates/forms/views under `{% trans %}` / `gettext(_lazy)` so `makemessages` can extract them.
  - After translation edits, always run `compilemessages` and `./scripts/verify.sh`.

### Optional environment variables
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`1` or `0`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DATABASE_URL` (preferred in production)
- `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` (fallback if no `DATABASE_URL`)
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` (Cloudtype-style fallback keys)
- `GA4_MEASUREMENT_ID` (if you want GA4 tracking)
- `QUROOM_CONTACT_EMAIL` (defaults to `help@quroom.kr`)
- `CONTACT_EMAIL_ASYNC` (`1` enables async email send, default `0`)
- `DJANGO_SITE_BASE_URL` (메일 CTA 링크 기준 URL, 예: `https://quroom.kr`)

## Cloudtype deployment quickstart
1. Build/install dependencies from `requirements.txt`.
2. Set production env values:
   - `DJANGO_DEBUG=0`
   - `DJANGO_SECRET_KEY` (non-default)
   - `DJANGO_ALLOWED_HOSTS` (no `*`)
   - `DJANGO_CSRF_TRUSTED_ORIGINS`
   - `DATABASE_URL` (or PG*/DB* variables)
3. Use release command:
   - `python manage.py migrate --no-input && python manage.py collectstatic --no-input`
4. Use web command:
   - `gunicorn --workers=2 --threads=2 --bind 0.0.0.0:${PORT:-8000} landing.project.wsgi:application`

`Procfile` already contains matching `release`/`web` entries.

### Local env profiles (recommended)
- `.env.local`: daily local development profile (safe mode)
  - `DJANGO_DEBUG=1`
  - `DJANGO_EMAIL_BACKEND=console`
  - `DJANGO_ALLOW_REAL_EMAIL_IN_DEBUG=0`
- `.env.debug`: intentional debug profile for real SMTP tests
  - `DJANGO_DEBUG=1`
  - `DJANGO_EMAIL_BACKEND=smtp`
  - `DJANGO_ALLOW_REAL_EMAIL_IN_DEBUG=1`
- `.env.deploy`: production deployment template
  - `DJANGO_DEBUG=0`
  - real SMTP backend + async enabled
  - domain/CSRF/secret must be replaced before use
- Production should NOT use local files; set variables in Railway.

#### Profile switch commands
- Apply local safe profile:
  - `cp .env.local .env`
- Apply debug SMTP test profile:
  - `cp .env.debug .env`
- Create deploy template copy (local dry run only):
  - `cp .env.deploy .env`
- (optional) load variables into current shell:
  - `set -a; source .env; set +a`

### SMTP mail settings (for real delivery)
- `DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST` (example: `smtp.daum.net`)
- `EMAIL_PORT` (example: `465` for SSL or `587` for TLS)
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS` (`1` for TLS/587)
- `EMAIL_USE_SSL` (`1` for SSL/465)
- `EMAIL_TIMEOUT` (seconds, default `20`)
- `DJANGO_DEFAULT_FROM_EMAIL` (recommended to match `EMAIL_HOST_USER`)

### Contact + Lead Magnet behavior
- Contact form endpoint: `/contact/submit/`
- Lead magnet endpoint: `/lead-magnet/submit/`
- Lead magnet page: `/free-diagnosis/`
- Lead magnet flow:
  - user submits 8-question diagnosis
  - partial result is shown immediately (score/grade/top priorities)
  - full detailed report is delivered by email

### Async email mode (recommended for slow SMTP)
- Enable:
  - `CONTACT_EMAIL_ASYNC=1`
- Behavior:
  - form response returns immediately
  - email sending runs in background thread
  - UI shows "처리 중" loading indicator during HTMX request
- Note:
  - current async mode is process-local thread based (simple, no queue persistence)
  - if you need retry/durable jobs, migrate to Celery/Redis later

### Contact mail ops check
- Production value should be:
  - `QUROOM_CONTACT_EMAIL=help@quroom.kr`
- Verify in runtime settings before deploy:
  - `.venv/bin/python manage.py shell -c "from django.conf import settings; print(settings.QUROOM_CONTACT_EMAIL)"`
- SMTP smoke test:
  - `set -a; source .env; set +a`
  - `.venv/bin/python manage.py shell -c "from django.core.mail import send_mail; from django.conf import settings; print(send_mail('[SMTP 테스트] QuRoom','SMTP 테스트', settings.DEFAULT_FROM_EMAIL, [settings.QUROOM_CONTACT_EMAIL], fail_silently=False))"`

### Admin operational checks
- Django Admin: `/admin/`
- Admin dashboard: `/admin-dashboard/`
- Recommended quick checks:
  - verify contact inquiry count increases after form submit
  - verify lead-magnet inquiry appears with type `lead_magnet_diagnosis`
  - verify funnel events (`lead_magnet_start`, `lead_magnet_submit`, `lead_magnet_email_sent`) are visible in dashboard metrics

### Testimonial invite ops checklist (face-to-face meeting)
1. Create an invite in Django Admin: `Testimonial invites` (set target note and expiry).
2. Share URL `/testimonials/invite/<token>/` right after the consultation.
3. Confirm submission is stored as `pending` and invite is marked consumed.
4. Review testimonial in Admin and change status to `approved` only if publish-safe.
5. Public testimonial section appears on homepage only when approved count reaches threshold (`TESTIMONIAL_PUBLIC_THRESHOLD`, default `3`).

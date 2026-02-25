## Migration notes

### Moved paths
- `quroom_landing/` -> `landing/project/`
- `templates/` -> `landing/templates/`
- `static/` -> `landing/static/`

### Runtime path updates
- `DJANGO_SETTINGS_MODULE` now points to `landing.project.settings`.
- `ROOT_URLCONF`, `WSGI_APPLICATION`, `ASGI_APPLICATION` now use `landing.project.*`.
- Template/static directories now resolve from `landing/`, while image assets remain in `images/`.

### Verification log
- `python3 -m compileall landing manage.py` passed.
- `./.venv/bin/python manage.py check` passed.
- Main routes (`/`, `/for-founders/`, `/for-foreign-developers/`, `/privacy/`, `/terms/`) verified via Django test client with HTTP 200.
- Static assets verified present:
  - `landing/static/landing/css/site.css`
  - `landing/static/landing/js/site.js`
  - `images/hero-quroom.jpg`
  - `images/logo.jpg`

### Notes
- `runserver` socket bind was blocked in this sandbox (`Operation not permitted`), so route verification used the Django test client instead.

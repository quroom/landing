web: gunicorn --workers=2 --threads=2 --bind 0.0.0.0:${PORT:-8000} landing.project.wsgi:application
release: python manage.py migrate --no-input && python manage.py collectstatic --no-input

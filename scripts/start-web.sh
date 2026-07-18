#!/usr/bin/env sh
set -eu

mkdir -p logs
touch logs/django.log logs/project.log logs/email.log logs/signals.log

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec gunicorn main.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3} --timeout 120

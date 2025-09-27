#!/bin/sh

set -e

python manage.py migrate --noinput

if [ "${DEBUG}" = "0" ]; then
  python manage.py collectstatic --noinput
  exec gunicorn app.wsgi:application --bind 0.0.0.0:${PORT} --workers 3
else
  exec python manage.py runserver 0.0.0.0:${PORT}
fi

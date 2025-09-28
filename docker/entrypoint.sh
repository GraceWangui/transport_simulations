#!/usr/bin/env sh
set -e

# Run migrations only for long-lived containers; don't force them during 'test'
if [ "$1" != "test" ]; then
  python manage.py migrate --noinput
fi

# If the first arg is 'test', run Django tests and exit
if [ "$1" = "test" ]; then
  shift
  exec python manage.py test "$@"
fi

# If any command was provided, run it
if [ "$#" -gt 0 ]; then
  exec "$@"
fi

# Default: run the app (use gunicorn in CI/containers)
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000

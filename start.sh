#!/bin/bash
set -e

# Apply DB migrations
echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn Nird_Quiz.wsgi:application --bind 0.0.0.0:8030 --workers 3

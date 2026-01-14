#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Seeding demo data..."
python manage.py seed_data

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --threads 4 config.wsgi:application

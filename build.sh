#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py makemigrations content_app
python manage.py makemigrations hotel
python manage.py makemigrations users
python manage.py migrate
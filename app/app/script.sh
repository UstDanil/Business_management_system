#!/bin/bash
ENV_FILE=".env"

cd src || { echo "Directory 'src' not found."; exit 1; }

python manage.py migrate
python manage.py collectstatic --noinput
export DJANGO_SUPERUSER_EMAIL=$INIT_ADMIN_EMAIL
export DJANGO_SUPERUSER_PASSWORD=$INIT_ADMIN_PASSWORD
export DJANGO_SUPERUSER_USERNAME=$INIT_ADMIN_USERNAME
python manage.py createsuperuser --no-input

gunicorn --bind 0.0.0.0:8000 config.wsgi
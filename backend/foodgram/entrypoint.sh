#!/bin/sh


python manage.py makemigrations;
python manage.py migrate;
python manage.py collectstatic --noinput;
python manage.py import_csv;
gunicorn --bind ${GUNICORN_HOST}:${GUNICORN_PORT} foodgram.wsgi;
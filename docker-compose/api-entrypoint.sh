#!/bin/bash
docker-compose/wait-for-postgres.sh

poetry run python projects/manage.py db upgrade

echo 'creating db'
poetry run python projects/manage.py db_create
echo 'upgrading db'
poetry run python projects/manage.py db upgrade
echo 'starting server'
poetry run gunicorn -w 2 --bind 0.0.0.0:5000 "projects.app:create_app()"

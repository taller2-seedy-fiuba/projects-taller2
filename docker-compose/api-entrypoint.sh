#!/bin/bash
docker-compose/wait-for-postgres.sh

python s/manage.py db upgrade

echo 'creating db'
python ../manage.py db_create
echo 'upgrading db'
python ../manage.py db upgrade
echo 'starting server'
gunicorn -w 2 --bind 0.0.0.0:5000 "projects.app:create_app()"

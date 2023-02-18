#!/bin/sh
echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python3 manage.py makemigrations --noinput
python3 manage.py migrate
python3 manage.py collectstatic --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(mobile='01111111111').exists() or User.objects.create_superuser(name='admin',mobile='01111111111',password='enter1234')" | python3 manage.py shell
gunicorn --config gunicorn-cfg.py --reload project.wsgi

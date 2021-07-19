#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python services/web/manage.py create_db
python services/web/manage.py insert_db
python services/web/manage.py create_admin
python services/web/manage.py create_unknown
exec "$@"
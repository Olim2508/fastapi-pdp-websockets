#!/bin/sh

#python backend_pre_start.py

echo "Waiting for postgres connection..."

while ! nc -z db 5432; do
    echo "not available yet, waiting for 1 sec"
    sleep 1
done

echo "PostgreSQL started"

echo "Running alembic migrations..."
alembic upgrade head

exec "$@"

#!/bin/sh

while !</dev/tcp/db/5432; do
  sleep 1;
done;

echo "Start app..."
alembic upgrade head

exec "$@"

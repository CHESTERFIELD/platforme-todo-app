#!/bin/sh
set -e

if [ "$RUN_MIGRATE" != "" ];
then
    python manage.py migrate --noinput
fi

if [ "$RUN_COLLECTSTATIC" != "" ];
then
    python manage.py collectstatic --noinput
fi

exec "$@"

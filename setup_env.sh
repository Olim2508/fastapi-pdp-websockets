#!/bin/sh


echo POSTGRES_USER=$POSTGRES_USER >> .env
echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD >> .env
echo POSTGRES_HOST=$POSTGRES_HOST >> .env
echo POSTGRES_PORT=$POSTGRES_PORT >> .env
echo POSTGRES_DB=$POSTGRES_DB >> .env

echo IMAGE=olim2508/fastapi-pdp-blog >> .env

echo WEB_IMAGE=$IMAGE:web  >> .env
echo NGINX_IMAGE=$IMAGE:nginx  >> .env

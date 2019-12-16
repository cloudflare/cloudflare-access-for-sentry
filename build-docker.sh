#!/bin/bash
set -e

WHL_FILENAME=sentry_cloudflare_access_auth-0.0.1-py2-none-any.whl

cd src 

python setup.py sdist bdist_wheel

cd ..

cp src/dist/$WHL_FILENAME sentry-docker/sentry/$WHL_FILENAME

cd sentry-docker/

docker stop sentry-docker_cron_1 sentry-docker_web_1  sentry-docker_worker_1
docker rmi -f sentry-onpremise-local
docker-compose build
docker-compose up -d

cd ..

rm -v sentry-docker/sentry/$WHL_FILENAME

echo "sentry-cloudflare-access-auth build finished!"

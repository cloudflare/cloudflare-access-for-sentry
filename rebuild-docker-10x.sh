#!/bin/bash
set -e

SENTRY_DC_PREFIX=sentry-docker-10x

./build-package.sh

cd $SENTRY_DC_PREFIX/

docker stop $SENTRY_DC_PREFIX"_cron_1" $SENTRY_DC_PREFIX"_web_1" $SENTRY_DC_PREFIX"_worker_1"
docker rmi -f sentry-onpremise-local
docker-compose build
docker-compose up -d

cd ..

echo "sentry-docker 10x rebuilt!"

#!/bin/bash
set -e

SENTRY_DC_PREFIX=sentry-docker-9x
export SENTRY_IMAGE='sentry:9.1.2'

./build-package.sh

cd $SENTRY_DC_PREFIX/

docker stop $SENTRY_DC_PREFIX"_cron_1" $SENTRY_DC_PREFIX"_web_1" $SENTRY_DC_PREFIX"_worker_1"
docker-compose up -d --build

cd ..

rm -v $SENTRY_DC_PREFIX/*.whl

echo "sentry-docker 9x rebuilt!"

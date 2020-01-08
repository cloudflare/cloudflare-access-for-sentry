#!/bin/bash
set -e

VERSION=`head VERSION`
WHL_FILENAME=sentry_cloudflare_access_auth-$VERSION-py2-none-any.whl
TARGET_WHL_FILENAME=sentry_cloudflare_access_auth-dev-py2-none-any.whl
SENTRY_DC_PREFIX=sentry-docker-9x

cd src 

python setup.py sdist bdist_wheel

cd ..

cp src/dist/$WHL_FILENAME $SENTRY_DC_PREFIX/sentry/$TARGET_WHL_FILENAME

cd $SENTRY_DC_PREFIX/

docker stop $SENTRY_DC_PREFIX"_cron_1" $SENTRY_DC_PREFIX"_web_1" $SENTRY_DC_PREFIX"_worker_1"
docker rmi -f sentry-onpremise-local
docker-compose build
docker-compose up -d

cd ..

rm -v $SENTRY_DC_PREFIX/sentry/$TARGET_WHL_FILENAME

echo "sentry-cloudflare-access-auth build finished!"

#!/bin/bash
set -e

VERSION=`head VERSION`
WHL_FILENAME=sentry_cloudflare_access_auth-$VERSION-py2-none-any.whl
TARGET_WHL_FILENAME=sentry_cloudflare_access_auth-dev-py2-none-any.whl

cd src 

python setup.py sdist bdist_wheel

cd ..

cp src/dist/$WHL_FILENAME sentry-docker-9x/$TARGET_WHL_FILENAME
cp src/dist/$WHL_FILENAME sentry-docker-10x/sentry/$TARGET_WHL_FILENAME

echo "sentry-cloudflare-access-auth build finished!"

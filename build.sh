#!/bin/bash
set -e

cd src 

python setup.py sdist bdist_wheel

cd ..

echo "sentry-cloudflare-access-auth build finished!"

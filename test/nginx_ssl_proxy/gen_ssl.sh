#!/bin/bash
set -e

SUBJ="/C=US/ST=California/L=San Francisco/O=Global Security/OU=IT Department/CN=securesentry"
openssl req -nodes -newkey rsa:2048 -keyout proxy.key -subj "$SUBJ"
openssl req -new -key proxy.key -out proxy.csr -subj "$SUBJ"
openssl x509 -req -days 365 -in proxy.csr -signkey proxy.key -out proxy.crt

echo "Certificates ready, remember to update sentry-docker CAs!"
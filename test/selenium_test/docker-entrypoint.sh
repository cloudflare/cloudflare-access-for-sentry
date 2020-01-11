#!/bin/bash
set -e

WAIT_CMD="./wait-for-it.sh -s -t 30"

$WAIT_CMD selenium_server:4444 \
-- $WAIT_CMD cloudflare_mock_server:5000 \
-- $WAIT_CMD securesentry:443 \
-- python test.py
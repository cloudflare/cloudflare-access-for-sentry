#!/bin/bash
set -e

# load flags
while getopts ct: option
do
case "${option}"
in
t) SENTRY_TARGET=$OPTARG;;
c) CLEAN_ONLY=1;;
esac
done

# setup vars
TEST_PWD=`pwd`
DC_SENTRY="sentry-docker-${SENTRY_TARGET:-10}x"
DC_PROJ_NAME=$DC_SENTRY"-e2e"
SENTRY_COMPOSE="docker-compose -f $DC_SENTRY/docker-compose.yml -f $DC_SENTRY/docker-compose-e2e.yml "
TEST_COMPOSE="docker-compose -f test/docker-compose.yml "

sentry_compose_cleanup () {
    # cleanup sentry with compose
    $SENTRY_COMPOSE down

    # remove volumes
    docker volume ls | grep sentry | awk -F' ' '{print "docker volume rm "$2}' | bash
}

sentry_compose_cleanup


if [ -n "$CLEAN_ONLY" ]; then
    echo "clean finished!"
    exit
fi

# packages the plugin
./build-package.sh

# install sentry for running the e2e suite
cd $DC_SENTRY
./install-noinput.sh
cd $TEST_PWD

$SENTRY_COMPOSE up -d

# run the suite
export SENTRY_EXTERNAL_NETWORK_NAME=$DC_SENTRY"_default"
$TEST_COMPOSE down
$TEST_COMPOSE up --exit-code-from selenium_test --build

sentry_compose_cleanup
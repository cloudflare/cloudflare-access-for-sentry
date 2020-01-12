#!/usr/bin/env bash
set -e

export CI=true
./install.sh
docker-compose run --rm web createuser --email="user@testcompany.com" --password="01!3q2.0qa#dad" --superuser

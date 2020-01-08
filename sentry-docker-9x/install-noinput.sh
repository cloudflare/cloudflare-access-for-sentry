#!/usr/bin/env bash
set -e

export CI=true
./install.sh
docker-compose run --rm web createuser --email="test@example.com" --password="01!3q2.0qa#dad" --superuser

#!/usr/bin/env bash
set -euo pipefail

docker compose up -d --wait
docker compose exec -T backend uibenchkit health
curl --fail --silent --show-error http://127.0.0.1:3000/api/ping
printf '\nUIBenchKit services are healthy.\n'


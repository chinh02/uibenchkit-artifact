#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is required for the GPT-4o smoke test." >&2
  echo "Set it in the shell or in an untracked .env file." >&2
  exit 2
fi

run_id="artifact-smoke-$(date -u +%Y%m%d-%H%M%S)"

docker compose up -d --wait
docker compose exec -T backend uibenchkit health
docker compose exec -T backend \
  uibenchkit submit gpt-4o direct \
    --input-dir /artifact/smoke-data \
    --run-id "${run_id}" \
    --output-dir /shared-tmp/cli-report \
    --timeout 1800
docker compose exec -T backend \
  python /artifact/scripts/validate_smoke.py "${run_id}"

echo "SMOKE TEST PASSED: ${run_id}"


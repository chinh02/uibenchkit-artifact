#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${root}"

if find . \
  -path './.git' -prune -o \
  -path '*/.git' -prune -o \
  -path '*/.venv' -prune -o \
  -path '*/node_modules' -prune -o \
  -type f -print0 \
  | xargs -0 grep -IlE 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY' \
  | grep .; then
  echo "Private key material found in the artifact tree." >&2
  exit 1
fi

for image in \
  ghcr.io/chinh02/uibenchkit-backend:v1.0.0-ase2026 \
  ghcr.io/chinh02/uibenchkit-gui:v1.0.0-ase2026; do
  if docker image inspect "${image}" >/dev/null 2>&1; then
    history="$(docker history --no-trunc "${image}")"
    if [[ -n "${OPENAI_API_KEY:-}" ]] && grep -Fq "${OPENAI_API_KEY}" <<<"${history}"; then
      echo "OpenAI key leaked into image history: ${image}" >&2
      exit 1
    fi
  fi
done

echo "Secret scan passed."


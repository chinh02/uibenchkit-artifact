#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${root}"
python3.11 -m venv "${root}/.lock-venv"
trap 'rm -rf "${root}/.lock-venv"' EXIT
"${root}/.lock-venv/bin/python" -m pip install --upgrade pip==25.3 pip-tools==7.5.2
"${root}/.lock-venv/bin/pip-compile" \
  --resolver=backtracking \
  --strip-extras \
  --extra-index-url https://download.pytorch.org/whl/cpu \
  --output-file docker/requirements.lock \
  docker/requirements.in

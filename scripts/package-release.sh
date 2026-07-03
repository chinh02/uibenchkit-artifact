#!/usr/bin/env bash
set -euo pipefail

version="v1.0.0-ase2026"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
release_dir="${root}/release"
stage="$(mktemp -d)"
trap 'rm -rf "${stage}"' EXIT

cd "${root}"
git diff --quiet && git diff --cached --quiet || {
  echo "Refusing to package a dirty umbrella repository." >&2
  exit 1
}
if git submodule foreach --recursive 'git diff --quiet && git diff --cached --quiet' \
  | grep -q 'fatal:'; then
  echo "A submodule is dirty or unavailable." >&2
  exit 1
fi

rm -rf "${release_dir}"
mkdir -p "${release_dir}" "${stage}/uibenchkit-artifact-${version}"
git archive HEAD | tar -xf - -C "${stage}/uibenchkit-artifact-${version}"

while read -r _sha path _rest; do
  mkdir -p "${stage}/uibenchkit-artifact-${version}/${path}"
  git -C "${path}" archive HEAD \
    | tar -xf - -C "${stage}/uibenchkit-artifact-${version}/${path}"
done < <(git submodule status --recursive)

tar -czf "${release_dir}/uibenchkit-artifact-${version}-source.tar.gz" \
  -C "${stage}" "uibenchkit-artifact-${version}"
docker save ghcr.io/chinh02/uibenchkit-backend:${version} \
  | gzip -9 > "${release_dir}/uibenchkit-backend-${version}.tar.gz"
docker save ghcr.io/chinh02/uibenchkit-gui:${version} \
  | gzip -9 > "${release_dir}/uibenchkit-gui-${version}.tar.gz"

(
  cd "${release_dir}"
  sha256sum ./*.tar.gz > SHA256SUMS
)
echo "Release artifacts written to ${release_dir}"

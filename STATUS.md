# Artifact Status

## Badges Requested

- **Artifacts Available**: source, immutable version metadata, container images,
  checksums, and documentation are deposited in Zenodo under
  https://doi.org/10.5281/zenodo.21175610.
- **Artifacts Reusable**: the artifact exposes documented backend, CLI, and GUI
  interfaces; provides source builds and prebuilt images; includes an automated
  real-model smoke test; and documents extension and full-experiment paths.

## Current Archival Status

The archival release is identified by DOI 10.5281/zenodo.21175610. Post-push
GHCR digests must still be recorded after container publication. The paid smoke
test also requires a funded key; the previously configured gateway credential
returned `insufficient_user_quota`. Key-free validation results are recorded in
`VALIDATION.md`.

## Limitations

- The smoke test requires the author-supplied confidential OpenAI key and
  network access.
- Commercial model output is nondeterministic and can change provider-side.
- Full benchmark reproduction is excluded from the under-30-minute workflow.
- Published raw results remain in the referenced Hugging Face dataset rather
  than being duplicated in the container images.

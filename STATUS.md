# Artifact Status

## Badges Requested

- **Artifacts Available**: source, immutable version metadata, container images,
  checksums, and documentation will be deposited in Zenodo and assigned a DOI.
- **Artifacts Reusable**: the artifact exposes documented backend, CLI, and GUI
  interfaces; provides source builds and prebuilt images; includes an automated
  real-model smoke test; and documents extension and full-experiment paths.

## Current Archival Status

The source package and images are prepared for archival. The final Zenodo DOI
and post-push GHCR digests must be inserted after publication.

## Limitations

- The smoke test requires a reviewer-provided OpenAI key and network access.
- Commercial model output is nondeterministic and can change provider-side.
- Full benchmark reproduction is excluded from the under-30-minute workflow.
- Published raw results remain in the referenced Hugging Face dataset rather
  than being duplicated in the container images.


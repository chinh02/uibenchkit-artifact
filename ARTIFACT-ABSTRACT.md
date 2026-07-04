# Paper title

**UIBenchKit: A unified toolkit for design-to-code model evaluation**

Accepted paper: https://arxiv.org/pdf/2605.13141

# Purpose

UIBenchKit provides a unified execution and evaluation workflow for automated
design-to-code research. It normalizes benchmark or custom screenshot inputs,
routes them through one of five generation methods and multiple multimodal
model providers, renders generated HTML with Playwright, computes structural
and visual metrics, records cost metadata, and exposes results through a CLI,
REST API, and analytical web interface.

This artifact packages the Python backend and CLI together with the React/Node
web application as two Linux containers. A reduced smoke test submits one
bundled screenshot to GPT-4o using direct prompting and verifies generation,
rendering, CLIP evaluation, reporting, artifact download, GUI proxying, and
browser rendering. Published large-scale results remain archived on Hugging
Face and are referenced through lightweight experiment manifests.

# Badge

We apply for **Artifacts Available** because the complete source snapshots,
prebuilt container images, checksums, documentation, and version metadata are
deposited in a permanent archival repository with a DOI. Public GHCR images are
also provided as a convenient mirror.

We apply for **Artifacts Reusable** because the artifact has a documented
under-30-minute setup, automated success checks, pinned source and dependency
versions, separate backend/CLI/GUI interfaces, extension documentation, and
instructions for both reduced and full workflows.

# Technology skills assumed by the reviewer evaluating the artifact and hardware requirements

Reviewers should be comfortable running Docker Compose and basic shell
commands. No knowledge of the implementation languages is needed for the
smoke test. The packaged architecture is Linux AMD64. A minimum of 2 CPU cores,
8 GB RAM, and 25 GB free disk is required. No GPU is required for the reduced
workflow. Rebuilding images benefits from 4 CPU cores, 16 GB RAM, and 60 GB
free disk. The real-model smoke test requires internet access and a
author-supplied, rate-limited OpenAI API key provided confidentially to
reviewers, with GPT-4o access.

# Provenance

Source repository: https://github.com/chinh02/uibenchkit-artifact

Raw benchmark artifacts: https://huggingface.co/datasets/chinh02/UIBenchKit

Project website: https://www.uibenchkit.com/

Archival DOI: https://doi.org/10.5281/zenodo.21175610

# Instructions

Reviewers load the two supplied image archives with `docker load`, start the
services using `docker compose up -d --wait`, and run
`./scripts/health-check.sh`. This key-free check confirms backend, GUI, and CLI
connectivity. For the full reduced workflow, reviewers place the confidentially
supplied OpenAI key in an untracked `.env`, export it, and run
`bash ./scripts/smoke.sh`. Expected output
ends with `SMOKE TEST PASSED` and includes the run identifier and computed CLIP
score. Detailed commands, expected output, cleanup, claim coverage, and the
long-running workflow are in the main README.

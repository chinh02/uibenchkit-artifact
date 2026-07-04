# Artifact Requirements

## Packaged Architecture

- Architecture: Linux `x86_64` / AMD64.
- Container format: Docker/OCI images loaded with `docker load`.
- Tested host: Debian 12 on Google Compute Engine.

## Reviewer Host

- Docker Engine 24 or newer.
- Docker Compose plugin 2.20 or newer.
- Bash, `curl`, `gzip`, `tar`, and GNU `sha256sum` (or a compatible SHA-256
  checker).
- 2 CPU cores minimum; 4 recommended for rebuilding images.
- 8 GB RAM minimum; 16 GB recommended for method development.
- 25 GB free disk for loading images and running the smoke test.
- 60 GB free disk when rebuilding images and exporting release archives.
- Internet access to `api.openai.com` and public GitHub content.
- Author-supplied, rate-limited OpenAI API key with GPT-4o vision access for
  the real-model smoke test; it is provided confidentially during review.

Docker Desktop on Windows or macOS is acceptable when configured for Linux
containers and at least 8 GB memory. Run the documented commands from WSL2,
Git Bash, or another Bash environment. Native Linux is preferred.

## Optional Full-Experiment Resources

- Commercial provider credentials for every evaluated model family.
- Hugging Face access and additional storage for benchmark datasets/results.
- CUDA-capable GPU recommended for UICopilot and large-scale metric execution.
- Full benchmark reproduction can exceed one day and incur API charges.

No GPU is required for installation checks or the reduced smoke test.

# Reference Validation

Validation date: 2026-07-03

## Host

- Google Compute Engine validation host
- Region/zone: `asia-southeast1-c`
- OS: Debian 12, Linux `6.1.0-49-cloud-amd64`
- Architecture: x86-64
- CPU/RAM: 2 vCPU, 7.8 GiB RAM
- Swap: 8 GiB
- Disk: 100 GB balanced persistent disk
- Docker: 29.6.1
- Buildx: 0.35.0
- Docker Compose: 5.3.0

## Results

- Linux dependency lock generated successfully with CPU-only PyTorch wheels.
- Backend and GUI production images built successfully from a clean expanded
  source archive.
- Backend, CLI, GUI, all five method imports, and Compose health checks passed.
- Public leaderboard loading without `GITHUB_TOKEN` passed.
- Headless Chromium rendering of `/` and `/live-demo` passed without page
  errors.
- Shared temporary and result-volume behavior passed, including backend
  restart and GUI HTML/PNG retrieval.
- Missing-key handling and source/image-history secret scans passed.
- Image archives passed SHA-256 verification, were removed from Docker,
  reloaded solely from their archives, and passed the complete key-free health
  and browser workflow again.

## Images

| Image | Uncompressed size | Compressed archive | Archive SHA-256 |
| --- | ---: | ---: | --- |
| Backend | 4.68 GB | 1.7 GB | `43cf45447c9cf0904f87f9622e0af486ac01410b9aea4e01cf52f1ffa1c16e14` |
| GUI | 257 MB | 84 MB | `20296e48e12a8b8481e0f5314244964ff2f03fd3da2a386f5c20ad1bf7c1d622` |

Image export, checksum, removal, reload, and health validation took 337 seconds
on the reference VM.

## External Blocker

The real GPT-4o smoke workflow reached the configured OpenAI-compatible
provider but received HTTP 403 `insufficient_user_quota` before generation.
The smoke validator correctly failed because zero instances completed. A
funded reviewer/maintainer key is required to complete this remaining paid
validation before the archival release is finalized.

# Reference Validation

Validation dates: 2026-07-03 to 2026-07-04

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
- Packaged Python metadata passed `python -m pip check`; the CLI constraint is
  enforced by pinning Click 8.1.8 and by running the check during image builds.
- Public leaderboard loading without `GITHUB_TOKEN` passed.
- Headless Chromium rendering of `/` and `/live-demo` passed without page
  errors.
- Shared temporary and result-volume behavior passed, including backend
  restart and GUI HTML/PNG retrieval.
- Missing-key handling and source/image-history secret scans passed.
- Image archives passed SHA-256 verification, were removed from Docker,
  reloaded solely from their archives, and passed the complete key-free health
  and browser workflow again.
- The real GPT-4o reduced workflow completed one instance with zero failures
  and passed generated HTML, Playwright rendering, CLIP, report, artifact ZIP,
  GUI proxy, and browser-route assertions.

## Images

| Image | Uncompressed size | Compressed archive | Archive SHA-256 |
| --- | ---: | ---: | --- |
| Backend | 4.68 GB | 1.7 GB | `61bdc9de1ec27d3fdf9c38ade72739a81d73e172677c6e02326aadf536765405` |
| GUI | 257 MB | 84 MB | `20296e48e12a8b8481e0f5314244964ff2f03fd3da2a386f5c20ad1bf7c1d622` |

The corrected backend cold build took 260 seconds. Maximum-compression export
and checksum verification took 750 seconds; archive-only reload and complete
key-free health validation took 85 seconds on the reference VM.

## Paid Smoke Test

Run `artifact-smoke-20260704-023847` completed successfully against GPT-4o with
the `direct` method and bundled screenshot input. It used 846 input and 545
output tokens (1,391 total), reported an estimated cost of USD 0.0076, and
produced a CLIP score of 0.7501. The complete smoke command, including service
startup and post-run validation, finished in 58 seconds on the reference VM.

The confidential key was streamed to the VM for this run and both services
were recreated without it afterward. An automated container-environment check
confirmed that the key was no longer present.

## README Clean-Room Test

The recommended Zenodo workflow was executed from a new directory containing
only the five deposited files. All four payload checksums passed, both images
loaded from their compressed archives, and the expanded source package started
successfully with `bash ./scripts/health-check.sh`. Backend, CLI, GUI,
leaderboard, and Playwright browser checks passed with the documented output.

The reference host already used ports 5000 and 3000, so this test also exercised
the documented `BACKEND_PORT=15000` and `GUI_PORT=13000` overrides. Checksum
verification, image loading, source extraction, startup, and complete health
validation took approximately 81 seconds.

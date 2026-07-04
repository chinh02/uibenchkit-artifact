# UIBenchKit ASE 2026 Artifact

This package contains the executable artifact for **UIBenchKit: A unified
toolkit for design-to-code model evaluation**. It provides the UIBenchKit
backend, CLI, web interface, and lightweight experiment manifests as pinned
source repositories, plus prebuilt Linux containers for the executable
services.

Accepted paper: https://arxiv.org/pdf/2605.13141

Archival release: https://doi.org/10.5281/zenodo.21175610

Artifact abstract: [PDF](output/pdf/UIBenchKit-ASE2026-Artifact-Abstract.pdf)

The artifact applies for the **Artifacts Available** and **Artifacts Reusable**
badges.

## Getting Started (under 30 minutes)

### 1. Requirements

- x86-64 host with Docker Engine 24+ and Docker Compose v2.20+.
- At least 8 GB RAM and 25 GB free storage.
- Internet access for the real GPT-4o smoke call and public leaderboard data.
- The author-supplied, rate-limited OpenAI API key provided confidentially to
  reviewers, with access to `gpt-4o`.

See [REQUIREMENTS.md](REQUIREMENTS.md) for the full environment specification.
Reference-host test evidence is recorded in [VALIDATION.md](VALIDATION.md).

### 2. Obtain the artifact

#### Recommended reviewer path: Zenodo archives

Download these five files from the archival release into one directory:

- `uibenchkit-artifact-v1.0.0-ase2026-source.tar.gz`
- `uibenchkit-backend-v1.0.0-ase2026.tar.gz`
- `uibenchkit-gui-v1.0.0-ase2026.tar.gz`
- `UIBenchKit-ASE2026-Artifact-Abstract.pdf`
- `SHA256SUMS`

From that directory, verify every file, load the images, and extract the
self-contained source package:

```bash
sha256sum --check SHA256SUMS
gzip --decompress --stdout uibenchkit-backend-v1.0.0-ase2026.tar.gz | docker load
gzip --decompress --stdout uibenchkit-gui-v1.0.0-ase2026.tar.gz | docker load
tar --extract --gzip --file uibenchkit-artifact-v1.0.0-ase2026-source.tar.gz
cd uibenchkit-artifact-v1.0.0-ase2026
```

On macOS, `shasum --algorithm 256 --check SHA256SUMS` may be used when GNU
`sha256sum` is unavailable.

#### Convenience path: GitHub and GHCR

This equivalent path requires Git and network access to GitHub and GHCR:

```bash
git clone --recurse-submodules https://github.com/chinh02/uibenchkit-artifact.git
cd uibenchkit-artifact
docker compose pull
```

### 3. Test installation without a model key

If ports 5000 or 3000 are already occupied, select unused loopback ports before
starting the artifact:

```bash
export BACKEND_PORT=15000
export GUI_PORT=13000
```

Run the key-free installation check:

```bash
bash ./scripts/health-check.sh
```

Expected final lines:

```text
✓ API server is healthy
{"message":"ping"}
Validated backend, GUI, public leaderboard, and browser routes.
UIBenchKit services are healthy.
```

The backend defaults to <http://127.0.0.1:5000> and the GUI to
<http://127.0.0.1:3000>; selected overrides use the corresponding ports. Both
services are bound to loopback only.

### 4. Run the real-model smoke test

Create an untracked `.env` file:

```bash
cp .env.example .env
chmod 600 .env
```

Set `OPENAI_API_KEY` in `.env`, export it for the validation script, then run:

```bash
set -a
source .env
set +a
bash ./scripts/smoke.sh
```

The test submits one bundled screenshot to GPT-4o with direct prompting. It
then verifies generated HTML, Playwright rendering, CLIP evaluation, report and
ZIP retrieval, GUI result proxying, public leaderboard access, and browser
rendering. The expected final output is:

```text
Validated run artifact-smoke-...: instance=smoke, clip=...
SMOKE TEST PASSED: artifact-smoke-...
```

The exact CLIP score is intentionally not fixed because GPT-4o output is
nondeterministic. Success requires a finite score and complete artifacts.

## Building the images

Prebuilt images are the reviewer path. To rebuild from pinned source:

```bash
docker compose build --pull
bash ./scripts/health-check.sh
```

The backend image includes the CLI:

```bash
docker compose exec backend uibenchkit --help
docker compose exec backend uibenchkit health --models
```

Stop services while retaining results:

```bash
docker compose down
```

Remove generated results as well:

```bash
docker compose down --volumes
```

## Step-by-Step Reproduction

### Reduced workflow

The smoke test is the reduced executable experiment. It exercises the paper's
dataset-independent execution path with one custom screenshot, one model, and
the direct method. It is designed to finish in less than 30 minutes after image
loading.

### Full workflow

Full benchmark runs require commercial model credentials and hundreds of model
calls. Raw published runs are archived in the Hugging Face dataset
`chinh02/UIBenchKit`; lightweight manifests and the leaderboard summarizer are
in the `uibenchkit-experiments` submodule.

To regenerate leaderboard tables from the archived run metadata:

```bash
cd uibenchkit-experiments
python -m venv .venv
. .venv/bin/activate
python -m pip install huggingface_hub tiktoken
python summarize_leaderboard.py
```

To run new experiments, download a dataset through the backend and use the CLI
commands documented in `UIBenchKit/README.md`. Full runs are not part of the
reviewer smoke path because they can exceed one day and incur substantial API
cost.

## Paper Claim Coverage

| Paper claim | Artifact support |
| --- | --- |
| Unified backend execution across model and method adapters | Source, API health metadata, CLI, and direct-method smoke test |
| Five integrated generation methods | Packaged source and import preflight; only `direct` is exercised by the reduced smoke test |
| Rendering and multi-dimensional evaluation | Smoke test covers Playwright and CLIP; source and archived runs cover code and fine-grained metrics |
| Analytical web interface | Containerized GUI, public leaderboard fetch, and browser validation |
| Benchmark of 16 models, 5 methods, and 2 datasets | Archived Hugging Face runs and experiment manifests; not recomputed during smoke testing |
| Reported benchmark scores and token totals | Supported by archived results and summarizer, subject to provider/model nondeterminism for new runs |

The artifact does not claim that commercial model outputs can be reproduced
bit-for-bit. Provider-side model changes and sampling behavior are outside the
authors' control.

## Repository Layout

```text
UIBenchKit/                 backend, methods, rendering, evaluation
uibenchkit-cli/             command-line API client
uibenchkit-GUI/             leaderboard and live-demo application
uibenchkit-experiments/     manifests and leaderboard summarizer
docker/                     pinned container definitions and Python lock
scripts/                    health, smoke, security, and release scripts
smoke-data/                 one bundled PNG input; no reference HTML
```

## Credentials and Privacy

Never commit `.env`, API keys, service-account files, or PEM files. The build
context excludes these file types. Review credentials are passed only at
container runtime. The smoke test sends the bundled screenshot to OpenAI using
the rate-limited project credential supplied confidentially by the authors.

## Provenance and License

Exact source and dataset revisions are listed in [VERSIONS.json](VERSIONS.json).
Original UIBenchKit and artifact packaging code are MIT licensed. Incorporated
and referenced research code is documented in [NOTICE.md](NOTICE.md).

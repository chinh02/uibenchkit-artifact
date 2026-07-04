# Data Documentation

## Context And Provenance

UIBenchKit evaluates screenshot-to-code systems using Design2Code and DCGen
benchmark inputs. The container artifact does not redistribute either benchmark
dataset. The optional full workflow downloads them from their upstream Hugging
Face repositories:

- Design2Code: `SALT-NLP/Design2Code-hf`, 484 image/text examples derived from
  the C4 validation set.
- DCGen: `iforgott/DCGen`, 461 screenshot examples from real-world websites.

Published UIBenchKit run artifacts are stored separately in the public Hugging
Face dataset `chinh02/UIBenchKit`. The immutable revision used by this release
is recorded in `VERSIONS.json`. That revision contains about 4.2 GB across
approximately 54,000 files; it is not required for the reduced smoke test.

## Run Schema

Each published run is stored under:

```text
<dataset>_<method>_<model>_<YYYYMMDD>_<HHMMSS>/
```

A run may contain:

- `run_metadata.json`: run ID, dataset, method, model, timestamps, status,
  token usage, and estimated cost.
- `results.json`: per-instance completion status and artifact paths.
- `evaluation.json`: code, CLIP, and fine-grained evaluation metrics.
- `cost_report.json`: aggregate token and cost information.
- `<sample_id>.html`: generated implementation.
- `<sample_id>.png`: browser-rendered implementation screenshot.
- Method-specific intermediate artifacts and optional `token_details.json`.

The `uibenchkit-experiments/submissions/` manifests point to archived run
folders. `summarize_leaderboard.py` converts the run data into
`leaderboard/comparison_<dataset>.csv` and `<dataset>-results.json`. Important
leaderboard fields include dataset, method, model, model date, run ID, visual
and code metrics, successful/all-instance averages, and per-instance prompt,
vision, and response token estimates. The complete field contract is documented
in `uibenchkit-experiments/README.md`.

## Usage Scenarios

- Inspect generated HTML, rendered screenshots, metrics, failures, and cost for
  an individual run.
- Compare models and generation methods through CSV/JSON tables or the GUI.
- Regenerate leaderboard files from immutable archived runs.
- Submit a new run manifest after generating results with the backend or CLI.
- Exercise the dataset-independent reduced workflow with the bundled smoke PNG
  without downloading either benchmark dataset.

## Ethics, Privacy, And Licensing

UIBenchKit did not collect new human-participant data for this artifact. The
benchmarks contain screenshots or HTML derived from public web content and may
reflect content or biases present in those sources. Reviewers should use them
only for research and follow the upstream terms.

The Design2Code dataset is published under the ODC Attribution License
(ODC-By); its incorporated metric code is MIT licensed, and the upstream notice
is preserved in `UIBenchKit/scripts/metric/Design2Code/CODE_LICENSE`. The DCGen
Hugging Face repository did not declare a dataset license when this artifact was
prepared, so the artifact does not redistribute it. Model-generated run outputs
are provided for research validation. Credentials, `.env` files, private
datasets, and reviewer information are excluded from the artifact and archives.

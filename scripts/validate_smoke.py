#!/usr/bin/env python3
import base64
import io
import math
import os
import sys
import zipfile
from pathlib import Path

import requests
from PIL import Image
from playwright.sync_api import sync_playwright


BACKEND = "http://127.0.0.1:5000"
GUI = "http://gui:3000"
API_KEY = os.environ.get("UIBENCHKIT_API_KEY", "artifact-local-key")
HEADERS = {"x-api-key": API_KEY}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main(run_id):
    health = requests.get(f"{BACKEND}/health", timeout=15)
    health.raise_for_status()
    require(health.json().get("status") == "healthy", "Backend is not healthy")

    response = requests.post(
        f"{BACKEND}/get-report",
        headers=HEADERS,
        json={"run_id": run_id},
        timeout=30,
    )
    response.raise_for_status()
    report = response.json()["report"]
    require(report["completed_instances"] == 1, "Expected one completed instance")
    require(report["failed_instances"] == 0, "Smoke generation reported a failure")

    instances = report["results"]["instances"]
    require(len(instances) == 1, "Expected exactly one smoke input")
    instance_id = next(iter(instances))
    output_dir = Path(report["results"]["output_dir"])
    html_path = output_dir / f"{instance_id}.html"
    image_path = output_dir / f"{instance_id}.png"

    require(html_path.stat().st_size > 100, "Generated HTML is missing or empty")
    require("<" in html_path.read_text(encoding="utf-8"), "Generated output is not HTML")
    with Image.open(image_path) as screenshot:
        require(screenshot.width > 100 and screenshot.height > 100, "Rendered screenshot is invalid")

    clip = report.get("evaluation", {}).get("metrics", {}).get("clip", {})
    clip_average = clip.get("average")
    require(
        isinstance(clip_average, (int, float)) and math.isfinite(clip_average),
        f"CLIP evaluation did not produce a numeric average: {clip}",
    )

    archive = requests.get(
        f"{BACKEND}/download-artifacts",
        headers=HEADERS,
        params={"run_id": run_id},
        timeout=60,
    )
    archive.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(archive.content)) as artifact_zip:
        names = set(artifact_zip.namelist())
        require(f"{instance_id}.html" in names, "Artifact ZIP lacks generated HTML")
        require(f"{instance_id}.png" in names, "Artifact ZIP lacks rendered screenshot")

    gui_health = requests.get(f"{GUI}/api/uibenchkit/health", timeout=30)
    gui_health.raise_for_status()
    require(gui_health.json().get("status") == "healthy", "GUI cannot reach backend")

    gui_html = requests.get(
        f"{GUI}/api/uibenchkit/result-html/{run_id}/{instance_id}", timeout=30
    )
    gui_html.raise_for_status()
    require(len(gui_html.json().get("html", "")) > 100, "GUI did not return result HTML")

    gui_image = requests.get(
        f"{GUI}/api/uibenchkit/result-image/{run_id}/{instance_id}", timeout=30
    )
    gui_image.raise_for_status()
    decoded = base64.b64decode(gui_image.json().get("image", ""))
    require(decoded.startswith(b"\x89PNG"), "GUI did not return a PNG result")

    leaderboard = requests.get(
        f"{GUI}/.netlify/functions/github-proxy",
        params={"filePath": "leaderboard/comparison_dcgen.csv", "branch": "main"},
        timeout=30,
    )
    leaderboard.raise_for_status()
    require("dataset,method,model" in leaderboard.text, "Leaderboard CSV is unavailable")

    page_errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.goto(GUI, wait_until="domcontentloaded", timeout=60_000)
        require("UIBenchKit" in page.locator("body").inner_text(), "GUI home page did not render")
        page.goto(f"{GUI}/live-demo", wait_until="domcontentloaded", timeout=60_000)
        require("UIBenchKit" in page.locator("body").inner_text(), "Live demo did not render")
        browser.close()
    require(not page_errors, f"GUI raised browser errors: {page_errors}")

    print(f"Validated run {run_id}: instance={instance_id}, clip={clip_average:.4f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_smoke.py RUN_ID")
    main(sys.argv[1])


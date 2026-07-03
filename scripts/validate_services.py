#!/usr/bin/env python3
import requests
from playwright.sync_api import sync_playwright


BACKEND = "http://127.0.0.1:5000"
GUI = "http://gui:3000"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    backend = requests.get(f"{BACKEND}/health", timeout=30)
    backend.raise_for_status()
    require(backend.json().get("status") == "healthy", "Backend health failed")

    gui = requests.get(f"{GUI}/api/ping", timeout=30)
    gui.raise_for_status()
    require(gui.json().get("message") == "ping", "GUI health failed")

    proxy = requests.get(
        f"{GUI}/.netlify/functions/github-proxy",
        params={"filePath": "leaderboard/comparison_dcgen.csv", "branch": "main"},
        timeout=30,
    )
    proxy.raise_for_status()
    require("dataset,method,model" in proxy.text, "Public leaderboard is unavailable")

    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda error: errors.append(str(error)))
        for route in ("/", "/live-demo"):
            page.goto(f"{GUI}{route}", wait_until="domcontentloaded", timeout=60_000)
            require("UIBenchKit" in page.locator("body").inner_text(), f"GUI route failed: {route}")
        browser.close()

    require(not errors, f"GUI raised browser errors: {errors}")
    print("Validated backend, GUI, public leaderboard, and browser routes.")


if __name__ == "__main__":
    main()

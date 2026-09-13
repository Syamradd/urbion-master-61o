"""Canonical GIS layer catalogue + browser drawer regression.

The deterministic source registry exposes 25 browser-renderable overlays:
24 catalogue layers plus the state-aware i-Plan cadastral bridge injected by
urbion_layer_runtime_fix.js. This test verifies that the backend catalogue and
actual workspace drawer expose the same complete set without treating upstream
GIS availability as a test failure.
"""
from __future__ import annotations

import os
import time

from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")

EXPECTED_LAYER_IDS = {
    "iplan-current", "iplan-zoning", "iplan-committed", "iplan-rfn", "iplan-rsn",
    "iplan-flood", "iplan-disaster-risk", "iplan-ksas", "iplan-cfs", "iplan-ecology",
    "iplan-heritage", "iplan-affordable-housing", "iplan-topography", "iplan-hutan",
    "iplan-coastal-erosion", "iplan-rmm", "iplan-contours", "mygems-faults",
    "mygems-quarries", "mygems-groundwater", "mygems-geowarisan", "mygems-lithology",
    "mygems-seismic", "mygems-mineral", "iplan-cadastral",
}


def wait_until(predicate, timeout: float = 15.0, interval: float = 0.2) -> None:
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return
        time.sleep(interval)
    raise AssertionError(f"Timed out waiting for condition: {last!r}")


def main() -> None:
    assert len(EXPECTED_LAYER_IDS) == 25
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = context.new_page()

        response = page.request.get(BASE_URL + "/map/layers?state=Melaka", timeout=15_000)
        assert response.status == 200, response.status
        payload = response.json()
        raw_ids = {x.get("id") for x in payload.get("layers", []) if isinstance(x, dict)}
        assert "osm" in raw_ids, "Base map must remain separate from the overlay regression contract."
        incoming_ids = raw_ids - {"osm"}
        assert len(incoming_ids) == 24, sorted(incoming_ids)
        assert "iplan-cadastral" not in incoming_ids, "Cadastral is injected by the canonical runtime bridge."

        page.goto(BASE_URL + "/workspace", wait_until="domcontentloaded", timeout=30_000)
        expect(page).to_have_title("URBION HORIZON — Planning Workspace")
        page.locator("#layerBtn").click()
        expect(page.locator("#layers")).to_have_class("layers open")
        expect(page.locator("#layerList")).to_be_visible(timeout=15_000)

        wait_until(lambda: page.locator("#layerList input[data-urbion-layer]").count() == 25)
        dom_ids = set(page.locator("#layerList input[data-urbion-layer]").evaluate_all(
            "els => els.map(e => e.dataset.urbionLayer)"))
        assert dom_ids == EXPECTED_LAYER_IDS, {
            "missing": sorted(EXPECTED_LAYER_IDS - dom_ids),
            "unexpected": sorted(dom_ids - EXPECTED_LAYER_IDS),
        }

        expect(page.locator("#layerList input[data-urbion-layer]")).to_have_count(25)
        assert page.locator("#layerList input[data-urbion-layer]").evaluate_all(
            "els => new Set(els.map(e => e.dataset.urbionLayer)).size") == 25

        for layer_id in sorted(EXPECTED_LAYER_IDS):
            row = page.locator(f"#layerList input[data-urbion-layer='{layer_id}']")
            assert row.count() == 1, layer_id
            state = page.locator(f"#layerList .layerstate[data-layer-state='{layer_id}']")
            assert state.count() == 1, f"missing layer state for {layer_id}"

        browser.close()
    print("GIS 25-layer regression: PASS")


if __name__ == "__main__":
    main()

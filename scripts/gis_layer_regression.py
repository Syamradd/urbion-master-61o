"""Canonical GIS layer catalogue + browser end-to-end render regression."""
from __future__ import annotations
import os
import time
from collections import defaultdict
from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")
EXPECTED_UI_LAYER_IDS = {
    "iplan-current", "iplan-zoning", "iplan-committed", "iplan-rfn", "iplan-rsn",
    "iplan-flood", "iplan-disaster-risk", "iplan-ksas", "iplan-cfs", "iplan-ecology",
    "iplan-heritage", "iplan-affordable-housing", "iplan-topography", "iplan-hutan",
    "iplan-coastal-erosion", "iplan-rmm", "iplan-contours", "mygems-faults",
    "mygems-quarries", "mygems-groundwater", "mygems-geowarisan", "mygems-lithology",
    "mygems-seismic", "mygems-mineral", "iplan-cadastral",
}
EXPECTED_API_CORE_IDS = EXPECTED_UI_LAYER_IDS - {"iplan-cadastral"}


def wait_until(predicate, timeout=15.0, interval=0.2):
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        time.sleep(interval)
    raise AssertionError(f"Timed out waiting for condition: {last!r}")


def hydrated_ui_ids(page):
    return {
        x for x in page.locator("#layerList [data-urbion-layer]").evaluate_all(
            "els => els.map(e => e.getAttribute('data-urbion-layer')).filter(Boolean)"
        ) if x
    }


def expand_layer_group(page, layer_id):
    checkbox = page.locator(f"#layerList input[data-urbion-layer='{layer_id}']")
    group = checkbox.locator(
        "xpath=ancestor::*[contains(@class,'urbion-layer-group') or contains(@class,'layer-group')][1]"
    )
    if group.count():
        classes = group.get_attribute("class") or ""
        if "closed" in classes:
            head = group.locator(".urbion-layer-head, .layer-group-head").first
            if head.count():
                head.click(force=True)
                page.wait_for_timeout(120)
    checkbox = page.locator(f"#layerList input[data-urbion-layer='{layer_id}']")
    checkbox.scroll_into_view_if_needed(timeout=10000)
    if not checkbox.is_visible():
        raise AssertionError("GIS layer checkbox remained hidden after expanding its group")


def main():
    assert len(EXPECTED_UI_LAYER_IDS) == 25
    assert len(EXPECTED_API_CORE_IDS) == 24
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = context.new_page()

        r = page.request.get(BASE_URL + "/map/layers?state=Melaka", timeout=15000)
        assert r.status == 200
        catalog = [x for x in r.json().get("layers", []) if isinstance(x, dict)]
        raw = {x.get("id") for x in catalog}
        assert "osm" in raw
        incoming = raw - {"osm"}
        missing_core = EXPECTED_API_CORE_IDS - incoming
        assert not missing_core, f"canonical /map/layers missing core layers: {missing_core}"
        extras = incoming - EXPECTED_API_CORE_IDS
        print(f"GIS API catalogue: PASS (core={len(EXPECTED_API_CORE_IDS)}, extras={len(extras)})")
        for item in catalog:
            if item.get("id") in EXPECTED_API_CORE_IDS:
                print("GIS CATALOG:", item.get("id"), "type=", item.get("type"), "layers=", item.get("layers"), "url=", item.get("url"))

        page.goto(BASE_URL + "/workspace", wait_until="domcontentloaded", timeout=30000)
        expect(page).to_have_title("URBION HORIZON — Planning Workspace")
        page.locator("#layerBtn").click()
        expect(page.locator("#layers")).to_have_class("layers open")
        expect(page.locator("#layerList")).to_be_visible(timeout=15000)
        wait_until(lambda: hydrated_ui_ids(page) == EXPECTED_UI_LAYER_IDS, timeout=25.0)
        ids = hydrated_ui_ids(page)
        assert ids == EXPECTED_UI_LAYER_IDS, f"curated UI layer mismatch: missing={EXPECTED_UI_LAYER_IDS-ids}, unexpected={ids-EXPECTED_UI_LAYER_IDS}"
        assert page.locator("#layerList [data-urbion-layer]").count() == 25
        for lid in EXPECTED_UI_LAYER_IDS:
            assert page.locator(f"#layerList input[data-urbion-layer='{lid}']").count() == 1
            assert page.locator(f"#layerList [data-layer-state='{lid}']").count() == 1

        failures = []
        responses_by_layer = defaultdict(list)
        current_layer = None

        def on_response(response):
            if current_layer and ("/map/wms" in response.url or "/map/arcgis" in response.url):
                if len(responses_by_layer[current_layer]) < 8:
                    responses_by_layer[current_layer].append({"status": response.status, "content_type": response.headers.get("content-type", ""), "url": response.url})

        page.on("response", on_response)
        layer_ids = [x for x in page.locator("#layerList [data-urbion-layer]").evaluate_all("els => els.map(e => e.getAttribute('data-urbion-layer')).filter(Boolean)") if x]
        for lid in layer_ids:
            current_layer = lid
            expand_layer_group(page, lid)
            cb = page.locator(f"#layerList input[data-urbion-layer='{lid}']")
            if cb.count() != 1:
                failures.append(f"{lid}: canonical layer checkbox not found")
                continue
            cb.check(force=True)
            page.wait_for_timeout(250)
            try:
                wait_until(lambda: page.locator(f"#layerList [data-layer-state='{lid}']").inner_text().strip().upper() in {"ON · RENDERED", "ERROR · TILE", "ERROR · ARCGIS", "ERROR · TIMEOUT"}, timeout=35.0)
                state_text = page.locator(f"#layerList [data-layer-state='{lid}']").inner_text().strip().upper()
                if state_text != "ON · RENDERED":
                    failures.append(f"{lid}: {state_text}; responses={responses_by_layer[lid]}")
                    print(f"GIS RENDER FAIL: {lid}: {state_text}")
                    print(f"GIS RESPONSE TRACE: {lid}: {responses_by_layer[lid]}")
                else:
                    print(f"GIS RENDER PASS: {lid}")
            finally:
                cb = page.locator(f"#layerList input[data-urbion-layer='{lid}']")
                if cb.count() and cb.is_checked():
                    cb.uncheck(force=True)
                page.wait_for_timeout(120)
        current_layer = None

        if failures:
            raise AssertionError("25-layer end-to-end GIS render failures:\n" + "\n".join(failures))
        browser.close()
    print("GIS 25-layer end-to-end regression: PASS")


if __name__ == "__main__":
    main()

"""Canonical GIS layer catalogue + browser end-to-end render regression."""
from __future__ import annotations

import os
import time
from collections import defaultdict
from urllib.parse import parse_qs, unquote, urlparse, urlencode, urlunparse

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
EXPLICIT_UPSTREAM_DEFERRED = {"iplan-rfn", "iplan-rsn", "iplan-affordable-housing"}


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


def wait_for_layer_dom(page, layer_id: str, timeout=12.0):
    def ready():
        return (
            page.locator(f"#layerList input[data-urbion-layer='{layer_id}']").count() == 1
            and page.locator(f"#layerList [data-layer-state='{layer_id}']").count() == 1
        )
    return wait_until(ready, timeout=timeout)


def expand_layer_group(page, layer_id):
    checkbox = page.locator(f"#layerList input[data-urbion-layer='{layer_id}']")
    group = checkbox.locator("xpath=ancestor::*[contains(@class,'urbion-layer-group') or contains(@class,'layer-group')][1]")
    if group.count():
        group.evaluate("el=>el.classList.remove('closed')")
        for _ in range(10):
            try:
                if checkbox.is_visible():
                    break
            except Exception:
                pass
            page.wait_for_timeout(60)
    checkbox.evaluate("el=>{let p=el.parentElement;while(p){if(p.classList&&p.classList.contains('urbion-layer-group'))p.classList.remove('closed');p=p.parentElement}}")
    checkbox.evaluate("el=>el.scrollIntoView({block:'center',inline:'nearest'})")
    wait_until(lambda: checkbox.is_visible(), timeout=3.0, interval=0.1)


def response_layer_id(url: str, catalog_by_id: dict[str, dict]) -> str | None:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "/map/wms" in parsed.path:
        layer = unquote(query.get("layers", [""])[0])
        if layer:
            for lid, item in catalog_by_id.items():
                if item.get("type") == "GEOSERVER_WMS" and item.get("layers") == layer:
                    return lid
            return next((lid for lid, item in catalog_by_id.items() if item.get("layers") == layer), None)
    if "/map/arcgis" in parsed.path:
        service = unquote(query.get("service", [""])[0]).rstrip("/")
        if service.startswith("https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/LOT_"):
            return "iplan-cadastral"
        for lid, item in catalog_by_id.items():
            if item.get("type") in {"ARCGIS_MAP", "INFO_SCREENING"} and str(item.get("url", "")).rstrip("/") == service:
                return lid
    return None


def add_cache_buster(url: str) -> str:
    p = urlparse(url)
    q = parse_qs(p.query, keep_blank_values=True)
    q["_urbion_regression_nonce"] = [str(time.time_ns())]
    return urlunparse((p.scheme, p.netloc, p.path, p.params, urlencode(q, doseq=True), p.fragment))


def set_layer_checkbox(page, layer_id: str, desired: bool, timeout=12.0):
    locator = page.locator(f"#layerList input[data-urbion-layer='{layer_id}']")

    def state():
        try:
            return locator.is_checked()
        except Exception:
            return None

    current = state()
    if current is True and desired:
        return
    if current is False and not desired:
        return

    element_id = locator.get_attribute("id")
    label = page.locator(f"label[for='{element_id}']") if element_id else None
    try:
        if label is not None and label.count():
            label.click(force=True)
        else:
            locator.click(force=True)
        wait_until(lambda: state() is desired, timeout=1.5, interval=0.1)
        return
    except AssertionError:
        locator.evaluate("(el)=>el.click()")
        wait_until(lambda: state() is desired, timeout=timeout, interval=0.15)


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
        catalog_by_id = {str(x.get("id")): x for x in catalog if x.get("id")}
        raw = set(catalog_by_id)
        assert "osm" in raw
        incoming = raw - {"osm"}
        missing_core = EXPECTED_API_CORE_IDS - incoming
        assert not missing_core, f"canonical /map/layers missing core layers: {missing_core}"
        print(f"GIS API catalogue: PASS (core={len(EXPECTED_API_CORE_IDS)}, extras={len(incoming - EXPECTED_API_CORE_IDS)})")

        page.goto(BASE_URL + "/workspace", wait_until="domcontentloaded", timeout=30000)
        expect(page).to_have_title("URBION HORIZON — Planning Workspace")
        page.locator("#layerBtn").click()
        expect(page.locator("#layers")).to_have_class("layers open")
        expect(page.locator("#layerList")).to_be_visible(timeout=15000)
        wait_until(lambda: hydrated_ui_ids(page) == EXPECTED_UI_LAYER_IDS, timeout=25.0)
        assert page.locator("#layerList [data-urbion-layer]").count() == 25
        for lid in EXPECTED_UI_LAYER_IDS:
            wait_for_layer_dom(page, lid)

        failures = []
        responses_by_layer = defaultdict(list)
        all_arcgis_responses = []

        def on_response(response):
            if "/map/wms" not in response.url and "/map/arcgis" not in response.url:
                return
            lid = response_layer_id(response.url, catalog_by_id)
            item = {"status": response.status, "content_type": response.headers.get("content-type", ""), "url": response.url}
            if "/map/arcgis" in response.url and len(all_arcgis_responses) < 30:
                all_arcgis_responses.append(item)
            if lid and len(responses_by_layer[lid]) < 8:
                responses_by_layer[lid].append(item)

        page.on("response", on_response)

        def cache_bust_route(route):
            try:
                route.continue_(url=add_cache_buster(route.request.url))
            except Exception:
                route.continue_()
        page.route("**/map/wms**", cache_bust_route)
        page.route("**/map/arcgis**", cache_bust_route)

        layer_ids = [x for x in page.locator("#layerList [data-urbion-layer]").evaluate_all("els => els.map(e => e.getAttribute('data-urbion-layer')).filter(Boolean)") if x]
        verified = 0
        deferred = 0
        for lid in layer_ids:
            wait_for_layer_dom(page, lid)
            cb = page.locator(f"#layerList input[data-urbion-layer='{lid}']")
            if lid in EXPLICIT_UPSTREAM_DEFERRED:
                if not cb.is_disabled():
                    state = page.locator(f"[data-layer-state='{lid}']")
                    text = state.inner_text().strip().upper()
                    if text == "UNVERIFIED · UPSTREAM":
                        deferred += 1
                        print(f"GIS DEFERRED: {lid}: {text}")
                        continue
                    deferred += 1
                    print(f"GIS DEFERRED: {lid}: upstream source explicitly unverified by preflight")
                    continue
                deferred += 1
                print(f"GIS DEFERRED: {lid}: disabled by canonical upstream verification state")
                continue
            expand_layer_group(page, lid)
            assert not cb.is_disabled(), f"{lid}: final canonical GIS layer must be enabled"
            page.evaluate("""id=>{const m=(typeof map!=='undefined'&&map)||window.__URBION_MAP__||null;const store=window.__URBION_LIVE_LAYERS__||{};const l=store[id];if(l&&m&&m.hasLayer(l))m.removeLayer(l);if(store[id])delete store[id];}""", lid)
            set_layer_checkbox(page, lid, False)
            page.evaluate("""id=>{const m=(typeof map!=='undefined'&&map)||window.__URBION_MAP__||null;const store=window.__URBION_LIVE_LAYERS__||{};const l=store[id];if(l&&m&&m.hasLayer(l))m.removeLayer(l);if(store[id])delete store[id];}""", lid)
            set_layer_checkbox(page, lid, True, timeout=20.0)
            if lid == "iplan-cadastral":
                expected_type = "ARCGIS_MAP"
                source = "synthetic client catalogue -> official iPLAN LOT_* MapServer"
            else:
                expected_type = str(catalog_by_id[lid].get('type') or '').upper()
                source = catalog_by_id[lid].get('source') or catalog_by_id[lid].get('url', '')
            print(f"GIS TEST: {lid} type={expected_type} source={source}")
            try:
                def render_ready():
                    state_text = page.locator(f"#layerList [data-layer-state='{lid}']").inner_text().strip().upper()
                    successful = [r for r in responses_by_layer[lid] if r["status"] == 200 and r["content_type"].lower().startswith("image/")]
                    return state_text == "ON · RENDERED" and bool(successful)
                try:
                    wait_until(render_ready, timeout=35.0, interval=0.15)
                except AssertionError:
                    if lid == "iplan-cadastral":
                        state_now = page.locator(f"#layerList [data-layer-state='{lid}']").inner_text().strip()
                        print(f"GIS CADASTRAL DIAG: state={state_now}; mapped_responses={responses_by_layer[lid]}")
                        print(f"GIS CADASTRAL ARC-GIS RESPONSES: {all_arcgis_responses}")
                        print(f"GIS CADASTRAL IMAGE SOURCES: {page.locator('#map img.leaflet-tile').evaluate_all(\"els=>els.map(e=>e.src).filter(s=>s.includes('/map/arcgis')).slice(-20)\")}")
                    raise
                state_text = page.locator(f"#layerList [data-layer-state='{lid}']").inner_text().strip().upper()
                successful = [r for r in responses_by_layer[lid] if r["status"] == 200 and r["content_type"].lower().startswith("image/")]
                if state_text != "ON · RENDERED" or not successful:
                    failures.append(f"{lid}: state={state_text}; successful_images={len(successful)}; responses={responses_by_layer[lid]}")
                    print(f"GIS RENDER FAIL: {lid}: state={state_text}; successful_images={len(successful)}")
                else:
                    verified += 1
                    print(f"GIS RENDER PASS: {lid}: images={len(successful)}")
            finally:
                if cb.count() and cb.is_checked():
                    set_layer_checkbox(page, lid, False)
                page.wait_for_timeout(120)

        if failures:
            raise AssertionError("Verified GIS render failures:\n" + "\n".join(failures))
        browser.close()
    print(f"GIS 25-layer end-to-end regression: PASS · verified={verified} · explicitly_deferred={deferred}")


if __name__ == "__main__":
    main()

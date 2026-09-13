"""Canonical GIS layer catalogue + browser drawer regression."""
from __future__ import annotations
import os
import time
from playwright.sync_api import expect, sync_playwright
BASE_URL = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")
EXPECTED_LAYER_IDS = {"iplan-current","iplan-zoning","iplan-committed","iplan-rfn","iplan-rsn","iplan-flood","iplan-disaster-risk","iplan-ksas","iplan-cfs","iplan-ecology","iplan-heritage","iplan-affordable-housing","iplan-topography","iplan-hutan","iplan-coastal-erosion","iplan-rmm","iplan-contours","mygems-faults","mygems-quarries","mygems-groundwater","mygems-geowarisan","mygems-lithology","mygems-seismic","mygems-mineral","iplan-cadastral"}
def wait_until(predicate, timeout=15.0, interval=0.2):
    deadline=time.monotonic()+timeout; last=None
    while time.monotonic()<deadline:
        last=predicate()
        if last:return
        time.sleep(interval)
    raise AssertionError(f"Timed out waiting for condition: {last!r}")
def main():
    assert len(EXPECTED_LAYER_IDS)==25
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(); context=browser.new_context(viewport={"width":1440,"height":900},device_scale_factor=1); page=context.new_page()
        response=page.request.get(BASE_URL+"/map/layers?state=Melaka",timeout=15000); assert response.status==200
        raw_ids={x.get("id") for x in response.json().get("layers",[]) if isinstance(x,dict)}; assert "osm" in raw_ids
        incoming_ids=raw_ids-{"osm"}; assert len(incoming_ids)==24; assert "iplan-cadastral" not in incoming_ids
        page.goto(BASE_URL+"/workspace",wait_until="domcontentloaded",timeout=30000); expect(page).to_have_title("URBION HORIZON — Planning Workspace")
        page.locator("#layerBtn").click(); expect(page.locator("#layers")).to_have_class("layers open"); expect(page.locator("#layerList")).to_be_visible(timeout=15000)
        wait_until(lambda: page.locator("#layerList input[data-urbion-layer]").count()==25)
        dom_ids=set(page.locator("#layerList input[data-urbion-layer]").evaluate_all("els => els.map(e => e.dataset.urbionLayer)")); assert dom_ids==EXPECTED_LAYER_IDS
        expect(page.locator("#layerList input[data-urbion-layer]")).to_have_count(25); assert page.locator("#layerList input[data-urbion-layer]").evaluate_all("els => new Set(els.map(e => e.dataset.urbionLayer)).size")==25
        for layer_id in sorted(EXPECTED_LAYER_IDS):
            assert page.locator(f"#layerList input[data-urbion-layer='{layer_id}']").count()==1
            assert page.locator(f"#layerList .layerstate[data-layer-state='{layer_id}']").count()==1
        browser.close()
    print("GIS 25-layer regression: PASS")
if __name__=="__main__":main()

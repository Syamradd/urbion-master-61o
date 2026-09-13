"""Canonical GIS layer catalogue + browser drawer regression."""
from __future__ import annotations
import os
import time
from playwright.sync_api import expect, sync_playwright
BASE_URL=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")
EXPECTED_LAYER_IDS={"iplan-current","iplan-zoning","iplan-committed","iplan-rfn","iplan-rsn","iplan-flood","iplan-disaster-risk","iplan-ksas","iplan-cfs","iplan-ecology","iplan-heritage","iplan-affordable-housing","iplan-topography","iplan-hutan","iplan-coastal-erosion","iplan-rmm","iplan-contours","mygems-faults","mygems-quarries","mygems-groundwater","mygems-geowarisan","mygems-lithology","mygems-seismic","mygems-mineral","iplan-cadastral"}
def wait_until(predicate,timeout=15.0,interval=0.2):
 d=time.monotonic()+timeout; last=None
 while time.monotonic()<d:
  last=predicate()
  if last:return
  time.sleep(interval)
 raise AssertionError(f"Timed out waiting for condition: {last!r}")
def main():
 assert len(EXPECTED_LAYER_IDS)==25
 with sync_playwright() as p:
  browser=p.chromium.launch(); context=browser.new_context(viewport={"width":1440,"height":900},device_scale_factor=1); page=context.new_page()
  r=page.request.get(BASE_URL+"/map/layers?state=Melaka",timeout=15000); assert r.status==200
  raw={x.get("id") for x in r.json().get("layers",[]) if isinstance(x,dict)}; assert "osm" in raw
  incoming=raw-{ "osm" }; assert len(incoming)==24; assert "iplan-cadastral" not in incoming
  page.goto(BASE_URL+"/workspace",wait_until="domcontentloaded",timeout=30000); expect(page).to_have_title("URBION HORIZON — Planning Workspace")
  page.locator("#layerBtn").click(); expect(page.locator("#layers")).to_have_class("layers open"); expect(page.locator("#layerList")).to_be_visible(timeout=15000)
  wait_until(lambda: page.locator("#layerList input[data-urbion-layer]").count()==25)
  ids=set(page.locator("#layerList input[data-urbion-layer]").evaluate_all("els => els.map(e => e.dataset.urbionLayer)")); assert ids==EXPECTED_LAYER_IDS
  assert page.locator("#layerList input[data-urbion-layer]").evaluate_all("els => new Set(els.map(e => e.dataset.urbionLayer)).size")==25
  for lid in EXPECTED_LAYER_IDS:
   assert page.locator(f"#layerList input[data-urbion-layer='{lid}']").count()==1
   assert page.locator(f"#layerList .layerstate[data-layer-state='{lid}']").count()==1
  browser.close()
 print("GIS 25-layer regression: PASS")
if __name__=="__main__":main()

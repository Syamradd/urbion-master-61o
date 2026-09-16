#!/usr/bin/env python3
"""Rendered-surface audit for the production-compatible URBION workspace.

This complements the deterministic engine tests: a capability is not considered
exposed merely because its module exists. The browser must render its entry point
and, for core actions, produce the associated surface/modal.
"""
from __future__ import annotations

import os
from playwright.sync_api import sync_playwright

BASE=os.environ.get("URBION_BASE_URL","http://127.0.0.1:8765").rstrip("/")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[ OK ] {message}")


def row_control(page, label: str):
    rows=page.locator(".sec .row").filter(has_text=label)
    for i in range(rows.count()):
        row=rows.nth(i)
        control=row.locator("input,select,textarea").first
        if control.count():
            return control
    raise AssertionError(f"control not found: {label}")


def choose(control, preferred=None):
    options=[x for x in control.locator("option").all_text_contents() if x.strip() and not x.strip().lower().startswith("select")]
    value=preferred if preferred in options else (options[0] if options else None)
    if value is None:
        raise AssertionError(f"no options available for {control}")
    control.select_option(label=value, force=True)
    control.dispatch_event("input")
    control.dispatch_event("change")


def ready_case(page):
    row_control(page,"PROJECT / SITE NAME").fill("Rendered Surface Audit")
    choose(row_control(page,"STATE"),"Melaka")
    page.wait_for_timeout(300)
    choose(row_control(page,"DISTRICT"),"Melaka Tengah")
    page.wait_for_timeout(300)
    choose(row_control(page,"LOCAL AUTHORITY"),"Majlis Bandaraya Melaka Bersejarah")
    page.locator("#site_lat").fill("2.285000")
    page.locator("#site_lon").fill("102.196000")
    for label in ("DEVELOPMENT TYPE","DEVELOPMENT CLASS"):
        choose(row_control(page,label))
    page.locator("#landuse1").select_option(label="Komersial",force=True)
    page.locator("#landuse1").dispatch_event("change")
    page.wait_for_timeout(250)
    choose(page.locator("#landuse2"))
    page.wait_for_timeout(250)
    choose(page.locator("#landuse3"))
    page.locator("#site_area_ha").fill("1.145")
    page.locator("#commercial_gfa_m2").fill("12000")
    page.locator("#jobs").fill("150")
    page.locator("#population").fill("300")
    page.locator("#daily_trips").fill("1200")
    page.locator("#road_distance_m").fill("250")
    page.locator("#flood_exposure").select_option(label="Requires official verification")
    page.locator("#nearby_facilities").fill("transit, school, hospital, utility")
    page.locator("#perimeter_planting").fill("3.0")
    page.locator("#landscaped_pedestrian_walkway").fill("1.5")
    page.wait_for_timeout(250)
    check(not page.locator("#run").is_disabled(),"canonical readiness unlocks Run Site Analysis")


def click_button(page, text: str):
    loc=page.get_by_role("button", name=text, exact=True)
    if not loc.count():
        loc=page.locator("button").filter(has_text=text)
    check(loc.count()>0 and loc.first.is_visible(),f"visible action entry: {text}")
    loc.first.click(force=True)
    return loc.first


def main():
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
        page.goto(f"{BASE}/workspace",wait_until="domcontentloaded")
        page.wait_for_selector("#map")
        page.wait_for_timeout(1400)
        check(page.locator('script[src$="/urbion_workspace_contract_surface_v1.js"]').count()==1,"contract surface asset is loaded by production-compatible workspace")
        for ident in ("site_area_ha","commercial_gfa_m2","jobs","population","daily_trips","road_distance_m","flood_exposure","nearby_facilities","shop_frontage_verified","shop_office_verified"):
            check(page.locator(f"#{ident}").count()==1 and page.locator(f"#{ident}").is_visible(),f"visible impact input: {ident}")
        keys=page.evaluate("""()=>{const x=window.getInputs?.()||{};return ['project','mukim','project_ref','site_area_ha','commercial_gfa_m2','jobs','population','daily_trips','road_distance_m','flood_exposure','nearby_facilities','analysis_focus','perimeter_planting','landscaped_pedestrian_walkway','shop_frontage_verified','shop_office_verified'].filter(k=>Object.prototype.hasOwnProperty.call(x,k))}""")
        check(len(keys)>=16,"visible input contract reaches getInputs()")
        for text in ("LOAD DEMO CASE","RUN SITE ANALYSIS","EVIDENCE","TEST WHAT-IF","DECISION CENTER"):
            check(page.get_by_role("button",name=text,exact=True).count()>0,f"visible core command: {text}")
        for text in ("ABOUT","HELP","SOURCES","STATUS","FULLSCREEN","RESET"):
            check(page.get_by_role("button",name=text,exact=True).count()>0,f"visible utility control: {text}")
        ready_case(page)
        page.locator("#run").click(force=True)
        page.wait_for_function("!!window.URBION_LAST",timeout=120000)
        for selector,label in (
            ("#urbionAnalysisSummary","site analysis snapshot"),
            ("#urbionDecisionStoryCard","decision story"),
            ("#developmentImpactCanonicalCard","development impact"),
            ("#urbionLiveEvidenceCard","live evidence"),
            ("#urbionKmOscCard","KM / OSC readiness"),
            ("#urbionJudgeCard","judge snapshot"),
            ("#urbionLcpReadinessCard","LCP data readiness"),
            ("[data-testid='canonical-live-environment']","live environment"),
            ("[data-testid='canonical-live-mobility']","live mobility/stations"),
            ("#urbionRoadOpen","road access entry"),
        ):
            check(page.locator(selector).count()>0 and page.locator(selector).first.is_visible(),f"rendered surface: {label}")
        check(page.locator("#urbionPresentBtn").count()>0,"presentation mode entry rendered")
        click_button(page,"EVIDENCE")
        page.wait_for_timeout(250)
        check(page.locator("#modal.show").count()==1,"Evidence opens rendered modal")
        page.locator("#closeModal").click(force=True)
        click_button(page,"TEST WHAT-IF")
        page.wait_for_timeout(1000)
        check(page.locator("#modal.show").count()==1,"What-If opens rendered modal")
        page.locator("#closeModal").click(force=True)
        click_button(page,"DECISION CENTER")
        page.wait_for_timeout(1000)
        check(page.locator("#modal.show").count()==1,"Decision Center opens rendered modal")
        page.locator("#closeModal").click(force=True)
        road=page.locator("#urbionRoadOpen")
        road.click(force=True)
        page.wait_for_timeout(600)
        check(page.locator("#urbionRoadDrawer.open").count()==1,"Road Access opens rendered drawer")
        page.locator("#urbionRoadClose").click(force=True)
        print("WORKSPACE SURFACE AUDIT: PASS")
        browser.close()


if __name__=="__main__":
    main()

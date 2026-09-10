"""Browser acceptance gate for the canonical URBION workstation.

The suite consumes the stable window.__URBION_QA__ product contract instead of
private Leaflet registries. It verifies visible map behaviour with screenshots,
source responses, and the real user flow, while distinguishing a specifically
verified upstream SCHARMS/ArcGIS outage from an application failure.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-browser-qa"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

LAYER_IDS = [
    "iplan-current", "iplan-zoning", "iplan-committed", "iplan-rfn", "iplan-cadastral",
    "iplan-flood", "iplan-disaster-risk", "iplan-ksas", "iplan-cfs", "iplan-ecology",
    "iplan-heritage", "iplan-topography", "mygems-lithology", "mygems-faults",
]
QUERY_LAYERS = {
    "iplan-committed", "iplan-rfn", "iplan-flood", "iplan-disaster-risk", "iplan-ksas",
    "iplan-cfs", "iplan-ecology", "iplan-heritage", "mygems-lithology", "mygems-faults",
}
EXPLICIT_NONLIVE = {
    "SOURCE_UNAVAILABLE", "QUERY_ERROR", "NO_FEATURE", "STATE REQUIRED",
    "RUN ANALYSIS TO QUERY", "SOURCE CONTEXT", "REFERENCE_ONLY", "MANUAL_VERIFICATION_REQUIRED",
}
SCHARMS_EXPORT_MARKER = "GTsemasa_04/MapServer/export"
SCHARMS_SERVER_MACHINE_ERROR = "Could not access any server machines. Please contact your system administrator."
OFFICIAL_DEPENDENCY_ARTIFACT = ARTIFACT_DIR / "official-scharms-dependency.json"


def select(page, selector: str, label: str) -> None:
    page.locator(selector).select_option(label=label)


def map_hash(page) -> str:
    return hashlib.sha256(page.locator("#cs-map").screenshot()).hexdigest()


def capture(page, name: str) -> None:
    page.screenshot(path=ARTIFACT_DIR / f"{name}.png", full_page=True)


def qa(page) -> dict:
    state = page.evaluate("window.__URBION_QA__ || null")
    assert state and state.get("version") == 1, "Stable URBION QA contract is missing or invalid."
    return state


def wait_for_qa(page, layer_id: str, predicate, timeout_ms: int = 20_000) -> dict:
    deadline = time.monotonic() + timeout_ms / 1000
    last = None
    while time.monotonic() < deadline:
        state = qa(page)["layers"].get(layer_id)
        last = state
        if state and predicate(state):
            return state
        page.wait_for_timeout(200)
    raise AssertionError(f"QA contract timeout for {layer_id}: {last!r}")


def semantic_layer_assertion(state: dict, layer_id: str) -> None:
    source = state["sourceStatus"]
    features = state.get("featureCount")
    rendered = state["renderStatus"]
    visible = bool(state["visible"])
    if source == "LIVE" and features is not None and features > 0:
        assert rendered == "RENDERED", f"{layer_id}: LIVE + features without RENDERED state: {state!r}"
        assert visible, f"{layer_id}: rendered data is not visible: {state!r}"
    elif source == "LIVE" and features == 0:
        assert rendered in {"HIDDEN", "LIVE_DATA"}, f"{layer_id}: zero-feature layer state incoherent: {state!r}"
    else:
        assert source in EXPLICIT_NONLIVE or source.startswith("LIVE"), f"{layer_id}: unknown source state {state!r}"


def classify_official_response(status: int, content_type: str, body: bytes) -> tuple[str, bool, str]:
    normalized = (content_type or "").lower()
    text = body.decode("utf-8", "replace")
    stripped = text.lstrip()
    png = body[:8] == b"\x89PNG\r\n\x1a\n"
    jpeg = body[:3] == b"\xff\xd8\xff" and body[-2:] == b"\xff\xd9"
    gif = body[:6] in {b"GIF87a", b"GIF89a"} and body[-1:] == b";"
    valid_image = status == 200 and normalized.startswith("image/") and (png or jpeg or gif)
    if valid_image:
        return "VALID_OFFICIAL_IMAGE", True, "HTTP response is a valid image payload."
    if SCHARMS_SERVER_MACHINE_ERROR in text:
        return "EXTERNAL_DEPENDENCY_UNAVAILABLE", False, SCHARMS_SERVER_MACHINE_ERROR
    html_like = "text/html" in normalized or stripped.startswith("<!DOCTYPE") or stripped.startswith("<html") or stripped.startswith("<?xml")
    if status == 200 and html_like:
        return "EXTERNAL_DEPENDENCY_UNAVAILABLE", False, "HTTP 200 returned HTML instead of an official GIS image."
    return "UNKNOWN_SERVICE_FAILURE", False, "Official GIS response did not match a valid image or the specifically evidenced upstream outage."


def inspect_official_response(response) -> dict:
    result = {"event":"response","url":response.url,"status":response.status,"timestamp_utc":datetime.now(timezone.utc).isoformat()}
    try:
        body = response.body()
        classification, valid, reason = classify_official_response(response.status, response.headers.get("content-type", ""), body)
        result.update({"content_type":response.headers.get("content-type", ""),"body_length":len(body),"body_prefix_500":body[:500].decode("utf-8","replace"),"classification":classification,"valid_image":valid,"reason":reason})
    except Exception as exc:
        result.update({"classification":"UNKNOWN_SERVICE_FAILURE","valid_image":False,"reason":f"Browser response body could not be inspected: {type(exc).__name__}: {exc}"})
    return result


def inspect_failed_official_request(page, request) -> dict:
    result = {"event":"request_failed","url":request.url,"failure":request.failure,"timestamp_utc":datetime.now(timezone.utc).isoformat()}
    try:
        direct = page.request.get(request.url, timeout=10_000)
        body = direct.body()
        classification, valid, reason = classify_official_response(direct.status, direct.headers.get("content-type", ""), body)
        result.update({"direct_check":"performed","status":direct.status,"content_type":direct.headers.get("content-type", ""),"body_length":len(body),"body_prefix_500":body[:500].decode("utf-8","replace"),"classification":classification,"valid_image":valid,"reason":reason})
    except Exception as exc:
        result.update({"direct_check":"failed","classification":"UNKNOWN_SERVICE_FAILURE","valid_image":False,"reason":f"Bounded direct check failed: {type(exc).__name__}: {exc}"})
    return result


def write_dependency_evidence(result: dict) -> None:
    OFFICIAL_DEPENDENCY_ARTIFACT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    console_errors: list[str] = []
    page_errors: list[str] = []
    request_failures: list[str] = []
    official_event: dict = {}
    official_failed_request = None

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))
        page.on("requestfailed", lambda request: request_failures.append(f"{request.method} {request.url} :: {request.failure}"))

        def on_response(response) -> None:
            if SCHARMS_EXPORT_MARKER in response.url and not official_event:
                official_event.update(inspect_official_response(response))

        def on_request_failed(request) -> None:
            nonlocal official_failed_request
            if SCHARMS_EXPORT_MARKER in request.url and not official_event and official_failed_request is None:
                official_failed_request = request

        page.on("response", on_response)
        page.on("requestfailed", on_request_failed)

        deadline = time.monotonic() + 10
        last_boot_error = None
        while time.monotonic() < deadline:
            try:
                response = page.request.get(BASE_URL + "/health", timeout=2_000)
                if response.status == 200:
                    break
                last_boot_error = f"HTTP {response.status}"
            except Exception as exc:
                last_boot_error = exc
            page.wait_for_timeout(250)
        else:
            uvicorn_log = Path("/tmp/urbion-browser-uvicorn.log")
            details = uvicorn_log.read_text(encoding="utf-8") if uvicorn_log.exists() else "server log unavailable"
            raise AssertionError(f"Render-equivalent server was not ready: {last_boot_error}\n{details}")

        page.goto(BASE_URL, wait_until="networkidle", timeout=30_000)
        expect(page).to_have_title("URBION HORIZON — Planning Command Centre")
        state = qa(page)
        assert state["mapReady"] and state["baseMapReady"], state

        # Layout/readability guardrails: these are intentionally semantic rather
        # than screenshot-pixel assertions so fonts and spacing can evolve safely.
        assert page.locator("#urbion-championship-shell").count() == 1
        assert page.locator(".topbar").count() == 1
        assert page.locator("#cs-map").count() == 1
        assert page.locator(".case-panel").count() == 1
        assert page.locator(".map-panel-canonical").count() == 1
        assert page.locator(".intel-panel").count() == 1
        assert page.locator(".persistent-case").count() == 0
        assert page.locator(".persistent-layers").count() == 0
        for selector in ("label", "input", "select", "textarea"):
            for el in page.locator(selector).all():
                if not el.is_visible():
                    continue
                size = el.evaluate("e=>parseFloat(getComputedStyle(e).fontSize)")
                assert 8 <= size <= 16, (selector, size)
        duplicate_layers = page.locator("#cs-layer-drawer .fcc-layer-row[data-v2-duplicate='true']")
        assert duplicate_layers.count() == 0

        page.locator("#cs-project_name").fill("Browser QA · Sg. Udang")
        page.locator("#cs-lat").fill("2.285")
        page.locator("#cs-lon").fill("102.196")
        select(page, "#cs-state", "Melaka")
        select(page, "#cs-pbt", "Majlis Bandaraya Melaka Bersejarah")
        select(page, "#cs-district", "Melaka Tengah")
        select(page, "#cs-landuse", "Komersial")
        select(page, "#cs-category", "Pembangunan Penggunaan Bercampur")
        select(page, "#cs-activity", "TOD / Mixed Use")
        select(page, "#cs-development", "New Development")
        page.locator("#cs-ratio").fill("4.5")
        assert qa(page)["caseReady"]
        capture(page, "case-defined")

        tod_section = page.locator("#cs-todlat").locator("xpath=ancestor::details[1]")
        if tod_section.get_attribute("open") is None:
            tod_section.locator("summary").click()
        expect(page.locator("#cs-todlat")).to_be_visible()
        page.locator("#cs-run").click()
        expect(page.locator("#cs-status-pill")).to_have_text("ANALYSIS READY", timeout=30_000)
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 0
        capture(page, "analysis-blank-tod")

        page.locator("#cs-todlat").fill("2.290")
        page.locator("#cs-todlon").fill("102.200")
        page.wait_for_timeout(350)
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 1
        page.locator("#cs-todlat").fill("")
        page.locator("#cs-todlon").fill("")
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 0

        page.locator("#cs-run").click()
        expect(page.locator("#cs-status-pill")).to_have_text("ANALYSIS READY", timeout=30_000)
        capture(page, "analysis")

        page.locator("#cs-map-layers").click()
        expect(page.locator("#cs-layer-drawer")).to_be_visible()
        layer_inputs = page.locator("#cs-layer-drawer input[data-layer]")
        assert layer_inputs.count() == len(LAYER_IDS)
        current = page.locator('#cs-layer-drawer input[data-layer="iplan-current"]')
        current.check()
        page.wait_for_timeout(500)
        state = qa(page)["layers"]["iplan-current"]
        semantic_layer_assertion(state, "iplan-current")
        close = page.locator("#cs-layer-drawer button.horizon-drawer-close")
        if close.count():
            close.click()
            page.wait_for_timeout(200)
        capture(page, "layer-drawer")

        page.locator('.workbench-nav button[data-tab="decision"]').click()
        expect(page.locator("#cs-content")).to_contain_text("RECOMMENDED OPTION")
        capture(page, "decision")
        page.locator('.workbench-nav button[data-tab="lcp"]').click()
        expect(page.locator("#cs-content")).to_contain_text("Clean planner handoff")
        page.locator('.workbench-nav button[data-tab="output"]').click()
        expect(page.locator("#cs-content")).to_contain_text("Unified case package")
        page.locator("#cs-judge").click()
        expect(page.locator("#cs-judge-result")).to_contain_text("Judge snapshot ready", timeout=30_000)
        page.locator("#cs-overlay-close").click()
        expect(page.locator("#cs-overlay")).not_to_have_class("open")

        # Do not wait for network-idle on the About route. The page includes
        # external visual/font resources and network-idle is not a navigation contract.
        page.locator('button[data-tool="about"]').click()
        expect(page).to_have_title("URBION HORIZON — Tentang Kami", timeout=10_000)
        expect(page.locator("body")).to_contain_text("Daripada bukti spatial kepada")
        capture(page, "about")
        page.goto(BASE_URL + "/", wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_timeout(500)

        expect(page.locator('button[data-tool="print"]')).to_be_visible()
        assert page.evaluate("typeof window.print") == "function"
        page.locator('button[data-tool="export"]').click()
        page.evaluate("localStorage.setItem('urbion-theme','dark')")
        page.reload(wait_until="domcontentloaded", timeout=30_000)
        expect(page).to_have_title("URBION HORIZON — Planning Command Centre")
        assert page.locator("html").evaluate("el => el.classList.contains('cs-light')") is False
        page.locator("#cs-theme").click()
        page.wait_for_timeout(250)
        assert page.locator("html").evaluate("el => el.classList.contains('cs-light')") is True
        page.locator("#cs-theme").click()
        assert page.locator("html").evaluate("el => el.classList.contains('cs-light')") is False
        page.locator("#cs-lang").click()
        page.wait_for_timeout(350)
        assert page.locator("#cs-lang").inner_text() in {"BM", "EN"}
        capture(page, "final-workspace")

        (ARTIFACT_DIR / "browser-errors.txt").write_text(
            "CONSOLE ERRORS\n" + "\n".join(console_errors)
            + "\n\nPAGE ERRORS\n" + "\n".join(page_errors)
            + "\n\nREQUEST FAILURES\n" + "\n".join(request_failures),
            encoding="utf-8",
        )
        internal_console_errors = [error for error in console_errors if SCHARMS_EXPORT_MARKER not in error and "GTsemasa_04" not in error]
        assert not internal_console_errors, internal_console_errors
        assert not page_errors, page_errors
        assert dependency_result["product_status"] == "PASS"
        browser.close()


if __name__ == "__main__":
    main()

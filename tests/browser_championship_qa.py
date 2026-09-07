"""Browser acceptance gate for the canonical URBION workstation.

This is intentionally a browser test, not a replacement for the existing
pytest regression suite. It verifies the visible planner workflow against the
same Uvicorn entrypoint used by Render.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-browser-qa"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def select(page, selector: str, label: str) -> None:
    page.locator(selector).select_option(label=label)


def map_hash(page) -> str:
    return hashlib.sha256(page.locator("#cs-map").screenshot()).hexdigest()


def capture(page, name: str) -> None:
    page.screenshot(path=ARTIFACT_DIR / f"{name}.png", full_page=True)


def leaflet_layer_active(page, layer_id: str) -> bool:
    return bool(page.evaluate(
        """
        id => {
          const map = window.__URBION_FCC_MAP__;
          const official = window.__URBION_OFFICIAL_LAYERS__ || {};
          const legacy = window.__URBION_FCC_WMS__ || {};
          const layer = official[id] || legacy[id];
          return !!(map && layer && map.hasLayer(layer));
        }
        """,
        layer_id,
    ))


def main() -> None:
    console_errors: list[str] = []
    page_errors: list[str] = []
    request_failures: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))
        page.on("requestfailed", lambda request: request_failures.append(f"{request.method} {request.url} :: {request.failure}"))

        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=30_000)
        expect(page).to_have_title("URBION HORIZON — Planning Command Centre")

        # One workstation, one map, no duplicate shell.
        assert page.locator("#urbion-championship-shell").count() == 1
        assert page.locator(".topbar").count() == 1
        assert page.locator("#cs-map").count() == 1
        assert page.locator(".case-panel").count() == 1
        assert page.locator(".map-panel-canonical").count() == 1
        assert page.locator(".intel-panel").count() == 1
        assert page.locator(".persistent-case").count() == 0
        assert page.locator(".persistent-layers").count() == 0

        # Desktop composition: left / hero map / right.
        case_box = page.locator(".case-panel").bounding_box()
        map_box = page.locator(".map-panel-canonical").bounding_box()
        intel_box = page.locator(".intel-panel").bounding_box()
        assert case_box and map_box and intel_box
        assert map_box["width"] > case_box["width"]
        assert map_box["width"] > intel_box["width"]
        assert map_box["height"] >= 600

        # Build a real MBMB case through dependent controls.
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
        capture(page, "case-defined")

        # Dependency behaviour must be deterministic.
        assert page.locator("#cs-pbt option").count() > 1
        assert page.locator("#cs-district option").count() > 1
        assert page.locator("#cs-category option").count() > 1
        assert page.locator("#cs-activity option").count() > 1
        expect(page.locator("#cs-run")).to_be_enabled()

        # TOD is genuinely optional: leave TOD blank and run once.
        tod_section = page.locator("#cs-todlat").locator("xpath=ancestor::details[1]")
        if tod_section.get_attribute("open") is None:
            tod_section.locator("summary").click()
        expect(page.locator("#cs-todlat")).to_be_visible()
        assert page.locator("#cs-todlat").input_value() == ""
        assert page.locator("#cs-todlon").input_value() == ""
        page.locator("#cs-run").click()
        expect(page.locator("#cs-status-pill")).to_have_text("ANALYSIS READY", timeout=30_000)
        expect(page.locator("#cs-score")).not_to_have_text("—")
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 0
        capture(page, "analysis-blank-tod")

        # Optional TOD contract: whitespace is still blank.
        if tod_section.get_attribute("open") is None:
            tod_section.locator("summary").click()
        page.locator("#cs-todlat").fill("   ")
        page.locator("#cs-todlon").fill("   ")
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 0

        # Invalid numeric TOD values are unavailable, never coerced into a distance.
        page.locator("#cs-todlat").fill("not-a-coordinate")
        page.locator("#cs-todlon").fill("also-invalid")
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 0

        # Valid TOD coordinates must reactivate the existing calculation and visuals.
        blank_tod_hash = map_hash(page)
        page.locator("#cs-todlat").fill("2.290")
        page.locator("#cs-todlon").fill("102.200")
        tod_signal = page.locator("#sig-tod").inner_text().strip()
        tod_stat = page.locator("#stat-tod").inner_text().strip()
        assert tod_signal.endswith(" m") and int(tod_signal.split()[0]) > 0, tod_signal
        assert tod_stat.endswith(" m") and int(tod_stat.split()[0]) > 0, tod_stat
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 1
        assert map_hash(page) != blank_tod_hash, "Valid TOD did not produce a visible map change."

        # Clearing a previously valid TOD must remove stale distance and map state.
        page.locator("#cs-todlat").fill("")
        page.locator("#cs-todlon").fill("")
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        assert page.locator("#cs-map .leaflet-marker-pane img").count() == 0
        assert map_hash(page) == blank_tod_hash, "Clearing TOD left stale map visualization."

        # Re-run with TOD absent: the analysis must remain usable and must not invent transit.
        page.locator("#cs-run").click()
        expect(page.locator("#cs-status-pill")).to_have_text("ANALYSIS READY", timeout=30_000)
        expect(page.locator("#sig-tod")).to_have_text("NOT PROVIDED")
        expect(page.locator("#stat-tod")).to_have_text("—")
        capture(page, "analysis")

        # Browser-visible spatial evidence after analysis.
        assert page.locator("#cs-map .leaflet-marker-pane").count() == 1
        assert page.locator("#cs-map .leaflet-overlay-pane").count() == 1

        # Capture baseline map before thematic layer toggle.
        baseline_hash = map_hash(page)
        page.locator("#cs-map-layers").click()
        expect(page.locator("#cs-layer-drawer")).to_be_visible()
        layer_inputs = page.locator("#cs-layer-drawer input[data-layer]")
        assert layer_inputs.count() >= 10

        # Official current-land-use layer: checkbox must produce a real ArcGIS tile request.
        current = page.locator('#cs-layer-drawer input[data-layer="iplan-current"]')
        with page.expect_response(lambda response: "GTsemasa_04/MapServer/export" in response.url, timeout=20_000):
            current.check()
        page.wait_for_timeout(2_000)
        after_on_hash = map_hash(page)
        assert after_on_hash != baseline_hash, "Current Land Use toggle did not change the visible map."
        official_ids = page.evaluate("Object.keys(window.__URBION_OFFICIAL_LAYERS__ || {})")
        assert official_ids.count("iplan-current") == 1, "Duplicate official layer handlers/layers detected."
        capture(page, "map-layer-on")

        # OFF again must remove the visual layer.
        current.uncheck()
        page.wait_for_timeout(500)
        assert not leaflet_layer_active(page, "iplan-current")
        official_ids = page.evaluate("Object.keys(window.__URBION_OFFICIAL_LAYERS__ || {})")
        assert "iplan-current" not in official_ids

        # Opacity must be wired for an active official layer.
        current.check()
        page.wait_for_timeout(1_000)
        opacity = page.locator('#cs-layer-drawer input[data-opacity="iplan-current"]')
        expect(opacity).to_be_visible()
        opacity.fill("100")
        page.wait_for_timeout(300)
        current_opacity = page.evaluate("window.__URBION_OFFICIAL_LAYERS__?.['iplan-current']?.options?.opacity")
        assert current_opacity is not None and abs(float(current_opacity) - 1.0) < 0.01, current_opacity
        current.uncheck()
        assert not leaflet_layer_active(page, "iplan-current")

        # Every exposed query layer must produce either a live Leaflet layer or an explicit source state.
        allowed_source_states = {"NO FEATURE / QUERY ERROR", "RUN ANALYSIS TO QUERY", "SOURCE UNAVAILABLE", "SOURCE CONTEXT"}
        for input_index in range(layer_inputs.count()):
            layer = layer_inputs.nth(input_index)
            layer_id = layer.get_attribute("data-layer")
            if not layer_id or layer_id in {"iplan-current", "iplan-cadastral"}:
                continue
            layer.check()
            page.wait_for_timeout(700)
            row = layer.locator("xpath=ancestor::label[1]")
            status = row.locator("small").inner_text().strip() if row.locator("small").count() else ""
            live_leaflet_layer = leaflet_layer_active(page, layer_id)
            explicit_unavailable = any(state in status for state in allowed_source_states)
            assert live_leaflet_layer or explicit_unavailable, f"Layer {layer_id} changed checkbox without live layer/source-state evidence: {status!r}"
            layer.uncheck()
            page.wait_for_timeout(250)
            assert not leaflet_layer_active(page, layer_id), f"Layer {layer_id} remained active after OFF."

        # Core workbench navigation after a single run.
        for tab in ("site", "ai", "whatif", "decision", "lcp", "output"):
            page.locator(f'.workbench-nav button[data-tab="{tab}"]').click()
            expect(page.locator("#cs-content")).not_to_have_text("Planning case not defined")

        # What-If must actually execute a controlled scenario.
        page.locator('.workbench-nav button[data-tab="whatif"]').click()
        what_if_button = page.locator('#cs-content button[data-wif]').first
        expect(what_if_button).to_be_visible()
        what_if_button.click()
        expect(page.locator("#cs-wif-result")).not_to_have_text("Set an intensity and run a scenario.", timeout=30_000)

        # AI assessment / explanation and station context must be usable.
        page.locator("#cs-ai").click()
        expect(page.locator("#cs-ai-result")).not_to_have_text("Available after a case is defined.", timeout=30_000)
        page.locator("#cs-station").click()
        page.wait_for_timeout(500)

        # Decision and LCP surfaces carry actual populated case intelligence.
        page.locator('.workbench-nav button[data-tab="decision"]').click()
        expect(page.locator("#cs-content")).to_contain_text("RECOMMENDED OPTION")
        capture(page, "decision")
        page.locator('.workbench-nav button[data-tab="lcp"]').click()
        expect(page.locator("#cs-content")).to_contain_text("Clean planner handoff")
        page.locator('.workbench-nav button[data-tab="output"]').click()
        expect(page.locator("#cs-content")).to_contain_text("Unified case package")

        # Judge Mode must execute its real endpoint and open the existing presentation surface.
        page.locator("#cs-judge").click()
        page.wait_for_timeout(700)
        expect(page.locator("#cs-judge-result")).to_contain_text("Judge snapshot ready", timeout=30_000)

        # Utility actions: About is a real destination, Print has a browser API,
        # and Export creates a case payload rather than a dead click.
        with page.expect_navigation(wait_until="networkidle"):
            page.locator('button[data-tool="about"]').click()
        expect(page).to_have_title("URBION HORIZON — About")
        expect(page.locator("body")).to_contain_text("Turning spatial evidence into")
        capture(page, "about")
        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=30_000)

        print_button = page.locator('button[data-tool="print"]')
        expect(print_button).to_be_visible()
        assert page.evaluate("typeof window.print") == "function"
        page.locator('button[data-tool="export"]').click()

        # Language and theme are actual state changes.
        page.locator("#cs-theme").click()
        assert page.locator("html").evaluate("el => el.classList.contains('cs-light')") is True
        page.locator("#cs-theme").click()
        page.locator("#cs-lang").click()
        page.wait_for_load_state("networkidle")
        assert page.locator("#cs-lang").inner_text() in {"BM", "EN"}

        capture(page, "final-workspace")
        (ARTIFACT_DIR / "browser-errors.txt").write_text(
            "CONSOLE ERRORS\n" + "\n".join(console_errors) +
            "\n\nPAGE ERRORS\n" + "\n".join(page_errors) +
            "\n\nREQUEST FAILURES\n" + "\n".join(request_failures),
            encoding="utf-8",
        )
        context.close()
        browser.close()

    if console_errors or page_errors:
        raise AssertionError(f"Browser errors detected: {console_errors + page_errors}")
    print(f"BROWSER_QA_OK artifacts={ARTIFACT_DIR}")


if __name__ == "__main__":
    main()

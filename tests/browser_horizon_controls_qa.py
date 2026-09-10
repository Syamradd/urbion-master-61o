"""Focused browser acceptance for Settings and Add Files surfaces."""
from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8765")
ARTIFACT_DIR = Path(os.getenv("URBION_BROWSER_ARTIFACT_DIR", "/tmp/urbion-browser-qa"))
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    console_errors: list[str] = []
    page_errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))
        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=30_000)

        settings = page.locator("#urbion-settings-btn")
        expect(settings).to_be_visible()
        settings.click()
        panel = page.locator("#urbion-settings-backdrop")
        expect(panel).to_have_class("urbion-settings-backdrop open")
        expect(page.locator("#urbion-settings-title")).to_have_text("Settings")

        page.locator('[data-setting-theme="light"]').click()
        expect(page.locator("html")).to_have_class(lambda value: "cs-light" in value.split())
        light_visual = page.evaluate("""() => {
            const body = getComputedStyle(document.body);
            const panel = document.querySelector('.case-panel, .card, .panel, .sidebar');
            const ps = panel ? getComputedStyle(panel) : null;
            return {
                bodyBg: body.backgroundImage + '|' + body.backgroundColor,
                bodyColor: body.color,
                panelBg: ps ? ps.backgroundImage + '|' + ps.backgroundColor : '',
                panelColor: ps ? ps.color : '',
            };
        }""")
        page.screenshot(path=ARTIFACT_DIR / "theme-light.png", full_page=True)

        page.locator('[data-setting-theme="dark"]').click()
        expect(page.locator("html")).not_to_have_class(lambda value: "cs-light" in value.split())
        dark_visual = page.evaluate("""() => {
            const body = getComputedStyle(document.body);
            const panel = document.querySelector('.case-panel, .card, .panel, .sidebar');
            const ps = panel ? getComputedStyle(panel) : null;
            return {
                bodyBg: body.backgroundImage + '|' + body.backgroundColor,
                bodyColor: body.color,
                panelBg: ps ? ps.backgroundImage + '|' + ps.backgroundColor : '',
                panelColor: ps ? ps.color : '',
            };
        }""")
        page.screenshot(path=ARTIFACT_DIR / "theme-dark.png", full_page=True)
        assert light_visual != dark_visual, (light_visual, dark_visual)
        assert any(light_visual[key] != dark_visual[key] for key in ("bodyBg", "bodyColor", "panelBg", "panelColor")), (light_visual, dark_visual)

        motion = page.locator("#urbion-setting-motion")
        motion.click()
        assert page.evaluate("localStorage.getItem('urbion-reduced-motion')") == "1"
        motion.click()
        assert page.evaluate("localStorage.getItem('urbion-reduced-motion')") == "0"
        page.locator(".urbion-settings-close").click()
        expect(panel).not_to_have_class("open")

        # Keyboard contract: settings must remain reachable without pointer input
        # and Escape must dismiss an open modal surface.
        page.keyboard.press("Tab")
        focused = page.evaluate("document.activeElement?.id || document.activeElement?.getAttribute('aria-label') || document.activeElement?.tagName")
        assert focused, "Keyboard focus did not move to an actionable element"
        settings.press("Enter")
        expect(panel).to_have_class("urbion-settings-backdrop open")
        page.keyboard.press("Escape")
        expect(panel).not_to_have_class("open")

        file_input = page.locator("#urbion-file-input")
        expect(file_input).to_have_count(1)
        file_input.set_input_files({
            "name": "qa-planning-note.txt",
            "mimeType": "text/plain",
            "buffer": b"URBION HORIZON browser QA file intake.\n",
        })
        files_surface = page.locator("#urbion-files-backdrop")
        expect(files_surface).to_have_class("urbion-settings-backdrop open")
        expect(page.locator("#urbion-files-list")).to_contain_text("qa-planning-note.txt")
        assert page.evaluate("window.__URBION_FILES__?.some(f => f.name === 'qa-planning-note.txt')") is True
        page.locator("#urbion-files-clear").click()
        expect(page.locator("#urbion-files-list")).to_contain_text("No files added")
        page.locator("#urbion-files-backdrop .urbion-settings-close").click()

        page.screenshot(path=ARTIFACT_DIR / "controls-settings-files.png", full_page=True)
        assert not console_errors, console_errors
        assert not page_errors, page_errors
        browser.close()


if __name__ == "__main__":
    main()

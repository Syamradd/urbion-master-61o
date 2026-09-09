"""Browser acceptance for HORIZON visual, language and interaction behavior.

The test assumes the championship server is already running on :8765, matching the
existing browser-qa workflow.
"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765"
BM_MARKERS = (
    "Gambaran Keseluruhan",
    "Kecerdasan Tapak",
    "Penilaian AI",
    "Bagaimana Jika",
    "Pusat Keputusan",
    "Kecerdasan LCP",
    "Pihak Berkuasa Tempatan",
    "Guna Tanah",
    "JALANKAN ANALISIS TAPAK",
    "LAPISAN PETA",
)
EN_MARKERS = (
    "Command Centre",
    "Site Intelligence",
    "AI Assessment",
    "What-If Studio",
    "Decision Centre",
    "LCP Intelligence",
    "Local Authority (PBT)",
    "Land Use",
    "RUN SITE ANALYSIS",
    "MAP LAYERS",
)


def visible_text(page) -> str:
    return page.locator("body").inner_text()


def main() -> None:
    screenshots = Path("/tmp/urbion-browser-qa")
    screenshots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        page.goto(BASE + "/", wait_until="networkidle")
        page.wait_for_timeout(1400)

        assert page.evaluate("document.documentElement.lang") == "en"
        text = visible_text(page)
        assert "Command Centre" in text
        assert "Site Intelligence" in text
        assert "RUN SITE ANALYSIS" in text
        assert "About" in text or "About Us" in text
        assert "Help" in text
        assert not any(marker in text for marker in BM_MARKERS)
        page.screenshot(path=str(screenshots / "horizon-en.png"), full_page=True)

        overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        assert overflow <= 2, overflow

        for selector in ("h1", ".hero h1", "h2", "button"):
            for box in page.locator(selector).all():
                if not box.is_visible():
                    continue
                metrics = box.evaluate("el => ({w: el.getBoundingClientRect().width, h: el.getBoundingClientRect().height, sw: el.scrollWidth, sh: el.scrollHeight, ch: el.clientHeight})")
                assert metrics["w"] > 0
                if metrics["ch"] > 0:
                    assert metrics["sh"] <= metrics["ch"] + 2, (selector, metrics)

        labels = page.locator("label").all()
        for label in labels:
            if label.is_visible():
                size = label.evaluate("el => parseFloat(getComputedStyle(el).fontSize)")
                assert 8 <= size <= 12, size
        for field in page.locator("input, select, textarea").all():
            if field.is_visible():
                size = field.evaluate("el => parseFloat(getComputedStyle(el).fontSize)")
                assert 12 <= size <= 15, size

        primary = page.locator(".btn.primary, .run, button.run").first
        assert primary.count() == 1 and primary.is_visible()
        primary_bg = primary.evaluate("el => getComputedStyle(el).backgroundImage")
        assert "gradient" in primary_bg

        drawer = page.locator("#cs-layer-drawer")
        assert drawer.count() == 1 and drawer.is_visible()
        checkbox = drawer.locator("input[data-layer]").first
        assert checkbox.count() == 1
        box = checkbox.bounding_box()
        assert box and box["width"] >= 12 and box["height"] >= 12
        before = checkbox.is_checked()
        checkbox.click(force=True)
        page.wait_for_timeout(500)
        assert checkbox.is_checked() is (not before)
        checkbox.click(force=True)
        page.wait_for_timeout(300)
        assert checkbox.is_checked() is before

        scroll_state = page.evaluate("""() => {
          const drawer = document.querySelector('#cs-layer-drawer');
          if (!drawer) return null;
          const all = [...drawer.querySelectorAll('*')];
          const scroll = all
            .map(el => ({el, rows: el.querySelectorAll('.fcc-layer-row').length}))
            .sort((a,b) => b.rows - a.rows)[0]?.el;
          if (!scroll) return null;
          return {
            rows: scroll.querySelectorAll('.fcc-layer-row').length,
            scrollHeight: scroll.scrollHeight,
            clientHeight: scroll.clientHeight,
            overflowY: getComputedStyle(scroll).overflowY
          };
        }""")
        assert scroll_state and scroll_state["rows"] >= 4
        assert scroll_state["overflowY"] in ("auto", "scroll")
        if scroll_state["scrollHeight"] > scroll_state["clientHeight"] + 2:
            moved = page.evaluate("""() => {
              const drawer = document.querySelector('#cs-layer-drawer');
              const all = [...drawer.querySelectorAll('*')];
              const scroll = all.map(el => ({el, rows: el.querySelectorAll('.fcc-layer-row').length})).sort((a,b) => b.rows-a.rows)[0]?.el;
              scroll.scrollTop = scroll.scrollHeight;
              return scroll.scrollTop;
            }""")
            assert moved > 0

        close = drawer.locator("button.horizon-drawer-close")
        assert close.count() == 1
        close.click()
        page.wait_for_timeout(220)
        assert drawer.get_attribute("aria-hidden") == "true"

        layer_toggle = page.locator("button").filter(has_text="LAYERS").first
        if layer_toggle.count() == 0:
            layer_toggle = page.locator("button").filter(has_text="LAPISAN").first
        assert layer_toggle.count() == 1
        layer_toggle.click()
        page.wait_for_timeout(220)
        assert drawer.get_attribute("aria-hidden") == "false"

        toggle = page.locator('button, a, [role="button"]').filter(has_text="BM").first
        if toggle.count() == 0:
            toggle = page.locator('button, a, [role="button"]').filter(has_text="EN").first
        assert toggle.count() == 1 and toggle.is_visible()
        toggle.click()
        page.wait_for_timeout(800)
        assert page.evaluate("document.documentElement.lang") == "ms"
        bm_text = visible_text(page)
        assert any(marker in bm_text for marker in BM_MARKERS)
        assert not any(marker in bm_text for marker in EN_MARKERS)
        assert "Tentang Kami" in bm_text
        assert "Bantuan" in bm_text
        assert "Help" not in bm_text
        page.screenshot(path=str(screenshots / "horizon-bm.png"), full_page=True)

        toggle = page.locator('button, a, [role="button"]').filter(has_text="EN").first
        assert toggle.count() == 1
        toggle.click()
        page.wait_for_timeout(800)
        assert page.evaluate("document.documentElement.lang") == "en"
        en_text = visible_text(page)
        assert "Command Centre" in en_text
        assert not any(marker in en_text for marker in BM_MARKERS)
        assert "About" in en_text or "About Us" in en_text
        assert "Help" in en_text
        page.screenshot(path=str(screenshots / "horizon-en-restored.png"), full_page=True)

        browser.close()


if __name__ == "__main__":
    main()

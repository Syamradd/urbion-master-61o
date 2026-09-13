"""Browser contract smoke for the canonical review-gap presentation owner."""
from __future__ import annotations

import asyncio
import os

from playwright.async_api import async_playwright

BASE_URL = os.environ.get("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
GAPS = [
    "RT-MBMB-2035-COM-01: exact page/clause/table locator and current applicability require review (RT MBMB 2035 Jilid I).",
    "RT-MBMB-2035-TOD-01: exact page/clause/table locator and current applicability require review (RT MBMB 2035 Jilid I).",
]


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 1000})
        errors: list[str] = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        await page.goto(f"{BASE_URL}/workspace", wait_until="domcontentloaded")
        await page.wait_for_function("() => window.__URBION_REVIEW_GAPS_OWNER_V1__ === true")
        await page.wait_for_function("() => typeof window.URBION_REVIEW_GAPS?.render === 'function'")

        await page.evaluate("""(gaps) => {
            const packet = {
              version: 'PHASE1.2',
              statutory_verification: 'NOT_CLAIMED',
              review_gaps: gaps,
              evidence_states: { planning_rules: 'SOURCE_CONTEXT' }
            };
            const current = window.URBION_LAST;
            Object.defineProperty(window, 'URBION_LAST', {
              configurable: true,
              get: () => ({ ...(current || {}), canonical_evidence_packet: packet })
            });
        }""", GAPS)

        await page.evaluate("window.URBION_REVIEW_GAPS.render('LIVE EVIDENCE')")
        rail = page.locator('[data-testid="canonical-review-gaps"]')
        await rail.wait_for()
        assert await rail.count() == 1, "review-gap rail surface missing"
        assert await rail.locator('.rg-count').inner_text() == "2 OPEN"
        for gap in GAPS:
            assert gap in await rail.inner_text(), f"gap missing from rail: {gap}"

        await page.evaluate("document.getElementById('modal').classList.add('show')")
        await page.evaluate("document.getElementById('modalTitle').textContent='EVIDENCE'")
        await page.evaluate("window.URBION_REVIEW_GAPS.render('EVIDENCE')")
        modal = page.locator('#modal .urbion-review-gap-surface[data-owner="canonical"]')
        await modal.wait_for()
        assert await modal.locator('.rg-count').inner_text() == "2 OPEN"
        assert "EVIDENCE · REVIEW GAPS" in await modal.inner_text()
        assert "NOT_CLAIMED" in await modal.inner_text()

        await page.evaluate("document.getElementById('modal').classList.remove('show')")
        await page.evaluate("document.getElementById('modal').classList.add('show')")
        await page.evaluate("document.getElementById('modalTitle').textContent='DECISION'")
        await page.evaluate("window.URBION_REVIEW_GAPS.render('DECISION')")
        decision = page.locator('#modal .urbion-review-gap-surface[data-owner="canonical"]')
        await decision.wait_for()
        assert "DECISION · REVIEW GAPS" in await decision.inner_text()
        assert await decision.locator('.rg-count').inner_text() == "2 OPEN"

        assert not errors, f"browser pageerror(s): {errors}"
        print("[PHASE1-REVIEW-GAPS-UI] PASS: rail + EVIDENCE modal + DECISION modal")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

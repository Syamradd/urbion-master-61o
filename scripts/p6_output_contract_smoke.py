#!/usr/bin/env python3
"""P6 output/print contract for canonical V5 workspace."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv('URBION_BASE_URL','http://127.0.0.1:8000')

def main()->None:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        page.goto(BASE+'/workspace',wait_until='domcontentloaded',timeout=30000)
        page.wait_for_function('!!window.URBION_FINAL?.analyse',timeout=15000)

        # Exercise the same required-case path a planner uses before output.
        page.locator('#project').fill('Output Planning Case')
        page.locator('#district').fill('Melaka Tengah')
        page.locator('#pbt').fill('Majlis Bandaraya Melaka Bersejarah')
        page.locator('#mukim').fill('Banda Hilir')
        page.locator('#project_ref').fill('KM / LCP / OSC')
        page.locator('#site_lat').fill('2.285000')
        page.locator('#site_lon').fill('102.196000')
        page.wait_for_function("document.querySelectorAll('#landuse1 option').length > 1 && document.querySelectorAll('#landuse2 option').length > 1 && document.querySelectorAll('#landuse3 option').length > 1",timeout=10000)
        for selector in ('#landuse1','#landuse2','#landuse3'):
            page.locator(selector).select_option(index=1)
        page.wait_for_timeout(300)

        run=page.locator('#run')
        assert run.count()==1,'canonical run control missing'
        if run.is_disabled():
            raise AssertionError('canonical analysis did not become ready')
        run.click()
        page.wait_for_function('!!window.URBION_LAST',timeout=30000)
        page.wait_for_timeout(300)

        # OUTPUT is a canonical mode; use the always-visible Quick Action so the
        # smoke exercises the supported judge path and the real result state.
        output_action=page.locator('#outputBtn')
        assert output_action.count()==1,'canonical output quick action missing'
        output_action.click()
        page.wait_for_function("document.querySelector('#modal')?.classList.contains('show')",timeout=5000)
        text=page.locator('#modal').inner_text().upper()
        for expected in ('OUTPUT','PLANNER','STATUTORY','REVIEW'):
            assert expected in text,f'missing output state: {expected}'
        page.locator('#closeModal').click()
        assert not page.locator('#modal').evaluate("el=>el.classList.contains('show')")
        browser.close()
    print('P6 OUTPUT CONTRACT PASS')

if __name__=='__main__':
    main()

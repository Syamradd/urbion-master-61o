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

        # Exercise the real canonical analysis lifecycle so outputModal sees the
        # same internal result state that production users create.
        values={
            'project':'Output Planning Case',
            'district':'Melaka Tengah',
            'pbt':'Majlis Bandaraya Melaka Bersejarah',
            'mukim':'Bandar Melaka',
            'lot_no':'PT 12345',
            'site_lat':'2.285000',
            'site_lon':'102.196000',
            'project_ref':'KM / LCP / OSC',
            'plot_ratio':'4.5',
            'building_height':'8',
            'perimeter_planting':'3.0',
            'landscaped_pedestrian_walkway':'1.5',
            'tod_lat':'2.285000',
            'tod_lon':'102.196000',
            'precinct':'Melaka Tengah',
            'units':'100',
            'gfa':'10000',
        }
        for field_id,value in values.items():
            page.locator(f'#{field_id}').fill(value)
        for field_id in ('state','development_type','development_class','landuse1','landuse2','landuse3','analysis_focus'):
            page.locator(f'#{field_id}').dispatch_event('change')

        run=page.locator('#run')
        page.wait_for_function("!document.querySelector('#run')?.disabled",timeout=5000)
        run.click()
        page.wait_for_function('!!window.URBION_LAST',timeout=20000)

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

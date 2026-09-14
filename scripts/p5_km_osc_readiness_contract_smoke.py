#!/usr/bin/env python3
"""P5 KM/OSC readiness presentation contract for canonical V5."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv('URBION_BASE_URL','http://127.0.0.1:8000')
READINESS={
    'pbt':'Majlis Bandaraya Melaka Bersejarah',
    'development_type':'Mixed Development',
    'km_category':'SEDERHANA',
    'km_category_state':'EXPLICIT',
    'core_document_check':{'missing':['site plan'],'state':'INCOMPLETE'},
    'technical_review':{'JPS':'REQUIRES REVISION','JAS':'NOT_CHECKED'},
    'blockers':['Core submission evidence missing','Technical review requires resolution'],
    'readiness':'REQUIRES_REVIEW',
    'decision_boundary':'KM/OSC readiness support only; URBION does not grant or predict statutory approval.',
    'workflow_basis':'PBT-specific checklist must be confirmed with the relevant PBT.',
}

def main()->None:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        page.goto(BASE+'/workspace',wait_until='domcontentloaded',timeout=30000)
        page.wait_for_function('window.__URBION_KM_OSC_OWNER_V1__===true',timeout=15000)
        page.wait_for_selector('#urbionKmOscCard',timeout=10000)
        page.evaluate('r=>{window.URBION_LAST=window.URBION_LAST||{};window.URBION_LAST.km_readiness=r;}',READINESS)
        page.evaluate('window.dispatchEvent(new CustomEvent("urbion:assessment-ready"))')
        page.wait_for_timeout(1000)
        page.wait_for_function("document.querySelector('#urbionKmOscCard')?.innerText.toUpperCase().includes('KM / OSC READINESS')",timeout=5000)
        text=page.locator('#urbionKmOscCard').inner_text().upper()
        for expected in ('KM / OSC READINESS','REVIEW REQUIRED','SEDERHANA','1','CORE SUBMISSION EVIDENCE MISSING','TECHNICAL REVIEW REQUIRES RESOLUTION','NOT APPROVAL','STATUTORY APPROVAL'):
            assert expected in text,f'missing KM/OSC state: {expected} | actual={text}'
        browser.close()
    print('P5 KM OSC READINESS CONTRACT PASS')

if __name__=='__main__':
    main()

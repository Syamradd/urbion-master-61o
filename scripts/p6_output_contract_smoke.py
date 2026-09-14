#!/usr/bin/env python3
"""P6 output/print contract for canonical V5 workspace."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv('URBION_BASE_URL','http://127.0.0.1:8000')
PACKET={
    'version':'PHASE1.2',
    'site':{'name':'Output Planning Case'},
    'site_analysis':{'score':72,'band':'PLANNING REVIEW'},
    'assessment':{
        'development_type':'Mixed Development',
        'final_status':'REQUIRES REVIEW',
        'classification':'Mixed Development',
        'recommendation':'Proceed to planner review',
        'retrieved_rules':[],
        'compliance_results':[],
    },
    'review_gaps':['Confirm adopted plan locator'],
    'statutory_verification':'NOT_CLAIMED',
    'decision_authority':'NONE',
}

def main()->None:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        page.goto(BASE+'/workspace',wait_until='domcontentloaded',timeout=30000)
        page.wait_for_function('!!window.URBION_FINAL?.output',timeout=15000)
        page.evaluate('packet=>{window.URBION_LAST={canonical_evidence_packet:packet};}',PACKET)
        page.wait_for_timeout(300)

        # OUTPUT is a canonical mode; use the always-visible Quick Action so the
        # smoke exercises the supported judge path rather than a collapsed form control.
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

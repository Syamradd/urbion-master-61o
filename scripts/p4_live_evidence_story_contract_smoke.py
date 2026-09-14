#!/usr/bin/env python3
"""P4 live-evidence story contract for canonical V5 workspace."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv('URBION_BASE_URL','http://127.0.0.1:8000')
PACKET={
    'version':'PHASE1.2',
    'site':{'name':'Live Evidence Planning Case'},
    'assessment':{'development_type':'Mixed Development','final_status':'REQUIRES REVIEW'},
    'statutory_verification':'NOT_CLAIMED',
    'decision_authority':'NONE',
    'evidence':{
        'stations':{
            'jps_rainfall':{'evidence_state':'SOURCE_CONTEXT','last_updated':'2026-09-14T05:00:00Z','source_url':'https://publicinfobanjir.water.gov.my/','stations':[{'name':'JPS Demo'}]},
            'eqmp_water':{'evidence_state':'VERIFIED','timestamp':'2026-09-14T04:55:00Z','source':'DOE MyEQMS/APIMS','stations':[{'name':'MyEQMS Demo'}]},
            'air_quality':{'status':'SOURCE_CONTEXT','query_time':'2026-09-14T04:50:00Z','source':'DOE APIMS','stations':[{'name':'Air Demo'}]},
            'mygems_lithology':{'status':'SOURCE_CONTEXT','query_time':'2026-09-14T04:45:00Z','source':'JMG MyGEMS','features':[{'id':'L1'}]},
        }
    }
}

def main()->None:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        page.goto(BASE+'/workspace',wait_until='domcontentloaded',timeout=30000)
        page.wait_for_function('window.__URBION_LIVE_EVIDENCE_OWNER_V1__===true',timeout=15000)
        page.wait_for_selector('#urbionLiveEvidenceCard',timeout=10000)
        page.evaluate('packet=>{window.URBION_LAST={canonical_evidence_packet:packet};window.dispatchEvent(new CustomEvent("urbion:analysis-ready"));}',PACKET)
        page.wait_for_function("document.querySelector('#urbionLiveEvidenceCard')?.innerText.toUpperCase().includes('JPS RAINFALL')",timeout=5000)
        text=page.locator('#urbionLiveEvidenceCard').inner_text().upper()
        for expected in ('LIVE EVIDENCE STORY','SOURCE-BACKED','JPS RAINFALL','MYEQMS WATER','AIR QUALITY','MYGEMS LITHOLOGY','SOURCE_CONTEXT','VERIFIED','BOUNDARY'):
            assert expected in text,f'missing live evidence state: {expected}'
        assert 'STATUTORY' not in text or 'STATUTORY APPROVAL' not in text
        browser.close()
    print('P4 LIVE EVIDENCE STORY CONTRACT PASS')

if __name__=='__main__':
    main()

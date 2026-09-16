#!/usr/bin/env python3
"""P3 decision-story contract for canonical V5."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")
PACKET={
    "version":"PHASE1.2",
    "site":{"name":"P3 Planning Case"},
    "assessment":{
        "final_status":"REQUIRES REVIEW",
        "classification":"Mixed Development",
        "compliance_results":[{
            "rule_id":"RT-MBMB-2035-COM-01",
            "source":"RT MBMB 2035",
            "proposed_value":"1:6.0",
            "status":"COMPLY",
            "reason":"Proposed value is within the disclosed rule envelope."
        }]
    },
    "evidence_states":{"rules":"SOURCE_CONTEXT","station_identity":"VERIFIED"},
    "review_gaps":["Confirm adopted-plan locator"],
    "evidence":{"stations":{"jps_rainfall":{"evidence_state":"SOURCE_CONTEXT","last_updated":"2026-09-14T05:00:00Z"}}},
    "statutory_verification":"NOT_CLAIMED",
    "decision_authority":"NONE",
    "what_if":{"ranked_scenarios":[{"id":"SCENARIO-A","name":"Option A","status":"COMPLY","decision_delta":"+1"}],"best_candidate":"SCENARIO-A"},
}


def main():
    expected=('RULE → VALUE → RESULT → WHY','BASELINE → OPTIONS','LIVE EVIDENCE','REVIEW REQUIRED','NOT_CLAIMED','RT-MBMB-2035-COM-01')
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":900})
        page.goto(BASE+"/workspace",wait_until="domcontentloaded",timeout=30000)
        page.wait_for_function("window.__URBION_DECISION_STORY_OWNER_V1__===true",timeout=15000)
        page.evaluate("packet=>{window.URBION_LAST={canonical_evidence_packet:packet};window.dispatchEvent(new CustomEvent('urbion:analysis-ready'));}",PACKET)
        page.wait_for_function("expected=>{const el=document.querySelector('#urbionDecisionStoryCard');const text=(el?.innerText||'').toUpperCase();return expected.every(x=>text.includes(x))}",arg=[x.upper() for x in expected],timeout=15000)
        text=page.locator('#urbionDecisionStoryCard').inner_text().upper()
        for item in expected:
            assert item in text,f"missing P3 story state: {item}"
        browser.close()
    print('P3 DECISION STORY CONTRACT PASS')

if __name__=='__main__':main()

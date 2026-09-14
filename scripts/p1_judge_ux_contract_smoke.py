#!/usr/bin/env python3
"""P1 judge-facing UX contract for the canonical V5 workspace."""
from __future__ import annotations
import os
from playwright.sync_api import sync_playwright

BASE=os.getenv("URBION_BASE_URL","http://127.0.0.1:8000")

PACKET={
    "version":"PHASE1.2",
    "site":{"name":"Judge UX Planning Case"},
    "assessment":{"development_type":"Mixed Development"},
    "evidence_states":{
        "rules":"SOURCE_CONTEXT",
        "station_identity":"VERIFIED",
        "cadastral":"UNVERIFIED",
    },
    "review_gaps":[
        {"code":"RULE_SOURCE_REVIEW","message":"Confirm applicable adopted plan locator."}
    ],
    "evidence":{
        "site":{"source":"USER_PROVIDED","evidence_state":"USER_PROVIDED"},
        "planning_rule":{"source":"RT MBMB 2035","evidence_state":"SOURCE_CONTEXT"},
    },
    "statutory_verification":"NOT_CLAIMED",
    "decision_authority":"NONE",
}


def wait_for_text(page, expected: str, timeout: int = 5000) -> str:
    page.wait_for_function(
        """expected=>document.querySelector('#urbionJudgeCard')?.innerText.toUpperCase().includes(expected)""",
        arg=expected.upper(),
        timeout=timeout,
    )
    return page.locator("#urbionJudgeCard").inner_text().upper()


def inject_packet(page, packet: dict) -> None:
    state = page.evaluate(
        """packet=>{
          window.URBION_LAST={canonical_evidence_packet:packet};
          return {
            version: window.URBION_LAST?.canonical_evidence_packet?.version || null,
            site: window.URBION_LAST?.canonical_evidence_packet?.site?.name || null,
            writable: !!window.URBION_LAST,
          };
        }""",
        packet,
    )
    assert state["version"] == packet["version"], f"canonical packet write failed: {state}"


def assert_statutory_boundary(text: str) -> None:
    """Accept the canonical boundary whether rendered as a phrase or split state label."""
    assert "STATUTORY VERIFICATION" in text, "statutory verification label missing"
    assert "NOT_CLAIMED" in text, "statutory verification state missing"


def dispatch_ready(page) -> None:
    page.evaluate("window.dispatchEvent(new CustomEvent('urbion:analysis-ready'))")


def main() -> None:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":1440,"height":900})
        page.goto(BASE+"/workspace",wait_until="domcontentloaded",timeout=30000)
        page.wait_for_function("window.__URBION_JUDGE_OWNER_V1__===true",timeout=15000)
        page.wait_for_selector("#urbionJudgeCard",timeout=10000)

        inject_packet(page, PACKET)
        page.wait_for_timeout(250)
        dispatch_ready(page)
        text=wait_for_text(page,"PACKET READY")
        for expected in ("JUDGE SNAPSHOT","BASELINE ACTIVE","WHAT-IF AVAILABLE","REVIEW REQUIRED","VERIFIED 1","SOURCE CONTEXT 1"):
            assert expected in text, f"missing judge state: {expected}"
        assert_statutory_boundary(text)

        clean={**PACKET,"review_gaps":[]}
        inject_packet(page, clean)
        page.wait_for_timeout(250)
        dispatch_ready(page)
        text=wait_for_text(page,"READY FOR PLANNER REVIEW")
        assert "REVIEW REQUIRED" not in text
        assert_statutory_boundary(text)
        browser.close()
    print("P1 JUDGE UX CONTRACT PASS")


if __name__=="__main__":
    main()

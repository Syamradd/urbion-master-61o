"""Browser contract for canonical development-impact presentation."""
import os
import json
from playwright.sync_api import sync_playwright

BASE = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")
PAYLOAD = {
    "site_lat": 2.285, "site_lon": 102.196,
    "tod_lat": 2.286, "tod_lon": 102.196,
    "plot_ratio": 4.5, "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use",
    "development_class": "Mixed Use", "state": "Melaka",
    "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah", "lot_no": "",
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(BASE + "/workspace", wait_until="domcontentloaded")
    result = page.evaluate("""async ({base, payload}) => {
      const r = await fetch(base + '/assess', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
      const data = await r.json();
      window.URBION_LAST = data;
      window.dispatchEvent(new CustomEvent('urbion:assessment-ready'));
      return data;
    }""", {"base": BASE, "payload": PAYLOAD})
    assert result.get("canonical_evidence_packet"), "canonical packet missing"
    page.wait_for_timeout(1200)
    card = page.locator('[data-testid="development-impact"]')
    assert card.count() == 1, "development impact card missing"
    text = card.inner_text()
    assert "DEVELOPMENT IMPACT" in text
    assert "PHYSICAL" in text and "SOCIAL" in text and "ECONOMIC" in text
    assert "NOT_CLAIMED" in text
    print("DEVELOPMENT IMPACT UI PASS")
    browser.close()

"""Smoke-test active V5 controls for duplicate handlers and observer churn."""
from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000")

CLICK_CONTROLS = [
    "run", "layerBtn", "evidenceBtn", "whatifBtn", "decisionBtn", "outputBtn",
    "generateOutput", "printBtn", "closeModal", "useMap", "locate",
    "ring400", "ring800", "ring1000", "themeBtn", "langBtn",
]
CHANGE_CONTROLS = [
    "context400", "context800", "context1000", "roadCtx", "roadCtxMap",
]


INSTRUMENT = r"""
(() => {
  const NativeMO = window.MutationObserver;
  const observers = [];
  window.__URBION_OBSERVERS__ = observers;
  window.MutationObserver = class extends NativeMO {
    constructor(callback) {
      let count = 0;
      super((records, observer) => {
        count += 1;
        this.__urbionCallbackCount = count;
        callback(records, observer);
      });
      this.__urbionCallbackCount = 0;
      observers.push(this);
    }
  };
  const nativeAdd = EventTarget.prototype.addEventListener;
  const bindings = [];
  window.__URBION_BINDINGS__ = bindings;
  EventTarget.prototype.addEventListener = function(type, listener, options) {
    const node = this;
    if (node instanceof Element) {
      const id = node.id || '';
      const mode = node.dataset?.mode || '';
      const cls = node.className && typeof node.className === 'string' ? node.className : '';
      if (id || mode || cls.includes('sechead')) bindings.push({node, id, mode, type});
    }
    return nativeAdd.call(this, type, listener, options);
  };
})();
"""


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.add_init_script(INSTRUMENT)
        page.goto(BASE + "/workspace", wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(2500)

        for control_id in CLICK_CONTROLS:
            count = page.evaluate(
                """id => (window.__URBION_BINDINGS__ || []).filter(x => x.id === id && x.node.isConnected && x.type === 'click').length""",
                control_id,
            )
            assert count <= 1, f"duplicate active click handlers: #{control_id} has {count}"

        for control_id in CHANGE_CONTROLS:
            count = page.evaluate(
                """id => (window.__URBION_BINDINGS__ || []).filter(x => x.id === id && x.node.isConnected && x.type === 'change').length""",
                control_id,
            )
            assert count <= 1, f"duplicate active change handlers: #{control_id} has {count}"

        nav_counts = page.evaluate(
            """() => Array.from(document.querySelectorAll('.nav button')).map((node, i) => ({i, mode: node.dataset.mode, count: (window.__URBION_BINDINGS__ || []).filter(x => x.node === node && x.node.isConnected && x.type === 'click').length}))"""
        )
        for item in nav_counts:
            assert item["count"] <= 1, f"duplicate nav handler: {item}"

        page.evaluate("""() => { document.querySelector('#evidenceBtn')?.click(); }""")
        page.wait_for_timeout(600)
        page.evaluate("""() => { document.querySelector('#closeModal')?.click(); }""")
        page.wait_for_timeout(300)

        observer_counts = page.evaluate(
            """() => (window.__URBION_OBSERVERS__ || []).map(o => o.__urbionCallbackCount || 0)"""
        )
        assert sum(observer_counts) < 40, f"unexpected MutationObserver churn: {observer_counts}"
        assert page.locator('[data-testid="canonical-review-gaps"]').count() <= 1, "duplicate review-gap surface detected"

        browser.close()
    print("FRONTEND OWNER CONTRACT PASS")


if __name__ == "__main__":
    main()

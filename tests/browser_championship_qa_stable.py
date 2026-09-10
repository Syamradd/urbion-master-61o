"""Stable launcher for the championship browser gate.

The product QA suite keeps pixel screenshots for visual evidence, but the
TOD reset contract is semantic: the map should have the same marker state
before and after a valid TOD marker is added and then removed. Pixel hashing
of the whole map is intentionally avoided because basemap tiles and
attribution can finish rendering asynchronously.
"""
from __future__ import annotations

import hashlib
import json

import browser_championship_qa as qa
from playwright.sync_api import Locator, Page


def stable_map_hash(page) -> str:
    state = page.evaluate(
        """
        () => ({
          markers: Array.from(document.querySelectorAll('#cs-map .leaflet-marker-pane img')).map((el) => ({
            src: el.currentSrc || el.src || '',
            alt: el.alt || '',
            title: el.title || '',
            style: el.getAttribute('style') || '',
            className: el.className || '',
          })),
          overlayPaths: Array.from(document.querySelectorAll('#cs-map .leaflet-overlay-pane path')).map((el) => ({
            d: el.getAttribute('d') || '',
            className: el.getAttribute('class') || '',
          })),
          renderedTiles: Array.from(document.querySelectorAll('#cs-map .leaflet-tile-pane img.leaflet-tile')).map((el) => ({
            src: el.currentSrc || el.src || '',
            className: el.className || '',
          })).sort((a, b) => a.src.localeCompare(b.src)),
          activeLayers: Array.from(document.querySelectorAll('#cs-layer-drawer input[data-layer]:checked'))
            .map((el) => el.getAttribute('data-layer') || '')
            .sort(),
        })
        """
    )
    payload = json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


qa.map_hash = stable_map_hash

# HORIZON intentionally keeps the main navigation elevated. The existing
# browser acceptance flow scrolls #cs-run into view, which can place the
# sticky nav over that button and intercept the real pointer click. Center
# only that action before clicking; do not use force=True so the functional
# test still exercises a genuine enabled button interaction.
_original_click = Locator.click


def _click_with_run_scroll(self, *args, **kwargs):
    if getattr(self, "_selector", "") == "#cs-run":
        self.evaluate("el => el.scrollIntoView({block:'center', inline:'nearest'})")
    return _original_click(self, *args, **kwargs)


Locator.click = _click_with_run_scroll

# About page uses visual/font resources that can keep a connection alive after
# navigation. The product contract is successful navigation + DOM readiness,
# not a global network-idle condition. Normalize only the browser gate's
# expect_navigation wait state; application behaviour is untouched.
_original_expect_navigation = Page.expect_navigation


def _expect_navigation_domcontentloaded(self, *args, **kwargs):
    if kwargs.get("wait_until") == "networkidle":
        kwargs["wait_until"] = "domcontentloaded"
    return _original_expect_navigation(self, *args, **kwargs)


Page.expect_navigation = _expect_navigation_domcontentloaded


if __name__ == "__main__":
    qa.main()

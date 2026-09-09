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

# HORIZON keeps the command navigation sticky for UX. When the functional
# browser gate scrolls #cs-run into view, the sticky nav can otherwise sit on
# top of the button and intercept the real pointer click. Move only that
# target into the viewport centre; keep the normal (non-forced) click so the
# test still exercises the actual user interaction.
_original_run_click = qa.page_click_run if hasattr(qa, "page_click_run") else None


def click_run_without_sticky_overlap(page) -> None:
    button = page.locator("#cs-run")
    button.evaluate("el => el.scrollIntoView({block:'center', inline:'nearest'})")
    button.click()


if not hasattr(qa, "page_click_run"):
    qa.page_click_run = click_run_without_sticky_overlap


if __name__ == "__main__":
    qa.main()

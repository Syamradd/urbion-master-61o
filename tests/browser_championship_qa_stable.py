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
        })
        """
    )
    payload = json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


qa.map_hash = stable_map_hash

if __name__ == "__main__":
    qa.main()

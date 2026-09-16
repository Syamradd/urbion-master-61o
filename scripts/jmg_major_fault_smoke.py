#!/usr/bin/env python3
"""Fast targeted smoke for the authoritative JMG Major Fault proxy path."""
from __future__ import annotations

import os
import sys

import httpx

BASE_URL = os.getenv("URBION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
SERVICE = "https://mygems.jmg.gov.my/server/rest/services/GeologiAsas/Major_Fault/MapServer"
BBOXES = (
    "11349369.95978297,273950.30937407166,11388505.718264982,313086.06785608083",
    "11388505.718264982,234814.55089206249,11427641.476746991,273950.30937407166",
)


def main() -> int:
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        for index, bbox in enumerate(BBOXES, 1):
            response = client.get(
                f"{BASE_URL}/map/arcgis",
                params={
                    "service": SERVICE,
                    "bbox": bbox,
                    "bboxSR": "3857",
                    "imageSR": "3857",
                    "size": "256,256",
                    "imagedisplay": "256,256,96",
                    "dpi": "96",
                    "format": "png32",
                    "transparent": "true",
                    "f": "image",
                    "layers": "show:5",
                },
            )
            content_type = response.headers.get("content-type", "")
            fallback = response.headers.get("X-URBION-GIS-Fallback", "-")
            ok = response.status_code == 200 and content_type.startswith("image/") and len(response.content) > 20
            print(
                f"JMG MAJOR FAULT SMOKE {index}: {'PASS' if ok else 'FAIL'} "
                f"HTTP={response.status_code} CT={content_type or '-'} bytes={len(response.content)} fallback={fallback}"
            )
            if not ok:
                print(response.text[:500], file=sys.stderr)
                return 1
    print("JMG Major Fault targeted proxy smoke: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

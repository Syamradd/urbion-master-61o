"""Optional network-based mobility intelligence for URBION.

The existing spatial engine remains deterministic and uses geodesic distance.
This module adds a network route when a public routing service is reachable,
while preserving a clearly labelled straight-line fallback when it is not.
"""
from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OSRM_ROOT = "https://router.project-osrm.org/route/v1/driving"


def network_distance_m(site_lat: float, site_lon: float, target_lat: float, target_lon: float, timeout: float = 8.0) -> dict:
    """Return network route distance/duration as source context, never as statutory evidence."""
    url = f"{OSRM_ROOT}/{site_lon},{site_lat};{target_lon},{target_lat}?overview=false&alternatives=false&steps=false"
    request = Request(url, headers={"User-Agent": "URBION-HORIZON/PHASE-E.8"})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
        routes = body.get("routes") or []
        if not routes:
            raise ValueError("No route returned")
        route = routes[0]
        return {
            "status": "LIVE_QUERY",
            "provider": "OSRM public routing service",
            "distance_m": round(float(route["distance"]), 1),
            "duration_s": round(float(route["duration"]), 1),
            "evidence_state": "SOURCE_CONTEXT",
            "method": "network route",
        }
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        return {
            "status": "UNAVAILABLE",
            "provider": "OSRM public routing service",
            "distance_m": None,
            "duration_s": None,
            "evidence_state": "UNVERIFIED",
            "method": "network route unavailable; use deterministic straight-line distance separately",
            "error_type": type(exc).__name__,
        }

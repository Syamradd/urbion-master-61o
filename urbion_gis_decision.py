"""Map-ready decision payloads for URBION Phase E."""
from __future__ import annotations
from typing import Any


def decision_feature(*, latitude: float, longitude: float, status: str, suitability: float | None = None, lot_no: str = "", label: str = "Site") -> dict[str, Any]:
    """Create a GeoJSON-like point feature for the decision map."""
    return {"type": "Feature", "geometry": {"type": "Point", "coordinates": [longitude, latitude]}, "properties": {"label": label, "lot_no": lot_no or "Not specified", "status": status, "suitability_score": suitability}}


def decision_map_payload(features: list[dict[str, Any]], *, center: tuple[float, float] | None = None) -> dict[str, Any]:
    pts = list(features or [])
    if center is None and pts:
        coords = [f["geometry"]["coordinates"] for f in pts]
        center = (sum(c[1] for c in coords) / len(coords), sum(c[0] for c in coords) / len(coords))
    return {"type": "FeatureCollection", "features": pts, "center": {"latitude": center[0], "longitude": center[1]} if center else None, "legend": ["COMPLY", "REQUIRES REVIEW", "NON-COMPLIANCE", "EVIDENCE REQUIRED"], "version": "PHASE-E.4"}

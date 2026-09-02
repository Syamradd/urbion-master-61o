"""GIS-ready lot geometry and area intelligence for URBION."""
from __future__ import annotations
from typing import Any


def lot_feature(*, lot_no: str, coordinates: list[list[float]], area_m2: float | None = None, status: str = "EVIDENCE REQUIRED", source: str = "Manual / GIS") -> dict[str, Any]:
    """Create a GeoJSON Polygon feature; coordinates use [longitude, latitude]."""
    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coordinates]},
        "properties": {
            "lot_no": lot_no,
            "area_m2": area_m2,
            "area_ha": round(area_m2 / 10000, 4) if area_m2 is not None else None,
            "status": status,
            "source": source,
        },
    }


def lot_area_summary(area_m2: float | None) -> dict[str, Any]:
    """Return presentation-friendly area metrics without inventing geometry."""
    if area_m2 is None or area_m2 <= 0:
        return {"area_m2": None, "area_ha": None, "area_status": "EVIDENCE REQUIRED"}
    return {"area_m2": round(float(area_m2), 2), "area_ha": round(float(area_m2) / 10000, 4), "area_status": "AVAILABLE"}

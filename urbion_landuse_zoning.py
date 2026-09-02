"""Land-use and zoning evidence intelligence for URBION."""
from __future__ import annotations
from typing import Any


def layer_feature(*, latitude: float, longitude: float, layer: str, value: Any, status: str = "EVIDENCE REQUIRED", source: str = "PBT GIS / MelGIS", lot_no: str = "") -> dict[str, Any]:
    """Create a GeoJSON point carrying transparent planning-layer provenance."""
    return {"type":"Feature","geometry":{"type":"Point","coordinates":[float(longitude),float(latitude)]},"properties":{"layer":layer.upper(),"value":value,"status":status,"source":source,"lot_no":lot_no or "Not specified"}}


def zoning_signal(*, development_class: str, land_use: str | None, zoning: str | None) -> dict[str, Any]:
    """Return a conservative compatibility signal; never infer statutory permission."""
    text=" ".join(str(x or "") for x in (land_use,zoning)).strip().lower()
    if not text: return {"signal":"UNKNOWN","reason":"No land-use or zoning evidence supplied.","decision_safe":False}
    cls=str(development_class or "").lower()
    if cls and (cls in text or ("mixed" in cls and "mixed" in text)): return {"signal":"POTENTIAL_ALIGNMENT","reason":"Evidence contains an indicative development-class alignment signal; planner verification remains required.","decision_safe":False}
    return {"signal":"REVIEW","reason":"Available land-use/zoning evidence does not establish a clear class alignment.","decision_safe":False}


def landuse_summary(*, land_use: str | None, zoning: str | None, source_status: str = "DISCOVERY_COMPLETE") -> dict[str, Any]:
    return {"land_use":land_use,"zoning":zoning,"source_status":source_status,"evidence_required":not bool(land_use or zoning),"version":"PHASE-E.5"}

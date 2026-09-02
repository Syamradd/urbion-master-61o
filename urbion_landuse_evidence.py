"""Land-use and zoning evidence layer for URBION Phase E."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import build_evidence


def landuse_evidence(*, land_use: str | None = None, zoning: str | None = None, source: str = "PBT GIS / MelGIS", status: str = "DISCOVERY_COMPLETE", confidence: str = "MEDIUM", source_reference: str | None = None) -> list[dict[str, Any]]:
    items = []
    if land_use:
        items.append(build_evidence(source=source, layer="LAND_USE", value=land_use, evidence_type="LAND_USE", confidence=confidence, source_reference=source_reference, status=status))
    if zoning:
        items.append(build_evidence(source=source, layer="ZONING", value=zoning, evidence_type="ZONING", confidence=confidence, source_reference=source_reference, status=status))
    return items


def compatibility_signal(*, development_class: str, land_use: str | None, zoning: str | None) -> dict[str, Any]:
    """Provide a non-statutory signal; never converts a missing policy rule into compliance."""
    text = " ".join(str(x or "") for x in (land_use, zoning)).lower()
    cls = development_class.lower()
    if not text:
        return {"signal": "UNKNOWN", "reason": "No land-use or zoning evidence supplied."}
    if cls in text or "mixed" in cls and "mixed" in text:
        return {"signal": "POTENTIAL_ALIGNMENT", "reason": "Evidence text contains a development-class alignment signal; planner verification remains required."}
    return {"signal": "REVIEW", "reason": "Land-use/zoning evidence does not establish a clear class alignment."}

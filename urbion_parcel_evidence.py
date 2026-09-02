"""Parcel/lot evidence normalisation for URBION Phase E."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import build_evidence


def parcel_evidence(*, lot_no: str, source: str = "JUPEM", boundary: Any = None, confidence: str = "MEDIUM", status: str = "PLANNED", source_reference: str | None = None) -> dict[str, Any]:
    """Normalise a lot identifier without claiming cadastral verification."""
    return build_evidence(source=source, layer="PARCEL", location={"lot_no": lot_no}, value={"lot_no": lot_no, "boundary": boundary}, evidence_type="CADASTRAL", confidence=confidence, source_reference=source_reference, status=status)


def parcel_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    verified = [x for x in items if x.get("decision_safe")]
    return {"count": len(items), "verified_count": len(verified), "lots": [x.get("location", {}).get("lot_no") for x in items], "status": "VERIFIED" if verified else "EVIDENCE_REQUIRED", "version": "PHASE-E.2"}

"""Evidence-safe environmental intelligence for URBION."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import SAFE_STATES, build_evidence


def environment_evidence(*, layer: str, value: Any = None, source: str = "MyGEMS / MyEQMS", status: str = "QUERY_UNAVAILABLE", confidence: str = "LOW", source_reference: str | None = None) -> dict[str, Any]:
    """Create environmental evidence without implying verification."""
    return build_evidence(
        source=source,
        layer=layer.upper(),
        location={},
        value=value,
        evidence_type="ENVIRONMENT",
        confidence=confidence,
        source_reference=source_reference,
        status=status,
    )


def environment_summary(items: list[dict[str, Any]] | None) -> dict[str, Any]:
    records = list(items or [])
    verified = [x for x in records if x.get("status") in SAFE_STATES and x.get("decision_safe")]
    gaps = [x for x in records if not x.get("decision_safe")]
    return {
        "count": len(records),
        "verified_count": len(verified),
        "evidence_gap_count": len(gaps),
        "decision_safe": bool(records) and len(verified) == len(records),
        "status": "VERIFIED" if verified else ("EVIDENCE_REQUIRED" if gaps else "NO_EVIDENCE"),
        "version": "MASTER-108",
    }

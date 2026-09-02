"""Evidence-safe RT / i-Plan planning source binding."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import build_evidence

def planning_source_evidence(*, source: str, layer: str, value: Any = None, status: str = "REFERENCE_REGISTERED", confidence: str = "MEDIUM", source_reference: str | None = None) -> dict[str, Any]:
    return build_evidence(source=source, layer=layer.upper(), location={}, value=value, evidence_type="PLANNING", confidence=confidence, source_reference=source_reference, status=status)

def bind_planning_sources(*, items: list[dict[str, Any]] | None) -> dict[str, Any]:
    records=list(items or [])
    safe=[x for x in records if x.get("decision_safe")]
    return {"count":len(records),"decision_safe_count":len(safe),"status":"SUPPORTED" if safe else "EVIDENCE_REQUIRED","sources":sorted({str(x.get("source","")) for x in records}),"version":"MASTER-113"}

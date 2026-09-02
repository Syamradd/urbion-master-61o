"""Evidence-safe binding for GIS-derived planning layers."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import SAFE_STATES


def bind_gis_layers(*, evidence: list[dict[str, Any]], required_layers: list[str]) -> dict[str, Any]:
    items = list(evidence or [])
    layers = [str(x).upper() for x in required_layers]
    bound = []
    for layer in layers:
        matches = [e for e in items if str(e.get("layer", "")).upper() == layer]
        safe = [e for e in matches if e.get("status") in SAFE_STATES and e.get("decision_safe")]
        bound.append({"layer": layer, "evidence_count": len(matches), "verified_count": len(safe), "status": "VERIFIED" if safe else ("GAP" if matches else "NO_EVIDENCE")})
    verified = sum(1 for x in bound if x["status"] == "VERIFIED")
    return {"layers": bound, "verified_layers": verified, "decision_ready": verified == len(layers) if layers else False, "version": "MASTER-106"}

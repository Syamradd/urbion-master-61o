"""Bind available evidence to rules without manufacturing statutory support."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import SAFE_STATES


def bind_evidence_to_rules(evidence: list[dict[str, Any]], rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items = list(evidence or [])
    output = []
    for rule in list(rules or []):
        rid = rule.get("rule_id")
        layer = str(rule.get("evidence_layer") or rule.get("layer") or "").upper()
        matches = [e for e in items if (not layer or str(e.get("layer", "")).upper() == layer)]
        safe = [e for e in matches if e.get("status") in SAFE_STATES and e.get("decision_safe")]
        output.append({"rule_id": rid, "evidence_count": len(matches), "decision_safe_evidence": len(safe), "evidence_status": "SUPPORTED" if safe else ("GAP" if matches else "NO_EVIDENCE"), "evidence": matches})
    return output

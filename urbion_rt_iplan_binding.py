"""Evidence-safe RT/i-Plan binding helpers for URBION."""
from __future__ import annotations
from typing import Any
from urbion_evidence_contract import SAFE_STATES

def bind_planning_sources(*, evidence: list[dict[str, Any]], required_layers: list[str] | None = None) -> dict[str, Any]:
    required = [str(x).upper() for x in (required_layers or ['RT','ZONING','LAND_USE'])]
    rows=[]
    for layer in required:
        matches=[e for e in evidence if str(e.get('layer','')).upper()==layer]
        safe=[e for e in matches if e.get('status') in SAFE_STATES and e.get('decision_safe')]
        rows.append({'layer':layer,'evidence_count':len(matches),'verified_count':len(safe),'status':'VERIFIED' if safe else ('GAP' if matches else 'NO_EVIDENCE')})
    return {'layers':rows,'decision_ready':bool(rows) and all(x['status']=='VERIFIED' for x in rows),'version':'MASTER-113'}

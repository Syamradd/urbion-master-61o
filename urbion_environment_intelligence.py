"""Evidence-aware environmental and geohazard screening for URBION.

The module deliberately separates source availability from verified site facts.
It never invents flood, KSAS, geology, slope, groundwater or environmental
conditions. Explicit evidence supplied by a connected source or planner is
converted into transparent screening flags; missing evidence becomes a review
gap rather than a favourable assumption.
"""
from __future__ import annotations
from typing import Any

DOMAINS = {
    "flood": ("Flood / Banjir", "JPS / i-Plan"),
    "ksas": ("KSAS", "i-Plan"),
    "slope": ("Slope / Cerun", "JMG NaTSIS / terrain"),
    "geohazard": ("Geohazard", "JMG MyGEMS"),
    "geology": ("Geology / Lithology", "JMG MyGEMS"),
    "seismic": ("Seismic", "JMG MyGEMS"),
    "groundwater": ("Groundwater", "JMG MyGEMS"),
    "quarry_mining": ("Mines / Quarries", "JMG MyGEMS"),
    "ecology": ("Ecological Network / CFS", "i-Plan"),
    "water_quality": ("Water / Environmental Quality", "JAS MyEQMS / JPS"),
    "river_reserve": ("River / Drainage Reserve", "JPS / PBT"),
}


def _normalise(item: Any) -> tuple[Any, str, str | None]:
    if isinstance(item, dict):
        return item.get("value"), str(item.get("evidence", "UNVERIFIED")), item.get("source")
    if item is None:
        return None, "UNVERIFIED", None
    return item, "USER_PROVIDED", None


def _flag(domain: str, raw: Any) -> dict[str, Any]:
    label, default_source = DOMAINS[domain]
    value, evidence, source = _normalise(raw)
    evidence = evidence.upper()
    source = source or default_source
    known = value is not None
    risk = None
    status = "REVIEW_REQUIRED"
    if known:
        if domain in {"flood", "ksas", "geohazard", "seismic", "quarry_mining", "river_reserve"}:
            risk = bool(value)
            status = "RISK_FLAG" if risk else "NO_FLAG"
        elif domain == "ecology":
            risk = bool(value)
            status = "SENSITIVITY_FLAG" if risk else "NO_FLAG"
        elif domain == "slope":
            try:
                risk = float(value) >= 25.0
                status = "SLOPE_RISK" if risk else "SCREENED"
            except (TypeError, ValueError):
                status = "REVIEW_REQUIRED"
        else:
            risk = bool(value) if isinstance(value, bool) else None
            status = "SOURCE_REVIEW" if risk is None else ("RISK_FLAG" if risk else "NO_FLAG")
    return {
        "id": domain,
        "name": label,
        "value": value,
        "status": status,
        "risk_flag": risk,
        "evidence": evidence,
        "source": source,
        "decision_use": "SCREENING_ONLY",
    }


def build_environment_intelligence(context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build an auditable environmental/geohazard screening package."""
    context = context or {}
    metrics = [_flag(domain, context.get(domain)) for domain in DOMAINS]
    known = [m for m in metrics if m["value"] is not None and m["status"] != "REVIEW_REQUIRED"]
    flagged = [m for m in metrics if m["risk_flag"] is True]
    gaps = [f"environment:{m['id']}" for m in metrics if m["status"] == "REVIEW_REQUIRED"]
    return {
        "version": "MASTER-226",
        "status": "RISK_FLAGGED" if flagged else ("PARTIALLY_SCREENED" if known else "EVIDENCE_REQUIRED"),
        "metrics": metrics,
        "summary": {
            "domain_count": len(metrics),
            "screened_count": len(known),
            "flagged_count": len(flagged),
            "review_gap_count": len(gaps),
        },
        "review_gaps": gaps,
        "sources": sorted({m["source"] for m in metrics}),
        "decision_boundary": "ENVIRONMENTAL_SCREENING_SUPPORT",
        "statutory_verification": "NOT_CLAIMED",
        "disclaimer": "Environmental and geohazard screening is decision support only. Confirm authoritative currency, technical thresholds and agency requirements before planning reliance.",
    }

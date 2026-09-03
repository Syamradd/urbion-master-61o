"""Evidence-aware environmental and geohazard screening for URBION."""
from __future__ import annotations
from typing import Any

DOMAINS = {
    "flood": ("Flood / Banjir", "PLANMalaysia DPFDN / JPS"),
    "ksas": ("KSAS", "PLANMalaysia DPFDN"),
    "slope": ("Slope / Cerun", "PLANMalaysia DPFDN / JMG NaTSIS"),
    "geohazard": ("Geohazard / Tanah Runtuh", "PLANMalaysia DPFDN / JMG MyGEMS"),
    "geology": ("Geology / Lithology", "JMG MyGEMS"),
    "seismic": ("Seismic", "PLANMalaysia DPFDN / JMG MyGEMS"),
    "groundwater": ("Groundwater", "JMG MyGEMS"),
    "quarry_mining": ("Mines / Quarries", "JMG MyGEMS"),
    "ecology": ("Ecological Network / CFS", "PLANMalaysia DPFDN / i-Plan"),
    "water_quality": ("Water / Environmental Quality", "JAS MyEQMS / JPS"),
    "river_reserve": ("River / Drainage Context", "PLANMalaysia DPFDN / JPS / PBT"),
}

def _normalise(item: Any) -> tuple[Any, str, str | None, dict[str, Any]]:
    if isinstance(item, dict): return item.get("value"), str(item.get("evidence", "UNVERIFIED")), item.get("source"), item
    if item is None: return None, "UNVERIFIED", None, {}
    return item, "USER_PROVIDED", None, {}

def _flag(domain: str, raw: Any) -> dict[str, Any]:
    label, default_source = DOMAINS[domain]
    value, evidence, source, meta = _normalise(raw)
    evidence = evidence.upper(); source = source or default_source
    known = value is not None; risk = None; status = "REVIEW_REQUIRED"
    if known:
        if domain in {"flood", "ksas", "geohazard", "seismic", "quarry_mining", "river_reserve"}:
            risk = bool(value); status = "RISK_FLAG" if risk else "NO_FLAG"
        elif domain == "ecology":
            risk = bool(value); status = "SENSITIVITY_FLAG" if risk else "NO_FLAG"
        elif domain == "slope":
            try: risk = float(value) >= 25.0; status = "SLOPE_RISK" if risk else "SCREENED"
            except (TypeError, ValueError): status = "REVIEW_REQUIRED"
        else:
            risk = bool(value) if isinstance(value, bool) else None
            status = "SOURCE_REVIEW" if risk is None else ("RISK_FLAG" if risk else "NO_FLAG")
    return {"id":domain,"name":label,"value":value,"status":status,"risk_flag":risk,"evidence":evidence,"source":source,"decision_use":"SCREENING_ONLY",**meta}

def _derive_from_planmalaysia(context: dict[str, Any]) -> dict[str, Any]:
    layers = context.get("layers") or {}; out: dict[str, Any] = {}
    def hit(key: str) -> bool: return bool((layers.get(key) or {}).get("feature_count", 0))
    if "flood" in layers: out["flood"]={"value":hit("flood"),"evidence":"SOURCE_CONTEXT","source":"PLANMalaysia DPFDN — Banjir 100 tahun","query":layers["flood"]}
    if "ksas" in layers: out["ksas"]={"value":hit("ksas"),"evidence":"SOURCE_CONTEXT","source":"PLANMalaysia DPFDN — KSAS","query":layers["ksas"]}
    if "geohazard" in layers: out["geohazard"]={"value":hit("geohazard"),"evidence":"SOURCE_CONTEXT","source":"PLANMalaysia DPFDN — Tanah Runtuh","query":layers["geohazard"]}
    if "seismic" in layers: out["seismic"]={"value":hit("seismic"),"evidence":"SOURCE_CONTEXT","source":"PLANMalaysia DPFDN — Risiko Gempa Bumi","query":layers["seismic"]}
    if "quarry_mining" in layers: out["quarry_mining"]={"value":hit("quarry_mining"),"evidence":"SOURCE_CONTEXT","source":"JMG MyGEMS","query":layers["quarry_mining"]}
    if "ecology" in layers: out["ecology"]={"value":hit("ecology"),"evidence":"SOURCE_CONTEXT","source":"PLANMalaysia DPFDN — CFS","query":layers["ecology"]}
    if "river" in layers: out["river_reserve"]={"value":hit("river"),"evidence":"SOURCE_CONTEXT","source":"PLANMalaysia DPFDN — Sungai","query":layers["river"]}
    slope=layers.get("slope") or {}
    if slope.get("feature_count"):
        values=[str(x.get("DEGREES", "")) for x in slope.get("features", [])]
        high=any("Above 35" in v or "25 - 35" in v for v in values)
        out["slope"]={"value":25.0 if high else 0.0,"evidence":"SOURCE_CONTEXT","source":"PLANMalaysia DPFDN — Kecerunan","query":slope,"classification":values}
    return out

def build_environment_intelligence(context: dict[str, Any] | None = None) -> dict[str, Any]:
    context=context or {}; merged=dict(context)
    for key,value in _derive_from_planmalaysia(context).items(): merged.setdefault(key,value)
    metrics=[_flag(domain,merged.get(domain)) for domain in DOMAINS]
    known=[m for m in metrics if m["value"] is not None and m["status"] != "REVIEW_REQUIRED"]
    flagged=[m for m in metrics if m["risk_flag"] is True]
    gaps=[f"environment:{m['id']}" for m in metrics if m["status"] == "REVIEW_REQUIRED"]
    return {"version":"MASTER-226","status":"RISK_FLAGGED" if flagged else ("PARTIALLY_SCREENED" if known else "EVIDENCE_REQUIRED"),"metrics":metrics,"summary":{"domain_count":len(metrics),"screened_count":len(known),"flagged_count":len(flagged),"review_gap_count":len(gaps)},"review_gaps":gaps,"sources":sorted({m["source"] for m in metrics}),"site":context.get("site"),"radius_m":context.get("radius_m"),"decision_boundary":"ENVIRONMENTAL_SCREENING_SUPPORT","statutory_verification":"NOT_CLAIMED","disclaimer":"Environmental/geohazard screening is decision support only. A spatial hit within a configured radius is not a legal setback or statutory determination; confirm authoritative currency, technical thresholds and agency requirements."}

"""URBION MASTER-63 site intelligence layer.

Safe-by-design: this module does not pretend to have live access to external
GIS portals. It records source coverage/status and computes transparent
preliminary suitability and recommendation indicators from inputs already
available to URBION.
"""
from __future__ import annotations

from typing import Any

STATE_PBT = {
    "Melaka": [
        "Majlis Bandaraya Melaka Bersejarah",
        "Majlis Perbandaran Alor Gajah",
        "Majlis Perbandaran Jasin",
        "Majlis Perbandaran Hang Tuah Jaya",
    ],
    "Selangor": [
        "Majlis Bandaraya Shah Alam", "Majlis Bandaraya Petaling Jaya", "Majlis Bandaraya Subang Jaya",
        "Majlis Bandaraya DiRaja Klang", "Majlis Perbandaran Ampang Jaya", "Majlis Perbandaran Kajang",
        "Majlis Perbandaran Selayang", "Majlis Perbandaran Sepang", "Majlis Perbandaran Kuala Langat",
        "Majlis Perbandaran Hulu Selangor", "Majlis Perbandaran Kuala Selangor", "Majlis Daerah Sabak Bernam",
    ],
    "Johor": [
        "Majlis Bandaraya Johor Bahru", "Majlis Bandaraya Iskandar Puteri", "Majlis Bandaraya Pasir Gudang",
        "Majlis Perbandaran Batu Pahat", "Majlis Perbandaran Kluang", "Majlis Perbandaran Muar",
        "Majlis Perbandaran Kulai", "Majlis Perbandaran Segamat",
    ],
    "Pulau Pinang": ["Majlis Bandaraya Pulau Pinang", "Majlis Bandaraya Seberang Perai"],
    "Perak": ["Majlis Bandaraya Ipoh", "Majlis Perbandaran Manjung", "Majlis Perbandaran Taiping", "Majlis Perbandaran Kuala Kangsar", "Majlis Perbandaran Teluk Intan"],
    "Negeri Sembilan": ["Majlis Bandaraya Seremban", "Majlis Perbandaran Port Dickson", "Majlis Perbandaran Jempol", "Majlis Daerah Jelebu", "Majlis Daerah Kuala Pilah", "Majlis Daerah Rembau", "Majlis Daerah Tampin"],
    "Pahang": ["Majlis Bandaraya Kuantan", "Majlis Perbandaran Temerloh", "Majlis Perbandaran Bentong", "Majlis Perbandaran Pekan"],
    "Terengganu": ["Majlis Bandaraya Kuala Terengganu", "Majlis Perbandaran Kemaman", "Majlis Perbandaran Dungun", "Majlis Daerah Besut"],
    "Kedah": ["Majlis Bandaraya Alor Setar", "Majlis Perbandaran Langkawi Bandaraya Pelancongan", "Majlis Perbandaran Sungai Petani", "Majlis Perbandaran Kulim"],
    "Perlis": ["Majlis Perbandaran Kangar"],
    "Kelantan": ["Majlis Perbandaran Kota Bharu Bandaraya Islam", "Majlis Daerah Ketereh", "Majlis Daerah Tanah Merah"],
    "Wilayah Persekutuan": ["Dewan Bandaraya Kuala Lumpur"],
    "Sabah": ["Dewan Bandaraya Kota Kinabalu", "Majlis Perbandaran Sandakan", "Majlis Perbandaran Tawau"],
    "Sarawak": ["Dewan Bandaraya Kuching Utara", "Majlis Bandaraya Kuching Selatan", "Majlis Bandaraya Miri", "Majlis Perbandaran Sibu"],
}

DEVELOPMENT_CLASSES = {
    "Residential": ["Apartment / High-Rise", "Terrace Housing", "Semi-Detached", "Detached Housing", "Cluster Housing"],
    "Commercial": ["Free-Standing Commercial", "Free-Standing Building", "Commercial Shop Frontage", "Commercial Shop-Office"],
    "Industrial": ["Light Industry", "Medium Industry", "Heavy Industry", "SME / Cottage Industry"],
    "Institutional": ["Education", "Healthcare", "Government / Civic", "Religious / Community"],
    "Recreation": ["Public Open Space", "Sports / Recreation", "Tourism / Leisure"],
    "Infrastructure": ["Transport", "Utility", "Infrastructure Support"],
    "Mixed Use": ["TOD Development / Mixed Use", "Transit-Oriented Mixed Use", "Urban Mixed Use"],
}

SOURCE_REGISTRY = [
    {"source": "PLANMalaysia / Rancangan Tempatan", "category": "PLANNING", "status": "REFERENCE_REGISTERED", "evidence": "Planning policy / RT context", "note": "RT MBMB 2035 rule engine is active for covered typologies."},
    {"source": "PBT GIS / MelGIS", "category": "PBT / GIS", "status": "DISCOVERY_COMPLETE", "evidence": "Parcel / zoning / land-use architecture", "note": "Public layer architecture was discovered; live parcel query is not claimed here."},
    {"source": "i-Plan", "category": "PLANNING", "status": "PLANNED", "evidence": "Planning / land-use context", "note": "Connector interface registered; no live query is claimed."},
    {"source": "JUPEM", "category": "CADASTRAL", "status": "PLANNED", "evidence": "Parcel / cadastral", "note": "Connector interface registered; no live query is claimed."},
    {"source": "MyGEMS", "category": "GEOLOGY", "status": "QUERY_UNAVAILABLE", "evidence": "Geology / lithology", "note": "Recovered diagnostic recorded query unavailability."},
    {"source": "MyEQMS", "category": "ENVIRONMENT", "status": "PLANNED", "evidence": "Air / river / marine environment", "note": "Connector interface registered; no live query is claimed."},
    {"source": "Manual Planner Verification", "category": "VERIFICATION", "status": "AVAILABLE", "evidence": "Site observation / planning context", "note": "Can be used when a planner supplies verified site evidence."},
]


def pbt_options(state: str) -> list[str]:
    return STATE_PBT.get(state, [])


def policy_coverage(pbt: str) -> dict[str, Any]:
    if pbt == "Majlis Bandaraya Melaka Bersejarah":
        return {"coverage": "FULL_RULE_ENGINE", "reference": "RT MBMB 2035", "message": "Verified MASTER-61O planning rules are active for the supported typologies."}
    return {"coverage": "SPATIAL_DEMO_ONLY", "reference": "PBT selected; local policy rules not loaded", "message": "URBION can demonstrate site intelligence, but does not invent local development controls."}


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def _recommendation(final_status: str, suitability: float, pbt: str, development_type: str) -> dict[str, Any]:
    if final_status == "NON-COMPLIANCE":
        return {
            "headline": "REDESIGN BEFORE PROCEEDING",
            "level": "BLOCKED",
            "reason": "A verified planning control is currently not satisfied.",
            "next_actions": ["Review the failed control", "Adjust the proposal or typology", "Re-run URBION analysis"],
        }
    if final_status == "COMPLY" and suitability >= 80:
        return {
            "headline": "STRONG CANDIDATE FOR FURTHER STUDY",
            "level": "POSITIVE",
            "reason": "The current proposal passes the loaded rule checks and scores strongly on preliminary site indicators.",
            "next_actions": ["Validate cadastral and zoning evidence", "Complete technical due diligence", "Proceed to detailed planning assessment"],
        }
    if final_status == "NOT APPLICABLE":
        return {
            "headline": "RECONSIDER DEVELOPMENT POSITION",
            "level": "CAUTION",
            "reason": "The selected development concept does not satisfy the current spatial applicability condition.",
            "next_actions": ["Review the TOD / spatial threshold", "Test an alternative location or typology", "Re-run URBION analysis"],
        }
    if pbt != "Majlis Bandaraya Melaka Bersejarah":
        return {
            "headline": "EVIDENCE REQUIRED BEFORE DECISION",
            "level": "REVIEW",
            "reason": "Site intelligence is available, but the selected PBT's local statutory rule set is not loaded into the verified engine.",
            "next_actions": ["Load / verify the applicable local plan", "Confirm zoning and development controls", "Re-run the compliance assessment"],
        }
    return {
        "headline": "PROCEED WITH PLANNER REVIEW",
        "level": "REVIEW",
        "reason": "The site shows useful potential, but one or more policy or evidence conditions still require verification.",
        "next_actions": ["Resolve outstanding evidence gaps", "Review applicable controls", "Re-run URBION analysis"],
    }


def _decision_confidence(pbt: str, lot_no: str, final_status: str, tod_distance_m: float) -> dict[str, Any]:
    score = 55
    reasons = []
    if pbt == "Majlis Bandaraya Melaka Bersejarah":
        score += 22
        reasons.append("verified MBMB rule coverage")
    else:
        reasons.append("local PBT rules not loaded")
    if lot_no.strip():
        score += 10
        reasons.append("lot identity supplied")
    else:
        reasons.append("lot identity not supplied")
    if tod_distance_m <= 800:
        score += 8
        reasons.append("TOD proximity calculated")
    else:
        score += 3
        reasons.append("TOD proximity calculated but outside 800 m")
    if final_status in {"COMPLY", "NON-COMPLIANCE"}:
        score += 5
        reasons.append("rule outcome resolved")
    else:
        reasons.append("decision remains review-dependent")
    score = round(_clamp(score), 1)
    band = "HIGH" if score >= 80 else "MEDIUM" if score >= 65 else "LOW"
    return {"score": score, "band": band, "basis": reasons, "note": "Confidence reflects evidence and rule coverage, not approval probability."}


def build_site_analysis(*, state: str, district: str, pbt: str, lot_no: str, latitude: float, longitude: float,
                        tod_distance_m: float, development_class: str, development_type: str,
                        policy_status: str, final_status: str) -> dict[str, Any]:
    if tod_distance_m <= 400:
        access, transit_band = 92, "HIGH TRANSIT ACCESS"
    elif tod_distance_m <= 800:
        access, transit_band = 78, "GOOD TRANSIT ACCESS"
    elif tod_distance_m <= 1500:
        access, transit_band = 58, "MODERATE TRANSIT ACCESS"
    else:
        access, transit_band = 36, "LOW TRANSIT PROXIMITY"

    planning = 94 if policy_status == "COMPLY" else 72 if policy_status in {"REQUIRES REVIEW", "CONDITIONAL RISK"} else 42 if policy_status == "NON-COMPLIANCE" else 60
    data_confidence = 88 if pbt == "Majlis Bandaraya Melaka Bersejarah" else 64
    completeness = 90 if lot_no.strip() else 76
    environment = 55
    suitability = round(_clamp((planning * .30) + (access * .25) + (data_confidence * .20) + (completeness * .10) + (environment * .15)), 1)
    band = "HIGH POTENTIAL" if suitability >= 80 else "MODERATE POTENTIAL" if suitability >= 65 else "REQUIRES FURTHER STUDY"
    recommendation = _recommendation(final_status, suitability, pbt, development_type)
    confidence = _decision_confidence(pbt, lot_no, final_status, tod_distance_m)

    return {
        "title": "Preliminary Site Suitability",
        "score": suitability,
        "band": band,
        "disclaimer": "Decision-support indicator only. It is not a statutory approval or a substitute for site investigation.",
        "recommendation": recommendation,
        "decision_confidence": confidence,
        "indicators": [
            {"name": "Planning Fit", "score": round(planning, 1), "basis": final_status},
            {"name": "Transit Access", "score": round(access, 1), "basis": f"{round(tod_distance_m, 1)} m from TOD node"},
            {"name": "Data Confidence", "score": round(data_confidence, 1), "basis": "PBT / planning source coverage"},
            {"name": "Site Completeness", "score": round(completeness, 1), "basis": "Lot / site identity fields"},
            {"name": "Environment Evidence", "score": round(environment, 1), "basis": "No live MyGEMS / MyEQMS evidence claimed"},
        ],
        "spatial_summary": {
            "state": state, "district": district, "pbt": pbt, "lot_no": lot_no or "Not specified",
            "latitude": latitude, "longitude": longitude, "development_class": development_class,
            "development_type": development_type, "transit_band": transit_band,
        },
    }


def source_registry_snapshot() -> list[dict[str, Any]]:
    return [dict(item) for item in SOURCE_REGISTRY]

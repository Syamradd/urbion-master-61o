"""URBION MASTER-62 site intelligence layer.

Safe-by-design: this module does not pretend to have live access to external
GIS portals. It records source coverage/status and computes transparent
preliminary suitability indicators from inputs already available to URBION.
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
        "Majlis Bandaraya Shah Alam",
        "Majlis Bandaraya Petaling Jaya",
        "Majlis Bandaraya Subang Jaya",
        "Majlis Bandaraya DiRaja Klang",
        "Majlis Perbandaran Ampang Jaya",
        "Majlis Perbandaran Kajang",
        "Majlis Perbandaran Selayang",
        "Majlis Perbandaran Sepang",
        "Majlis Perbandaran Kuala Langat",
        "Majlis Perbandaran Hulu Selangor",
        "Majlis Perbandaran Kuala Selangor",
        "Majlis Daerah Sabak Bernam",
    ],
    "Johor": [
        "Majlis Bandaraya Johor Bahru",
        "Majlis Bandaraya Iskandar Puteri",
        "Majlis Bandaraya Pasir Gudang",
        "Majlis Perbandaran Batu Pahat",
        "Majlis Perbandaran Kluang",
        "Majlis Perbandaran Muar",
        "Majlis Perbandaran Kulai",
        "Majlis Perbandaran Segamat",
    ],
    "Pulau Pinang": [
        "Majlis Bandaraya Pulau Pinang",
        "Majlis Bandaraya Seberang Perai",
    ],
    "Perak": [
        "Majlis Bandaraya Ipoh",
        "Majlis Perbandaran Manjung",
        "Majlis Perbandaran Taiping",
        "Majlis Perbandaran Kuala Kangsar",
        "Majlis Perbandaran Teluk Intan",
    ],
    "Negeri Sembilan": [
        "Majlis Bandaraya Seremban",
        "Majlis Perbandaran Port Dickson",
        "Majlis Perbandaran Jempol",
        "Majlis Daerah Jelebu",
        "Majlis Daerah Kuala Pilah",
        "Majlis Daerah Rembau",
        "Majlis Daerah Tampin",
    ],
    "Pahang": [
        "Majlis Bandaraya Kuantan",
        "Majlis Perbandaran Temerloh",
        "Majlis Perbandaran Bentong",
        "Majlis Perbandaran Pekan",
    ],
    "Terengganu": [
        "Majlis Bandaraya Kuala Terengganu",
        "Majlis Perbandaran Kemaman",
        "Majlis Perbandaran Dungun",
        "Majlis Daerah Besut",
    ],
    "Kedah": [
        "Majlis Bandaraya Alor Setar",
        "Majlis Perbandaran Langkawi Bandaraya Pelancongan",
        "Majlis Perbandaran Sungai Petani",
        "Majlis Perbandaran Kulim",
    ],
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
        return {
            "coverage": "FULL_RULE_ENGINE",
            "reference": "RT MBMB 2035",
            "message": "Verified MASTER-61O planning rules are active for the supported typologies.",
        }
    return {
        "coverage": "SPATIAL_DEMO_ONLY",
        "reference": "PBT selected; local policy rules not loaded",
        "message": "URBION can demonstrate site intelligence, but does not invent local development controls.",
    }


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def build_site_analysis(
    *,
    state: str,
    district: str,
    pbt: str,
    lot_no: str,
    latitude: float,
    longitude: float,
    tod_distance_m: float,
    development_class: str,
    development_type: str,
    policy_status: str,
    final_status: str,
) -> dict[str, Any]:
    # These are preliminary decision-support indicators, not statutory scores.
    if tod_distance_m <= 400:
        access = 92
        transit_band = "HIGH TRANSIT ACCESS"
    elif tod_distance_m <= 800:
        access = 78
        transit_band = "GOOD TRANSIT ACCESS"
    elif tod_distance_m <= 1500:
        access = 58
        transit_band = "MODERATE TRANSIT ACCESS"
    else:
        access = 36
        transit_band = "LOW TRANSIT PROXIMITY"

    planning = 94 if policy_status == "COMPLY" else 72 if policy_status == "REQUIRES REVIEW" else 42 if policy_status == "NON-COMPLIANCE" else 60
    data_confidence = 88 if pbt == "Majlis Bandaraya Melaka Bersejarah" else 64
    completeness = 90 if lot_no.strip() else 76
    environment = 55  # intentionally neutral: no live MyGEMS/MyEQMS evidence is claimed
    suitability = round(_clamp((planning * 0.30) + (access * 0.25) + (data_confidence * 0.20) + (completeness * 0.10) + (environment * 0.15)), 1)

    if suitability >= 80:
        band = "HIGH POTENTIAL"
    elif suitability >= 65:
        band = "MODERATE POTENTIAL"
    else:
        band = "REQUIRES FURTHER STUDY"

    return {
        "title": "Preliminary Site Suitability",
        "score": suitability,
        "band": band,
        "disclaimer": "Decision-support indicator only. It is not a statutory approval or a substitute for site investigation.",
        "indicators": [
            {"name": "Planning Fit", "score": round(planning, 1), "basis": final_status},
            {"name": "Transit Access", "score": round(access, 1), "basis": f"{round(tod_distance_m, 1)} m from TOD node"},
            {"name": "Data Confidence", "score": round(data_confidence, 1), "basis": "PBT / planning source coverage"},
            {"name": "Site Completeness", "score": round(completeness, 1), "basis": "Lot / site identity fields"},
            {"name": "Environment Evidence", "score": round(environment, 1), "basis": "No live MyGEMS / MyEQMS evidence claimed"},
        ],
        "spatial_summary": {
            "state": state,
            "district": district,
            "pbt": pbt,
            "lot_no": lot_no or "Not specified",
            "latitude": latitude,
            "longitude": longitude,
            "development_class": development_class,
            "development_type": development_type,
            "transit_band": transit_band,
        },
    }


def source_registry_snapshot() -> list[dict[str, Any]]:
    return [dict(item) for item in SOURCE_REGISTRY]

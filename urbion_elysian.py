"""Legacy Elysian GIS bridge.

Elysian is retained as a user/project-provided reference dataset. It is never
silently treated as authoritative when it conflicts with live official sources.
"""
from __future__ import annotations

ELYSIAN_LOT_11213 = {
    "lot_no": "11213",
    "location": "Jalan Taman Bandaraya, Padang Semabok, Melaka Tengah",
    "area_ha": 1.145,
    "current_land_use": "Pertanian",
    "secondary_land_use": "Tanah Tidak Diusahakan",
    "tertiary_land_use": "Semak Samun / Belukar / Tanah Terbiar",
    "district": "Melaka Tengah",
    "mukim": "Padang Semabok",
    "code": "PT126",
    "data_year": 2024,
    "updated": "2024-12-31",
    "evidence_status": "PROJECT_REFERENCE",
}

def compare_official_context(official: dict | None) -> dict:
    """Compare Elysian's known parcel context with an official query result."""
    official = official or {}
    attrs = official.get("attributes") or {}
    candidates = {
        "land_use": [attrs.get("gunatanah1"), attrs.get("guna_tanah"), attrs.get("LANDUSE")],
        "area_ha": [attrs.get("luas_ha"), attrs.get("area_ha"), attrs.get("LUAS_HA")],
        "lot_no": [attrs.get("no_lot"), attrs.get("lot_no"), attrs.get("LOT_NO")],
        "district": [attrs.get("daerah"), attrs.get("district"), attrs.get("DAERAH")],
        "mukim": [attrs.get("mukim"), attrs.get("MUKIM")],
    }
    conflicts = []
    land_values = [v for v in candidates["land_use"] if v is not None]
    if land_values:
        value = str(land_values[0])
        if value.strip().lower() != ELYSIAN_LOT_11213["current_land_use"].lower():
            conflicts.append({"field":"current_land_use","elysian":ELYSIAN_LOT_11213["current_land_use"],"official":value})
    return {
        "reference": ELYSIAN_LOT_11213,
        "official_status": official.get("status", "NOT_PROVIDED"),
        "conflicts": conflicts,
        "resolution_policy": "OFFICIAL_SOURCE_WINS_FOR_DECISION_CONTEXT; ELYSIAN RETAINED AS TRACEABLE PROJECT REFERENCE",
        "decision_safe": False,
    }

def elysian_source_record() -> dict:
    return {
        "id": "elysian-legacy-gis",
        "name": "Elysian GIS Legacy Reference",
        "type": "PROJECT_REFERENCE",
        "status": "REFERENCE_REGISTERED",
        "role": "Legacy parcel/site context and historical GIS attributes used for cross-source reconciliation",
        "decision_safe": False,
        "notes": "Not authoritative by itself; reconcile against current official i-Plan/JUPEM/PBT evidence before decision use.",
    }

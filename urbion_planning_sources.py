"""Authoritative planning-source registry for URBION.

Sources are classified by role. A registered reference is not automatically
statutory evidence; applicability and currency remain planner responsibilities.
"""
from __future__ import annotations
from typing import Any

PLANNING_SOURCES: list[dict[str, Any]] = [
    {"id":"RFN4","name":"Rancangan Fizikal Negara Keempat (RFN4)","name_ms":"Rancangan Fizikal Negara Keempat (RFN4)","level":"NATIONAL","layers":["NATIONAL_POLICY","SPATIAL_STRATEGY"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia","reference":"https://myplan.planmalaysia.gov.my/portal-main/publication-details?id=7"},
    {"id":"DPN2","name":"National Urban Policy 2 (DPN2)","name_ms":"Dasar Perbandaran Negara Kedua (DPN2)","level":"NATIONAL","layers":["NATIONAL_POLICY","URBAN_POLICY"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia","reference":"https://myplan.planmalaysia.gov.my/portal-main/publication-details?id=4"},
    {"id":"DPFDN","name":"National Rural Physical Planning Policy 2030","name_ms":"Dasar Perancangan Fizikal Desa Negara 2030","level":"NATIONAL","layers":["NATIONAL_POLICY","RURAL_POLICY"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia","reference":"https://myplan.planmalaysia.gov.my/portal-main/publication-details?id=2"},
    {"id":"RT_MBMB","name":"RT Majlis Bandaraya Melaka Bersejarah 2035","name_ms":"Rancangan Tempatan Majlis Bandaraya Melaka Bersejarah 2035","level":"LOCAL","layers":["RT","ZONING","LAND_USE","PLANNING_POLICY"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia Melaka","reference":"https://www.jpbdmelaka.gov.my/rt-rancangan-tempatan"},
    {"id":"RT_STATE_MELAKA","name":"Melaka Local Plans","name_ms":"Rancangan Tempatan Negeri Melaka","level":"LOCAL","layers":["RT","ZONING","LAND_USE"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia Melaka","reference":"https://www.jpbdmelaka.gov.my/rt-rancangan-tempatan"},
    {"id":"RSN_MELAKA_2040","name":"Melaka State Structure Plan 2040 review","name_ms":"Kajian Semula Rancangan Struktur Negeri Melaka 2040","level":"STATE","layers":["RSN","STATE_STRATEGY","SPATIAL_STRATEGY"],"status":"IN_PROGRESS","authority":"PLANMalaysia Melaka","reference":"https://www.jpbdmelaka.gov.my/rsn-rancangan-struktur-negeri"},
    {"id":"RKK_MELAKA","name":"Special Area Plans (RKK) Melaka","name_ms":"Rancangan Kawasan Khas (RKK) Negeri Melaka","level":"LOCAL","layers":["RKK","SPECIAL_AREA","DETAILED_PLANNING"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia Melaka","reference":"https://www.jpbdmelaka.gov.my/rkk-rancangan-kawasan-khas"},
    {"id":"GPP_MELAKA","name":"Melaka Planning Guidelines and Standards","name_ms":"Garis Panduan dan Piawaian Perancangan Negeri Melaka","level":"STATE","layers":["PLANNING_GUIDELINE","DEVELOPMENT_CONTROL","STANDARDS"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia Melaka","reference":"https://www.jpbdmelaka.gov.my/piawaian-perancangan"},
    {"id":"IPLAN","name":"PLANMalaysia i-Plan","name_ms":"PLANMalaysia i-Plan","level":"SPATIAL_DATA","layers":["CURRENT_LAND_USE","ZONING","COMMITTED_LAND_USE","LOT","RT"],"status":"LIVE_ARCGIS_REST","authority":"PLANMalaysia","reference":"https://iplan.planmalaysia.gov.my/"},
    {"id":"MYPLAN","name":"PLANMalaysia MyPLAN","name_ms":"PLANMalaysia MyPLAN","level":"NATIONAL","layers":["RFN4","DPN2","DPFDN","SECTORAL_POLICY"],"status":"REFERENCE_REGISTERED","authority":"PLANMalaysia","reference":"https://myplan.planmalaysia.gov.my/portal-main/home"},
    {"id":"MELGIS","name":"MelGIS / PBT GIS","name_ms":"MelGIS / GIS PBT","level":"LOCAL","layers":["PARCEL","LAND_USE","ZONING","BOUNDARY"],"status":"DISCOVERY_COMPLETE","authority":"Melaka GIS / PBT","reference":"https://melgis.melaka.gov.my"},
    {"id":"JUPEM","name":"JUPEM MyLot","name_ms":"JUPEM MyLot","level":"CADASTRAL","layers":["PARCEL","CADASTRAL","BOUNDARY"],"status":"PUBLIC_PORTAL","authority":"JUPEM","reference":"https://jupem2u.kul.jupem.gov.my/mylot/index.html"},
]

def planning_source_summary() -> dict[str, Any]:
    counts: dict[str, int] = {}
    for source in PLANNING_SOURCES:
        status = source["status"]
        counts[status] = counts.get(status, 0) + 1
    return {"sources":PLANNING_SOURCES,"status_counts":counts,"verified_query_sources":[s["id"] for s in PLANNING_SOURCES if s["status"]=="VERIFIED"],"evidence_gaps":[s["id"] for s in PLANNING_SOURCES if s["status"] in {"PLANNED","DISCOVERY_COMPLETE","LIVE_ARCGIS_REST","IN_PROGRESS"}],"version":"MASTER-165"}

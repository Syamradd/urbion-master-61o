"""Radius-based technical-agency context for planning screening.

The engine accepts connected asset records when available and computes nearest
assets deterministically. It never invents infrastructure capacity or service
availability when an agency source has not supplied evidence.
"""
from __future__ import annotations
import math
from typing import Any

AGENCIES = {
    "JPS":{"name":"Jabatan Pengairan dan Saliran","topics":["river","drainage","flood","rainfall","water_level","MSMA"],"verification":"JPS/PBT technical review"},
    "JKR":{"name":"Jabatan Kerja Raya","topics":["road","access","traffic","road_hierarchy"],"verification":"JKR/PBT technical review"},
    "TNB":{"name":"Tenaga Nasional Berhad","topics":["electricity","power"],"verification":"TNB technical confirmation"},
    "IWK":{"name":"Indah Water Konsortium","topics":["sewerage","sewer"],"verification":"IWK technical confirmation"},
    "AIR_SELANGOR":{"name":"Air Selangor","topics":["water_supply","water"],"verification":"water-utility confirmation; operator depends on jurisdiction"},
    "SKMM":{"name":"Suruhanjaya Komunikasi dan Multimedia Malaysia","topics":["telecom","communications"],"verification":"SKMM/telecom technical review"},
}

def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r=6371000.0;p1=math.radians(lat1);p2=math.radians(lat2);dp=math.radians(lat2-lat1);dl=math.radians(lon2-lon1);a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2;return r*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

def classify_distance(distance_m: float, thresholds: tuple[int,...]=(400,800,1000,2000,5000)) -> str:
    for threshold in thresholds:
        if distance_m <= threshold: return f"WITHIN_{threshold}M"
    return "BEYOND_5000M"

def build_agency_intelligence(site_lat: float, site_lon: float, assets: dict[str,list[dict[str,Any]]] | None = None, radius_m: float = 5000) -> dict[str,Any]:
    assets=assets or {}; agencies=[]
    for code,meta in AGENCIES.items():
        candidates=[]
        for asset in assets.get(code,[]) or []:
            try: lat=float(asset["latitude"]);lon=float(asset["longitude"])
            except (KeyError,TypeError,ValueError): continue
            d=haversine_m(site_lat,site_lon,lat,lon)
            if d <= radius_m:
                candidates.append({**asset,"distance_m":round(d,1),"distance_class":classify_distance(d),"evidence":asset.get("evidence","SOURCE_CONTEXT")})
        candidates.sort(key=lambda x:x["distance_m"])
        agencies.append({"id":code,"name":meta["name"],"topics":meta["topics"],"nearest":candidates[:5],"asset_count_in_radius":len(candidates),"status":"ASSET_CONTEXT_AVAILABLE" if candidates else "REQUIRES_TECHNICAL_VERIFICATION","verification":meta["verification"]})
    return {"version":"MASTER-228","site":{"latitude":site_lat,"longitude":site_lon},"radius_m":radius_m,"agencies":agencies,"decision_boundary":"TECHNICAL_AGENCY_SCREENING_SUPPORT","statutory_verification":"NOT_CLAIMED","disclaimer":"Distance to an agency asset does not establish capacity, serviceability, reserve width, approval or compliance. Confirm current technical requirements with the responsible agency/PBT."}

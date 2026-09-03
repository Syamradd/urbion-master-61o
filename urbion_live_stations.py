"""Live nearest-station intelligence for LCP-oriented site screening.

JPS Public Infobanjir is queried from its public station pages. DOE/APIMS is
kept as an explicit adapter boundary: if an authorised/public JSON endpoint is
configured, URBION can consume it; otherwise it reports SOURCE_CONTEXT rather
than inventing an air-quality value.
"""
from __future__ import annotations

import math, os, re, urllib.parse, urllib.request
from datetime import datetime, timezone
from typing import Any

JPS_RAIN_URL = "https://publicinfobanjir.water.gov.my/hujan/data-hujan/"
JPS_STATION_URL = "https://publicinfobanjir.water.gov.my/cari-station/"
APIMS_URL = os.getenv("URBION_APIMS_URL", "").strip()

STATE_CODES = {"Melaka": "MLK", "Johor": "JHR", "Selangor": "SEL", "Perak": "PRK", "Pulau Pinang": "PNG", "Pahang": "PHG", "Negeri Sembilan": "NSN", "Kedah": "KDH", "Kelantan": "KTN", "Terengganu": "TRG", "Sabah": "SBH", "Sarawak": "SWK", "Perlis": "PLS", "Wilayah Persekutuan Kuala Lumpur": "WLH"}


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def _fetch(url: str, timeout: float = 12.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "URBION-HORIZON/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def _clean_number(value: Any) -> float | None:
    if value is None: return None
    match = re.search(r"-?\d+(?:\.\d+)?", str(value).replace(",", ""))
    return float(match.group(0)) if match else None


def _html_text(html: str) -> str:
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.I|re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.I|re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _station_info(state: str, station_id: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"lang":"en", "state":STATE_CODES.get(state, state), "station_id":station_id})
    text = _html_text(_fetch(f"{JPS_STATION_URL}?{query}"))
    def between(a: str, b: str | None = None) -> str | None:
        i = text.lower().find(a.lower())
        if i < 0: return None
        chunk = text[i+len(a):]
        if b:
            j = chunk.lower().find(b.lower())
            if j >= 0: chunk = chunk[:j]
        return chunk.strip(" :-")[:160]
    lat = _clean_number(between("Latitude"))
    lon = _clean_number(between("Longitude"))
    return {"station_id": station_id, "latitude": lat, "longitude": lon,
            "name": between("Station Name"), "district": between("District"),
            "status": between("Status"), "last_updated_rainfall": between("Last Updated (Rainfall)"),
            "last_updated_water": between("Last Updated (Water Level)")}


def _rainfall_rows(state: str, html: str) -> list[dict[str, Any]]:
    # The public table is intentionally parsed conservatively; station IDs are
    # retained even if a future page layout changes other columns.
    rows = []
    for match in re.finditer(r"<tr[^>]*>(.*?)</tr>", html, flags=re.I|re.S):
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", match.group(1), flags=re.I|re.S)]
        if len(cells) < 5: continue
        station_id = cells[1].strip()
        if not re.fullmatch(r"\d{5,10}", station_id): continue
        rows.append({"station_id": station_id, "name": cells[2], "district": cells[3], "last_updated": cells[4], "daily_rainfall_mm": _clean_number(cells[5]) if len(cells)>5 else None, "rainfall_midnight_mm": _clean_number(cells[6]) if len(cells)>6 else None, "rainfall_1h_mm": _clean_number(cells[7]) if len(cells)>7 else None})
    return rows


def nearest_jps_stations(site_lat: float, site_lon: float, state: str = "Melaka", limit: int = 5) -> dict[str, Any]:
    if not (math.isfinite(site_lat) and math.isfinite(site_lon)): raise ValueError("Coordinates must be finite")
    query = urllib.parse.urlencode({"lang":"en", "state":STATE_CODES.get(state, state)})
    html = _fetch(f"{JPS_RAIN_URL}?{query}")
    rows = _rainfall_rows(state, html)
    candidates = []
    for row in rows[:40]:
        try: info = _station_info(state, row["station_id"])
        except Exception: continue
        if info.get("latitude") is None or info.get("longitude") is None: continue
        item = {**row, **info}
        item["distance_m"] = round(haversine_m(site_lat, site_lon, info["latitude"], info["longitude"]), 1)
        item["evidence"] = "SOURCE_CONTEXT"
        candidates.append(item)
    candidates.sort(key=lambda x: x["distance_m"])
    return {"provider":"JPS Public Infobanjir", "status":"LIVE", "site":{"latitude":site_lat,"longitude":site_lon}, "stations":candidates[:max(1,min(limit,10))], "source":JPS_RAIN_URL, "evidence":"SOURCE_CONTEXT", "decision_boundary":"OBSERVATION_CONTEXT"}


def nearest_air_quality(site_lat: float, site_lon: float, limit: int = 5) -> dict[str, Any]:
    if not APIMS_URL:
        return {"provider":"DOE APIMS", "status":"SOURCE_CONTEXT", "configured":False, "stations":[], "message":"No public/authorised APIMS JSON endpoint configured; air-quality values are not fabricated.", "evidence":"SOURCE_CONTEXT", "decision_boundary":"OBSERVATION_CONTEXT"}
    try:
        payload = _fetch(APIMS_URL)
        import json
        data = json.loads(payload)
        records = data.get("stations", data if isinstance(data, list) else [])
        candidates=[]
        for item in records:
            lat=_clean_number(item.get("latitude")); lon=_clean_number(item.get("longitude"))
            if lat is None or lon is None: continue
            x=dict(item); x["distance_m"]=round(haversine_m(site_lat,site_lon,lat,lon),1); x["evidence"]="SOURCE_CONTEXT"; candidates.append(x)
        candidates.sort(key=lambda x:x["distance_m"])
        return {"provider":"DOE APIMS","status":"LIVE","stations":candidates[:max(1,min(limit,10))],"evidence":"SOURCE_CONTEXT","decision_boundary":"OBSERVATION_CONTEXT"}
    except Exception as exc:
        return {"provider":"DOE APIMS","status":"UNAVAILABLE","stations":[],"evidence":"SOURCE_CONTEXT","error_type":type(exc).__name__,"decision_boundary":"OBSERVATION_CONTEXT"}


def build_live_station_snapshot(site_lat: float, site_lon: float, state: str = "Melaka", limit: int = 5) -> dict[str, Any]:
    """Return a judge/LCP-ready snapshot; individual provider failure is isolated."""
    try: jps=nearest_jps_stations(site_lat,site_lon,state,limit)
    except Exception as exc: jps={"provider":"JPS Public Infobanjir","status":"UNAVAILABLE","stations":[],"evidence":"SOURCE_CONTEXT","error_type":type(exc).__name__}
    air=nearest_air_quality(site_lat,site_lon,limit)
    return {"version":"MASTER-184","site":{"latitude":site_lat,"longitude":site_lon,"state":state},"jps_rainfall":jps,"air_quality":air,"lcp_fields":["station_name","station_id","distance_m","reading","unit","timestamp","status","source","evidence"],"statutory_verification":"NOT_CLAIMED"}

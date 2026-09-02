"""Safe i-Plan (PLANMalaysia) spatial connector."""
from __future__ import annotations
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN"
STATE_CODES = {"Johor":"01","Kedah":"02","Kelantan":"03","Melaka":"04","Negeri Sembilan":"05","Pahang":"06","Pulau Pinang":"07","Perak":"08","Perlis":"09","Selangor":"10","Terengganu":"11","Sabah":"12","Sarawak":"13","Wilayah Persekutuan":"14","Labuan":"15","Putrajaya":"16"}


def _query_layer(service: str, lat: float, lon: float, timeout: float = 8.0) -> dict:
    params = urlencode({"geometry": f"{lon},{lat}", "geometryType":"esriGeometryPoint", "inSR":"4326", "spatialRel":"esriSpatialRelIntersects", "outFields":"*", "returnGeometry":"true", "outSR":"4326", "f":"json"})
    url = f"{BASE}/{service}/MapServer/0/query?{params}"
    req = Request(url, headers={"User-Agent":"URBION-HORIZON/1.0"})
    try:
        with urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return {"status":"QUERY_UNAVAILABLE","error":str(exc),"url":url}
    if payload.get("error"):
        return {"status":"QUERY_UNAVAILABLE","error":payload["error"],"url":url}
    features = payload.get("features") or []
    if not features:
        return {"status":"NO_FEATURE","url":url,"feature_count":0}
    feature = features[0]
    return {"status":"LIVE_QUERY","url":url,"feature_count":len(features),"attributes":feature.get("attributes") or {},"geometry":feature.get("geometry")}


def query_iplan_context(lat: float, lon: float, state: str = "Melaka") -> dict:
    code = STATE_CODES.get(state)
    if not code:
        return {"status":"UNSUPPORTED_STATE","state":state}
    current = _query_layer(f"GTsemasa_{code}",lat,lon)
    zoning = _query_layer(f"GTzoning_{code}",lat,lon)
    # i-Plan's public REST folder does not currently establish a GTkomited_<state>
    # MapServer endpoint. Keep committed land use explicit rather than inventing a
    # queryable service. The portal can still be used as the reference source.
    committed = {
        "status":"PORTAL_REFERENCE",
        "provider":"PLANMalaysia i-Plan",
        "message":"Committed land use is referenced through the i-Plan portal; no public ArcGIS MapServer endpoint is asserted here.",
        "reference":"https://iplan.planmalaysia.gov.my/"
    }
    lot = _query_layer(f"LOT_{code}",lat,lon)
    contour = _query_layer(f"KONTUR5M_{code}",lat,lon)
    return {
        "provider":"PLANMalaysia i-Plan","state":state,"latitude":lat,"longitude":lon,
        "current_land_use":current,"zoning":zoning,"committed_land_use":committed,
        "cadastral_lot":lot,"terrain_contour_5m":contour,
        "source_type":"PUBLIC_ARCGIS_REST","decision_use":"SOURCE_CONTEXT_ONLY",
        "disclaimer":"i-Plan source context; verify currency, plan status and statutory applicability before relying on it for a planning decision. A successful query is not itself statutory verification."
    }

"""Safe i-Plan / DPFDN spatial connectors for Melaka-first site intelligence.

The connector separates queryable public ArcGIS source context from statutory
verification. Environmental layers use a configurable radius so a site can be
screened against nearby flood, KSAS, slope and ecological constraints without
pretending that a map hit is a statutory determination.
"""
from __future__ import annotations
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from typing import Any

BASE = "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN"
DPFDN_BASE = "https://scharms.planmalaysia.gov.my/arcgis/rest/services/DPFDN"
GEOSERVER_WMS = "https://iplan.planmalaysia.gov.my/geoserver/iplan/wms"
STATE_CODES = {"Johor":"01","Kedah":"02","Kelantan":"03","Melaka":"04","Negeri Sembilan":"05","Pahang":"06","Pulau Pinang":"07","Perak":"08","Perlis":"09","Selangor":"10","Terengganu":"11","Sabah":"12","Sarawak":"13","Wilayah Persekutuan":"14","Labuan":"15","Putrajaya":"16"}

ENVIRONMENT_LAYERS = {
    "flood": ("DPFDN/Bencana", 2, "Banjir 100 tahun"),
    "slope": ("DPFDN/Bencana", 3, "Kecerunan"),
    "geohazard": ("DPFDN/Bencana", 1, "Tanah Runtuh"),
    "seismic": ("DPFDN/Bencana", 4, "Risiko Gempa Bumi"),
    "coastal_erosion": ("DPFDN/Bencana", 5, "Hakisan Pantai"),
    "fault": ("DPFDN/Bencana", 0, "Garis Sesar"),
    "ksas": ("DPFDN/AlamSekitar", 2, "Kawasan Sensitif Alam Sekitar"),
    "ecology": ("DPFDN/AlamSekitar", 0, "Central Forest Spine (CFS)"),
    "protected_area": ("DPFDN/AlamSekitar", 1, "Kawasan Perlindungan"),
    "river": ("DPFDN/AlamSekitar", 3, "Sungai"),
    "catchment": ("DPFDN/AlamSekitar", 4, "Kawasan Tadahan"),
}

def _request_json(url: str, timeout: float = 8.0) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent":"URBION-HORIZON/1.0"})
    try:
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return {"status":"QUERY_UNAVAILABLE","error_type":type(exc).__name__,"error":str(exc),"url":url}

def _query_layer(service: str, layer_id: int, lat: float, lon: float, radius_m: float = 0, timeout: float = 8.0) -> dict[str, Any]:
    params: dict[str, Any] = {"geometry":f"{lon},{lat}","geometryType":"esriGeometryPoint","inSR":"4326","spatialRel":"esriSpatialRelIntersects","outFields":"*","returnGeometry":"false","outSR":"4326","f":"json"}
    if radius_m > 0:
        params.update({"distance":str(radius_m),"units":"esriSRUnit_Meter"})
    url = f"{DPFDN_BASE if service.startswith('DPFDN/') else BASE}/{service.split('/',1)[1] if service.startswith('DPFDN/') else service}/MapServer/{layer_id}/query?{urlencode(params)}"
    payload = _request_json(url, timeout)
    if payload.get("status") == "QUERY_UNAVAILABLE": return payload
    if payload.get("error"): return {"status":"QUERY_UNAVAILABLE","error":payload["error"],"url":url}
    features = payload.get("features") or []
    return {"status":"LIVE_QUERY" if features else "NO_FEATURE","url":url,"feature_count":len(features),"features":[f.get("attributes") or {} for f in features],"radius_m":radius_m}

def query_environment_context(lat: float, lon: float, radius_m: float = 1000, state: str = "Melaka") -> dict[str, Any]:
    """Query authoritative PLANMalaysia environmental layers around a site.

    Results are SOURCE_CONTEXT only. Radius means the layer contains a feature
    intersecting the site's query buffer; it is not a legal setback or hazard
    threshold.
    """
    if state != "Melaka":
        # The national DPFDN layers are still queryable, but keep the explicit
        # state in the response so callers cannot mistake the scope.
        scope = "NATIONAL_LAYER_SCREENED_FOR_REQUESTED_STATE"
    else:
        scope = "MELAKA_FOCUSED"
    results: dict[str, Any] = {}
    for key, (service, layer_id, label) in ENVIRONMENT_LAYERS.items():
        result = _query_layer(service, layer_id, lat, lon, radius_m)
        result.update({"id":key,"name":label,"provider":"PLANMalaysia","evidence":"SOURCE_CONTEXT","decision_use":"SCREENING_ONLY"})
        results[key] = result
    return {"provider":"PLANMalaysia DPFDN","state":state,"scope":scope,"site":{"latitude":lat,"longitude":lon},"radius_m":radius_m,"layers":results,"decision_boundary":"ENVIRONMENTAL_SCREENING_SUPPORT","statutory_verification":"NOT_CLAIMED","disclaimer":"Spatial hits are source context within the configured query radius. Confirm authoritative currency, plan status, technical thresholds and agency requirements before planning reliance."}

def query_iplan_context(lat: float, lon: float, state: str = "Melaka", environment_radius_m: float = 1000) -> dict[str, Any]:
    code = STATE_CODES.get(state)
    if not code: return {"status":"UNSUPPORTED_STATE","state":state}
    current = _query_layer(f"GTsemasa_{code}", 0, lat, lon)
    zoning = _query_layer(f"GTzoning_{code}", 0, lat, lon)
    lot = _query_layer(f"LOT_{code}", 0, lat, lon)
    contour = _query_layer(f"KONTUR5M_{code}", 0, lat, lon)
    committed = {"status":"LIVE_WMS","provider":"PLANMalaysia i-Plan","url":GEOSERVER_WMS,"layers":f"iplan:gunatanah_komited_{code}","message":"Official i-Plan GeoServer WMS committed-land-use layer is available for map visualisation. Attribute-level filtering/querying may require the portal's authorised GeoServer workflow.","decision_use":"SOURCE_CONTEXT_ONLY"}
    environment = query_environment_context(lat, lon, environment_radius_m, state)
    return {"provider":"PLANMalaysia i-Plan","state":state,"latitude":lat,"longitude":lon,"current_land_use":current,"zoning":zoning,"committed_land_use":committed,"cadastral_lot":lot,"terrain_contour_5m":contour,"environment":environment,"source_type":"PUBLIC_ARCGIS_REST + OFFICIAL_GEOSERVER_WMS","decision_use":"SOURCE_CONTEXT_ONLY","disclaimer":"i-Plan/DPFDN source context; verify currency, plan status and statutory applicability before relying on it for a planning decision. A successful query is not itself statutory verification."}

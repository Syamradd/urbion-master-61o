"""Live public GIS context bridge for URBION HORIZON.

This module deliberately separates:
- rendered map context,
- calculated spatial relationships, and
- decision-safe statutory evidence.

Only public services with an explicit query contract are queried. A failed or
unavailable source is disclosed as a gap; it is never converted into a
positive planning conclusion.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import math
from typing import Any

import httpx

from urbion_data_sources import map_layer_catalog

EARTH_RADIUS_M = 6_371_000.0
DEFAULT_RADIUS_M = 800
MAX_RADIUS_M = 5000
MAX_FEATURES_PER_LAYER = 60
TIMEOUT_S = 8.0

# Public services with queryable geometry. The map catalogue remains the source
# of display metadata; this table adds only the geometry-query contract.
QUERY_SPECS = {
    "iplan-current": {"kind": "WFS", "type_name": "iplan:gunatanah_semasa_{code}"},
    "iplan-zoning": {"kind": "WFS", "type_name": "iplan:gunatanah_zoning_{code}"},
    "iplan-committed": {"kind": "WFS", "type_name": "iplan:gunatanah_komited_{code}"},
    "iplan-flood": {"kind": "WFS", "type_name": "iplan:banjir"},
    "iplan-disaster-risk": {"kind": "WFS", "type_name": "iplan:risiko_bencana"},
    "iplan-ksas": {"kind": "WFS", "type_name": "iplan:ksas"},
    "iplan-cfs": {"kind": "WFS", "type_name": "iplan:cfs"},
    "iplan-ecology": {"kind": "WFS", "type_name": "iplan:rangkaian_ekologi"},
    "iplan-heritage": {"kind": "WFS", "type_name": "iplan:warisan"},
    "iplan-affordable-housing": {"kind": "WFS", "type_name": "iplan:rumah_mampu_milik"},
    "iplan-rfn": {"kind": "WFS", "type_name": "iplan:rfn"},
    "iplan-topography": {"kind": "WFS", "type_name": "iplan:topo"},
    "mygems-faults": {"kind": "ARCGIS", "layer": 5},
    "mygems-quarries": {"kind": "ARCGIS", "layer": 0},
    "mygems-groundwater": {"kind": "ARCGIS", "layer": 0},
    "mygems-geowarisan": {"kind": "ARCGIS", "layer": 1},
    "mygems-lithology": {"kind": "ARCGIS", "layer": 22},
}

ARCGIS_BASE = {
    "mygems-faults": "https://mygems.jmg.gov.my/server/rest/services/GeologiAsas/Major_Fault/MapServer",
    "mygems-quarries": "https://mygems.jmg.gov.my/server/rest/services/LombongKuari/Lombong_Kuari_Awam/MapServer",
    "mygems-groundwater": "https://mygems.jmg.gov.my/server/rest/services/Air_Bawah_Tanah/Air_Bawah_Tanah_Awam/MapServer",
    "mygems-geowarisan": "https://mygems.jmg.gov.my/server/rest/services/GeoWarisan/Geowarisan_Awam/MapServer",
    "mygems-lithology": "https://mygems.jmg.gov.my/server/rest/services/Demarcation/Litology_by_Negeri/MapServer",
}

DEFAULT_LAYERS = tuple(QUERY_SPECS.keys())


def _coords(lat: Any, lon: Any) -> tuple[float, float]:
    lat, lon = float(lat), float(lon)
    if not math.isfinite(lat) or not math.isfinite(lon) or not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("coordinates are outside valid geographic ranges")
    if (lat, lon) == (-90.0, -180.0):
        raise ValueError("placeholder coordinates are not allowed")
    return lat, lon


def _radius(value: Any) -> float:
    value = float(value or DEFAULT_RADIUS_M)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("radius_m must be positive")
    return min(value, MAX_RADIUS_M)


def _haversine(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    p = math.pi / 180.0
    p1, p2 = a_lat * p, b_lat * p
    dp, dl = (b_lat - a_lat) * p, (b_lon - a_lon) * p
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return EARTH_RADIUS_M * 2 * math.atan2(math.sqrt(h), math.sqrt(max(0.0, 1.0 - h)))


def _project(lat: float, lon: float, origin_lat: float, origin_lon: float) -> tuple[float, float]:
    scale = math.pi / 180.0
    return ((lon - origin_lon) * scale * EARTH_RADIUS_M * math.cos(math.radians(origin_lat)),
            (lat - origin_lat) * scale * EARTH_RADIUS_M)


def _point_segment_distance(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> float:
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _point_in_ring(point: tuple[float, float], ring: list[list[float]]) -> bool:
    x, y = point
    inside = False
    if len(ring) < 3:
        return False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        crosses = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-15) + xi)
        if crosses:
            inside = not inside
        j = i
    return inside


def _geometry_relationship(geometry: dict | None, lat: float, lon: float) -> dict:
    if not geometry:
        return {"inside": False, "distance_m": None}
    kind = geometry.get("type")
    coordinates = geometry.get("coordinates")
    if kind == "Point" and isinstance(coordinates, list) and len(coordinates) >= 2:
        return {"inside": False, "distance_m": round(_haversine(lat, lon, float(coordinates[1]), float(coordinates[0])), 2)}

    point = _project(lat, lon, lat, lon)
    min_distance = None
    inside = False

    def line_distance(line: list[list[float]]) -> float | None:
        if len(line) < 2:
            return None
        pts = [_project(float(y), float(x), lat, lon) for x, y, *_ in line if len([x, y]) >= 2]
        if len(pts) < 2:
            return None
        return min(_point_segment_distance(point[0], point[1], a[0], a[1], b[0], b[1]) for a, b in zip(pts, pts[1:]))

    if kind == "LineString" and isinstance(coordinates, list):
        min_distance = line_distance(coordinates)
    elif kind == "MultiLineString" and isinstance(coordinates, list):
        values = [line_distance(line) for line in coordinates]
        min_distance = min((x for x in values if x is not None), default=None)
    elif kind == "Polygon" and isinstance(coordinates, list):
        for ring in coordinates:
            if isinstance(ring, list) and _point_in_ring([lon, lat], ring):
                inside = True
            d = line_distance(ring)
            if d is not None:
                min_distance = d if min_distance is None else min(min_distance, d)
    elif kind == "MultiPolygon" and isinstance(coordinates, list):
        for polygon in coordinates:
            for ring in polygon:
                if isinstance(ring, list) and _point_in_ring([lon, lat], ring):
                    inside = True
                d = line_distance(ring)
                if d is not None:
                    min_distance = d if min_distance is None else min(min_distance, d)
    return {"inside": inside, "distance_m": round(float(min_distance), 2) if min_distance is not None else None}


def _feature_summary(feature: dict, relationship: dict) -> dict:
    props = feature.get("properties") or {}
    # Keep useful source attributes but avoid flooding the decision UI with huge records.
    selected = {}
    for key, value in props.items():
        if value in (None, ""):
            continue
        if isinstance(value, (str, int, float, bool)):
            selected[str(key)] = value
        if len(selected) >= 14:
            break
    return {"properties": selected, **relationship}


def _normalise_geojson(payload: dict) -> dict:
    if payload.get("type") == "FeatureCollection":
        return payload
    if payload.get("type") == "Feature":
        return {"type": "FeatureCollection", "features": [payload]}
    # ArcGIS JSON fallback: convert simple feature arrays.
    features = []
    for item in payload.get("features") or []:
        geometry = item.get("geometry") or {}
        gtype = geometry.get("type")
        coords = geometry.get("coordinates")
        if gtype and isinstance(coords, (list, tuple)):
            features.append({"type": "Feature", "properties": item.get("attributes") or {}, "geometry": {"type": gtype, "coordinates": coords}})
    return {"type": "FeatureCollection", "features": features}


def _http_json(url: str, params: dict) -> dict:
    with httpx.Client(timeout=TIMEOUT_S, follow_redirects=True, headers={"User-Agent": "URBION-HORIZON/MASTER-330"}) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        return response.json()


def _query_wfs(layer_id: str, type_name: str, lat: float, lon: float, radius_m: float) -> dict:
    dlat = radius_m / 111_320.0
    dlon = radius_m / max(1.0, 111_320.0 * math.cos(math.radians(lat)))
    params = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": type_name,
        "outputFormat": "application/json",
        "srsName": "EPSG:4326",
        "bbox": f"{lon-dlon},{lat-dlat},{lon+dlon},{lat+dlat},EPSG:4326",
        "maxFeatures": MAX_FEATURES_PER_LAYER,
    }
    return _normalise_geojson(_http_json("https://iplan.planmalaysia.gov.my/geoserver/iplan/ows", params))


def _query_arcgis(layer_id: str, layer_number: int, lat: float, lon: float, radius_m: float) -> dict:
    base = ARCGIS_BASE[layer_id].rstrip("/") + f"/{layer_number}/query"
    params = {
        "where": "1=1",
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "distance": radius_m,
        "units": "esriSRUnit_Meter",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "resultRecordCount": MAX_FEATURES_PER_LAYER,
        "f": "geojson",
    }
    return _normalise_geojson(_http_json(base, params))


def _catalog_by_id(state: str) -> dict[str, dict]:
    return {item["id"]: item for item in map_layer_catalog(state)}


def _run_one(layer_id: str, catalog: dict[str, dict], lat: float, lon: float, radius_m: float, state: str) -> dict:
    meta = catalog.get(layer_id, {"id": layer_id, "name": layer_id, "group": "UNKNOWN", "evidence": "SOURCE_CONTEXT"})
    spec = QUERY_SPECS[layer_id]
    try:
        if spec["kind"] == "WFS":
            code = {"Melaka": "04", "Johor": "01", "Kedah": "02", "Kelantan": "03", "Negeri Sembilan": "05", "Pahang": "06", "Pulau Pinang": "07", "Perak": "08", "Perlis": "09", "Selangor": "10", "Terengganu": "11", "Sabah": "12", "Sarawak": "13", "Wilayah Persekutuan": "14", "Labuan": "15", "Putrajaya": "16"}.get(state)
            if "{code}" in spec["type_name"] and not code:
                return {"id": layer_id, "name": meta.get("name", layer_id), "group": meta.get("group"), "status": "NOT_CONFIGURED", "feature_count": 0, "features": [], "source": meta.get("source", "iplan"), "evidence": "EVIDENCE_GAP"}
            data = _query_wfs(layer_id, spec["type_name"].format(code=code or ""), lat, lon, radius_m)
        else:
            data = _query_arcgis(layer_id, spec["layer"], lat, lon, radius_m)
        features = list(data.get("features") or [])[:MAX_FEATURES_PER_LAYER]
        relationships = [_feature_summary(feature, _geometry_relationship(feature.get("geometry"), lat, lon)) for feature in features]
        inside = sum(1 for item in relationships if item["inside"])
        distances = [item["distance_m"] for item in relationships if item["distance_m"] is not None]
        nearest = min(distances) if distances else None
        return {
            "id": layer_id,
            "name": meta.get("name", layer_id),
            "name_ms": meta.get("name_ms", meta.get("name", layer_id)),
            "group": meta.get("group", "UNKNOWN"),
            "status": "LIVE_QUERY" if features else "NO_FEATURE",
            "feature_count": len(features),
            "inside_count": inside,
            "nearest_distance_m": nearest,
            "nearest_feature": min((x for x in relationships if x["distance_m"] is not None), key=lambda x: x["distance_m"], default=None),
            "features": features,
            "source": meta.get("source", "iplan" if spec["kind"] == "WFS" else "jmg-mygems"),
            "evidence": "SOURCE_CONTEXT",
            "decision_safe": False,
            "query_kind": spec["kind"],
        }
    except Exception as exc:  # source outages must become explicit gaps, not crashes
        return {
            "id": layer_id,
            "name": meta.get("name", layer_id),
            "name_ms": meta.get("name_ms", meta.get("name", layer_id)),
            "group": meta.get("group", "UNKNOWN"),
            "status": "QUERY_ERROR",
            "feature_count": 0,
            "inside_count": 0,
            "nearest_distance_m": None,
            "nearest_feature": None,
            "features": [],
            "source": meta.get("source", "iplan" if spec["kind"] == "WFS" else "jmg-mygems"),
            "evidence": "EVIDENCE_GAP",
            "decision_safe": False,
            "query_kind": spec["kind"],
            "error": str(exc)[:240],
        }


@lru_cache(maxsize=64)
def _cached_context(lat: float, lon: float, radius_m: float, state: str, layer_key: tuple[str, ...]) -> dict:
    catalog = _catalog_by_id(state)
    results = []
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(layer_key)))) as pool:
        futures = {pool.submit(_run_one, layer_id, catalog, lat, lon, radius_m, state): layer_id for layer_id in layer_key}
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda x: (x.get("group", ""), x.get("name", "")))
    signals = []
    for item in results:
        if item["status"] == "LIVE_QUERY":
            signals.append({"id": item["id"], "label": item["name"], "group": item["group"], "status": "SOURCE_CONTEXT_HIT", "features": item["feature_count"], "inside": item["inside_count"], "nearest_distance_m": item["nearest_distance_m"], "decision_use": "SPATIAL_SCREENING"})
        elif item["status"] == "NO_FEATURE":
            signals.append({"id": item["id"], "label": item["name"], "group": item["group"], "status": "SOURCE_CONTEXT_NO_FEATURE", "features": 0, "inside": 0, "nearest_distance_m": None, "decision_use": "SPATIAL_SCREENING"})
        else:
            signals.append({"id": item["id"], "label": item["name"], "group": item["group"], "status": "EVIDENCE_GAP", "features": 0, "inside": 0, "nearest_distance_m": None, "decision_use": "REVIEW_PRIORITY"})
    return {
        "site": {"latitude": lat, "longitude": lon},
        "radius_m": radius_m,
        "state": state,
        "layers": results,
        "signals": signals,
        "query": {"parallel": True, "layer_count": len(layer_key), "max_features_per_layer": MAX_FEATURES_PER_LAYER},
        "evidence": "SOURCE_CONTEXT",
        "decision_safe": False,
        "disclaimer": "Live public GIS context for spatial screening. It is not statutory confirmation, cadastral certification or planning approval.",
    }


def build_site_context(lat: Any, lon: Any, radius_m: Any = DEFAULT_RADIUS_M, state: str = "Melaka", layer_ids: list[str] | tuple[str, ...] | None = None) -> dict:
    lat, lon = _coords(lat, lon)
    radius = _radius(radius_m)
    requested = tuple(layer_ids or DEFAULT_LAYERS)
    valid = tuple(x for x in requested if x in QUERY_SPECS)
    if not valid:
        valid = DEFAULT_LAYERS
    return _cached_context(round(lat, 6), round(lon, 6), float(radius), state or "Melaka", valid)


def clear_spatial_context_cache() -> None:
    _cached_context.cache_clear()

"""URBION national geospatial source registry.

The registry separates live/public map services from user-facing portals and
sources that require credentials or formal data access. No source is promoted
to statutory evidence merely because it is reachable.
"""
from __future__ import annotations

SOURCE_CATALOG = [
    {"id":"iplan","name":"PLANMalaysia i-Plan","agency":"PLANMalaysia","category":"PLANNING","status":"LIVE_ARCGIS_REST","role":"Current land use, zoning, cadastral context and selected spatial analysis layers","url":"https://iplan.planmalaysia.gov.my/"},
    {"id":"jupem-mylot","name":"JUPEM MyLot","agency":"JUPEM","category":"CADASTRAL","status":"PUBLIC_PORTAL","role":"Online location and boundary reference for surveyed land lots","url":"https://jupem2u.kul.jupem.gov.my/mylot/index.html"},
    {"id":"jmg-mygems","name":"JMG MyGEMS","agency":"Jabatan Mineral dan Geosains Malaysia","category":"GEOLOGY","status":"LIVE_ARCGIS_REST","role":"Geology, geohazard, mineral, groundwater and related geoscience layers","url":"https://mygems.jmg.gov.my/"},
    {"id":"doe-myeqms","name":"JAS MyEQMS / EQMP","agency":"Jabatan Alam Sekitar","category":"ENVIRONMENT","status":"PUBLIC_DATA_PORTAL","role":"Air, river-water and marine-water environmental monitoring context","url":"https://www.doe.gov.my/en/environmental-quality-monitoring/"},
]

IPLANS = {
    "Melaka": "04", "Johor": "01", "Kedah": "02", "Kelantan": "03",
    "Negeri Sembilan": "05", "Pahang": "06", "Pulau Pinang": "07",
    "Perak": "08", "Perlis": "09", "Selangor": "10", "Terengganu": "11",
    "Sabah": "12", "Sarawak": "13", "Wilayah Persekutuan": "14",
    "Labuan": "15", "Putrajaya": "16",
}

def source_catalog() -> list[dict]:
    return [dict(x) for x in SOURCE_CATALOG]

def map_layer_catalog(state: str = "Melaka") -> list[dict]:
    code = IPLANS.get(state)
    layers = [
        {"id":"osm","name":"OpenStreetMap","group":"BASEMAP","type":"TILE","url":"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png","attribution":"© OpenStreetMap contributors","evidence":"BASEMAP"},
        {"id":"iplan-current","name":"i-Plan · Guna Tanah Semasa","group":"PLANNING","type":"ARCGIS_QUERY","service":f"GTsemasa_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-zoning","name":"i-Plan · Guna Tanah Zoning","group":"PLANNING","type":"ARCGIS_QUERY","service":f"GTzoning_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-lot","name":"i-Plan · Lot Kadaster","group":"CADASTRAL","type":"ARCGIS_QUERY","service":f"LOT_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-contour","name":"i-Plan · Kontur 5m","group":"TERRAIN","type":"ARCGIS_QUERY","service":f"KONTUR5M_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-faults","name":"MyGEMS · Major Faults","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/GeologiAsas/Major_Fault/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-quarries","name":"MyGEMS · Mines & Quarries","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/LombongKuari/Lombong_Kuari_Awam/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-groundwater","name":"MyGEMS · Groundwater","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/Air_Bawah_Tanah/Air_Bawah_Tanah_Awam/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-geowarisan","name":"MyGEMS · Geowarisan / Geopark","group":"GEOHERITAGE","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/GeoWarisan/Geowarisan_Awam/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"myeqms","name":"MyEQMS / EQMP monitoring","group":"ENVIRONMENT","type":"PORTAL_REFERENCE","url":"https://www.doe.gov.my/en/environmental-quality-monitoring/","source":"doe-myeqms","evidence":"SOURCE_CONTEXT"},
        {"id":"mylot","name":"JUPEM MyLot","group":"CADASTRAL","type":"PORTAL_REFERENCE","url":"https://jupem2u.kul.jupem.gov.my/mylot/index.html","source":"jupem-mylot","evidence":"SOURCE_CONTEXT"},
    ]
    return layers

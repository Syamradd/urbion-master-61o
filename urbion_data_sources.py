"""URBION national geospatial and planning source registry.

Live/public map services are separated from portals and reference-only sources.
No reachable source is promoted to statutory evidence merely because it responds.
"""
from __future__ import annotations

SOURCE_CATALOG = [
    {"id":"iplan","name":"PLANMalaysia i-Plan","agency":"PLANMalaysia","category":"PLANNING","status":"LIVE_ARCGIS_REST + LIVE_WMS","role":"Current land use, zoning, committed land use, cadastral context and planning layers","url":"https://iplan.planmalaysia.gov.my/","acquisition":"Public geoportal; public ArcGIS REST layers and official GeoServer WMS are available; data request module is also available."},
    {"id":"myplan","name":"PLANMalaysia MyPLAN","agency":"PLANMalaysia","category":"PLANNING_DOCUMENTS","status":"PUBLIC_PORTAL","role":"National development-plan documents, GIS manuals and planning publications","url":"https://myplan.planmalaysia.gov.my/","acquisition":"Public document platform; supports document search and PDF access."},
    {"id":"jpbdm-geospatial","name":"PLANMalaysia Melaka · Geospatial Melaka","agency":"PLANMalaysia Melaka","category":"PLANNING_GIS","status":"PUBLIC_PORTAL","role":"State planning GIS/data portal and non-classified planning information request workflow","url":"https://www.jpbdmelaka.gov.my/maklumat-gunatanah-negeri","acquisition":"Public portal; detailed AOI data may require the department's user/application workflow."},
    {"id":"osc3plus","name":"OSC 3.0 Plus Online","agency":"KPKT","category":"DEVELOPMENT_CONTROL","status":"PUBLIC_WORKFLOW","role":"Planning-permission/OSC submission, technical review and application-status workflow context","url":"https://osc3plus.kpkt.gov.my/","acquisition":"Public workflow portal; user authentication and PBT-specific submission access apply."},
    {"id":"jupem-mylot","name":"JUPEM MyLot","agency":"JUPEM","category":"CADASTRAL","status":"PUBLIC_PORTAL","role":"Online location and boundary reference for surveyed land lots","url":"https://jupem2u.kul.jupem.gov.my/mylot/index.html","acquisition":"Public portal for lot-location and boundary reference."},
    {"id":"jmg-mygems","name":"JMG MyGEMS","agency":"Jabatan Mineral dan Geosains Malaysia","category":"GEOLOGY","status":"LIVE_ARCGIS_REST","role":"Geology, geohazard, mineral, groundwater and related geoscience layers","url":"https://mygems.jmg.gov.my/","acquisition":"Public geospatial portal and ArcGIS map services."},
    {"id":"jps-public-infobanjir","name":"JPS Public Infobanjir","agency":"Jabatan Pengairan dan Saliran Malaysia","category":"HYDROLOGY","status":"PUBLIC_REAL_TIME_PORTAL","role":"Real-time rainfall, water-level, flood warning and hydrological station context","url":"https://publicinfobanjir.water.gov.my/","acquisition":"Public portal with station status and real-time hydrology context; use official service/data route for detailed integration."},
    {"id":"doe-myeqms","name":"JAS MyEQMS / EQMP","agency":"Jabatan Alam Sekitar","category":"ENVIRONMENT","status":"PUBLIC_DATA_PORTAL","role":"Air, river-water and marine-water environmental monitoring context","url":"https://www.doe.gov.my/en/environmental-quality-monitoring/","acquisition":"Public environmental monitoring portal; use official data-access route for detailed datasets."},
    {"id":"elysian-legacy-gis","name":"Elysian GIS Legacy Reference","agency":"URBION project reference","category":"PROJECT_REFERENCE","status":"REFERENCE_REGISTERED","role":"Historical parcel/site context for cross-source reconciliation; not authoritative by itself","url":None,"acquisition":"Project reference dataset; reconcile against official i-Plan, JUPEM and PBT evidence before decision use."},
]

IPLANS = {
    "Melaka":"04","Johor":"01","Kedah":"02","Kelantan":"03","Negeri Sembilan":"05","Pahang":"06",
    "Pulau Pinang":"07","Perak":"08","Perlis":"09","Selangor":"10","Terengganu":"11","Sabah":"12",
    "Sarawak":"13","Wilayah Persekutuan":"14","Labuan":"15","Putrajaya":"16",
}


def source_catalog() -> list[dict]:
    return [dict(x) for x in SOURCE_CATALOG]


def map_layer_catalog(state: str = "Melaka") -> list[dict]:
    code = IPLANS.get(state)
    layers = [
        {"id":"osm","name":"OpenStreetMap","name_ms":"OpenStreetMap","group":"BASEMAP","type":"TILE","url":"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png","evidence":"BASEMAP"},
        {"id":"iplan-current","name":"i-Plan · Current Land Use","name_ms":"i-Plan · Guna Tanah Semasa","group":"PLANNING","type":"ARCGIS_QUERY","service":f"GTsemasa_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-zoning","name":"i-Plan · Zoning","name_ms":"i-Plan · Guna Tanah Zoning","group":"PLANNING","type":"ARCGIS_QUERY","service":f"GTzoning_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-committed","name":"i-Plan · Committed Land Use","name_ms":"i-Plan · Guna Tanah Komited","group":"PLANNING","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":f"iplan:gunatanah_komited_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT","access_note":"Official i-Plan GeoServer WMS layer. Visualisation is live source context; statutory currency/applicability must still be verified against authoritative plans."},
        {"id":"iplan-lot","name":"i-Plan · Cadastral Lot","name_ms":"i-Plan · Lot Kadaster","group":"CADASTRAL","type":"ARCGIS_QUERY","service":f"LOT_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-contour","name":"i-Plan · 5m Contours","name_ms":"i-Plan · Kontur 5m","group":"TERRAIN","type":"ARCGIS_QUERY","service":f"KONTUR5M_{code}" if code else None,"source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-flood","name":"i-Plan · Flood","name_ms":"i-Plan · Banjir","group":"HAZARD","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:banjir","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-disaster-risk","name":"i-Plan · Disaster Risk","name_ms":"i-Plan · Risiko Bencana","group":"HAZARD","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:risiko_bencana","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-ksas","name":"i-Plan · KSAS","name_ms":"i-Plan · Kawasan Sensitif Alam Sekitar","group":"ENVIRONMENT","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:ksas","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-cfs","name":"i-Plan · CFS","name_ms":"i-Plan · Central Forest Spine","group":"ECOLOGY","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:cfs","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-ecology","name":"i-Plan · Ecological Network","name_ms":"i-Plan · Rangkaian Ekologi","group":"ECOLOGY","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:rangkaian_ekologi","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-heritage","name":"i-Plan · Heritage","name_ms":"i-Plan · Warisan","group":"HERITAGE","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:warisan","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-affordable-housing","name":"i-Plan · Affordable Housing","name_ms":"i-Plan · Rumah Mampu Milik","group":"HOUSING","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:rumah_mampu_milik","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-rfn","name":"i-Plan · RFN","name_ms":"i-Plan · RFN","group":"PLANNING","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:rfn","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"iplan-topography","name":"i-Plan · Topography","name_ms":"i-Plan · Topografi","group":"TERRAIN","type":"GEOSERVER_WMS","url":"https://iplan.planmalaysia.gov.my/geoserver/iplan/wms","layers":"iplan:topo","source":"iplan","evidence":"SOURCE_CONTEXT"},
        {"id":"jps-infobanjir","name":"JPS · Public Infobanjir","name_ms":"JPS · Public Infobanjir","group":"HYDROLOGY","type":"PORTAL_REFERENCE","url":"https://publicinfobanjir.water.gov.my/","source":"jps-public-infobanjir","evidence":"SOURCE_CONTEXT","access_note":"Official real-time hydrology portal. Detailed API/service integration must follow the published/authorised access route."},
        {"id":"mygems-faults","name":"MyGEMS · Major Faults","name_ms":"MyGEMS · Sesar Utama","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/GeologiAsas/Major_Fault/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-quarries","name":"MyGEMS · Mines & Quarries","name_ms":"MyGEMS · Lombong & Kuari","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/LombongKuari/Lombong_Kuari_Awam/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-groundwater","name":"MyGEMS · Groundwater","name_ms":"MyGEMS · Air Bawah Tanah","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/Air_Bawah_Tanah/Air_Bawah_Tanah_Awam/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-geowarisan","name":"MyGEMS · Geoheritage / Geopark","name_ms":"MyGEMS · Geowarisan / Geopark","group":"GEOHERITAGE","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/GeoWarisan/Geowarisan_Awam/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-lithology","name":"MyGEMS · Lithology","name_ms":"MyGEMS · Litologi","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/Demarcation/Litology_by_Negeri/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-seismic","name":"MyGEMS · Seismic","name_ms":"MyGEMS · Seismik","group":"GEOHAZARD","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/MyGemsData/Seismik_A_MRSO/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"mygems-mineral","name":"MyGEMS · Mineral Resources","name_ms":"MyGEMS · Sumber Mineral","group":"GEOLOGY","type":"ARCGIS_MAP","url":"https://mygems.jmg.gov.my/server/rest/services/SumberMineral/Sumber_Mineral_Awam/MapServer","source":"jmg-mygems","evidence":"SOURCE_CONTEXT"},
        {"id":"myeqms","name":"MyEQMS / EQMP Monitoring","name_ms":"MyEQMS / EQMP · Pemantauan Alam Sekitar","group":"ENVIRONMENT","type":"PORTAL_REFERENCE","url":"https://www.doe.gov.my/en/environmental-quality-monitoring/","source":"doe-myeqms","evidence":"SOURCE_CONTEXT"},
        {"id":"mylot","name":"JUPEM MyLot","name_ms":"JUPEM MyLot","group":"CADASTRAL","type":"PORTAL_REFERENCE","url":"https://jupem2u.kul.jupem.gov.my/mylot/index.html","source":"jupem-mylot","evidence":"SOURCE_CONTEXT"},
    ]
    return layers

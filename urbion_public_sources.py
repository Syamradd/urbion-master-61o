/* MASTER-281: public-source bridge configuration and endpoints. */
from fastapi import Body, HTTPException
from urllib.parse import quote
from urllib.request import Request, urlopen
import json

PUBLIC_SOURCE_SERVICES = {
    "iplan_current_land_use": "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer",
    "iplan_zoning": "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTzoning_04/MapServer",
    "iplan_cadastral": "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/LOT_04/MapServer",
    "iplan_contour_5m": "https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/KONTUR5M_04/MapServer",
    "jmg_major_fault": "https://mygems.jmg.gov.my/server/rest/services/GeologiAsas/Major_Fault/MapServer",
    "jmg_lithology": "https://mygems.jmg.gov.my/server/rest/services/Demarcation/Litology_by_Negeri/MapServer",
    "jmg_geophysics": "https://mygems.jmg.gov.my/server/rest/services/GeoFizik/Geofizik_Awam/MapServer",
    "jmg_groundwater": "https://mygems.jmg.gov.my/server/rest/services/Air_Bawah_Tanah/Air_Bawah_Tanah_Awam/MapServer",
    "jmg_minerals": "https://mygems.jmg.gov.my/server/rest/services/SumberMineral/Sumber_Mineral_Awam/MapServer",
}

def _public_json(url: str, timeout: float = 8.0):
    req = Request(url, headers={"User-Agent":"URBION-HORIZON/MASTER-281 public-source evidence"})
    with urlopen(req, timeout=timeout) as r:
        raw=r.read().decode("utf-8",errors="replace")
    return json.loads(raw)

def install_public_source_bridge(app):
    @app.get("/public-sources/map-services")
    def public_map_services():
        result={}
        for name,url in PUBLIC_SOURCE_SERVICES.items():
            try:
                meta=_public_json(url+"?f=pjson",5)
                result[name]={"url":url,"status":"RESPONDED","name":meta.get("mapName") or meta.get("name") or name,"spatialReference":meta.get("spatialReference")}
            except Exception as exc:
                result[name]={"url":url,"status":"UNREACHABLE","error":str(exc)}
        return {"services":result,"statutory_verification":"NOT_CLAIMED"}

    @app.get("/public-sources/mygems")
    def public_mygems(lat:float=2.285,lon:float=102.196):
        layers={}
        for name in ["jmg_major_fault","jmg_lithology","jmg_geophysics","jmg_groundwater","jmg_minerals"]:
            url=PUBLIC_SOURCE_SERVICES[name]
            try:
                meta=_public_json(url+"?f=pjson",5);layers[name]={"status":"RESPONDED","service":meta.get("mapName") or meta.get("name"),"url":url,"site":{"lat":lat,"lon":lon}}
            except Exception as exc: layers[name]={"status":"UNREACHABLE","url":url,"error":str(exc)}
        return {"source":"JMG MyGEMS public ArcGIS services","site":{"lat":lat,"lon":lon},"layers":layers,"decision_boundary":"OBSERVATION_CONTEXT","statutory_verification":"NOT_CLAIMED"}

    @app.get("/public-sources/infobanjir")
    def public_infobanjir(state:str="Melaka"):
        # Public Infobanjir is a live public web service; retain the authoritative page
        # as the source while exposing a structured reachability record in URBION.
        url="https://publicinfobanjir.water.gov.my/aras-air/?lang=en&state="+quote(state)
        try:
            text=Request(url,headers={"User-Agent":"URBION-HORIZON/MASTER-281"})
            with urlopen(text,timeout=8) as r: body=r.read().decode("utf-8",errors="replace")
            return {"source":"JPS Public Infobanjir","state":state,"status":"RESPONDED","bytes":len(body),"url":url,"note":"Authoritative portal response reached; values remain source-owned."}
        except Exception as exc:
            return {"source":"JPS Public Infobanjir","state":state,"status":"UNREACHABLE","url":url,"error":str(exc)}

    @app.get("/public-sources/mygdi")
    def public_mygdi():
        return {"source":"MyGeoportal / MyGDI","status":"REFERENCE","url":"https://www.mygeoportal.gov.my/","note":"National geospatial sharing portal; direct dataset availability is service-dependent."}

    @app.post("/public-sources/site-evidence")
    def public_site_evidence(payload:dict=Body(default_factory=dict)):
        lat=payload.get("site_lat",2.285);lon=payload.get("site_lon",102.196);state=payload.get("state","Melaka")
        if lat is None or lon is None: raise HTTPException(status_code=422,detail={"code":"SITE_COORDINATES_REQUIRED"})
        sources={}
        try: sources["iPLAN"]={"status":"RESPONDED","context":query_environment_context(float(lat),float(lon),1000,state)}
        except Exception as exc: sources["iPLAN"]={"status":"FAILED","error":str(exc)}
        try: sources["MyGEMS"]={"status":"RESPONDED","layers":public_mygems(float(lat),float(lon))["layers"]}
        except Exception as exc: sources["MyGEMS"]={"status":"FAILED","error":str(exc)}
        try: sources["JPS"]={"status":"RESPONDED","environment":build_environment_intelligence(query_environment_context(float(lat),float(lon),1000,state)),"infobanjir":public_infobanjir(state)}
        except Exception as exc: sources["JPS"]={"status":"FAILED","error":str(exc)}
        return {"site":{"lat":float(lat),"lon":float(lon),"state":state},"sources":sources,"evidence_state":"SOURCE_CONTEXT","statutory_verification":"NOT_CLAIMED"}

# Call this from the main gateway after its imports are available.

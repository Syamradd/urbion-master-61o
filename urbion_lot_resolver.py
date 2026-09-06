"""Cross-source lot identity and evidence resolver for URBION HORIZON.

The resolver uses the public PLANMalaysia i-Plan cadastral service as the
queryable geometry anchor, then compares its lot identity against planning
attributes and optional user/project references. JUPEM MyLot is retained as
the cadastral verification authority/reference, but its browser application
is not scraped or represented as a fake API.

Evidence states are deliberately conservative:
- VERIFIED_CANDIDATE: official public geometry + exact identity match;
- SOURCE_CONTEXT: official public geometry without enough corroboration;
- USER_PROVIDED: user/project reference only;
- EVIDENCE_GAP: source unavailable or conflicting.
"""
from __future__ import annotations
from typing import Any
from urllib.parse import urlencode
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

STATE_CODES={"Johor":"01","Kedah":"02","Kelantan":"03","Melaka":"04","Negeri Sembilan":"05","Pahang":"06","Pulau Pinang":"07","Perak":"08","Perlis":"09","Selangor":"10","Terengganu":"11","Sabah":"12","Sarawak":"13","Wilayah Persekutuan":"14","Labuan":"15","Putrajaya":"16"}
IPLANS_BASE="https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN"
MYLOT_URL="https://jupem2u.kul.jupem.gov.my/mylot/index.html"

def _json(url:str,timeout:float=8.0)->dict[str,Any]:
    req=Request(url,headers={"User-Agent":"URBION-HORIZON/MASTER-330"})
    try:
        with urlopen(req,timeout=timeout) as response:return json.loads(response.read().decode("utf-8"))
    except (HTTPError,URLError,TimeoutError,OSError,json.JSONDecodeError) as exc:
        return {"status":"QUERY_UNAVAILABLE","error_type":type(exc).__name__,"error":str(exc),"url":url}

def _normalise_arcgis(payload:dict[str,Any])->list[dict[str,Any]]:
    return list(payload.get("features") or []) if isinstance(payload,dict) else []

def _quote_sql(value:Any)->str:
    return "'"+str(value).replace("'","''")+"'"

def _query_layer(service:str,lat:float|None=None,lon:float|None=None,where:str="1=1",return_geometry:bool=True,max_records:int=20)->dict[str,Any]:
    base=f"{IPLANS_BASE}/{service}/MapServer/0/query"
    params={"where":where,"outFields":"*","returnGeometry":"true" if return_geometry else "false","outSR":"4326","resultRecordCount":max_records,"f":"geojson"}
    if lat is not None and lon is not None:params.update({"geometry":f"{lon},{lat}","geometryType":"esriGeometryPoint","inSR":"4326","spatialRel":"esriSpatialRelIntersects"})
    url=f"{base}?{urlencode(params)}";payload=_json(url)
    if payload.get("status")=="QUERY_UNAVAILABLE":return {**payload,"features":[]}
    if payload.get("error"):return {"status":"QUERY_UNAVAILABLE","error":payload["error"],"url":url,"features":[]}
    features=_normalise_arcgis(payload)
    return {"status":"LIVE_QUERY" if features else "NO_FEATURE","url":url,"feature_count":len(features),"features":features}

def _attrs(feature:dict[str,Any])->dict[str,Any]:return feature.get("properties") or feature.get("attributes") or {}
def _clean(v:Any)->str:return str(v or "").strip().casefold()
def _first(attrs:dict[str,Any],*keys:str)->Any:
    for key in keys:
        if attrs.get(key) not in (None,""):return attrs[key]
    return None

def _lot_identity(attrs:dict[str,Any])->dict[str,Any]:
    return {"lot_no":_first(attrs,"LOT","lot_no","NO_LOT"),"upi":_first(attrs,"UPI","upi"),"state":_first(attrs,"NEGERI","negeri"),"district":_first(attrs,"DAERAH","daerah"),"mukim":_first(attrs,"MUKIM","mukim"),"section":_first(attrs,"SEKSYEN","seksyen"),"area":_first(attrs,"KELUASAN","luas")}

def _same_identity(a:dict[str,Any],b:dict[str,Any])->bool:
    au,bu=_clean(a.get("upi")),_clean(b.get("upi"))
    if au and bu:return au==bu
    al,bl=_clean(a.get("lot_no")),_clean(b.get("lot_no"))
    return bool(al and bl and al==bl)

def resolve_lot(lat:float|None=None,lon:float|None=None,state:str="Melaka",lot_no:str|None=None,upi:str|None=None,project_reference:dict[str,Any]|None=None)->dict[str,Any]:
    if state not in STATE_CODES:return {"status":"UNSUPPORTED_STATE","state":state,"decision_safe":False}
    service=f"LOT_{STATE_CODES[state]}"
    if (lat is None)!=(lon is None):raise ValueError("lat and lon must be supplied together")
    if lat is None and not(lot_no or upi):raise ValueError("provide site coordinates, lot_no, or upi")
    where="1=1"
    if upi:where=f"UPI={_quote_sql(upi)}"
    elif lot_no:where=f"LOT={_quote_sql(lot_no)}"
    query=_query_layer(service,lat,lon,where=where,return_geometry=True,max_records=20)
    features=query["features"]
    requested={"lot_no":lot_no,"upi":upi}
    if lot_no or upi:
        wanted_lot,wanted_upi=_clean(lot_no),_clean(upi)
        features=[f for f in features if (wanted_upi and _clean(_lot_identity(_attrs(f)).get("upi"))==wanted_upi) or (wanted_lot and _clean(_lot_identity(_attrs(f)).get("lot_no"))==wanted_lot)]
    if not features:return {"status":"EVIDENCE_GAP" if query["status"]=="QUERY_UNAVAILABLE" else "NO_FEATURE","state":state,"requested":requested,"source":{"id":"iplan","service":service,"layer":"Lot Melaka" if state=="Melaka" else f"Lot {state}","url":query.get("url"),"evidence":"SOURCE_CONTEXT"},"jupem_verification":{"provider":"JUPEM MyLot","url":MYLOT_URL,"status":"MANUAL_VERIFICATION_REQUIRED","decision_safe":False},"decision_safe":False}
    candidates=[]
    ref_identity=_lot_identity(project_reference or {})
    for feature in features:
        identity=_lot_identity(_attrs(feature));matches=[]
        if lot_no and _clean(identity.get("lot_no"))==_clean(lot_no):matches.append("LOT")
        if upi and _clean(identity.get("upi"))==_clean(upi):matches.append("UPI")
        reference_match=_same_identity(identity,ref_identity) if project_reference else False
        if reference_match:matches.append("PROJECT_REFERENCE")
        candidates.append({"identity":identity,"geometry":feature.get("geometry"),"properties":_attrs(feature),"matches":matches,"reference_match":reference_match})
    selected=max(candidates,key=lambda x:len(x["matches"]));corroboration=list(selected["matches"])
    status="VERIFIED_CANDIDATE" if any(x in selected["matches"] for x in ("LOT","UPI")) else "SOURCE_CONTEXT"
    if project_reference and not selected["reference_match"]:status="EVIDENCE_GAP"
    return {"status":status,"state":state,"requested":requested,"selected":selected,"candidate_count":len(candidates),"corroboration":corroboration,"sources":[{"id":"iplan","name":"PLANMalaysia i-Plan LOT","service":service,"evidence":"SOURCE_CONTEXT","geometry":"LIVE_ARCGIS_REST"},{"id":"jupem-mylot","name":"JUPEM MyLot","url":MYLOT_URL,"evidence":"MANUAL_VERIFICATION","status":"REFERENCE / VERIFICATION CHANNEL"}],"authority_model":"OFFICIAL_SOURCE_CANDIDATE; JUPEM CADASTRAL VERIFICATION REQUIRED FOR AUTHORITATIVE CLAIM","decision_safe":False,"disclaimer":"A public i-Plan lot geometry is a strong official planning/GIS anchor, but URBION does not silently label it as JUPEM-authoritative cadastral evidence. Verify against JUPEM MyLot/eKadaster or an authorised cadastral product before statutory reliance."}

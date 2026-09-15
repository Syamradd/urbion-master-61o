"""Compatibility launcher for the existing URBION HORIZON Render V4 service.

Render keeps the historical module-level start command for this service, but the
actual application is the single canonical public wrapper in ``landing_server``.
This module intentionally contains no second FastAPI app, planning engine, or
frontend owner. It exposes the canonical About raster asset, normalizes legacy
UI payloads, routes critical Melaka i-Plan map requests to the proven ArcGIS
service, and serves the bundled release-hardening asset used by the same V5
workspace.
"""
import json
from pathlib import Path
from urllib.parse import urlencode
from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from landing_server import app

_BASE_DIR=Path(__file__).resolve().parent
_ABOUT_MASTER=_BASE_DIR/"about_master.png"
_HARDENING_ASSET=_BASE_DIR/"urbion_workspace_release_hardening_v6.js"
_LEGACY_BOOLEAN_FIELDS={"perimeter_planting","landscaped_pedestrian_walkway"}
_CRITICAL_IPLAN_ARCGIS={
 "iplan:gunatanah_semasa_04":"https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer",
 "iplan:gunatanah_zoning_04":"https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTzoning_04/MapServer",
}

def _normalise_legacy_inputs(payload:object)->object:
 if not isinstance(payload,dict): return payload
 target=payload.get("assessment") if isinstance(payload.get("assessment"),dict) else payload
 target=dict(target)
 for key in _LEGACY_BOOLEAN_FIELDS:
  value=target.get(key)
  if isinstance(value,str):
   token=value.strip().lower()
   if token in {"","yes","no","n/a","na","not verified","unverified"}: target[key]=None
   else:
    try: target[key]=float(token)
    except ValueError: pass
 if "assessment" in payload and isinstance(payload.get("assessment"),dict):
  out=dict(payload);out["assessment"]=target;return out
 return target

async def _read_response_body(response:Response)->bytes:
 if getattr(response,"body",None) is not None:return response.body
 chunks=[]
 async for chunk in response.body_iterator:chunks.append(chunk)
 return b"".join(chunks)

@app.middleware("http")
async def _urbion_v4_compatibility(request:Request,call_next):
 if request.method=="POST" and request.url.path in {"/assess","/workstation/analysis"}:
  raw=await request.body()
  if raw:
   try:
    payload=json.loads(raw.decode("utf-8"));normalised=_normalise_legacy_inputs(payload)
    if normalised!=payload:request._body=json.dumps(normalised,separators=(",",":")).encode("utf-8")
   except (UnicodeDecodeError,json.JSONDecodeError):pass
 if request.method=="GET" and request.url.path=="/map/wms":
  layer=request.query_params.get("layers","");service=_CRITICAL_IPLAN_ARCGIS.get(layer)
  if service:
   params={k:v for k,v in request.query_params.multi_items()};params.pop("layers",None);params["service"]=service;params.setdefault("f","image");params.setdefault("format","png32");params.setdefault("transparent","true");params["layers"]="show:0"
   return RedirectResponse(url="/map/arcgis?"+urlencode(params),status_code=307)
 response=await call_next(request)
 if request.method=="GET" and request.url.path=="/workspace" and _HARDENING_ASSET.is_file():
  try:
   body=await _read_response_body(response)
   if b"urbion_workspace_release_hardening_v6.js" not in body and b"</body>" in body:
    body=body.replace(b"</body>",b'<script src="/urbion_workspace_release_hardening_v6.js"></script></body>',1)
   headers={k:v for k,v in dict(response.headers).items() if k.lower() not in {"content-length","content-type","transfer-encoding"}}
   headers["Cache-Control"]="no-store, max-age=0, must-revalidate"
   return Response(content=body,status_code=response.status_code,headers=headers,media_type="text/html; charset=utf-8")
  except Exception:return response
 return response

@app.get("/urbion_workspace_release_hardening_v6.js",include_in_schema=False)
def release_hardening_asset():
 if not _HARDENING_ASSET.is_file():return Response("URBION workspace release hardening asset missing.",status_code=500,media_type="text/plain; charset=utf-8")
 return Response(_HARDENING_ASSET.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

@app.get("/about_master.png",include_in_schema=False)
def about_master():
 if not _ABOUT_MASTER.is_file():return Response("URBION HORIZON canonical About visual master missing.",status_code=500,media_type="text/plain; charset=utf-8")
 return FileResponse(_ABOUT_MASTER,media_type="image/png",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

__all__=["app"]

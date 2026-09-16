"""Compatibility launcher for the existing URBION HORIZON Render V4 service.

Render keeps the historical module-level start command for this service, but the
actual application is the single canonical public wrapper in ``landing_server``.
This module intentionally contains no second FastAPI app, planning engine, or
frontend owner. It exposes the canonical About raster asset, the canonical
Development Impact UI asset, the narrative/demo workspace layer, normalizes
legacy UI payloads, serves the bundled release-hardening asset used by the same
V5 workspace, and reconnects visible planning inputs to the canonical evidence
packet at the presentation boundary.
"""
import json
from pathlib import Path
from fastapi import Request
from fastapi.responses import FileResponse, Response, JSONResponse
from landing_server import app, _development_impact, _canonical_packet

_BASE_DIR=Path(__file__).resolve().parent
_ABOUT_MASTER=_BASE_DIR/"about_master.png"
_HARDENING_ASSET=_BASE_DIR/"urbion_workspace_release_hardening_v6.js"
_DEVELOPMENT_IMPACT_ASSET=_BASE_DIR/"urbion_workspace_development_impact_owner_v4.js"
_DEMO_COMMAND_ASSET=_BASE_DIR/"urbion_workspace_demo_command_layer.js"
_CONTRACT_SURFACE_ASSET=_BASE_DIR/"urbion_workspace_contract_surface_v1.js"
_DEMO_ENRICHMENT_ASSET=_BASE_DIR/"urbion_workspace_demo_enrichment_v1.js"
_LEGACY_BOOLEAN_FIELDS={"perimeter_planting","landscaped_pedestrian_walkway"}

VISIBLE_CONTRACT_FIELDS=(
 "project","project_ref","mukim","landuse1","landuse2","landuse3",
 "site_area_ha","commercial_gfa_m2","jobs","population","daily_trips",
 "road_distance_m","flood_exposure","nearby_facilities","environment_note",
 "infra_note","constraint_note","source_note","analysis_focus","units","gfa"
)

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


def _visible_contract_from_request(raw_payload:object)->dict:
 if not isinstance(raw_payload,dict):return {}
 source=raw_payload.get("assessment") if isinstance(raw_payload.get("assessment"),dict) else raw_payload
 out={}
 for key in VISIBLE_CONTRACT_FIELDS:
  if key in source and source.get(key) is not None:
   value=source.get(key)
   if isinstance(value,str):
    value=value.strip()
    if value=="":continue
   out[key]=value
 for key in ("shop_frontage_verified","shop_office_verified"):
  if key in source:out[key]=bool(source.get(key))
 return out


def _enrich_workspace_response(payload:object,raw_payload:object)->object:
 if not isinstance(payload,dict):return payload
 assessment=payload.get("assessment")
 if not isinstance(assessment,dict):return payload
 visible=_visible_contract_from_request(raw_payload)
 if not visible:return payload
 proposal=dict(assessment.get("proposal") or {})
 for key,value in visible.items():proposal[key]=value
 assessment["proposal"]=proposal
 assessment["user_input_contract"]={"fields":visible,"source":"CANONICAL_WORKSPACE_VISIBLE_INPUTS","note":"Visible planning inputs are preserved for evidence/impact presentation. Missing values remain review-required."}
 assessment.pop("development_impact",None)
 try:
  impact=_development_impact(assessment)
  assessment["development_impact"]=impact
  packet=_canonical_packet(assessment)
  payload["development_impact"]=packet.get("evidence",{}).get("development_impact",{})
  payload["canonical_evidence_packet"]=packet
  payload["user_input_contract"]=assessment["user_input_contract"]
  if isinstance(payload.get("decision_center"),dict):
   payload["decision_center"]["development_impact"]=payload["development_impact"]
   payload["decision_center"]["canonical_evidence_packet"]=packet
   payload["decision_center"]["review_gaps"]=list(packet.get("review_gaps",[]))
   payload["decision_center"]["review_required"]=bool(packet.get("review_gaps",[]))
 except Exception:
  pass
 return payload

async def _read_response_body(response:Response)->bytes:
 if getattr(response,"body",None) is not None:return response.body
 chunks=[]
 async for chunk in response.body_iterator:chunks.append(chunk)
 return b"".join(chunks)

STATIC_IMPACT_SURFACE='''<section id="urbionImpactInputs" class="sec"><div class="sechead"><span class="num">04A</span><button type="button">IMPACT &amp; TECHNICAL INPUTS</button><span class="tag">OPTIONAL · EVIDENCE-AWARE</span></div><div class="body"><div class="g2"><div class="row"><label class="lab">SITE AREA (ha)</label><input id="site_area_ha" class="field" type="number" min="0" step="0.001" placeholder="e.g. 1.145"></div><div class="row"><label class="lab">COMMERCIAL GFA (m²)</label><input id="commercial_gfa_m2" class="field" type="number" min="0" step="1" placeholder="e.g. 12000"></div></div><div class="g2"><div class="row"><label class="lab">JOBS</label><input id="jobs" class="field" type="number" min="0" step="1" placeholder="Estimated jobs"></div><div class="row"><label class="lab">POPULATION / USERS</label><input id="population" class="field" type="number" min="0" step="1" placeholder="Estimated population/users"></div></div><div class="g2"><div class="row"><label class="lab">DAILY TRIPS</label><input id="daily_trips" class="field" type="number" min="0" step="1" placeholder="Estimated daily trips"></div><div class="row"><label class="lab">ROAD DISTANCE (m)</label><input id="road_distance_m" class="field" type="number" min="0" step="1" placeholder="Source-backed distance"></div></div><div class="row"><label class="lab">FLOOD / RISK EXPOSURE</label><select id="flood_exposure" class="select"><option value="">Not specified</option><option value="None identified">None identified</option><option value="Low">Low</option><option value="Moderate">Moderate</option><option value="High">High</option><option value="Requires official verification">Requires official verification</option></select></div><div class="row"><label class="lab">NEARBY FACILITIES</label><input id="nearby_facilities" class="field" placeholder="e.g. school, hospital, transit, utility"></div><div class="g2"><label class="checkitem"><input id="shop_frontage_verified" type="checkbox"> Shop frontage verified</label><label class="checkitem"><input id="shop_office_verified" type="checkbox"> Shop-office control verified</label></div><div class="hint">These fields are carried into the canonical evidence packet when supplied. Missing values remain review-required; no value is inferred as verified.</div></div></section>'''

@app.middleware("http")
async def _urbion_v4_compatibility(request:Request,call_next):
 raw_contract_payload=None
 if request.method=="POST" and request.url.path in {"/assess","/workstation/analysis"}:
  raw=await request.body()
  if raw:
   try:
    payload=json.loads(raw.decode("utf-8"));raw_contract_payload=payload;normalised=_normalise_legacy_inputs(payload)
    if normalised!=payload:request._body=json.dumps(normalised,separators=(",",":")).encode("utf-8")
   except (UnicodeDecodeError,json.JSONDecodeError):pass
 response=await call_next(request)
 if request.method=="POST" and request.url.path=="/workstation/analysis" and raw_contract_payload is not None:
  try:
   body=await _read_response_body(response)
   payload=json.loads(body.decode("utf-8")) if body else None
   if isinstance(payload,dict):
    payload=_enrich_workspace_response(payload,raw_contract_payload)
    headers={k:v for k,v in dict(response.headers).items() if k.lower() not in {"content-length","content-type","transfer-encoding"}}
    return JSONResponse(payload,status_code=response.status_code,headers=headers)
  except Exception:
   return response
 if request.method=="GET" and request.url.path=="/workspace" and (_HARDENING_ASSET.is_file() or _DEMO_COMMAND_ASSET.is_file() or _CONTRACT_SURFACE_ASSET.is_file() or _DEMO_ENRICHMENT_ASSET.is_file()):
  try:
   body=await _read_response_body(response)
   if b'id="urbionImpactInputs"' not in body and b'<div class="leftscroll">' in body:
    marker=b'</div></aside>'
    if marker in body: body=body.replace(marker,STATIC_IMPACT_SURFACE.encode("utf-8")+marker,1)
   scripts=b''
   if _HARDENING_ASSET.is_file() and b"urbion_workspace_release_hardening_v6.js" not in body:
    scripts+=b'<script src="/urbion_workspace_release_hardening_v6.js"></script>'
   if _DEMO_COMMAND_ASSET.is_file() and b"urbion_workspace_demo_command_layer.js" not in body:
    scripts+=b'<script src="/urbion_workspace_demo_command_layer.js"></script>'
   if _CONTRACT_SURFACE_ASSET.is_file() and b"urbion_workspace_contract_surface_v1.js" not in body:
    scripts+=b'<script src="/urbion_workspace_contract_surface_v1.js"></script>'
   if _DEMO_ENRICHMENT_ASSET.is_file() and b"urbion_workspace_demo_enrichment_v1.js" not in body:
    scripts+=b'<script src="/urbion_workspace_demo_enrichment_v1.js"></script>'
   if scripts and b"</body>" in body:body=body.replace(b"</body>",scripts+b"</body>",1)
   headers={k:v for k,v in dict(response.headers).items() if k.lower() not in {"content-length","content-type","transfer-encoding"}}
   headers["Cache-Control"]="no-store, max-age=0, must-revalidate"
   return Response(content=body,status_code=response.status_code,headers=headers,media_type="text/html; charset=utf-8")
  except Exception:return response
 return response

@app.get("/urbion_workspace_release_hardening_v6.js",include_in_schema=False)
def release_hardening_asset():
 if not _HARDENING_ASSET.is_file():return Response("URBION workspace release hardening asset missing.",status_code=500,media_type="text/plain; charset=utf-8")
 return Response(_HARDENING_ASSET.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

@app.get("/urbion_workspace_development_impact_owner_v4.js",include_in_schema=False)
def development_impact_ui_asset():
 if not _DEVELOPMENT_IMPACT_ASSET.is_file():return Response("URBION HORIZON development impact UI asset missing.",status_code=500,media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})
 return Response(_DEVELOPMENT_IMPACT_ASSET.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

@app.get("/urbion_workspace_demo_command_layer.js",include_in_schema=False)
def demo_command_asset():
 if not _DEMO_COMMAND_ASSET.is_file():return Response("URBION HORIZON demo command layer missing.",status_code=500,media_type="text/plain; charset=utf-8")
 return Response(_DEMO_COMMAND_ASSET.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

@app.get("/urbion_workspace_contract_surface_v1.js",include_in_schema=False)
def contract_surface_asset():
 if not _CONTRACT_SURFACE_ASSET.is_file():return Response("URBION HORIZON contract surface asset missing.",status_code=500,media_type="text/plain; charset=utf-8")
 return Response(_CONTRACT_SURFACE_ASSET.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

@app.get("/urbion_workspace_demo_enrichment_v1.js",include_in_schema=False)
def demo_enrichment_asset():
 if not _DEMO_ENRICHMENT_ASSET.is_file():return Response("URBION HORIZON demo enrichment asset missing.",status_code=500,media_type="text/plain; charset=utf-8")
 return Response(_DEMO_ENRICHMENT_ASSET.read_text(encoding="utf-8"),media_type="application/javascript; charset=utf-8",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

@app.get("/about_master.png",include_in_schema=False)
def about_master():
 if not _ABOUT_MASTER.is_file():return Response("URBION HORIZON canonical About visual master missing.",status_code=500,media_type="text/plain; charset=utf-8")
 return FileResponse(_ABOUT_MASTER,media_type="image/png",headers={"Cache-Control":"no-store, max-age=0, must-revalidate"})

__all__=["app"]

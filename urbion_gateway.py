"""Deployment gateway for optional advisory and intelligence integrations."""
from fastapi import Body, HTTPException
from server import AssessmentRequest, app, assess_core
from urbion_gemini_redteam import gemini_configured, review_with_gemini
from urbion_live_stations import build_live_station_snapshot
from urbion_station_intelligence import build_station_intelligence, _valid_coord
from urbion_lcp_intelligence import build_lcp_intelligence
from urbion_environment_intelligence import build_environment_intelligence
from urbion_iplan import query_environment_context
from urbion_release_packet import build_release_packet
from urbion_review_packet import build_review_packet
from urbion_release_contract import build_championship_gate
from urbion_what_if import execute_what_if
from urbion_decision_center import build_decision_center
import json
from pathlib import Path


def _validate_site_coords(site_lat: float, site_lon: float) -> None:
    if not _valid_coord(site_lat, site_lon) or (float(site_lat), float(site_lon)) == (-90.0, -180.0):
        raise HTTPException(status_code=422, detail={"code": "INVALID_SPATIAL_INPUT"})


@app.get("/gemini/status")
def gemini_status(): return {"provider":"Google Gemini","role":"RED_TEAM_ADVISORY","configured":gemini_configured(),"decision_authority":"NONE"}
@app.post("/gemini/red-team")
def gemini_red_team(packet:dict=Body(...)): return review_with_gemini(packet)
@app.post("/gemini/red-team-assessment")
def gemini_red_team_assessment(r:AssessmentRequest): return review_with_gemini({"assessment":assess_core(r),"guardrails":{"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED","purpose":"independent red-team review only"}})
@app.get("/stations/nearby")
def stations_nearby(site_lat:float,site_lon:float,state:str="Melaka",limit:int=5):
    _validate_site_coords(site_lat, site_lon)
    return build_live_station_snapshot(site_lat,site_lon,state,limit)
@app.get("/station-intelligence")
def station_intelligence(site_lat:float,site_lon:float,state:str="Melaka"):
    _validate_site_coords(site_lat, site_lon)
    live=build_live_station_snapshot(site_lat,site_lon,state,5);core=build_station_intelligence(site_lat,site_lon,state);core["live_snapshot"]=live;core["decision_boundary"]="OBSERVATION_CONTEXT";core["statutory_verification"]="NOT_CLAIMED";return core
@app.post("/environment/intelligence")
def environment_intelligence(payload:dict=Body(default_factory=dict)):
    context=payload.get("environment_context") or payload.get("context")
    if context is None and payload.get("site_lat") is not None and payload.get("site_lon") is not None: context=query_environment_context(float(payload["site_lat"]),float(payload["site_lon"]),float(payload.get("radius_m",1000)),payload.get("state","Melaka"))
    return build_environment_intelligence(context or payload)
@app.post("/lcp/intelligence")
def lcp_intelligence(payload:dict=Body(...),live_stations:bool=False,auto_environment:bool=True):
    raw=payload.get("assessment") or payload.get("assessment_inputs")
    if not isinstance(raw,dict): raise HTTPException(status_code=422,detail={"code":"ASSESSMENT_INPUT_REQUIRED"})
    try: assessment=assess_core(AssessmentRequest(**raw))
    except Exception as exc: raise HTTPException(status_code=422,detail={"code":"INVALID_LCP_INPUT","message":str(exc)})
    station=payload.get("station_snapshot")
    if live_stations: station=build_live_station_snapshot(assessment["site"]["latitude"],assessment["site"]["longitude"],assessment["site"].get("state","Melaka"),int(payload.get("station_limit",5)))
    env=payload.get("environment_context")
    if env is None and auto_environment: env=query_environment_context(assessment["site"]["latitude"],assessment["site"]["longitude"],float(payload.get("environment_radius_m",1000)),assessment["site"].get("state","Melaka"))
    variants=payload.get("scenario_variants") or payload.get("variants");what_if=None
    if variants:
        if not isinstance(variants,list) or len(variants)>12: raise HTTPException(status_code=422,detail={"code":"INVALID_SCENARIO_VARIANTS"})
        comparison=execute_what_if(raw,variants,lambda inputs:assess_core(AssessmentRequest(**inputs)));what_if={k:comparison.get(k) for k in ["title","version","baseline_status","baseline_score","scenarios","ranked_scenarios","best_candidate","disclaimer"]}
    return build_lcp_intelligence(assessment=assessment,development_inputs=payload.get("development_inputs"),policy_links=payload.get("policy_links"),national_links=payload.get("national_links"),sdg_links=payload.get("sdg_links"),spatial_inputs=payload.get("spatial_inputs"),station_snapshot=station,km_inputs=payload.get("km_inputs"),what_if_summary=what_if,environment_context=env,agency_assets=payload.get("agency_assets"),agency_radius_m=float(payload.get("agency_radius_m",5000)),guideline_topics=payload.get("guideline_topics"))
@app.post("/lcp/release-packet")
def lcp_release_packet(payload:dict=Body(...)):
    lcp=payload.get("lcp") or payload.get("lcp_intelligence")
    if not isinstance(lcp,dict): raise HTTPException(status_code=422,detail={"code":"LCP_RESULT_REQUIRED"})
    return build_release_packet(lcp)
@app.post("/lcp/review-packet")
def lcp_review_packet(payload:dict=Body(...)):
    lcp=payload.get("lcp") or payload.get("lcp_intelligence")
    if not isinstance(lcp,dict): raise HTTPException(status_code=422,detail={"code":"LCP_RESULT_REQUIRED"})
    return build_review_packet(lcp=lcp)
@app.get("/championship-gate")
def championship_gate():
    manifest=json.loads((Path(__file__).resolve().parent/"DEPLOYMENT_MANIFEST.json").read_text(encoding="utf-8"));return build_championship_gate(lcp=build_lcp_intelligence(assessment=assess_core(AssessmentRequest(site_lat=2.285,site_lon=102.196,tod_lat=2.286,tod_lon=102.197))),manifest=manifest)

# MASTER-270: championship execution overlay. It is injected at the gateway so the
# functional cockpit, judge mode and legacy workspace share one visible QA surface.
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

_CHAMPIONSHIP_OVERLAY = r'''<script>
(()=>{
'use strict';
if(window.__urbionChampionshipOverlay)return;window.__urbionChampionshipOverlay=1;
const css=`#uhx{position:fixed;right:16px;bottom:16px;z-index:2147483000;width:min(420px,calc(100vw - 32px));max-height:72vh;overflow:auto;background:#07121cf5;color:#eff8ff;border:1px solid #29445f;border-radius:16px;box-shadow:0 18px 50px #0008;font:10px Inter,system-ui,sans-serif}#uhx *{box-sizing:border-box}#uhx .h{padding:11px 13px;border-bottom:1px solid #203343;display:flex;justify-content:space-between;gap:8px;align-items:center}#uhx .t{font:700 13px 'Space Grotesk',sans-serif}#uhx .k{font-size:7px;letter-spacing:.16em;color:#5ee7c2;font-weight:900}#uhx button{border:1px solid #29445f;background:#07121c;color:#eff8ff;border-radius:7px;padding:6px 8px;font:900 8px Inter;cursor:pointer}#uhx .body{padding:9px}#uhx .grid{display:grid;grid-template-columns:1fr 1fr;gap:5px}#uhx .r{border:1px solid #203343;border-radius:8px;padding:7px;display:flex;justify-content:space-between;gap:8px}#uhx .ok{color:#5ee7c2}#uhx .wait{color:#ffd37a}#uhx .bad{color:#ff7b8b}#uhx .muted{color:#7890a3;font-size:8px;line-height:1.4;margin-top:7px}#uhx .foot{display:flex;gap:5px;margin-top:7px;flex-wrap:wrap}@media(max-width:560px){#uhx{right:8px;bottom:8px;width:calc(100vw - 16px)}}`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const el=document.createElement('aside');el.id='uhx';el.innerHTML='<div class="h"><div><div class="k">MASTER-270 · CHAMPIONSHIP EXECUTION</div><div class="t">Planner QA / Evidence / Handoff</div></div><button id="uhx-x">HIDE</button></div><div class="body"><div id="uhx-status" class="grid"></div><div id="uhx-note" class="muted">Runs against the current site inputs when available. Green means the endpoint responded; it does not claim statutory approval.</div><div class="foot"><button id="uhx-run">RUN WORKSTATION CHECK</button><button id="uhx-j">JUDGE MODE</button><button id="uhx-d">DECISION CENTRE</button><button id="uhx-l">LCP INTELLIGENCE</button></div></div>';
document.body.appendChild(el);document.getElementById('uhx-x').onclick=()=>el.remove();
function val(id,def){const x=document.getElementById(id);return x&&x.value!==''?x.value:def}
function payload(){return{site_lat:+val('uc-lat',2.285),site_lon:+val('uc-lon',102.196),tod_lat:+val('uc-todlat',2.286),tod_lon:+val('uc-todlon',102.197),plot_ratio:+val('uc-ratio',4.5),precinct:val('uc-precinct','Terminal Sg. Udang'),development_type:val('uc-devtype','TOD Development / Mixed Use'),development_class:val('uc-devclass','Mixed Use'),state:val('uc-state','Melaka'),district:val('uc-district','Melaka Tengah'),pbt:val('uc-pbt','Majlis Bandaraya Melaka Bersejarah'),lot_no:val('uc-lot','')}}
async function get(u,o){const r=await fetch(u,o);if(!r.ok)throw Error(String(r.status));return r.json()}
function row(name,state){return '<div class="r"><span>'+esc(name)+'</span><b class="'+(state==='OK'?'ok':state==='WAIT'?'wait':'bad')+'">'+esc(state)+'</b></div>'}
async function run(){const p=payload(),s=document.getElementById('uhx-status');s.innerHTML=row('Health','WAIT')+row('i-Plan / GIS','WAIT')+row('Environment','WAIT')+row('Assessment','WAIT')+row('Decision','WAIT')+row('Championship Gate','WAIT');const jobs=[['Health',()=>get('/health')],['i-Plan / GIS',()=>get('/iplan/context?site_lat='+p.site_lat+'&site_lon='+p.site_lon+'&state='+encodeURIComponent(p.state))],['Environment',()=>get('/station-intelligence?site_lat='+p.site_lat+'&site_lon='+p.site_lon+'&state='+encodeURIComponent(p.state))],['Assessment',()=>get('/assess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)})],['Decision',()=>get('/decision-center',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)})],['Championship Gate',()=>get('/championship-gate')]];const results=await Promise.allSettled(jobs.map(x=>x[1]()));results.forEach((r,i)=>{s.children[i].outerHTML=row(jobs[i][0],r.status==='fulfilled'?'OK':'FAIL')})}
document.getElementById('uhx-run').onclick=run;document.getElementById('uhx-j').onclick=()=>location.href='/judge-mode';document.getElementById('uhx-d').onclick=()=>{const p=payload();sessionStorage.setItem('urbion_assessment_inputs',JSON.stringify(p));location.href='/decision-center'};document.getElementById('uhx-l').onclick=async()=>{try{const p=payload();await get('/lcp/intelligence',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({assessment_inputs:p,live_stations:true,auto_environment:true,scenario_variants:[{id:'LOWER_DENSITY',name:'Lower density',plot_ratio:Math.max(.5,p.plot_ratio-.5)},{id:'HIGHER_DENSITY',name:'Higher density',plot_ratio:p.plot_ratio+.5}]})});alert('LCP intelligence responded successfully. Open Judge Mode or Decision Centre for the visible handoff.')}catch(e){alert('LCP intelligence failed: '+e.message)}};setTimeout(run,900);
})();</script>'''

class ChampionshipOverlayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        ctype = response.headers.get("content-type", "")
        if "text/html" not in ctype:
            return response
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        marker = b"</body>"
        if marker in body and b"MASTER-270" not in body:
            body = body.replace(marker, _CHAMPIONSHIP_OVERLAY.encode("utf-8") + b'<script src="/urbion_championship_dashboard.js"></script>' + marker, 1)
        headers = dict(response.headers)
        headers.pop("content-length", None)
        return Response(content=body, status_code=response.status_code, headers=headers, media_type="text/html")

app.add_middleware(ChampionshipOverlayMiddleware)

# MASTER-271: aggregate championship QA endpoint. It lets the UI/test harness hit
# the critical execution chain concurrently and returns per-surface truth without
# turning any advisory result into statutory approval.
@app.get("/championship-health")
def championship_health(site_lat:float=2.285,site_lon:float=102.196,tod_lat:float=2.286,tod_lon:float=102.197,state:str="Melaka"):
    _validate_site_coords(site_lat,site_lon)
    checks={}
    try: checks["health"]={"status":"OK","data":{"status":"healthy"}}
    except Exception as exc: checks["health"]={"status":"FAIL","error":str(exc)}
    try: checks["iplan"]={"status":"OK","data":query_environment_context(site_lat,site_lon,1000,state)}
    except Exception as exc: checks["iplan"]={"status":"FAIL","error":str(exc)}
    try: checks["stations"]={"status":"OK","data":build_live_station_snapshot(site_lat,site_lon,state,5)}
    except Exception as exc: checks["stations"]={"status":"FAIL","error":str(exc)}
    assessment_inputs=AssessmentRequest(site_lat=site_lat,site_lon=site_lon,tod_lat=tod_lat,tod_lon=tod_lon,state=state)
    try: checks["assessment"]={"status":"OK","data":assess_core(assessment_inputs)}
    except Exception as exc: checks["assessment"]={"status":"FAIL","error":str(exc)}
    if checks["assessment"]["status"]=="OK":
        try: checks["decision"]={"status":"OK","data":build_decision_center(assessment=checks["assessment"]["data"])}
        except Exception as exc: checks["decision"]={"status":"FAIL","error":str(exc)}
    else: checks["decision"]={"status":"BLOCKED","error":"Assessment did not return a usable result."}
    try:
        manifest=json.loads((Path(__file__).resolve().parent/"DEPLOYMENT_MANIFEST.json").read_text(encoding="utf-8"));checks["gate"]={"status":"OK","data":build_championship_gate(lcp=build_lcp_intelligence(assessment=assess_core(AssessmentRequest(site_lat=site_lat,site_lon=site_lon,tod_lat=tod_lat,tod_lon=tod_lon,state=state))),manifest=manifest)}
    except Exception as exc: checks["gate"]={"status":"FAIL","error":str(exc)}
    return {"project":"URBION HORIZON","version":"MASTER-271","checks":checks,"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED"}

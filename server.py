from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse,HTMLResponse
from pydantic import BaseModel,Field,field_validator
import math,sys,json
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE_DIR))
from urbion_spatial import urbion_create_spatial_context
from urbion_retrieval import urbion_retrieve_rules
from urbion_applicability import urbion_check_applicability
from urbion_compliance import urbion_evaluate_compliance,urbion_calculate_overall_status
from urbion_site_intelligence import STATE_PBT,DEVELOPMENT_CLASSES,build_site_analysis,policy_coverage,source_registry_snapshot
from urbion_evidence import summarise_sources,decision_trace
from urbion_demo_scenarios import demo_scenarios,get_demo_scenario
from urbion_planning_value import build_planning_value
from urbion_what_if import build_scenario_plan,compare_assessments
from urbion_scenario_ranking import rank_scenarios
from urbion_decision_center import build_decision_center
from urbion_judge_mode import build_judge_mode
from urbion_iplan import query_iplan_context
from urbion_data_sources import source_catalog,map_layer_catalog
from urbion_elysian import ELYSIAN_LOT_11213,compare_official_context,elysian_source_record
from urbion_kebenaran_merancang import build_km_readiness
from urbion_lcp_intelligence import build_lcp_intelligence
from urbion_release_contract import build_championship_gate
app=FastAPI(title='URBION API',version='PHASE-E.7');app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=False,allow_methods=['*'],allow_headers=['*'])
class AssessmentRequest(BaseModel):
 site_lat:float=Field(...,ge=-90,le=90);site_lon:float=Field(...,ge=-180,le=180);tod_lat:float=Field(...,ge=-90,le=90);tod_lon:float=Field(...,ge=-180,le=180);plot_ratio:float=Field(default=4.5,gt=0);precinct:str='Terminal Sg. Udang';development_type:str='TOD Development / Mixed Use';development_class:str='Mixed Use';state:str='Melaka';district:str='Melaka Tengah';pbt:str='Majlis Bandaraya Melaka Bersejarah';lot_no:str='';building_height:float|None=Field(default=None,ge=0);perimeter_planting:float|None=Field(default=None,ge=0);landscaped_pedestrian_walkway:float|None=Field(default=None,ge=0);shop_frontage_verified:bool=False;shop_office_verified:bool=False
class WhatIfRequest(BaseModel):
 baseline:AssessmentRequest;variants:list[dict]=Field(default_factory=list)
 @field_validator('variants')
 @classmethod
 def validate_variant_count(cls,value):
  if len(value)>12:raise ValueError('variants must contain at most 12 scenarios')
  return value
def distance_m(a,b,c,d):
 R=6371000;p1,p2=math.radians(a),math.radians(c);dp,dl=math.radians(c-a),math.radians(d-b);x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2;return R*2*math.atan2(math.sqrt(x),math.sqrt(1-x))
def classify(d):return'TOD 400m'if d<=400 else('TOD 800m'if d<=800 else'OUTSIDE TOD 800m')
def normalise_class(t,c):
 if c in DEVELOPMENT_CLASSES:return c
 v=t.lower()
 if'residential'in v or'housing'in v:return'Residential'
 if'industrial'in v:return'Industrial'
 if any(x in v for x in['institution','education','health']):return'Institutional'
 if any(x in v for x in['recreation','tourism']):return'Recreation'
 if any(x in v for x in['infrastructure','utility']):return'Infrastructure'
 if'mixed'in v or'tod'in v:return'Mixed Use'
 return'Commercial'
def _validate_spatial_input(r):
 values=(r.site_lat,r.site_lon,r.tod_lat,r.tod_lon)
 if not all(math.isfinite(float(value)) for value in values):raise HTTPException(status_code=422,detail={'code':'INVALID_SPATIAL_INPUT','message':'Site and TOD coordinates must be finite numeric values.'})
 if (float(r.site_lat),float(r.site_lon))==(-90.0,-180.0)or(float(r.tod_lat),float(r.tod_lon))==(-90.0,-180.0):raise HTTPException(status_code=422,detail={'code':'INVALID_SPATIAL_INPUT','message':'Placeholder coordinates (-90, -180) cannot be used for spatial assessment. Provide actual site and TOD coordinates.'})
def evidence_state(*,source:str|None=None,calculated:bool=False,verified:bool=False,user_provided:bool=False)->str:
 if verified:return'VERIFIED'
 if source:return'SOURCE_CONTEXT'
 if calculated:return'CALCULATED'
 if user_provided:return'USER_PROVIDED'
 return'UNVERIFIED'
def assess_core(r):
 _validate_spatial_input(r);d=distance_m(r.site_lat,r.site_lon,r.tod_lat,r.tod_lon);cl=classify(d);dc=normalise_class(r.development_type,r.development_class);cov=policy_coverage(r.pbt);sc=urbion_create_spatial_context(precinct=r.precinct,precinct_verified=False,tod_verified=d<=800,tod_400_verified=d<=400,tod_800_verified=d<=800,shop_frontage_verified=r.shop_frontage_verified,shop_office_verified=r.shop_office_verified,tod_distance_m=d);prop={'development_type':r.development_type,'authority':'MBMB'if r.pbt=='Majlis Bandaraya Melaka Bersejarah'else r.pbt,'planning_reference':'RT MBMB 2035'if r.pbt=='Majlis Bandaraya Melaka Bersejarah'else'Local planning policy not loaded','Plot Ratio':r.plot_ratio,'Building Height':r.building_height,'Perimeter Planting':r.perimeter_planting,'Landscaped Pedestrian Walkway':r.landscaped_pedestrian_walkway,'shop_frontage_verified':r.shop_frontage_verified,'shop_office_verified':r.shop_office_verified,'spatial_context':sc};rr=[];ar=[];cr=[];fr=None;fs='REQUIRES REVIEW'
 if r.pbt=='Majlis Bandaraya Melaka Bersejarah':
  rr=urbion_retrieve_rules(development_type=prop['development_type'],authority=prop['authority'],spatial_context=sc);ar=urbion_check_applicability(prop,rr);cr=urbion_evaluate_compliance(ar,prop);applicable=[x for x in cr if x.get('applicability')=='APPLICABLE']
  if applicable:
   fr=applicable[0].get('rule_id');overall=urbion_calculate_overall_status(cr);fs='NON-COMPLIANCE'if'NON-COMPLIANCE'in overall else('CONDITIONAL RISK'if 'CONDITIONAL RISK'in overall else('COMPLY'if'COMPLY'in overall else fs))
  elif cl=='OUTSIDE TOD 800m'and('tod'in r.development_type.lower()or'mixed'in r.development_type.lower()):fs='NOT APPLICABLE'
 else:cr=[{'rule_id':None,'applicability':'NOT_LOADED','status':'REQUIRES REVIEW','reason':'Local statutory rule set is not loaded into the verified decision engine.'}]
 sa=build_site_analysis(state=r.state,district=r.district,pbt=r.pbt,lot_no=r.lot_no,latitude=r.site_lat,longitude=r.site_lon,tod_distance_m=d,development_class=dc,development_type=r.development_type,policy_status=fs,final_status=fs,retrieved_rules=len(rr));reg=source_registry_snapshot();ei=summarise_sources(reg);trace=decision_trace(fs,rr,ar,cr);site={'latitude':r.site_lat,'longitude':r.site_lon,'state':r.state,'district':r.district,'pbt':r.pbt,'lot_no':r.lot_no or'Not specified','tod_distance_m':d};pv=build_planning_value(site=site,final_status=fs,policy_coverage=cov,retrieved_rules=rr,compliance_results=cr,site_analysis=sa,evidence_intelligence=ei);return{'project':'URBION','version':'PHASE-E.7','site':site,'tod':{'latitude':r.tod_lat,'longitude':r.tod_lon},'precinct':r.precinct,'development_class':dc,'development_type':r.development_type,'proposal':prop,'tod_distance_m':d,'classification':cl,'policy_coverage':cov,'retrieved_rules':rr,'applicability_results':ar,'compliance_results':cr,'final_rule':fr,'final_status':fs,'site_analysis':sa,'recommendation':sa['recommendation'],'decision_confidence':sa['decision_confidence'],'planning_value':pv,'source_registry':reg,'evidence_intelligence':ei,'decision_trace':trace,'evidence_state':{'site_coordinates':evidence_state(user_provided=True),'tod_distance':evidence_state(calculated=True),'planning_rules':evidence_state(source='RT MBMB 2035' if rr else None),'final_decision':evidence_state(calculated=True),'statutory_verification':'NOT_CLAIMED'},'gis_provenance':'URBION GIS decision pipeline + official-source registry; external GIS live-query status is explicitly disclosed.'}
@app.get('/',include_in_schema=False)
def root():
 source=(BASE_DIR/'index.html').read_text(encoding='utf-8');source=source.replace('MASTER-63 ENGINE ONLINE','PHASE-E.7 ENGINE ONLINE').replace('MASTER-65 VISUAL DECISION LAYER','PHASE-E.7 LIVE DECISION LAYER').replace("const API='https://urbion-master-61o-1.onrender.com';","const API=location.origin;");enhancement='''<script src="/urbion_ui.js"></script><script src="/urbion_championship_ui.js"></script><script>window.addEventListener('urbion-ui',function(e){document.documentElement.dataset.urbionLang=e.detail.lang;document.documentElement.dataset.urbionTheme=e.detail.theme});window.addEventListener('load',function(){try{if(window.L&&document.getElementById('map')){const wms='https://iplan.planmalaysia.gov.my/geoserver/iplan/wms';const l=L.tileLayer.wms(wms,{layers:'iplan:gunatanah_komited_04',format:'image/png',transparent:true,version:'1.1.1',opacity:.55,attribution:'PLANMalaysia i-Plan'});window.__urbionCommittedWms=l;const b=document.createElement('button');b.textContent='i-PLAN COMMITTED';b.style.cssText='position:absolute;z-index:1200;right:18px;top:18px;padding:9px 11px;border-radius:10px;border:1px solid #294052;background:#0b1621dd;color:#eff8ff;font:800 9px Inter;cursor:pointer';b.onclick=function(){if(map.hasLayer(l)){map.removeLayer(l);b.style.opacity='.65'}else{l.addTo(map);b.style.opacity='1'}};document.body.appendChild(b)}}catch(e){}});</script>''';source=source.replace('</body>',enhancement+'</body>');return HTMLResponse(source,media_type='text/html')
@app.get('/index.html',include_in_schema=False)
def index_html():return root()
@app.get('/health')
def health():return{'status':'healthy','engine':'URBION PHASE-E.7','frontend':'SERVING_INDEX_HTML'}
@app.get('/metadata')
def metadata():return{'project':'URBION HORIZON','version':'PHASE-E.7','states':sorted(STATE_PBT.keys()),'pbt':STATE_PBT,'development_classes':DEVELOPMENT_CLASSES,'source_registry':source_registry_snapshot(),'national_data_sources':source_catalog(),'map_layer_catalog':'/map/layers','policy_coverage':'RT MBMB 2035 rule engine active for supported typologies; other PBTs are spatial-demo coverage only.','decision_layer':'Explainable recommendation + evidence confidence + planning value + What-If scenario intelligence + championship decision center + deterministic judge mode; not statutory approval.','frontend':'index.html served by the same deployment origin.','evidence_model':['USER_PROVIDED','CALCULATED','SOURCE_CONTEXT','VERIFIED','UNVERIFIED']}
@app.get('/evidence-summary')
def evidence_summary():return summarise_sources(source_registry_snapshot())
@app.get('/sources')
def sources():return{'sources':source_catalog(),'evidence_policy':'Portal access or public map-service availability does not equal statutory verification.'}
@app.get('/map/layers')
def map_layers(state:str='Melaka'):return{'state':state,'layers':map_layer_catalog(state),'layer_controls':['toggle','opacity','identify','legend','fit-to-site','measure-distance','measure-area','basemap','share-location'],'disclaimer':'Layers are decision-support context. Verify authoritative currency and statutory applicability before relying on any layer for a planning decision.'}
@app.get('/iplan/context')
def iplan_context(site_lat:float=2.3,site_lon:float=102.2,state:str='Melaka'):
 if not math.isfinite(float(site_lat))or not math.isfinite(float(site_lon)):raise HTTPException(status_code=422,detail={'code':'INVALID_SPATIAL_INPUT','message':'Coordinates must be finite numeric values.'})
 if(float(site_lat),float(site_lon))==(-90.0,-180.0):raise HTTPException(status_code=422,detail={'code':'INVALID_SPATIAL_INPUT','message':'Placeholder coordinates (-90, -180) cannot be used for i-Plan query.'})
 return query_iplan_context(site_lat,site_lon,state)
@app.get('/elysian/reconcile')
def elysian_reconcile(site_lat:float|None=None,site_lon:float|None=None,state:str='Melaka'):
 result={'reference':ELYSIAN_LOT_11213,'source_record':elysian_source_record(),'official_query':None}
 if(site_lat is None)!=(site_lon is None):raise HTTPException(status_code=422,detail={'code':'INCOMPLETE_SPATIAL_INPUT','message':'Provide both site_lat and site_lon, or neither.'})
 if site_lat is not None:
  if not math.isfinite(float(site_lat))or not math.isfinite(float(site_lon)):raise HTTPException(status_code=422,detail={'code':'INVALID_SPATIAL_INPUT','message':'Coordinates must be finite numeric values.'})
  official=query_iplan_context(site_lat,site_lon,state);result['official_query']=official;result['reconciliation']=compare_official_context(official.get('current_land_use') or {})
 else:result['reconciliation']=compare_official_context(None)
 return result
@app.post('/assess')
def assess(r:AssessmentRequest):return assess_core(r)
@app.post('/km/readiness')
def km_readiness(pbt:str,development_type:str,documents:list[str]|None=None,km_category:str|None=None,technical_reviews:dict[str,str]|None=None):return build_km_readiness(pbt=pbt,development_type=development_type,documents=documents,km_category=km_category,technical_reviews=technical_reviews)
@app.get('/demo-scenarios')
def scenarios():return{'project':'URBION HORIZON','scenarios':demo_scenarios()}
@app.post('/demo-scenarios/{scenario_id}')
def run_scenario(scenario_id:str):
 item=get_demo_scenario(scenario_id)
 if not item:raise HTTPException(status_code=404,detail='Unknown demo scenario')
 return assess_core(AssessmentRequest(**item['inputs']))
@app.post('/planning-value')
def planning_value(r:AssessmentRequest):return assess_core(r)['planning_value']
@app.post('/what-if')
def what_if(r:WhatIfRequest):
 baseline=assess_core(r.baseline);plans=build_scenario_plan(r.baseline.model_dump(),r.variants);executed=[]
 for plan in plans:executed.append({'id':plan['id'],'name':plan['name'],'assessment':assess_core(AssessmentRequest(**plan['inputs']))})
 return rank_scenarios(compare_assessments(baseline,executed))
@app.post('/decision-center')
def decision_center(r:AssessmentRequest):return build_decision_center(assessment=assess_core(r))
@app.get('/judge-mode')
def judge_mode():
 executed=[]
 for item in demo_scenarios():executed.append({'id':item['id'],'name':item['name'],'assessment':assess_core(AssessmentRequest(**item['inputs']))})
 return build_judge_mode(scenarios=executed)
@app.get('/championship-gate')
def championship_gate():
 manifest=json.loads((BASE_DIR/'DEPLOYMENT_MANIFEST.json').read_text(encoding='utf-8'))
 return build_championship_gate(lcp=build_lcp_intelligence(assessment=assess_core(AssessmentRequest(site_lat=2.285,site_lon=102.196,tod_lat=2.286,tod_lon=102.197))),manifest=manifest)
import urbion_gateway
@app.get('/{page}.html',include_in_schema=False)
def html_workspace(page:str):
 if not page or any(ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.' for ch in page):raise HTTPException(status_code=404,detail='Unknown frontend page')
 target=(BASE_DIR/f'{page}.html').resolve()
 if target.parent!=BASE_DIR or not target.is_file():raise HTTPException(status_code=404,detail='Unknown frontend page')
 return FileResponse(target,media_type='text/html')

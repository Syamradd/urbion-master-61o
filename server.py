from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import math, sys
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE_DIR))
from urbion_spatial import urbion_create_spatial_context
from urbion_retrieval import urbion_retrieve_rules
from urbion_applicability import urbion_check_applicability
from urbion_compliance import urbion_evaluate_compliance, urbion_calculate_overall_status
from urbion_site_intelligence import STATE_PBT, DEVELOPMENT_CLASSES, build_site_analysis, policy_coverage, source_registry_snapshot
from urbion_demo_scenarios import demo_scenarios
app=FastAPI(title='URBION API',version='MASTER-66')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=False,allow_methods=['*'],allow_headers=['*'])
class AssessmentRequest(BaseModel):
 site_lat:float=Field(...,ge=-90,le=90); site_lon:float=Field(...,ge=-180,le=180); tod_lat:float=Field(...,ge=-90,le=90); tod_lon:float=Field(...,ge=-180,le=180)
 plot_ratio:float=Field(default=4.5,gt=0); precinct:str='Terminal Sg. Udang'; development_type:str='TOD Development / Mixed Use'; development_class:str='Mixed Use'; state:str='Melaka'; district:str='Melaka Tengah'; pbt:str='Majlis Bandaraya Melaka Bersejarah'; lot_no:str=''
 building_height:float|None=Field(default=None,ge=0); perimeter_planting:float|None=Field(default=None,ge=0); landscaped_pedestrian_walkway:float|None=Field(default=None,ge=0); shop_frontage_verified:bool=False; shop_office_verified:bool=False
def distance_m(a,b,c,d):
 R=6371000;p1,p2=math.radians(a),math.radians(c);dp,dl=math.radians(c-a),math.radians(d-b);x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2;return R*(2*math.atan2(math.sqrt(x),math.sqrt(1-x)))
def classify(d): return 'TOD 400m' if d<=400 else ('TOD 800m' if d<=800 else 'OUTSIDE TOD 800m')
def normalise_class(t,c):
 if c in DEVELOPMENT_CLASSES:return c
 v=t.lower()
 if 'residential' in v or 'housing' in v:return 'Residential'
 if 'industrial' in v:return 'Industrial'
 if any(x in v for x in ['institution','education','health']):return 'Institutional'
 if any(x in v for x in ['recreation','tourism']):return 'Recreation'
 if any(x in v for x in ['infrastructure','utility']):return 'Infrastructure'
 if 'mixed' in v or 'tod' in v:return 'Mixed Use'
 return 'Commercial'
def assess_core(r):
 d=distance_m(r.site_lat,r.site_lon,r.tod_lat,r.tod_lon);cl=classify(d);dc=normalise_class(r.development_type,r.development_class);cov=policy_coverage(r.pbt)
 sc=urbion_create_spatial_context(precinct=r.precinct,precinct_verified=True,tod_verified=d<=800,tod_400_verified=d<=400,tod_800_verified=d<=800,shop_frontage_verified=r.shop_frontage_verified,shop_office_verified=r.shop_office_verified,tod_distance_m=d)
 prop={'development_type':r.development_type,'authority':'MBMB' if r.pbt=='Majlis Bandaraya Melaka Bersejarah' else r.pbt,'planning_reference':'RT MBMB 2035' if r.pbt=='Majlis Bandaraya Melaka Bersejarah' else 'Local planning policy not loaded','Plot Ratio':r.plot_ratio,'Building Height':r.building_height,'Perimeter Planting':r.perimeter_planting,'Landscaped Pedestrian Walkway':r.landscaped_pedestrian_walkway,'shop_frontage_verified':r.shop_frontage_verified,'shop_office_verified':r.shop_office_verified,'spatial_context':sc}
 rr=[];ar=[];cr=[];fr=None;fs='REQUIRES REVIEW'
 if r.pbt=='Majlis Bandaraya Melaka Bersejarah':
  rr=urbion_retrieve_rules(development_type=prop['development_type'],authority=prop['authority'],spatial_context=sc);ar=urbion_check_applicability(prop,rr);cr=urbion_evaluate_compliance(ar,prop);applicable=[x for x in cr if x.get('applicability')=='APPLICABLE']
  if applicable:
   fr=applicable[0].get('rule_id');overall=urbion_calculate_overall_status(cr)
   fs='NON-COMPLIANCE' if 'NON-COMPLIANCE' in overall else ('CONDITIONAL RISK' if 'CONDITIONAL RISK' in overall else ('COMPLY' if 'COMPLY' in overall else fs))
  elif cl=='OUTSIDE TOD 800m' and ('tod' in r.development_type.lower() or 'mixed' in r.development_type.lower()):fs='NOT APPLICABLE'
 else:cr=[{'rule_id':None,'applicability':'NOT_LOADED','status':'REQUIRES REVIEW','reason':'Local statutory rule set is not loaded into the verified decision engine.'}]
 sa=build_site_analysis(state=r.state,district=r.district,pbt=r.pbt,lot_no=r.lot_no,latitude=r.site_lat,longitude=r.site_lon,tod_distance_m=d,development_class=dc,development_type=r.development_type,policy_status=fs,final_status=fs)
 return {'project':'URBION','version':'MASTER-66','site':{'latitude':r.site_lat,'longitude':r.site_lon,'state':r.state,'district':r.district,'pbt':r.pbt,'lot_no':r.lot_no or 'Not specified'},'tod':{'latitude':r.tod_lat,'longitude':r.tod_lon},'precinct':r.precinct,'development_class':dc,'development_type':r.development_type,'proposal':prop,'tod_distance_m':d,'classification':cl,'policy_coverage':cov,'retrieved_rules':rr,'applicability_results':ar,'compliance_results':cr,'final_rule':fr,'final_status':fs,'site_analysis':sa,'recommendation':sa['recommendation'],'decision_confidence':sa['decision_confidence'],'source_registry':source_registry_snapshot(),'gis_provenance':'URBION GIS decision pipeline + source registry; external portal live-query status is explicitly disclosed.'}
@app.get('/')
def root():return {'project':'URBION','version':'MASTER-66','status':'ONLINE'}
@app.get('/health')
def health():return {'status':'healthy','engine':'URBION MASTER-66'}
@app.get('/metadata')
def metadata():return {'project':'URBION HORIZON','version':'MASTER-66','states':sorted(STATE_PBT.keys()),'pbt':STATE_PBT,'development_classes':DEVELOPMENT_CLASSES,'source_registry':source_registry_snapshot(),'policy_coverage':'RT MBMB 2035 rule engine active for supported typologies; other PBTs are spatial-demo coverage only.','decision_layer':'Explainable recommendation + evidence confidence; not statutory approval.'}
@app.get('/demo-scenarios')
def demos():return {'version':'MASTER-66','scenarios':demo_scenarios()}
@app.post('/demo-scenarios/{scenario_id}')
def run_demo(scenario_id:str):
 item=next((x for x in demo_scenarios() if x['id']==scenario_id),None)
 if not item:raise HTTPException(status_code=404,detail='Demo scenario not found')
 return {'scenario':item,'assessment':assess_core(AssessmentRequest(**item['inputs']))}
@app.post('/assess')
def assess(r:AssessmentRequest):return assess_core(r)

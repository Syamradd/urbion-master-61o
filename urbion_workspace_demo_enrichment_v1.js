/* URBION HORIZON — enrich the one-click demo with explicit impact inputs. */
(()=>{
'use strict';
if(window.__URBION_DEMO_ENRICHMENT_V1__)return;
window.__URBION_DEMO_ENRICHMENT_V1__=true;
const values={site_area_ha:'1.145',commercial_gfa_m2:'12000',jobs:'150',population:'300',daily_trips:'1200',road_distance_m:'250',flood_exposure:'Requires official verification',nearby_facilities:'transit, school, hospital, utility',perimeter_planting:'3.0',landscaped_pedestrian_walkway:'1.5'};
const raw=id=>document.getElementById(id)?.value??'';
const num=id=>{const r=raw(id),n=Number(r);return Number.isFinite(n)&&String(r).trim()!==''?n:null};
const bool=id=>!!document.getElementById(id)?.checked;
const visible=()=>({project:raw('project'),project_ref:raw('project_ref'),mukim:raw('mukim'),landuse1:raw('landuse1'),landuse2:raw('landuse2'),landuse3:raw('landuse3'),site_area_ha:num('site_area_ha'),commercial_gfa_m2:num('commercial_gfa_m2'),jobs:num('jobs'),population:num('population'),daily_trips:num('daily_trips'),road_distance_m:num('road_distance_m'),flood_exposure:raw('flood_exposure'),nearby_facilities:raw('nearby_facilities'),environment_note:raw('environment_note'),infra_note:raw('infra_note'),constraint_note:raw('constraint_note'),source_note:raw('source_note'),analysis_focus:raw('analysis_focus'),units:num('units'),gfa:num('gfa'),perimeter_planting:num('perimeter_planting'),landscaped_pedestrian_walkway:num('landscaped_pedestrian_walkway'),shop_frontage_verified:bool('shop_frontage_verified'),shop_office_verified:bool('shop_office_verified')});
let wrapper=null,previous=null;
const installGetter=()=>{const current=window.getInputs;if(current&&current.__URBION_VISIBLE_INPUT_GETTER_V2__)return true;previous=typeof current==='function'?current:null;wrapper=function(){let base={};try{if(previous&&previous!==wrapper)base=previous()||{}}catch(_){base={}}return {...base,...visible()}};wrapper.__URBION_VISIBLE_INPUT_GETTER_V2__=true;try{window.getInputs=wrapper}catch(_){try{Object.defineProperty(window,'getInputs',{configurable:true,writable:true,value:wrapper})}catch(__){return false}}return window.getInputs===wrapper};
const set=(id,value)=>{const el=document.getElementById(id);if(!el)return false;el.value=value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return true};
const setChecked=(id,value)=>{const el=document.getElementById(id);if(!el)return false;el.checked=!!value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return true};
const hydrate=()=>{for(const [id,v] of Object.entries(values))set(id,v);setChecked('shop_frontage_verified',true);setChecked('shop_office_verified',true);installGetter();return true};
const hideBlockingBrief=()=>{const brief=document.getElementById('urbionWorkspaceBrief');if(!brief)return false;brief.classList.remove('show');brief.hidden=true;brief.setAttribute('aria-hidden','true');brief.style.display='none';brief.style.pointerEvents='none';return true};
const installPresentationGuards=()=>{hideBlockingBrief();if(!document.getElementById('urbionBriefGuardStyle')){const s=document.createElement('style');s.id='urbionBriefGuardStyle';s.textContent='#urbionWorkspaceBrief{display:none!important;pointer-events:none!important}#urbionWorkspaceBrief.show{display:none!important;pointer-events:none!important}';document.head.appendChild(s)}return true};
const watch=()=>{installGetter();installPresentationGuards();const ready=document.getElementById('udcDemoState')||document.querySelector('.udc-status');if(!ready)return setTimeout(watch,100);hydrate()};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch,{once:true});else watch();
window.addEventListener('load',()=>{installGetter();installPresentationGuards()},{once:true});
const guard=window.setInterval(()=>{installGetter();hideBlockingBrief()},50);window.setTimeout(()=>clearInterval(guard),30000);
})();

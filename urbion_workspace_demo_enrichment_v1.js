/* URBION HORIZON — enrich the one-click demo with explicit impact inputs. */
(()=>{
'use strict';
if(window.__URBION_DEMO_ENRICHMENT_V1__)return;
window.__URBION_DEMO_ENRICHMENT_V1__=true;
const values={site_area_ha:'1.145',commercial_gfa_m2:'12000',jobs:'150',population:'300',daily_trips:'1200',road_distance_m:'250',flood_exposure:'Requires official verification',nearby_facilities:'transit, school, hospital, utility',perimeter_planting:'3.0',landscaped_pedestrian_walkway:'1.5'};
const set=(id,value)=>{const el=document.getElementById(id);if(!el)return false;el.value=value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return true};
const setChecked=(id,value)=>{const el=document.getElementById(id);if(!el)return false;el.checked=!!value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return true};
const hydrate=()=>{for(const [id,v] of Object.entries(values))set(id,v);setChecked('shop_frontage_verified',true);setChecked('shop_office_verified',true);return true};
const watch=()=>{const ready=document.getElementById('udcDemoState')||document.querySelector('.udc-status');if(!ready)return setTimeout(watch,200);hydrate()};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',watch,{once:true});else watch();
})();

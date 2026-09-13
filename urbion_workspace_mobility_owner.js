/* URBION HORIZON — canonical live mobility/station evidence owner. */
(()=>{
'use strict';
if(window.__URBION_MOBILITY_OWNER_V1__) return;
window.__URBION_MOBILITY_OWNER_V1__=true;
const $=id=>document.getElementById(id); const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const esc=s=>String(s??'').replace(/[&<>\\"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}[m]));
let busy=false,last='';
function packet(){return window.URBION_LAST?.canonical_evidence_packet||null}
function render(payload,status='QUERYING'){
 const host=document.querySelector('.right'); if(!host)return;
 host.querySelectorAll('.urbion-mob-card[data-owner="canonical"]').forEach(x=>x.remove());
 const c=document.createElement('section'); c.className='urbion-env-card urbion-mob-card'; c.dataset.owner='canonical'; c.dataset.testid='canonical-live-mobility';
 if(!payload){c.innerHTML='<div class="urbion-env-head"><span class="urbion-env-title">LIVE MOBILITY</span><span class="urbion-env-state">QUERYING…</span></div><div class="urbion-env-foot">Nearest public station context is being refreshed from the selected site.</div>'}
 else {const j=payload.jps_rainfall||{}, a=payload.air_quality||{}; const js=Array.isArray(j.stations)?j.stations:[], as=Array.isArray(a.stations)?a.stations:[]; const nearest=js[0]||as[0]; const dist=nearest?.distance_m!=null?Math.round(nearest.distance_m):'—'; c.innerHTML=`<div class="urbion-env-head"><span class="urbion-env-title">LIVE MOBILITY / STATIONS</span><span class="urbion-env-state">${esc(j.status||status)}</span></div><div class="urbion-env-grid"><div class="urbion-env-m"><b>${js.length}</b><span>JPS STATIONS</span></div><div class="urbion-env-m"><b>${as.length}</b><span>AIR STATIONS</span></div><div class="urbion-env-m"><b>${dist}</b><span>NEAREST · m</span></div></div><div class="urbion-env-risks">${nearest?`<b>NEAREST:</b> ${esc(nearest.name||nearest.station_id||'Station')} · ${dist}m`:'<b>STATUS:</b> No station geometry returned.'}</div><div class="urbion-env-foot">JPS Public Infobanjir / DOE APIMS · SOURCE_CONTEXT · statutory verification NOT_CLAIMED</div>`}
 host.prepend(c)
}
function merge(payload,lat,lon){const last=window.URBION_LAST,p=packet();if(!last||!p)return false;p.evidence=p.evidence||{};p.evidence.stations=payload;p.stations=payload;const gaps=Array.isArray(p.review_gaps)?p.review_gaps.slice():[];for(const g of (payload.review_gaps||[])){if(!gaps.includes(g))gaps.push(g)}p.review_gaps=gaps;last.live_station_evidence=payload;last.mobility_site={latitude:lat,longitude:lon};return true}
async function enrich(){if(busy)return;const p=packet(),lat=Number($('site_lat')?.value),lon=Number($('site_lon')?.value);if(!p||!Number.isFinite(lat)||!Number.isFinite(lon))return;const fp=`${lat.toFixed(6)}|${lon.toFixed(6)}|${$('state')?.value||'Melaka'}`;if(fp===last)return;last=fp;busy=true;render();try{const q=new URLSearchParams({site_lat:String(lat),site_lon:String(lon),state:String($('state')?.value||'Melaka'),limit:'5'});const r=await fetch('/mobility/stations?'+q,{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);const payload=await r.json();if(!merge(payload,lat,lon))throw Error('Canonical packet unavailable');render(payload,payload.jps_rainfall?.status||'LIVE');document.dispatchEvent(new CustomEvent('urbion:mobility-ready',{detail:{payload}}));try{window.URBION_REVIEW_GAPS?.render?.('LIVE EVIDENCE')}catch(_){} }catch(e){render(null,'UNAVAILABLE')}finally{busy=false}}
async function boot(){for(let i=0;i<180;i++){if(packet())await enrich();await sleep(250)}}boot().catch(()=>{});
})();

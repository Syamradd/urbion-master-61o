/* URBION HORIZON — canonical live environment evidence owner.
   Enriches the already-completed canonical assessment with explicit live
   environmental screening context. This is asynchronous evidence enrichment,
   never a replacement planning engine and never statutory verification. */
(()=>{
'use strict';
if(window.__URBION_ENVIRONMENT_OWNER_V1__) return;
window.__URBION_ENVIRONMENT_OWNER_V1__=true;
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>\\\"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}[m]));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let lastFingerprint='';
let busy=false;

function packet(){return window.URBION_LAST?.canonical_evidence_packet||null}
function target(){return document.querySelector('.right')}
function toast(message,ok=true){const t=$('toast');if(!t)return;t.textContent=message;t.style.display='block';t.style.color=ok?'var(--good)':'var(--bad)';clearTimeout(window.__urbionEnvToast);window.__urbionEnvToast=setTimeout(()=>{t.style.display='none'},2600)}
function style(){if($('urbionEnvironmentOwnerStyle'))return;const s=document.createElement('style');s.id='urbionEnvironmentOwnerStyle';s.textContent=`
.urbion-env-card{border:1px solid rgba(47,225,233,.18);border-radius:10px;background:linear-gradient(145deg,rgba(7,29,41,.95),rgba(3,15,22,.98));padding:10px;margin-bottom:8px}
.light .urbion-env-card{background:#fff}
.urbion-env-head{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:7px}
.urbion-env-title{font-size:8px;font-weight:900;letter-spacing:.07em}
.urbion-env-state{font-size:6px;padding:3px 6px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.urbion-env-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:5px}
.urbion-env-m{padding:6px;border:1px solid var(--line);border-radius:8px;background:rgba(255,255,255,.02)}
.urbion-env-m b{display:block;font:700 12px 'Space Grotesk'}
.urbion-env-m span{display:block;font-size:5.8px;color:var(--muted);margin-top:2px}
.urbion-env-risks{margin-top:7px;font-size:6.5px;line-height:1.45;color:var(--muted)}
.urbion-env-risks b{color:var(--warn)}
.urbion-env-foot{margin-top:7px;font-size:5.8px;color:var(--muted);line-height:1.4}
` ;document.head.appendChild(s)}

function render(status='QUERYING',payload=null){
 const host=target();if(!host)return;
 style();host.querySelectorAll('.urbion-env-card[data-owner="canonical"]').forEach(x=>x.remove());
 const card=document.createElement('section');card.className='urbion-env-card';card.dataset.owner='canonical';card.dataset.testid='canonical-live-environment';
 if(!payload){card.innerHTML='<div class="urbion-env-head"><span class="urbion-env-title">LIVE ENVIRONMENT</span><span class="urbion-env-state">QUERYING…</span></div><div class="urbion-env-foot">PLANMalaysia environmental screening is being refreshed from the selected site coordinates.</div>';}else{
   const metrics=Array.isArray(payload.metrics)?payload.metrics:[];
   const flagged=metrics.filter(m=>m?.risk_flag===true);
   const errors=metrics.filter(m=>m?.status==='QUERY_ERROR');
   const screened=metrics.filter(m=>m?.value!==null&&m?.value!==undefined&&m?.status!=='REVIEW_REQUIRED'&&m?.status!=='QUERY_ERROR').length;
   const state=payload.status||status;
   const riskNames=flagged.slice(0,3).map(m=>m.name||m.id).join(' · ');
   const errNames=errors.slice(0,2).map(m=>m.name||m.id).join(' · ');
   card.innerHTML=`<div class="urbion-env-head"><span class="urbion-env-title">LIVE ENVIRONMENT</span><span class="urbion-env-state">${esc(state)}</span></div>
   <div class="urbion-env-grid"><div class="urbion-env-m"><b>${screened}</b><span>SCREENED</span></div><div class="urbion-env-m"><b>${flagged.length}</b><span>RISK FLAGS</span></div><div class="urbion-env-m"><b>${errors.length}</b><span>QUERY ERRORS</span></div></div>
   <div class="urbion-env-risks">${flagged.length?`<b>FLAGGED:</b> ${esc(riskNames)}`:'<b>SCREEN:</b> No live risk flag returned.'}${errors.length?`<br><b>REVIEW:</b> ${esc(errNames)}`:''}</div>
   <div class="urbion-env-foot">${esc(payload.live_query?.provider||'PLANMalaysia DPFDN')} · ${esc(payload.live_query?.radius_m||1000)}m radius · SOURCE_CONTEXT · statutory verification NOT_CLAIMED</div>`;
 }
 host.prepend(card);
}

function mergeIntoCanonical(payload,lat,lon){
 const last=window.URBION_LAST;const p=last?.canonical_evidence_packet;if(!last||!p)return false;
 p.environment=payload;
 p.environment_live_query=payload.live_query||null;
 const gaps=Array.isArray(p.review_gaps)?p.review_gaps.slice():[];
 for(const gap of (Array.isArray(payload.review_gaps)?payload.review_gaps:[])){if(!gaps.includes(gap))gaps.push(gap)}
 p.review_gaps=gaps;
 if(p.result && typeof p.result==='object')p.result.environment=payload;
 last.live_environment_evidence=payload;
 last.environment_site={latitude:lat,longitude:lon};
 last.environment_enriched_at_utc=new Date().toISOString();
 return true;
}

async function enrich(){
 if(busy)return;
 const last=window.URBION_LAST;const p=packet();if(!last||!p)return;
 const lat=Number($('site_lat')?.value);const lon=Number($('site_lon')?.value);
 if(!Number.isFinite(lat)||!Number.isFinite(lon))return;
 const fingerprint=`${String(last)}|${lat.toFixed(6)}|${lon.toFixed(6)}`;
 if(fingerprint===lastFingerprint)return;
 lastFingerprint=fingerprint;busy=true;render('QUERYING');
 try{
   const q=new URLSearchParams({site_lat:String(lat),site_lon:String(lon),state:String($('state')?.value||'Melaka'),radius_m:'1000'});
   const res=await fetch('/environment/live?'+q.toString(),{headers:{Accept:'application/json'},cache:'no-store'});
   if(!res.ok)throw Error('HTTP '+res.status);
   const payload=await res.json();
   if(!mergeIntoCanonical(payload,lat,lon))throw Error('Canonical packet unavailable');
   render(payload.status||'LIVE',payload);
   document.dispatchEvent(new CustomEvent('urbion:environment-ready',{detail:{payload}}));
   try{window.URBION_REVIEW_GAPS?.render?.('LIVE EVIDENCE')}catch(_){}
 }catch(e){
   render('UNAVAILABLE');
   toast('Live environment evidence unavailable; deterministic planning result preserved',false);
 }finally{busy=false}
}

async function boot(){
 for(let i=0;i<180;i++){
   if(packet()){await enrich();}
   await sleep(250);
 }
}
boot().catch(()=>{});
})();

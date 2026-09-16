/* URBION HORIZON — canonical modal + workspace interaction owner. */
(()=>{
'use strict';
if(window.__URBION_MODAL_OWNER_V2__) return;
window.__URBION_MODAL_OWNER_V2__=true;
const $=id=>document.getElementById(id);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

document.addEventListener('click',event=>{
  const target=event.target instanceof Element ? event.target.closest('#closeModal') : null;
  if(!target) return;
  event.preventDefault(); event.stopImmediatePropagation();
  $('modal')?.classList.remove('show');
},true);

function dismissWorkspaceBrief(){const brief=$('urbionWorkspaceBrief');if(brief)brief.remove()}
function installBriefGuard(){
  const styleId='urbion-brief-safety-css';
  if(!$(styleId)){
    const s=document.createElement('style');s.id=styleId;s.textContent='#urbionWorkspaceBrief{display:none!important;pointer-events:none!important}';document.head.appendChild(s)
  }
  dismissWorkspaceBrief();
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',dismissWorkspaceBrief,{once:true});
  else setTimeout(dismissWorkspaceBrief,0);
}

const DEMO={project:'Lot 11213 · Padang Semabok',state:'Melaka',district:'Melaka Tengah',pbt:'Majlis Bandaraya Melaka Bersejarah',lot_no:'11213',project_ref:'URBION-DEMO-11213',development_type:'Commercial Development',development_class:'Commercial',landuse1:'Komersial',landuse2:'Bangunan Sesebuah (free standing)',landuse3:'Kedai',site_area_ha:'1.145',commercial_gfa_m2:'12000',jobs:'150',population:'300',daily_trips:'1200',road_distance_m:'250',flood_exposure:'Requires official verification',nearby_facilities:'transit, school, hospital, utility',perimeter_planting:'3.0',landscaped_pedestrian_walkway:'1.5'};
function setV(id,v){const e=$(id);if(!e)return false;e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));return e.value===String(v)}
function checkV(id,v){const e=$(id);if(!e)return false;e.checked=!!v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));return e.checked===!!v}
async function opt(id,v,n=60){for(let i=0;i<n;i++){const e=$(id);if(e&&[...e.options].some(o=>String(o.value||o.textContent||'')===String(v)))return true;await sleep(50)}return false}
async function loadDemo(){
 Object.entries(DEMO).forEach(([k,v])=>{if(!['district','pbt','landuse2','landuse3'].includes(k))setV(k,v)});setV('state',DEMO.state);await sleep(120);
 if(await opt('district',DEMO.district))setV('district',DEMO.district);await sleep(100);if(await opt('pbt',DEMO.pbt))setV('pbt',DEMO.pbt);
 if(await opt('landuse1',DEMO.landuse1))setV('landuse1',DEMO.landuse1);await sleep(80);if(await opt('landuse2',DEMO.landuse2))setV('landuse2',DEMO.landuse2);await sleep(80);if(await opt('landuse3',DEMO.landuse3))setV('landuse3',DEMO.landuse3);
 checkV('shop_frontage_verified',true);checkV('shop_office_verified',true);const box=$('udcDemoCase');if(box)box.innerHTML='<strong>LIVE DEMO CASE ·</strong> Lot 11213 · Padang Semabok · Melaka Tengah · Melaka · ~1.145 ha · Commercial planning case.<span class="udc-status" id="udcDemoState">DEMO INPUTS LOADED</span><small>Map point remains demo context only; URBION does not claim authoritative parcel geometry here.</small>';return true
}
function mountDemoFallback(){
 if($('urbionDemoCommand'))return true;const host=document.querySelector('.center')||document.querySelector('.layout')||document.body;if(!host)return false;const box=document.createElement('section');box.id='urbionDemoCommand';box.className='urbion-demo-command';box.style.cssText='border:1px solid rgba(47,225,233,.24);border-radius:12px;padding:10px;margin:0 0 8px;background:rgba(3,20,28,.96)';
 box.innerHTML='<div style="font:800 17px Space Grotesk,system-ui,sans-serif;margin-bottom:5px">From <span style="color:var(--cyan)">Site</span> to <span style="color:var(--mint)">Decision</span>.</div><div style="font-size:7px;color:var(--muted);margin-bottom:8px">Planning intelligence workspace · evidence · impact · What-If · Decision Center</div><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px"><button type="button" data-udc="load" style="padding:8px;border:1px solid var(--line);border-radius:7px;background:#061923;color:var(--text);font-size:6.5px;font-weight:800">LOAD DEMO CASE</button><button type="button" data-udc="analysis" style="padding:8px;border:1px solid var(--line);border-radius:7px;background:#061923;color:var(--text);font-size:6.5px;font-weight:800">RUN SITE ANALYSIS</button><button type="button" data-udc="evidence" style="padding:8px;border:1px solid var(--line);border-radius:7px;background:#061923;color:var(--text);font-size:6.5px;font-weight:800">EVIDENCE</button><button type="button" data-udc="whatif" style="padding:8px;border:1px solid var(--line);border-radius:7px;background:#061923;color:var(--text);font-size:6.5px;font-weight:800">TEST WHAT-IF</button><button type="button" data-udc="decision" style="padding:8px;border:1px solid var(--line);border-radius:7px;background:#061923;color:var(--text);font-size:6.5px;font-weight:800">DECISION CENTER</button></div><div id="udcDemoCase" style="margin-top:7px;font-size:6px;color:var(--muted)"><strong>DEMO CASE CONTEXT ·</strong> Lot 11213 · Padang Semabok · Melaka Tengah · Melaka · ~1.145 ha · Commercial planning case.</div>';
 host.insertBefore(box,host.firstElementChild||null);
 box.querySelectorAll('[data-udc]').forEach(b=>b.addEventListener('click',async()=>{const k=b.dataset.udc;if(k==='load')return void loadDemo();if(k==='analysis'){const f=window.URBION_FINAL?.analyse;if(typeof f==='function')return void f();$('run')?.click();return}if(k==='evidence'&&typeof evidenceModal==='function')return evidenceModal();if(k==='whatif'&&typeof whatIfModal==='function')return whatIfModal();if(k==='decision'&&typeof decisionModal==='function')return decisionModal()}));return true
}
async function boot(){installBriefGuard();for(let i=0;i<120;i++){if(mountDemoFallback())return;await sleep(75)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>void boot(),{once:true});else void boot();
})();

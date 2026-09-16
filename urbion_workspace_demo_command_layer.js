/* URBION HORIZON — judge/demo narrative layer for the canonical V5 workspace.
   Presentation only: reuses existing analysis, GIS, evidence, What-If and Decision
   Center owners. No duplicate scoring engine, no fabricated evidence. */
(()=>{
'use strict';
if(window.__URBION_DEMO_COMMAND_LAYER_V1__)return;
window.__URBION_DEMO_COMMAND_LAYER_V1__=true;
const $=id=>document.getElementById(id);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const esc=v=>String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));

const DEMO_CASE={
  project:'Lot 11213 · Padang Semabok',
  state:'Melaka',
  district:'Melaka Tengah',
  pbt:'Majlis Bandaraya Melaka Bersejarah',
  lot_no:'11213',
  project_ref:'URBION-DEMO-11213',
  development_type:'Commercial Development',
  development_class:'Commercial',
  landuse1:'Komersial',
  landuse2:'Bangunan Sesebuah (free standing)',
  landuse3:'Kedai'
};

const DEMO_SCENARIOS=[
  {name:'Baseline Commercial',tag:'BASELINE',id:'DEMO-BASE'},
  {name:'Controlled Intensity',tag:'OPTION A',id:'DEMO-A'},
  {name:'Reduced GFA',tag:'OPTION B',id:'DEMO-B'},
  {name:'Access-First Test',tag:'OPTION C',id:'DEMO-C'},
  {name:'Evidence Review Stress Test',tag:'REVIEW',id:'DEMO-R'}
];

function style(){
 if($('urbionDemoCommandStyle'))return;
 const s=document.createElement('style');s.id='urbionDemoCommandStyle';s.textContent=`
.urbion-demo-command{border:1px solid rgba(47,225,233,.24);border-radius:12px;background:linear-gradient(145deg,rgba(8,31,43,.98),rgba(3,15,22,.99));padding:12px;margin:0 0 8px;box-shadow:0 12px 32px rgba(0,0,0,.18)}
.light .urbion-demo-command{background:#fff}.udc-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}.udc-kicker{font-size:7px;color:var(--mint);font-weight:900;letter-spacing:.14em}.udc-title{font:800 18px Space Grotesk,system-ui,sans-serif;margin-top:3px}.udc-title em{font-style:normal;color:var(--cyan)}.udc-copy{font-size:7.2px;color:var(--muted);line-height:1.5;max-width:820px;margin-top:4px}.udc-badge{font-size:5.8px;color:var(--cyan);border:1px solid rgba(47,225,233,.28);border-radius:999px;padding:5px 7px;white-space:nowrap}.udc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:9px}.udc-item{border:1px solid rgba(45,85,100,.22);border-radius:8px;padding:8px;background:rgba(255,255,255,.018)}.udc-item b{display:block;font-size:6.8px}.udc-item span{display:block;font-size:6px;color:var(--muted);line-height:1.45;margin-top:3px}.udc-flow{display:flex;align-items:center;gap:4px;margin-top:9px;overflow:auto;padding-bottom:1px}.udc-step{flex:1;min-width:82px;padding:7px 8px;border:1px solid rgba(47,225,233,.15);border-radius:7px;background:rgba(47,225,233,.025)}.udc-step b{display:block;color:var(--cyan);font-size:5.8px;letter-spacing:.06em}.udc-step span{display:block;font-size:5.8px;color:var(--muted);margin-top:2px}.udc-arrow{font-size:8px;color:#46616d}.udc-actions{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:9px}.udc-action{border:1px solid var(--line);border-radius:7px;background:#061923;color:var(--text);padding:8px;font-size:6.2px;font-weight:800;text-align:left}.light .udc-action{background:#f4f9fa}.udc-action:hover{border-color:rgba(47,225,233,.45);background:rgba(47,225,233,.06)}.udc-action span{font-size:5.4px;color:var(--muted);font-weight:500}.udc-action.primary-demo{border-color:rgba(88,232,196,.34);background:linear-gradient(100deg,rgba(88,232,196,.12),rgba(47,225,233,.08))}.udc-case{margin-top:8px;padding:8px 9px;border-left:2px solid var(--mint);background:rgba(88,232,196,.035);font-size:6px;color:var(--muted);line-height:1.45}.udc-case strong{color:var(--text)}.udc-case small{display:block;margin-top:3px;color:var(--muted);font-size:5.4px}.udc-status{display:inline-flex;margin-left:6px;padding:3px 5px;border-radius:5px;border:1px solid rgba(88,232,196,.28);color:var(--good);font-size:5.2px;font-weight:800;letter-spacing:.04em}.udc-scenarios{margin-top:8px;border-top:1px solid rgba(45,85,100,.16);padding-top:8px}.udc-scenarios-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}.udc-scenarios-head b{font-size:6.4px;letter-spacing:.08em}.udc-scenarios-head span{font-size:5.6px;color:var(--muted)}.udc-scenario-row{display:grid;grid-template-columns:1fr auto;gap:7px;padding:5px 0;border-bottom:1px solid rgba(45,85,100,.12)}.udc-scenario-row b{font-size:6.2px}.udc-scenario-row span{font-size:5.4px;color:var(--muted)}
@media(max-width:1100px){.udc-grid{grid-template-columns:1fr 1fr}.udc-actions{grid-template-columns:1fr 1fr 1fr}.udc-title{font-size:17px}}@media(max-width:700px){.udc-head{display:block}.udc-badge{display:inline-flex;margin-top:6px}.udc-grid,.udc-actions{grid-template-columns:1fr}.udc-flow{display:grid;grid-template-columns:1fr 1fr}.udc-arrow{display:none}}
`;
 document.head.appendChild(s)
}

function toast(message,ok=true){const t=$('toast');if(!t)return;t.textContent=message;t.style.display='block';t.style.color=ok?'var(--good)':'var(--warn)';clearTimeout(window.__urbionDemoToast);window.__urbionDemoToast=setTimeout(()=>t.style.display='none',2800)}

function setValue(id,value){
 const el=$(id);if(!el)return false;
 el.value=String(value);
 el.dispatchEvent(new Event('input',{bubbles:true}));
 el.dispatchEvent(new Event('change',{bubbles:true}));
 return el.value===String(value)
}

async function waitForOption(id,value,tries=50){
 for(let i=0;i<tries;i++){
  const el=$(id);
  if(el&&[...el.options].some(o=>String(o.value||o.textContent||'')===String(value)))return true;
  await sleep(80)
 }
 return false
}

async function loadDemoCase(){
 toast('Loading canonical demo case…');
 const okProject=setValue('project',DEMO_CASE.project);
 const okState=setValue('state',DEMO_CASE.state);
 await sleep(120);
 const okDistrictOption=await waitForOption('district',DEMO_CASE.district,40);
 const okDistrict=okDistrictOption&&setValue('district',DEMO_CASE.district);
 await sleep(120);
 const okPbtOption=await waitForOption('pbt',DEMO_CASE.pbt,40);
 const okPbt=okPbtOption&&setValue('pbt',DEMO_CASE.pbt);
 const okLot=setValue('lot_no',DEMO_CASE.lot_no);
 const okRef=setValue('project_ref',DEMO_CASE.project_ref);
 const okDev=setValue('development_type',DEMO_CASE.development_type);
 const okClass=setValue('development_class',DEMO_CASE.development_class);
 const okL1Option=await waitForOption('landuse1',DEMO_CASE.landuse1,40);
 const okL1=okL1Option&&setValue('landuse1',DEMO_CASE.landuse1);
 await sleep(80);
 const okL2Option=await waitForOption('landuse2',DEMO_CASE.landuse2,40);
 const okL2=okL2Option&&setValue('landuse2',DEMO_CASE.landuse2);
 await sleep(80);
 const okL3Option=await waitForOption('landuse3',DEMO_CASE.landuse3,40);
 const okL3=okL3Option&&setValue('landuse3',DEMO_CASE.landuse3);
 ['site_lat','site_lon','tod_lat','tod_lon'].forEach(id=>$(id)?.dispatchEvent(new Event('input',{bubbles:true})));
 const ready=[okProject,okState,okDistrict,okPbt,okLot,okRef,okDev,okClass,okL1,okL2,okL3].every(Boolean);
 if(ready){updateLoadedState();toast('Demo case loaded · ready for analysis');return true}
 toast('Demo case could not fully hydrate; complete the highlighted case fields before analysis',false);
 return false;
}

function updateLoadedState(){
 const caseBox=$('udcDemoCase');
 if(caseBox)caseBox.innerHTML='<strong>LIVE DEMO CASE ·</strong> Lot 11213 · Padang Semabok · Melaka Tengah · Melaka · ~1.145 ha · Commercial planning case.<span class="udc-status" id="udcDemoState">DEMO INPUTS LOADED</span><small>Map point remains demo context only; URBION does not claim authoritative parcel geometry here. Planning inputs can be traced through the evidence packet after analysis.</small>';
}

function clickCore(kind){
 if(kind==='load'){void loadDemoCase();return true;}
 if(kind==='analysis'){
  const b=$('run');
  if(b){b.click();return true}
  if(window.URBION_FINAL?.analyse){void window.URBION_FINAL.analyse();return true}
 }
 if(kind==='evidence'){
  if(typeof evidenceModal==='function'){evidenceModal();return true}
  const b=[...document.querySelectorAll('button')].find(x=>/view evidence|evidence summary/i.test(x.textContent||''));if(b){b.click();return true}
 }
 if(kind==='whatif'){
  if(typeof whatIfModal==='function'){void whatIfModal();return true}
  if(window.URBION_FINAL?.whatif){window.URBION_FINAL.whatif();return true}
 }
 if(kind==='decision'){
  if(typeof decisionModal==='function'){void decisionModal();return true}
  if(window.URBION_FINAL?.decision){void window.URBION_FINAL.decision();return true}
 }
 return false
}

function renderScenarios(host){
 const box=document.createElement('div');box.className='udc-scenarios';
 box.innerHTML='<div class="udc-scenarios-head"><b>DEMO SCENARIO TESTS</b><span>Deterministic showcase inputs</span></div>'+DEMO_SCENARIOS.map(x=>`<div class="udc-scenario-row"><b>${esc(x.name)}</b><span>${esc(x.tag)} · ${esc(x.id)}</span></div>`).join('');
 host.appendChild(box)
}

function mount(){
 const center=document.querySelector('.center');if(!center||$('urbionDemoCommand'))return false;
 style();
 const box=document.createElement('section');box.id='urbionDemoCommand';box.className='urbion-demo-command';
 box.innerHTML=`<div class="udc-head"><div><div class="udc-kicker">URBION HORIZON · PLANNING INTELLIGENCE WORKSPACE</div><div class="udc-title">From <em>Site</em> to <em>Decision</em>.</div><div class="udc-copy">An AI-assisted spatial planning decision-support workflow that connects location, GIS evidence, planning rules, development impact, scenario testing and explainable decision support in one workspace.</div></div><span class="udc-badge">DECISION SUPPORT · NOT STATUTORY APPROVAL</span></div><div class="udc-grid"><div class="udc-item"><b>WHAT IS URBION?</b><span>Connects people, places, policies and spatial evidence for clearer planning analysis.</span></div><div class="udc-item"><b>OBJECTIVE</b><span>Turn fragmented planning inputs into an evidence-aware, traceable planning workflow.</span></div><div class="udc-item"><b>CAPABILITIES</b><span>GIS · site analysis · policy/rules · impact screening · AI narrative · What-If · Decision Center.</span></div><div class="udc-item"><b>OUTPUT</b><span>Explainable findings, evidence trace, review gaps and planner handoff — not authority approval.</span></div></div><div class="udc-flow"><div class="udc-step"><b>01 · SITE</b><span>Case + location</span></div><i class="udc-arrow">→</i><div class="udc-step"><b>02 · SPATIAL</b><span>GIS + site intelligence</span></div><i class="udc-arrow">→</i><div class="udc-step"><b>03 · EVIDENCE</b><span>Sources + constraints</span></div><i class="udc-arrow">→</i><div class="udc-step"><b>04 · ASSESS</b><span>Rules + compliance</span></div><i class="udc-arrow">→</i><div class="udc-step"><b>05 · WHAT-IF</b><span>Test alternatives</span></div><i class="udc-arrow">→</i><div class="udc-step"><b>06 · DECIDE</b><span>Explain + review</span></div></div><div class="udc-actions"><button class="udc-action primary-demo" data-udc="load">✦ LOAD DEMO CASE<br><span>Lot 11213 · ready the canonical inputs</span></button><button class="udc-action" data-udc="analysis">▶ RUN SITE ANALYSIS<br><span>Use the canonical analysis owner</span></button><button class="udc-action" data-udc="evidence">◈ EVIDENCE<br><span>Trace source + review gaps</span></button><button class="udc-action" data-udc="whatif">◇ TEST WHAT-IF<br><span>Compare planning options</span></button><button class="udc-action" data-udc="decision">◆ DECISION CENTER<br><span>Review explainable output</span></button></div><div class="udc-case" id="udcDemoCase"><strong>DEMO CASE CONTEXT ·</strong> Lot 11213 · Padang Semabok · Melaka Tengah · Melaka · ~1.145 ha · Commercial planning case.<small>Map point remains demo context only; use the case builder and authoritative spatial layers to drive analysis. No parcel geometry is fabricated.</small></div>`;
 center.insertBefore(box,center.firstElementChild||null);
 renderScenarios(box);
 box.querySelectorAll('[data-udc]').forEach(b=>b.addEventListener('click',()=>{const ok=clickCore(b.dataset.udc);if(!ok)toast('Canonical '+b.dataset.udc+' function is not ready yet',false)}));
 return true
}

async function boot(){for(let i=0;i<100;i++){if(mount())return;await sleep(100)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>void boot(),{once:true});else void boot();
})();

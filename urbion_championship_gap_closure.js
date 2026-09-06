(()=>{
'use strict';
if(window.__URBION_GAP_CLOSURE__)return;
window.__URBION_GAP_CLOSURE__=true;

const $=s=>document.querySelector(s);
const $$=s=>Array.from(document.querySelectorAll(s));
const esc=v=>String(v??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
const read=id=>String($('#fcc-'+id)?.value||'').trim();
const lang=()=>localStorage.getItem('urbion-lang')||'en';
const tx=(en,bm)=>lang()==='bm'?bm:en;
function casePayload(){
 const s=window.__URBION_UNIFIED_STATE||{};
 return {
   project_name:read('project_name'),
   lat:read('lat'),lon:read('lon'),state:read('state'),pbt:read('pbt'),district:read('district'),
   lot:read('lot'),project_reference:read('project_reference'),landuse:read('landuse'),category:read('category'),
   activity:read('activity'),development:read('development'),ratio:read('ratio'),todlat:read('todlat'),todlon:read('todlon'),
   unified_state:s
 };
}
function upsertStyle(){
 if($('#urbion-gap-style'))return;
 const st=document.createElement('style');st.id='urbion-gap-style';st.textContent=`
 #urbion-gap-closure{margin:0 16px 18px;display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:12px;position:relative;z-index:5}
 .gap-card{border:1px solid rgba(112,225,207,.18);background:linear-gradient(145deg,rgba(13,31,43,.96),rgba(8,20,31,.96));border-radius:14px;padding:14px;box-shadow:0 12px 30px rgba(0,0,0,.18)}
 body.fcc-light .gap-card{background:#fff;border-color:#d9e8ec;box-shadow:0 8px 24px rgba(12,40,56,.08)}
 .gap-kicker{font:700 10px/1 Inter,system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#55dec1}
 .gap-card h3{margin:7px 0 4px;font-size:16px}.gap-card p{margin:0 0 10px;font-size:11px;line-height:1.45;opacity:.72}
 .gap-actions{display:flex;flex-wrap:wrap;gap:7px}.gap-btn{appearance:none;border:1px solid rgba(83,221,195,.28);background:rgba(27,194,173,.08);color:inherit;border-radius:9px;padding:7px 9px;font:700 10px/1 Inter,system-ui,sans-serif;cursor:pointer}.gap-btn:hover,.gap-btn:focus-visible{border-color:#53ddc3;outline:none}.gap-result{margin-top:10px;font-size:10px;line-height:1.45;max-height:170px;overflow:auto}.gap-pill{display:inline-flex;align-items:center;gap:4px;margin:2px 4px 2px 0;padding:4px 6px;border-radius:999px;background:rgba(83,221,195,.08);border:1px solid rgba(83,221,195,.14)}
 @media(max-width:1100px){#urbion-gap-closure{grid-template-columns:1fr}}`;
 document.head.appendChild(st);
}
function insertSurface(){
 const root=$('#urbion-final-command-centre'); if(!root||$('#urbion-gap-closure'))return false;
 const host=$('.fcc-main',root)||root;
 const wrap=document.createElement('section');wrap.id='urbion-gap-closure';
 wrap.innerHTML=`
 <article class="gap-card"><div class="gap-kicker">01 · ${esc(tx('INTELLIGENCE','KECERDASAN'))}</div><h3>${esc(tx('Explain This Case','Terangkan Kes Ini'))}</h3><p>${esc(tx('AI-backed explanation using the existing assessment/case evidence chain. Planner support only — not statutory approval.','Penjelasan berasaskan AI menggunakan rantaian bukti/penilaian sedia ada. Sokongan perancang sahaja — bukan kelulusan statutori.'))}</p><div class="gap-actions"><button class="gap-btn" id="gap-ai">${esc(tx('AI EXPLAIN','TERANGKAN DENGAN AI'))}</button><button class="gap-btn" id="gap-stations">${esc(tx('STATION / MOBILITY','STESEN / MOBILITI'))}</button></div><div class="gap-result" id="gap-ai-result">${esc(tx('Ready when a case is defined.','Sedia selepas kes ditakrifkan.'))}</div></article>
 <article class="gap-card"><div class="gap-kicker">02 · ${esc(tx('JUDGE VIEW','PANDANGAN JURI'))}</div><h3>${esc(tx('90-Second Decision Story','Cerita Keputusan 90 Saat'))}</h3><p>${esc(tx('Dedicated judge surface linked to the existing judge-mode contract.','Paparan khas juri yang dipautkan kepada kontrak judge-mode sedia ada.'))}</p><div class="gap-actions"><button class="gap-btn" id="gap-judge">${esc(tx('OPEN JUDGE VIEW','BUKA PAPARAN JURI'))}</button></div><div class="gap-result" id="gap-judge-result">${esc(tx('Evidence → Score → Why → Decision → Action','Bukti → Skor → Sebab → Keputusan → Tindakan'))}</div></article>
 <article class="gap-card"><div class="gap-kicker">03 · ${esc(tx('PACKAGE','PAKEJ KES'))}</div><h3>${esc(tx('Unified Case Package','Pakej Kes Bersepadu'))}</h3><p>${esc(tx('Export the complete orchestration state and explicit authority boundary for review/audit.','Eksport keseluruhan keadaan orkestrasi dan sempadan kuasa secara jelas untuk semakan/audit.'))}</p><div class="gap-actions"><button class="gap-btn" id="gap-export">${esc(tx('EXPORT UNIFIED PACKAGE','EKSPORT PAKEJ BERSEPADU'))}</button><button class="gap-btn" id="gap-cascade">${esc(tx('REFRESH CASCADE','SEGARKAN RANTAian INPUT'))}</button></div><div class="gap-result" id="gap-package-result">${esc(tx('Package ready for export after analysis.','Pakej sedia dieksport selepas analisis.'))}</div></article>`;
 const tabs=$('#fcc-tabs',root)||$('.fcc-tabs',root);
 if(tabs?.parentElement)tabs.parentElement.insertAdjacentElement('afterend',wrap); else host.prepend(wrap);
 return true;
}
function setResult(id,text){const e=$('#'+id);if(e)e.textContent=text}
function getUnified(){return window.__URBION_UNIFIED_STATE||{}};
async function aiExplain(){
 const p=casePayload();setResult('gap-ai-result',tx('Running AI explanation…','Menjalankan penjelasan AI…'));
 try{
   const res=await fetch('/copilot/run',{method:'POST',headers:{'content-type':'application/json','cache-control':'no-cache'},body:JSON.stringify(p)});
   const data=await res.json();
   if(!res.ok)throw new Error(data?.detail?.message||data?.detail||'AI endpoint unavailable');
   const insights=[];
   const spatial=data.spatial||{};const assess=data.assessment||data.assessments||{};const rec=data.recommendations||data.recommendation||{};
   if(spatial.network_access?.distance_m!=null)insights.push(`${tx('Network context','Konteks rangkaian')}: ${Number(spatial.network_access.distance_m).toFixed(0)} m`);
   if(assess)insights.push(JSON.stringify(assess).slice(0,700));
   if(rec)insights.push(JSON.stringify(rec).slice(0,700));
   if(!insights.length)insights.push(JSON.stringify(data).slice(0,1200));
   setResult('gap-ai-result',insights.join(' · '));
 }catch(err){setResult('gap-ai-result',tx(`AI explain unavailable: ${err.message}`,
   `Penjelasan AI tidak tersedia: ${err.message}`));}
}
async function stationExplain(){
 const lat=read('lat'),lon=read('lon'),state=read('state');
 if(!lat||!lon){setResult('gap-ai-result',tx('Enter site coordinates first.','Masukkan koordinat tapak dahulu.'));return}
 setResult('gap-ai-result',tx('Loading live station intelligence…','Memuatkan kecerdasan stesen langsung…'));
 try{
  const res=await fetch(`/station-intelligence?site_lat=${encodeURIComponent(lat)}&site_lon=${encodeURIComponent(lon)}&state=${encodeURIComponent(state)}`,{cache:'no-store'});
  const data=await res.json(); if(!res.ok)throw new Error(data?.detail?.message||'Station endpoint unavailable');
  const n=data.nearest||{};const lcp=data.lcp_snapshot||{};const gaps=data.review_gaps||[];
  setResult('gap-ai-result',`${tx('Nearest','Terdekat')}: ${esc(n.name||n.station_name||'—')} · ${n.distance_m!=null?Number(n.distance_m).toFixed(0)+' m':'—'} · ${tx('LCP','LCP')}: ${JSON.stringify(lcp).slice(0,500)} · ${tx('Review gaps','Jurang semakan')}: ${JSON.stringify(gaps).slice(0,500)}`);
 }catch(err){setResult('gap-ai-result',tx(`Station intelligence unavailable: ${err.message}`,`Kecerdasan stesen tidak tersedia: ${err.message}`));}
}
async function judgeView(){
 setResult('gap-judge-result',tx('Loading judge story…','Memuatkan cerita juri…'));
 try{
  const res=await fetch('/judge-mode',{cache:'no-store'}); const data=await res.json(); if(!res.ok)throw new Error(data?.detail||'Judge endpoint unavailable');
  const text=[`v${data.version}`,`${data.scenario_count} scenarios`,data.decision_boundary, data.statutory_verification].filter(Boolean).join(' · ');
  setResult('gap-judge-result',`${text} · ${tx('Open full judge surface','Buka paparan juri penuh')}: /judge-mode`);
 }catch(err){setResult('gap-judge-result',tx(`Judge view unavailable: ${err.message}`,`Paparan juri tidak tersedia: ${err.message}`));}
}
function fullPackage(){
 const s=getUnified(), p=casePayload();
 const pkg={
  schema:'urbion-horizon-unified-case-package',schema_version:'1.0.0',release:'MASTER-132',engine:'PHASE-E.8',frontend_release:'MASTER-331',
  exported_at:new Date().toISOString(),
  case:p,
  assessment:s.assessment??null,
  spatial_context:s.spatial??null,
  evidence:{spatial_summary:s.spatialSummary??null,layers:s.spatial?.layers??[],lot:s.lot??null},
  policy_guideline:s.km?.policy_guideline??s.assessment?.policy_guideline??null,
  policy_graph:s.km?.policy_graph??null,
  recommendations:s.assessment?.recommendations??s.lcp?.recommendations??null,
  agency_intelligence:s.km?.agency_intelligence??s.km?.agencies??null,
  km_readiness:s.km??null,
  what_if:s.whatIf??null,
  decision:s.decision??null,
  lcp_intelligence:s.lcp??null,
  evidence_gaps:(s.lcp?.evidence_gaps??s.assessment?.evidence_gaps??s.spatial?.evidence_gaps??[]),
  authority_boundary:{planner_decision_support_only:true,statutory_verification:'NOT_CLAIMED',cadastral_authority:'JUPEM / relevant PBT verification',source_context_is_not_statutory_verification:true},
  next_authority_action:s.decision?.next_authority_action??s.km?.next_authority_action??'Confirm current PBT/OSC requirements and statutory verification before submission.'
 };
 const blob=new Blob([JSON.stringify(pkg,null,2)],{type:'application/json'}); const url=URL.createObjectURL(blob); const a=document.createElement('a');a.href=url;a.download='urbion-horizon-unified-case-package.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 setResult('gap-package-result',tx('Unified package exported.','Pakej bersepadu telah dieksport.'));
}
const cascade={
 Residential:{categories:['New Development','Redevelopment','Infill Development','Urban Regeneration','Subdivision / Consolidation'],activities:['Housing'],proposals:['Residential Development','Urban Regeneration / Infill']},
 Commercial:{categories:['New Development','Redevelopment','Infill Development','Urban Regeneration','Change of Use'],activities:['Retail / Commercial','Office'],proposals:['Commercial Development','TOD Development / Mixed Use','Urban Regeneration / Infill']},
 'Mixed Use':{categories:['New Development','Redevelopment','Infill Development','Urban Regeneration'],activities:['Mixed Activity','Retail / Commercial','Office','Housing','Hospitality / Tourism'],proposals:['TOD Development / Mixed Use','Urban Regeneration / Infill']},
 Institutional:{categories:['New Development','Redevelopment','Change of Use'],activities:['Institution / Education'],proposals:['Institutional Development']},
 'Recreation / Tourism':{categories:['New Development','Redevelopment','Infill Development','Urban Regeneration'],activities:['Hospitality / Tourism','Recreation'],proposals:['Recreation / Tourism','TOD Development / Mixed Use']},
 Industrial:{categories:['New Development','Redevelopment','Infill Development','Subdivision / Consolidation'],activities:['Industrial / Logistics'],proposals:['Commercial Development']},
 'Transport / Infrastructure':{categories:['New Development','Redevelopment','Infrastructure / Transport'],activities:['Recreation','Mixed Activity'],proposals:['Infrastructure / Mobility']},
 'Open Space / Green':{categories:['New Development','Redevelopment','Change of Use'],activities:['Recreation'],proposals:['Recreation / Tourism']},
 Agriculture:{categories:['New Development','Change of Use','Subdivision / Consolidation'],activities:['Mixed Activity'],proposals:['Infrastructure / Mobility']}
};
function options(sel,items,keep){const cur=sel.value; sel.innerHTML=`<option value="">${sel.id.includes('category')?'Select category':sel.id.includes('activity')?'Select activity':'Select proposal'}</option>`+items.map(x=>`<option>${esc(x)}</option>`).join('');if(keep&&items.includes(cur))sel.value=cur;}
function applyCascade(){const lu=read('landuse'),c=$('#fcc-category'),a=$('#fcc-activity'),d=$('#fcc-development');const cfg=cascade[lu];if(!cfg||!c||!a||!d)return;options(c,cfg.categories,true);options(a,cfg.activities,true);options(d,cfg.proposals,true);}
function bind(){
 const lu=$('#fcc-landuse');if(lu&&!lu.dataset.gapCascade){lu.dataset.gapCascade='1';lu.addEventListener('change',()=>{applyCascade();window.dispatchEvent(new CustomEvent('urbion:inputs-change',{detail:{inputs:casePayload()}}))});applyCascade()}
 $('#gap-ai')?.addEventListener('click',aiExplain);$('#gap-stations')?.addEventListener('click',stationExplain);$('#gap-judge')?.addEventListener('click',judgeView);$('#gap-export')?.addEventListener('click',fullPackage);$('#gap-cascade')?.addEventListener('click',()=>{applyCascade();setResult('gap-package-result',tx('Input cascade refreshed from Land Use Type.','Rantaian input disegarkan berdasarkan Jenis Guna Tanah.'))});
}
function boot(){upsertStyle();if(insertSurface()){bind()}else setTimeout(()=>{if(insertSurface())bind()},500)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();

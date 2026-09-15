(()=>{
'use strict';
if(window.__URBION_DEVELOPMENT_IMPACT_OWNER_V5__)return;
window.__URBION_DEVELOPMENT_IMPACT_OWNER_V5__=true;
function packet(){return window.URBION_LAST?.canonical_evidence_packet||null}
function impactFromPacket(p){return p?.evidence?.development_impact||p?.development_impact||null}
function esc(v){return String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]))}
function host(){return document.querySelector('.right')||document.querySelector('.layout > :last-child')}
function mount(){
 const p=packet(),root=host(); if(!root)return false;
 const impact=impactFromPacket(p);
 let card=root.querySelector('[data-testid="development-impact"]');
 if(!card){
  card=document.createElement('section');
  card.className='urbion-live-card urbion-development-impact-card card';
  card.setAttribute('data-testid','development-impact');
  card.dataset.owner='canonical';
  root.appendChild(card);
 }
 const domains=['physical','social','economic'];
 const summary=impact&&typeof impact==='object'?(impact.impact_summary||{}):{};
 const rows=domains.map(d=>{
  const s=summary[d]||{};
  const state=!impact?'WAITING':(s.review_required?'REVIEW':'READY');
  const stateClass=state==='READY'?'ok':'warn';
  return `<div class="urbion-impact-row"><span class="urbion-impact-domain">${esc(d.toUpperCase())}</span><span class="urbion-impact-count">${Number(s.metric_count||0)} metrics</span><span class="urbion-impact-state ${stateClass}">${state}</span></div>`;
 }).join('');
 const gaps=impact&&Array.isArray(impact.review_gaps)?impact.review_gaps:[];
 const state=impact?.statutory_verification||'NOT_CLAIMED';
 const foot=impact?(gaps.length?`${gaps.length} review gap${gaps.length===1?'':'s'}`:'No open impact gaps'):'Run analysis to populate impact screening';
 const next=`<style>
 .urbion-development-impact-card .impact-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
 .urbion-development-impact-card .impact-head h3{margin:0;font-size:8px;letter-spacing:.07em}
 .urbion-development-impact-card .impact-sub{font-size:6.3px;color:var(--muted);margin-bottom:7px}
 .urbion-development-impact-card .impact-grid{display:grid;grid-template-columns:1fr;gap:4px}
 .urbion-development-impact-card .urbion-impact-row{display:grid;grid-template-columns:1fr auto auto;gap:7px;align-items:center;padding:5px 6px;border:1px solid rgba(45,85,100,.22);border-radius:7px;background:rgba(255,255,255,.012)}
 .urbion-development-impact-card .urbion-impact-domain{font-size:6.8px;font-weight:800;letter-spacing:.05em}
 .urbion-development-impact-card .urbion-impact-count{font-size:6.2px;color:var(--muted)}
 .urbion-development-impact-card .urbion-impact-state{font-size:5.8px;font-weight:800;letter-spacing:.04em;padding:3px 5px;border-radius:5px;border:1px solid rgba(255,203,93,.25)}
 .urbion-development-impact-card .urbion-impact-state.ok{color:var(--good);border-color:rgba(72,223,170,.28)}
 .urbion-development-impact-card .urbion-impact-state.warn{color:var(--warn);border-color:rgba(255,203,93,.25)}
 .urbion-development-impact-card .impact-foot{display:flex;justify-content:space-between;gap:8px;margin-top:6px;font-size:5.8px;color:var(--muted)}
 </style>
 <div class="impact-head"><h3>DEVELOPMENT IMPACT</h3><span class="tiny">DECISION SUPPORT</span></div>
 <div class="impact-sub">Physical · Social · Economic screening</div>
 <div class="impact-grid">${rows}</div>
 <div class="impact-foot"><span>${esc(foot)}</span><span>${esc(state)}</span></div>`;
 if(card.innerHTML!==next)card.innerHTML=next;
 return true;
}
function ensure(){
 if(mount())return;
 const root=host();
 if(!root)return;
 if(!window.__URBION_DEVELOPMENT_IMPACT_OBSERVER_V6__){
  const observer=new MutationObserver(()=>{
   if(mount())observer.disconnect();
  });
  window.__URBION_DEVELOPMENT_IMPACT_OBSERVER_V6__=observer;
  observer.observe(root,{childList:true});
 }
 let tries=0;
 const timer=setInterval(()=>{if(mount()&&impactFromPacket(packet()))clearInterval(timer);if(++tries>=300)clearInterval(timer)},100);
}
window.addEventListener('urbion:assessment-ready',ensure);
window.addEventListener('urbion:environment-ready',ensure);
window.addEventListener('urbion:mobility-ready',ensure);
window.addEventListener('urbion:workspace-ready',ensure);
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ensure,{once:true});else ensure();
})();

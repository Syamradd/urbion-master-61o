(()=>{
'use strict';
if(window.__URBION_DEVELOPMENT_IMPACT_OWNER_V5__)return;
window.__URBION_DEVELOPMENT_IMPACT_OWNER_V5__=true;
function packet(){return window.URBION_LAST?.canonical_evidence_packet||null}
function impactFromPacket(p){return p?.evidence?.development_impact||p?.development_impact||null}
function esc(v){return String(v??'').replace(/[&<>\\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;'}[c]))}
function host(){return document.querySelector('.right')||document.querySelector('.layout > :last-child')}
function mount(){
 const p=packet(),root=host(); if(!root)return false;
 let impact=impactFromPacket(p);
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
 const rows=domains.map(d=>{const s=summary[d]||{};return `<div class="rg-row"><span>${esc(d.toUpperCase())}</span><strong>${Number(s.metric_count||0)} metrics</strong><em>${s.review_required?'REVIEW REQUIRED':impact?'SCREENED':'REVIEW REQUIRED'}</em></div>`}).join('');
 const gaps=impact&&Array.isArray(impact.review_gaps)?impact.review_gaps:[];
 const state=impact?.statutory_verification||'NOT_CLAIMED';
 const next=`<div class="cardhead"><h3>DEVELOPMENT IMPACT</h3><span class="tiny">DECISION SUPPORT</span></div><div class="tiny" style="margin-bottom:7px">Physical · Social · Economic screening</div>${rows}<div class="tiny" style="margin-top:7px">${impact?(gaps.length?`${gaps.length} input/review gap(s)`:'No open impact gaps'):'Impact packet pending — review required'} · ${esc(state)}</div>`;
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
  // This owner only needs to recover if its card has not mounted yet. Once
  // mounted, disconnect so unrelated right-panel mutations cannot wake it.
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

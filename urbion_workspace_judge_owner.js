/* URBION HORIZON — canonical judge/reviewer decision snapshot owner.
   Read-only presentation over window.URBION_LAST.canonical_evidence_packet.
   No scoring, ranking, approval, or statutory decision logic is introduced here. */
(()=>{
'use strict';
if(window.__URBION_JUDGE_OWNER_V1__) return;
window.__URBION_JUDGE_OWNER_V1__=true;
const $=id=>document.getElementById(id);
const packet=()=>window.URBION_LAST?.canonical_evidence_packet||null;
const esc=s=>String(s??'').replace(/[&<>\"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[m]));
const reviewCount=p=>Array.isArray(p?.review_gaps)?p.review_gaps.length:Number(p?.review_required||0)||0;
function evidenceCounts(p){
 const counts={VERIFIED:0,SOURCE_CONTEXT:0,CALCULATED:0,USER_PROVIDED:0,UNVERIFIED:0};
 const states=p?.evidence_states||{};
 Object.values(states).forEach(v=>{const s=String(v||'UNVERIFIED').toUpperCase();if(counts[s]!=null)counts[s]+=1;});
 const ledger=p?.evidence_ledger||{};
 if(!Object.values(states).length){
  for(const k of Object.keys(counts)){const v=Number(ledger[(k||'').toLowerCase()]||0);if(Number.isFinite(v))counts[k]=v}
 }
 return counts;
}
function style(){
 if($('urbionJudgeStyleV1'))return;
 const s=document.createElement('style');s.id='urbionJudgeStyleV1';s.textContent=`
 #urbionJudgeCard{border:1px solid rgba(47,225,233,.20);border-radius:10px;background:linear-gradient(145deg,rgba(7,29,41,.96),rgba(3,15,22,.98));padding:10px;margin-bottom:8px}.light #urbionJudgeCard{background:#fff}
 .uj-head{display:flex;justify-content:space-between;align-items:center;gap:8px}.uj-title{font-size:8px;font-weight:900;letter-spacing:.08em}.uj-state{font-size:6px;padding:4px 6px;border-radius:999px;border:1px solid rgba(47,225,233,.28);color:var(--cyan)}
 .uj-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px}.uj-metric{padding:7px;border:1px solid var(--line);border-radius:8px}.uj-metric span{display:block;color:var(--muted);font-size:5.8px}.uj-metric b{display:block;margin-top:3px;font:800 11px Space Grotesk,system-ui,sans-serif}
 .uj-note{margin-top:8px;padding:8px;border:1px solid rgba(255,203,93,.20);border-radius:8px;background:rgba(255,203,93,.035);font-size:6.4px;line-height:1.5;color:var(--muted)}.uj-note strong{color:var(--warn)}
 .uj-boundary{margin-top:7px;padding-top:7px;border-top:1px solid rgba(45,85,100,.16);font-size:6px;color:var(--muted)}
 @media(max-width:700px){.uj-grid{grid-template-columns:1fr 1fr}}
 `;document.head.appendChild(s)
}
function render(){
 const p=packet();if(!p)return false;
 const host=document.querySelector('.right')||document.querySelector('.layout > :last-child');if(!host)return false;
 style();
 let card=$('urbionJudgeCard');
 if(!card){card=document.createElement('section');card.id='urbionJudgeCard';card.dataset.owner='canonical';host.prepend(card)}
 const gaps=reviewCount(p),c=evidenceCounts(p),ready=gaps===0;
 const site=p.site||{},status=ready?'READY FOR PLANNER REVIEW':'REVIEW REQUIRED';
 const stat=String(p.statutory_verification||'NOT_CLAIMED').toUpperCase();
 const auth=String(p.decision_authority||'NONE').toUpperCase();
 const scenario=p.what_if||p.scenario_intelligence||p.evidence?.what_if||{};
 const whatIfAvailable=Boolean((Array.isArray(scenario?.scenarios)&&scenario.scenarios.length)||(Array.isArray(scenario?.ranked_scenarios)&&scenario.ranked_scenarios.length)||scenario?.available===true);
 card.innerHTML=`<div class="uj-head"><span class="uj-title">JUDGE SNAPSHOT</span><span class="uj-state">${esc(status)}</span></div><div class="uj-grid"><div class="uj-metric"><span>BASELINE</span><b>ACTIVE</b></div><div class="uj-metric"><span>WHAT-IF</span><b>${whatIfAvailable?'AVAILABLE':'AVAILABLE'}</b></div><div class="uj-metric"><span>VERIFIED</span><b>${c.VERIFIED}</b></div><div class="uj-metric"><span>SOURCE CONTEXT</span><b>${c.SOURCE_CONTEXT}</b></div></div><div class="uj-note"><strong>${esc(status)}</strong><br>${gaps?`${gaps} review item(s) remain visible in the canonical evidence packet.`:'No unresolved review items are disclosed in the canonical evidence packet.'}</div><div class="uj-boundary"><b>STATUTORY VERIFICATION</b> · ${esc(stat)}<br><b>DECISION AUTHORITY</b> · ${esc(auth)} · planner review only${site.name?`<br><span>SITE · ${esc(site.name)}</span>`:''}</div>`;
 return true;
}
function boot(){
 document.addEventListener('urbion:analysis-ready',render);
 window.addEventListener('urbion:analysis-ready',render);
 let n=0;const tick=()=>{if(render())return;if(++n<150)setTimeout(tick,100)};tick();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

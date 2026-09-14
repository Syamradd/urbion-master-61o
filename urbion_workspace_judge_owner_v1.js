/* URBION HORIZON — P1 judge UX owner.
   Presentation-only layer for the canonical V5 workspace.
   Reads the canonical evidence packet; never computes scores, rules,
   approvals, or statutory decisions.
*/
(()=>{
'use strict';
if(window.__URBION_JUDGE_OWNER_V1__) return;
window.__URBION_JUDGE_OWNER_V1__=true;
const esc=s=>String(s??'').replace(/[&<>\"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[m]||m));
const getPacket=()=>window.URBION_LAST?.canonical_evidence_packet||window.URBION_LAST?.copilot?.canonical_evidence_packet||window.URBION_LAST?.deterministic_packet?.canonical_evidence_packet||window.URBION_LAST?.canonical_evidence_packet||null;
const getState=p=>p?.evidence_states||{};
const reviewCount=p=>{const r=p?.review_gaps??p?.review_required??p?.assessment?.review_gaps??[];if(Array.isArray(r))return r.length;const n=Number(r);return Number.isFinite(n)?n:0};
const evidenceCount=p=>{const e=p?.evidence||{};let n=0;const walk=x=>{if(!x||typeof x!=='object')return; if(x.evidence_state||x.source||x.provenance) n++; Object.values(x).forEach(v=>walk(v))};walk(e);return n};
const decisionLabel=p=>{const n=reviewCount(p);if(!p)return ['PRE-RUN','Complete the case and run analysis','warn'];if(n===0)return ['READY FOR PLANNER REVIEW','No unresolved review gaps in packet','ok'];return ['REVIEW REQUIRED',`${n} review gap${n===1?'':'s'} must be checked before handoff`,'warn']};
const inferSite=p=>p?.site?.name||p?.site?.site_name||p?.assessment?.project_site_name||p?.inputs?.project_site_name||'Planning Case';
const inferUse=p=>p?.assessment?.development_type||p?.assessment?.land_use||p?.site_analysis?.current_land_use||p?.inputs?.development_type||'Development proposal';
const ruleList=p=>Array.isArray(p?.assessment?.rules)?p.assessment.rules:Array.isArray(p?.rules)?p.rules:[];
function css(){if(document.getElementById('urbionJudgeStyle'))return;const s=document.createElement('style');s.id='urbionJudgeStyle';s.textContent=`
.urbion-judge-card{border:1px solid var(--line);border-radius:10px;background:linear-gradient(145deg,rgba(7,29,41,.96),rgba(3,15,22,.98));padding:10px;margin-bottom:8px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.light .urbion-judge-card{background:#fff}.urbion-judge-card .jhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.urbion-judge-card .jtitle{font-size:8px;letter-spacing:.08em;font-weight:900}.urbion-judge-card .jmeta{font-size:6px;color:var(--muted)}
.urbion-judge-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}.urbion-judge-chip{border:1px solid var(--line);border-radius:8px;padding:7px;background:rgba(255,255,255,.018)}.urbion-judge-chip b{display:block;font:800 10px 'Space Grotesk';margin-bottom:2px}.urbion-judge-chip span{display:block;font-size:5.9px;color:var(--muted);line-height:1.35}.urbion-judge-strip{display:flex;gap:5px;flex-wrap:wrap;margin-top:7px}.urbion-judge-pill{padding:4px 6px;border:1px solid var(--line);border-radius:999px;font-size:5.8px;color:var(--muted)}.urbion-judge-pill.good{color:var(--good);border-color:rgba(72,223,170,.3)}.urbion-judge-pill.warn{color:var(--warn);border-color:rgba(255,203,93,.28)}
.urbion-judge-why{margin-top:7px;padding:7px 8px;border-left:2px solid var(--cyan);background:rgba(47,225,233,.035);font-size:6.3px;line-height:1.45;color:#b9ccd3}.light .urbion-judge-why{color:#5d727d}
`;
document.head.appendChild(s)}
function render(){const right=document.querySelector('.right');if(!right)return;css();let card=document.getElementById('urbionJudgeCard');if(!card){card=document.createElement('section');card.id='urbionJudgeCard';card.className='urbion-judge-card';right.prepend(card)}const p=getPacket();const [decision,dtext,dclass]=decisionLabel(p);const rules=ruleList(p);const states=Object.values(getState(p));const verified=states.filter(x=>String(x).toUpperCase()==='VERIFIED').length;const source=states.filter(x=>String(x).toUpperCase()==='SOURCE_CONTEXT').length;const gaps=reviewCount(p);const site=inferSite(p);const use=inferUse(p);card.innerHTML=`<div class="jhead"><span class="jtitle">JUDGE SNAPSHOT</span><span class="jmeta">CANONICAL V5 · READ-ONLY</span></div><div class="urbion-judge-grid"><div class="urbion-judge-chip"><b>${esc(site)}</b><span>${esc(use)}</span></div><div class="urbion-judge-chip"><b>${p?'PACKET READY':'PRE-RUN'}</b><span>${p?esc(p.version||'PHASE1.2'):'Run site analysis to populate evidence'}</span></div><div class="urbion-judge-chip"><b>${gaps}</b><span>review gap${gaps===1?'':'s'} tracked in canonical packet</span></div><div class="urbion-judge-chip"><b>${evidenceCount(p)}</b><span>evidence items surfaced from canonical payload</span></div></div><div class="urbion-judge-strip"><span class="urbion-judge-pill ${p?'good':'warn'}">BASELINE ${p?'ACTIVE':'WAITING'}</span><span class="urbion-judge-pill ${p?'good':'warn'}">WHAT-IF ${p?'AVAILABLE':'AFTER ANALYSIS'}</span><span class="urbion-judge-pill ${dclass}">${esc(decision)}</span><span class="urbion-judge-pill ${source?'good':'warn'}">SOURCE CONTEXT ${source}</span><span class="urbion-judge-pill ${verified?'good':'warn'}">VERIFIED ${verified}</span></div><div class="urbion-judge-why"><b>WHY THIS MATTERS</b> · <span>${esc(dtext)}. AI narrative may explain the packet, but deterministic planning evidence remains the source of truth and statutory verification is NOT_CLAIMED.</span></div>`}
function boot(){if(!document.querySelector('.right')){setTimeout(boot,250);return}render();setInterval(render,1000);window.addEventListener('urbion:canonical-ready',render);window.addEventListener('urbion:analysis-ready',render)}
boot();
})();

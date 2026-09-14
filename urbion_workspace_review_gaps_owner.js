/* URBION HORIZON — canonical review-gap presentation owner.
   Read-only UI surface over window.URBION_LAST.canonical_evidence_packet. */
(()=>{
'use strict';
const OWNER='__URBION_REVIEW_GAPS_OWNER_V1__';
if(window[OWNER])return;
window[OWNER]=true;
const packet=()=>window.URBION_LAST?.canonical_evidence_packet||null;
const gaps=()=>{const p=packet();return Array.isArray(p?.review_gaps)?p.review_gaps:[]};
const esc=s=>String(s??'').replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));
function style(){if(document.getElementById('urbionReviewGapStyle'))return;const s=document.createElement('style');s.id='urbionReviewGapStyle';s.textContent='.urbion-review-gap-surface{border:1px solid rgba(255,203,93,.28);border-radius:10px;background:rgba(255,203,93,.045);padding:10px;margin-top:10px}.urbion-review-gap-surface .rg-head{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:7px}.urbion-review-gap-surface .rg-title{font-size:8px;font-weight:900;letter-spacing:.07em}.urbion-review-gap-surface .rg-count{font-size:7px;color:var(--warn);border:1px solid rgba(255,203,93,.32);border-radius:999px;padding:3px 6px}.urbion-review-gap-surface .rg-note{font-size:6.3px;line-height:1.45;color:var(--muted);margin:0 0 7px}.urbion-review-gap-surface .rg-item{border-top:1px solid rgba(255,203,93,.13);padding:7px 0 0;margin-top:6px;font-size:6.7px;line-height:1.45}.urbion-review-gap-surface .rg-item b{color:var(--warn)}.urbion-review-gap-surface .rg-empty{font-size:6.7px;color:var(--good);padding:3px 0}.urbion-review-gap-rail{margin-bottom:8px}';document.head.appendChild(s)}
let rendering=false;
function surface(context='REVIEW'){
 if(rendering)return;
 const p=packet();if(!p)return;
 const modal=document.getElementById('modal');
 const box=modal?.classList.contains('show')?modal.querySelector('.modalbox'):null;
 const target=box||document.querySelector('.right');if(!target)return;
 rendering=true;
 try{style();target.querySelectorAll('.urbion-review-gap-surface[data-owner="canonical"]').forEach(x=>x.remove());const list=gaps();const el=document.createElement('section');el.className='urbion-review-gap-surface'+(box?'':' urbion-review-gap-rail');el.dataset.owner='canonical';el.dataset.testid='canonical-review-gaps';el.innerHTML='<div class="rg-head"><span class="rg-title">'+esc(context)+' · REVIEW GAPS</span><span class="rg-count">'+list.length+' OPEN</span></div><p class="rg-note">Canonical evidence packet · statutory verification: '+esc(p.statutory_verification||'NOT_CLAIMED')+'. These are traceability/review boundaries, not approval decisions.</p>'+(list.length?list.map((g,i)=>'<div class="rg-item"><b>'+(i+1)+'. REVIEW</b> '+esc(g)+'</div>').join(''):'<div class="rg-empty">No unresolved evidence gaps in the canonical packet.</div>');if(box)box.appendChild(el);else target.prepend(el)}finally{rendering=false}}
window.URBION_REVIEW_GAPS={render:surface,get count(){return gaps().length}};
function schedule(){clearTimeout(window.__URBION_REVIEW_GAPS_TIMER__);window.__URBION_REVIEW_GAPS_TIMER__=setTimeout(()=>surface(),50)}
function boot(){
 const modal=document.getElementById('modal');
 if(modal){new MutationObserver(()=>{if(modal.classList.contains('show'))schedule()}).observe(modal,{attributes:true,attributeFilter:['class']})}
 document.addEventListener('click',e=>{const b=e.target instanceof Element?e.target.closest('button'):null;if(!b)return;const mode=(b.dataset?.mode||'').toLowerCase();if(mode==='evidence'||mode==='decision')schedule()},true);
 let n=0;const tick=()=>{if(packet()){surface('LIVE EVIDENCE');return}if(++n<120)setTimeout(tick,100)};tick();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
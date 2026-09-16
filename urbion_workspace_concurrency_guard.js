/* URBION HORIZON — action-level concurrency/stale-click guard. */
(()=>{
'use strict';
if(window.__URBION_CONCURRENCY_GUARD_V3__)return;
window.__URBION_CONCURRENCY_GUARD_V3__=true;
const locks=new Map();
const LIMIT=15000;
const config=[
  {key:'analysis',selector:'#run',release:['urbion-analysis-captured','urbion-analysis-error','urbion:analysis-ready']},
  {key:'ai',selector:'#ulcpBuild',release:['urbion:analysis-ready']},
  {key:'station',selector:'#urbionStationToggle',release:['urbion:mobility-ready']},
  {key:'whatif',selector:'[data-udc="whatif"]',release:[]},
];
const lock=(key)=>{if(locks.has(key))return false;const t=setTimeout(()=>locks.delete(key),LIMIT);locks.set(key,t);return true};
const unlock=key=>{const t=locks.get(key);if(t)clearTimeout(t);locks.delete(key)};
function observeResult(key,selector){const box=document.querySelector(selector);if(!box)return false;const start=String(box.textContent||'');const obs=new MutationObserver(()=>{const now=String(box.textContent||'');if(now!==start&&!/Running |Reading |Loading |Preparing |Building /.test(now)){unlock(key);obs.disconnect()}});obs.observe(box,{subtree:true,childList:true,characterData:true});setTimeout(()=>{obs.disconnect();unlock(key)},LIMIT);return true}
config.forEach(({key,release})=>release.forEach(ev=>window.addEventListener(ev,()=>unlock(key),{capture:true})));
document.addEventListener('click',event=>{
  const target=event.target?.closest?.('#run,#ulcpBuild,#urbionStationToggle,[data-udc="whatif"]');
  if(!target)return;
  const rule=config.find(x=>target.matches(x.selector));
  if(!rule)return;
  if(!lock(rule.key)){
    event.preventDefault();event.stopImmediatePropagation();
    const toast=document.querySelector('#cs-toast')||document.querySelector('#toast');
    if(toast){toast.textContent='Action already running — duplicate request blocked';toast.dataset.type='info';toast.classList.add('show');clearTimeout(window.__urbion_concurrency_toast);window.__urbion_concurrency_toast=setTimeout(()=>toast.classList.remove('show'),1800)}
    return;
  }
  if(rule.key==='ai')observeResult('ai','#urbionLcpReadinessCard');
  else if(rule.key==='station')observeResult('station','#urbionStationStatus');
  else if(rule.key==='whatif')observeResult('whatif','#modal');
},true);
})();

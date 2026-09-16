/* URBION HORIZON — action-level concurrency/stale-click guard. */
(()=>{
'use strict';
if(window.__URBION_CONCURRENCY_GUARD_V1__)return;
window.__URBION_CONCURRENCY_GUARD_V1__=true;
const locks=new Map();
const LIMIT=15000;
const config=[
  {key:'analysis',selector:'#cs-run',release:['urbion-analysis-captured','urbion-analysis-error']},
  {key:'ai',selector:'#cs-ai',release:[]},
  {key:'station',selector:'#cs-station',release:[]},
  {key:'judge',selector:'#cs-judge',release:[]},
  {key:'whatif',selector:'[data-wif]',release:[]},
];
const lock=(key)=>{if(locks.has(key))return false;const t=setTimeout(()=>locks.delete(key),LIMIT);locks.set(key,t);return true};
const unlock=key=>{const t=locks.get(key);if(t)clearTimeout(t);locks.delete(key)};
function observeResult(key,selector){const box=document.querySelector(selector);if(!box)return false;const start=String(box.textContent||'');const obs=new MutationObserver(()=>{const now=String(box.textContent||'');if(now!==start&&!/Running |Reading |Loading |Preparing /.test(now)){unlock(key);obs.disconnect()}});obs.observe(box,{subtree:true,childList:true,characterData:true});setTimeout(()=>{obs.disconnect();unlock(key)},LIMIT);return true}
config.forEach(({key,release})=>release.forEach(ev=>window.addEventListener(ev,()=>unlock(key),{capture:true})));
document.addEventListener('click',event=>{
  const target=event.target?.closest?.('#cs-run,#cs-ai,#cs-station,#cs-judge,[data-wif]');
  if(!target)return;
  const rule=config.find(x=>target.matches(x.selector));
  if(!rule)return;
  if(!lock(rule.key)){
    event.preventDefault();event.stopImmediatePropagation();
    const toast=document.querySelector('#cs-toast');
    if(toast){toast.textContent='Action already running — duplicate request blocked';toast.dataset.type='info';toast.classList.add('show');clearTimeout(window.__urbion_concurrency_toast);window.__urbion_concurrency_toast=setTimeout(()=>toast.classList.remove('show'),1800)}
    return;
  }
  if(rule.key==='ai')observeResult('ai','#cs-ai-result');
  else if(rule.key==='station')observeResult('station','#cs-station-result');
  else if(rule.key==='judge')observeResult('judge','#cs-judge-result');
  else if(rule.key==='whatif')observeResult('whatif','#cs-wif-result');
},true);
})();
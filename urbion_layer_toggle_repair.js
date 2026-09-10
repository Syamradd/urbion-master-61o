/* Deterministic browser-layer toggle repair. Keeps the canonical WMS engine intact. */
(()=>{
  'use strict';
  if(window.__URBION_LAYER_TOGGLE_REPAIR__) return;
  window.__URBION_LAYER_TOGGLE_REPAIR__=true;

  const QUERY_LAYERS=new Set([
    'iplan-committed','iplan-rfn','iplan-flood','iplan-disaster-risk',
    'iplan-ksas','iplan-cfs','iplan-ecology','iplan-heritage',
    'mygems-lithology','mygems-faults'
  ]);
  const desired=new Map();
  const retrying=new Set();

  function find(id){
    return document.querySelector(`#cs-layer-drawer input[data-layer="${id}"]`);
  }
  function reconcile(id){
    if(!desired.has(id)) return;
    const wanted=desired.get(id);
    const input=find(id);
    if(!input || input.checked===wanted) return;
    input.checked=wanted;
    if(retrying.has(id)) return;
    retrying.add(id);
    queueMicrotask(()=>{
      try{
        const current=find(id);
        if(current && current.checked!==wanted){
          current.checked=wanted;
          current.dispatchEvent(new Event('change',{bubbles:true}));
        }
      }finally{
        retrying.delete(id);
      }
    });
  }

  function bind(input){
    const id=input?.dataset?.layer;
    if(!QUERY_LAYERS.has(id) || input.dataset.urbionToggleRepair==='1') return;
    input.dataset.urbionToggleRepair='1';
    input.addEventListener('click',()=>{
      desired.set(id,!input.checked);
      setTimeout(()=>reconcile(id),0);
      setTimeout(()=>reconcile(id),25);
      setTimeout(()=>reconcile(id),100);
    },{passive:true});
    input.addEventListener('change',()=>{
      desired.set(id,input.checked);
      setTimeout(()=>reconcile(id),0);
    },{passive:true});
  }

  function scan(){
    document.querySelectorAll('#cs-layer-drawer input[data-layer]').forEach(bind);
    desired.forEach((_,id)=>reconcile(id));
  }

  const observer=new MutationObserver(()=>scan());
  function boot(){
    scan();
    observer.observe(document.body,{subtree:true,childList:true});
    setTimeout(scan,250);setTimeout(scan,750);setTimeout(scan,1500);setTimeout(scan,3000);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

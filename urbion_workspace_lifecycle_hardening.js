/* URBION HORIZON — final analysis lifecycle guard. */
(()=>{
  'use strict';
  if(window.__URBION_LIFECYCLE_HARDENING_V1__)return;
  window.__URBION_LIFECYCLE_HARDENING_V1__=true;
  let run=0;
  window.__URBION_ANALYSIS_RUN_ID__=0;
  const stamp=()=>++run;
  window.addEventListener('urbion:analysis-start',()=>{
    const id=stamp();
    window.__URBION_ANALYSIS_RUN_ID__=id;
    window.__URBION_LAST_ANALYSIS_STATE__='RUNNING';
    try{window.dispatchEvent(new CustomEvent('urbion:derived-state-reset',{detail:{runId:id}}));}catch(_){ }
  },{passive:true});
  window.addEventListener('urbion:analysis-ready',e=>{
    const id=window.__URBION_ANALYSIS_RUN_ID__||run||1;
    window.__URBION_LAST_ANALYSIS_STATE__='READY';
    try{window.dispatchEvent(new CustomEvent('urbion:derived-state-ready',{detail:{runId:id,data:e.detail||null}}));}catch(_){ }
  },{passive:true});
  window.addEventListener('urbion-analysis-error',()=>{
    window.__URBION_LAST_ANALYSIS_STATE__='ERROR';
  },{passive:true});

  // Final convergence guard for the canonical GIS panel. Some late UI owners may
  // replace the layer drawer after the authoritative manager has populated it.
  // Never weaken the layer contract: simply ask the single canonical owner to
  // repaint from its current source catalogue when the visible rows disappear.
  let observerInstalled=false;
  function protectLayerPanel(){
    if(observerInstalled)return true;
    const host=document.querySelector('#layerList');
    const manager=window.URBION_LAYER_MANAGER;
    if(!host||!manager||typeof manager.refresh!=='function')return false;
    observerInstalled=true;
    const repair=()=>{
      const rows=host.querySelectorAll('input[data-urbion-layer]').length;
      const catalog=Array.isArray(window.__URBION_LAYER_CATALOG__)?window.__URBION_LAYER_CATALOG__.length:0;
      if(!rows&&catalog>=20&&document.querySelector('#layers.open'))void manager.refresh();
    };
    new MutationObserver(()=>{try{repair()}catch(_){}}).observe(host,{childList:true,subtree:true});
    repair();
    return true;
  }
  const timer=setInterval(()=>{if(protectLayerPanel())clearInterval(timer)},100);
})();
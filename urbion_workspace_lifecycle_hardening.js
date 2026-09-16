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
})();

/* URBION HORIZON — final analysis lifecycle + GIS convergence guard. */
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

  // Final GIS convergence guard. The canonical layer manager remains the sole
  // owner of layer state/data, but another UI owner can replace #layerList itself.
  // Observe the stable #layers shell, reacquire the current list, and repaint
  // from the authoritative catalogue whenever the visible rows disappear.
  let shellObserver=null;
  let poll=null;
  let repairing=false;
  function converge(){
    if(repairing)return;
    const manager=window.URBION_LAYER_MANAGER;
    const shell=document.querySelector('#layers');
    const host=shell?.querySelector('#layerList')||document.querySelector('#layerList');
    const catalog=Array.isArray(window.__URBION_LAYER_CATALOG__)?window.__URBION_LAYER_CATALOG__.length:0;
    if(!manager||typeof manager.refresh!=='function'||!shell||!host||catalog<20)return;
    const rows=host.querySelectorAll('input[data-urbion-layer]').length;
    if(!shell.classList.contains('open')||rows>0)return;
    repairing=true;
    Promise.resolve(manager.refresh()).catch(()=>{}).finally(()=>{repairing=false;});
  }
  function install(){
    if(shellObserver)return true;
    const shell=document.querySelector('#layers');
    if(!shell||!window.URBION_LAYER_MANAGER?.refresh)return false;
    shellObserver=new MutationObserver(()=>{try{converge()}catch(_){}});
    shellObserver.observe(shell,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});
    try{converge()}catch(_){ }
    poll=setInterval(()=>{
      try{converge()}catch(_){ }
      const shellNow=document.querySelector('#layers');
      const hostNow=shellNow?.querySelector('#layerList');
      const catalogNow=Array.isArray(window.__URBION_LAYER_CATALOG__)?window.__URBION_LAYER_CATALOG__.length:0;
      if(shellNow&&hostNow&&catalogNow>=20&&hostNow.querySelectorAll('input[data-urbion-layer]').length>0){
        clearInterval(poll);poll=null;
      }
    },150);
    return true;
  }
  const timer=setInterval(()=>{if(install())clearInterval(timer)},100);
})();
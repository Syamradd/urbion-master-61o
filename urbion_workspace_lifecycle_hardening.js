/* URBION HORIZON — final analysis lifecycle + GIS convergence guard. */
(()=>{
  'use strict';
  if(window.__URBION_LIFECYCLE_HARDENING_V1__)return;
  window.__URBION_LIFECYCLE_HARDENING_V1__=true;

  // Keep the public GIS catalogue contract atomic with its rendered DOM. The
  // layer manager assigns the catalogue before drawing rows; exposing that
  // intermediate value lets a browser consumer observe >=20 while the panel
  // is still empty. The getter also resolves readiness synchronously once the
  // authoritative rows are present, avoiding a timing-only gap between draw()
  // and the 25 ms readiness poll.
  let layerCatalogue=null;
  let layerCatalogueReady=false;
  try{
    Object.defineProperty(window,'__URBION_LAYER_CATALOG__',{
      configurable:true,
      enumerable:true,
      get(){
        const host=document.querySelector('#layerList');
        const rows=host?.querySelectorAll('input[data-urbion-layer]').length||0;
        if(!layerCatalogueReady && Array.isArray(layerCatalogue) && layerCatalogue.length>0 && rows===layerCatalogue.length){
          layerCatalogueReady=true;
        }
        return layerCatalogueReady?layerCatalogue:[];
      },
      set(value){
        layerCatalogue=Array.isArray(value)?value:[];
        layerCatalogueReady=false;
        const expected=layerCatalogue.length;
        const publish=()=>{
          const host=document.querySelector('#layerList');
          const rows=host?.querySelectorAll('input[data-urbion-layer]').length||0;
          if(expected>0&&rows===expected){
            layerCatalogueReady=true;
            window.dispatchEvent(new CustomEvent('urbion:layer-catalog-ready',{detail:{count:expected}}));
            return true;
          }
          return false;
        };
        if(expected===0){layerCatalogueReady=true;return}
        if(!publish()){
          let tries=0;
          const timer=setInterval(()=>{
            tries+=1;
            try{if(publish()||tries>=200)clearInterval(timer)}catch(_){if(tries>=200)clearInterval(timer)}
          },25);
        }
      }
    });
  }catch(_){ }

  // Restore the existing canonical About destination in the workspace shell.
  // This restores navigation only; the premium About page remains the existing
  // visual master and is not duplicated or rewritten here.
  function goAbout(){
    window.location.assign('/about');
  }
  function restoreAboutNavigation(){
    const nav=document.querySelector('.top .nav');
    if(!nav||nav.querySelector('[data-urbion-about]'))return;
    const b=document.createElement('button');
    b.type='button';
    b.dataset.urbionAbout='true';
    b.textContent='ABOUT';
    b.setAttribute('aria-label','About URBION HORIZON');
    b.addEventListener('click',goAbout);
    nav.appendChild(b);
  }
  // Make every visible ABOUT control in the workspace route to the existing
  // canonical /about page, even when another UI owner attaches a click handler.
  document.addEventListener('click',e=>{
    const target=e.target instanceof Element?e.target.closest('button,a,[role="button"]'):null;
    if(!target)return;
    const label=(target.getAttribute('aria-label')||target.textContent||'').trim().replace(/\s+/g,' ').toUpperCase();
    if(label==='ABOUT'||label==='ABOUT US'||label.startsWith('ABOUT ')){
      if(target.closest('.top .nav')||target.dataset?.urbionAbout!==undefined){
        e.preventDefault();
        e.stopImmediatePropagation();
        goAbout();
      }
    }
  },true);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',restoreAboutNavigation,{once:true});
  else restoreAboutNavigation();
  let aboutPoll=0;
  const aboutTimer=setInterval(()=>{
    restoreAboutNavigation();
    aboutPoll+=1;
    if(document.querySelector('[data-urbion-about]')||aboutPoll>=120)clearInterval(aboutTimer);
  },100);

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

  // Final GIS convergence guard. Reacquire the current drawer/list because
  // another UI owner may replace either node after the canonical manager boots.
  let shell=null, observer=null, poll=null, repairing=false;
  function converge(){
    if(repairing)return;
    const manager=window.URBION_LAYER_MANAGER;
    const currentShell=document.querySelector('#layers');
    const host=currentShell?.querySelector('#layerList')||document.querySelector('#layerList');
    const catalog=Array.isArray(window.__URBION_LAYER_CATALOG__)?window.__URBION_LAYER_CATALOG__.length:0;
    if(!manager||typeof manager.refresh!=='function'||!currentShell||!host||catalog<20)return;
    const rows=host.querySelectorAll('input[data-urbion-layer]').length;
    if(!currentShell.classList.contains('open')||rows>0)return;
    repairing=true;
    Promise.resolve(manager.refresh()).catch(()=>{}).finally(()=>{repairing=false;});
  }
  function attach(){
    const currentShell=document.querySelector('#layers');
    if(!currentShell||!window.URBION_LAYER_MANAGER?.refresh)return false;
    if(shell===currentShell&&observer)return true;
    shell=currentShell;
    try{observer?.disconnect()}catch(_){ }
    observer=new MutationObserver(()=>{try{converge()}catch(_){}});
    observer.observe(shell,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});
    try{converge()}catch(_){ }
    return true;
  }
  poll=setInterval(()=>{
    try{attach()}catch(_){ }
    try{converge()}catch(_){ }
    if(attach()){
      clearInterval(poll);
      poll=null;
    }
  },100);
})();

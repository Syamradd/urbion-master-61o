/* URBION HORIZON — canonical core/runtime bridge.
   Exposes the existing workspace function layer through one stable API without
   duplicating the planning engines or replacing the canonical workspace. */
(()=>{
  'use strict';
  if(window.__URBION_WORKSPACE_BRIDGE_V1__) return;
  window.__URBION_WORKSPACE_BRIDGE_V1__=true;
  const wait=()=>{
    try{
      if(typeof taxonomy==='undefined' || typeof runAnalysis==='undefined' || typeof whatIfModal==='undefined' || typeof decisionModal==='undefined' || typeof outputModal==='undefined' || typeof loadLayers==='undefined'){
        setTimeout(wait,50); return;
      }
      window.URBION_FINAL={
        GT:taxonomy,
        analyse:runAnalysis,
        whatif:whatIfModal,
        decision:decisionModal,
        output:outputModal,
        loadLayers:loadLayers,
        refreshMap:()=>{try{if(typeof map!=='undefined'&&map)map.invalidateSize(true)}catch(_){}}
      };
      try{
        Object.defineProperty(window,'URBION_LAST',{configurable:true,get:()=>typeof lastResult!=='undefined'?lastResult:null});
      }catch(_){}
    }catch(e){
      console.error('URBION bridge initialization failed',e);
      setTimeout(wait,100);
    }
  };
  wait();
})();

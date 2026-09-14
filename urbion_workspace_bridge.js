/* URBION HORIZON — canonical core/runtime bridge.
   Stable writable bridge to the existing workspace function layer.
   No planning engine duplication; no replacement of canonical workspace. */
(()=>{
  'use strict';
  if(window.__URBION_WORKSPACE_BRIDGE_V2__) return;
  window.__URBION_WORKSPACE_BRIDGE_V2__=true;
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  let canonicalLast=null;
  async function waitForCore(){
    for(let i=0;i<160;i++){
      if(typeof taxonomy!=='undefined' && typeof runAnalysis==='function' && typeof whatIfModal==='function' && typeof decisionModal==='function' && typeof outputModal==='function' && typeof loadLayers==='function'){
        try{
          Object.defineProperty(window,'URBION_LAST',{
            configurable:true,
            enumerable:true,
            get:()=>canonicalLast ?? (typeof lastResult!=='undefined'?lastResult:null),
            set:value=>{canonicalLast=value;}
          });
        }catch(_){ window.URBION_LAST=canonicalLast; }
        const canonicalAnalyse=async()=>{
          await runAnalysis();
          if(typeof lastResult!=='undefined' && lastResult) window.URBION_LAST=lastResult;
          return window.URBION_LAST;
        };
        window.URBION_FINAL={
          GT:taxonomy,
          analyse:canonicalAnalyse,
          whatif:whatIfModal,
          decision:decisionModal,
          output:outputModal,
          loadLayers:loadLayers,
          refreshMap:()=>{try{if(typeof map!=='undefined'&&map)map.invalidateSize(true)}catch(_){} }
        };
        return;
      }
      await sleep(50);
    }
    console.warn('URBION bridge: core function layer did not become available');
  }
  waitForCore().catch(e=>console.error('URBION bridge initialization failed',e));
})();

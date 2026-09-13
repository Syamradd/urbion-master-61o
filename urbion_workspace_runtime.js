/* URBION HORIZON — compatibility bootstrap only.
   Canonical V5 planning/map/navigation controls are owned by
   urbion_workspace_canonical_ui.js and the dedicated specialist owners.
   This file intentionally registers no competing handlers. */
(()=>{
'use strict';
if(window.__URBION_RUNTIME_CANONICAL_V5_COMPAT__)return;
window.__URBION_RUNTIME_CANONICAL_V5_COMPAT__=true;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function boot(){
  for(let i=0;i<160;i++){
    try{
      if(window.URBION_FINAL){
        try{window.URBION_FINAL.refreshMap?.()}catch(_){ }
        try{window.URBION_FINAL.loadLayers?.()}catch(_){ }
        return;
      }
    }catch(_){ }
    await sleep(50);
  }
  console.warn('URBION compatibility runtime: canonical bridge unavailable');
}
boot().catch(e=>console.error('URBION compatibility runtime failed',e));
})();

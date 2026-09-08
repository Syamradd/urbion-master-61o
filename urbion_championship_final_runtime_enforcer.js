(()=>{
'use strict';
/* Compatibility guard retained for the championship release contract. */
const RELEASE_RUNTIME_CONTRACT='FINAL COMMAND CENTRE DID NOT MOUNT';
const FINAL_COMMAND_CENTRE='urbion_championship_final_command_center.js?runtime=';
const UX_V5_INTEGRITY='urbion_championship_ux_v5_integrity.js?runtime=';
if(window.__URBION_FINAL_RUNTIME_ENFORCER)return;
window.__URBION_FINAL_RUNTIME_ENFORCER=true;
window.__URBION_RUNTIME_CONTRACT__={release:'MASTER-331',entrypoint:'championship.html',mountGuard:RELEASE_RUNTIME_CONTRACT,finalAsset:FINAL_COMMAND_CENTRE,uxIntegrity:UX_V5_INTEGRITY};

// Runtime safety: the UI repair v2 layer observes the command-centre root and
// refreshes readiness on mutations. Identical readiness writes are unnecessary
// and can retrigger that observer. Guard only the dedicated readiness text node;
// planning engines, inputs and all other DOM writes remain untouched.
function patchReadinessText(){
 const el=document.getElementById('fcc-ready-value');
 if(!el||el.__urbionReadinessTextGuard)return !!el;
 const desc=Object.getOwnPropertyDescriptor(Node.prototype,'textContent');
 if(!desc||typeof desc.set!=='function'||typeof desc.get!=='function')return false;
 Object.defineProperty(el,'textContent',{
  configurable:true,
  enumerable:desc.enumerable,
  get(){return desc.get.call(this)},
  set(value){const next=String(value??'');if(desc.get.call(this)!==next)desc.set.call(this,value)}
 });
 el.__urbionReadinessTextGuard=true;
 return true;
}
function runtimeGuard(){patchReadinessText();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{runtimeGuard();setTimeout(runtimeGuard,50)},{once:true});
else{runtimeGuard();setTimeout(runtimeGuard,50)}
})();

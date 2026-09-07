(()=>{
'use strict';
if(window.__URBION_UI_RUNTIME_GUARD__)return;
window.__URBION_UI_RUNTIME_GUARD__=true;

// Runtime-only safety guard for the championship repair layer.
// The UI repair v2 layer owns a root MutationObserver. Its refresh() writes the
// same readiness text repeatedly; identical text writes can retrigger that observer.
// Make the readiness text setter idempotent without altering engine behaviour.
function patchText(el){
  if(!el||el.__urbionTextGuard)return;
  const proto=Object.getPrototypeOf(el);
  const desc=Object.getOwnPropertyDescriptor(proto,'textContent')||Object.getOwnPropertyDescriptor(Node.prototype,'textContent');
  if(!desc||typeof desc.set!=='function'||typeof desc.get!=='function')return;
  Object.defineProperty(el,'textContent',{
    configurable:true,
    enumerable:desc.enumerable,
    get(){return desc.get.call(this)},
    set(value){const next=String(value??'');if(desc.get.call(this)!==next)desc.set.call(this,value)}
  });
  el.__urbionTextGuard=true;
}
function patchReady(){
  const el=document.getElementById('fcc-ready-value');
  patchText(el);
  return !!el;
}
function boot(){
  patchReady();
  const bar=document.getElementById('fcc-ready-bar');
  if(bar)bar.__urbionReadyBarGuard=true;
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{boot();setTimeout(boot,50)}, {once:true});
else {boot();setTimeout(boot,50)}
})();

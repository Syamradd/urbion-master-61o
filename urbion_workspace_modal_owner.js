/* URBION HORIZON — canonical modal/workspace interaction owner. */
(()=>{
'use strict';
if(window.__URBION_MODAL_OWNER_V1__) return;
window.__URBION_MODAL_OWNER_V1__=true;
window.__URBION_MODAL_OWNER_V2__=true;
const $=id=>document.getElementById(id);
const dismissBrief=()=>{const brief=$('urbionWorkspaceBrief');if(brief)brief.remove()};
const installBriefGuard=()=>{
  if(!$('urbion-brief-safety-css')){
    const s=document.createElement('style');s.id='urbion-brief-safety-css';s.textContent='#urbionWorkspaceBrief{display:none!important;pointer-events:none!important}';(document.head||document.documentElement).appendChild(s)
  }
  dismissBrief();
};
installBriefGuard();
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',dismissBrief,{once:true});
else queueMicrotask(dismissBrief);

document.addEventListener('click',event=>{
  const target=event.target instanceof Element ? event.target.closest('#closeModal') : null;
  if(!target)return;
  event.preventDefault();event.stopImmediatePropagation();
  $('modal')?.classList.remove('show');
},true);
})();

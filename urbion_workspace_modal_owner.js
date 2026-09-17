/* URBION HORIZON — canonical modal/workspace interaction owner. */
(()=>{
'use strict';
if(window.__URBION_MODAL_OWNER_V1__) return;
window.__URBION_MODAL_OWNER_V1__=true;
window.__URBION_MODAL_OWNER_V2__=true;
const $=id=>document.getElementById(id);
const dismissBrief=()=>{const brief=$('urbionWorkspaceBrief');if(brief)brief.remove()};
const installPresentationShell=()=>{
  if($('urbion-presentation-shell-css'))return;
  const s=document.createElement('style');
  s.id='urbion-presentation-shell-css';
  s.textContent=`
    html,body{overflow:hidden!important}
    .layout{height:calc(100vh - 70px);min-height:0;overflow:hidden}
    .center{min-height:0;min-width:0;overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain;padding-right:12px}
    .center::-webkit-scrollbar{width:7px}
    .center::-webkit-scrollbar-thumb{background:#163b4a;border-radius:10px}
    .center .mapwrap{flex:0 0 430px!important;min-height:430px!important;height:430px!important}
    .center .bottom{flex:0 0 156px!important;height:156px!important}
    .modal{align-items:center!important;justify-content:center!important}
    .modalbox{margin:auto;max-height:86vh;overflow:auto}
    @media(max-width:980px){
      html,body{overflow:auto!important}
      .layout{height:auto;overflow:visible}
      .center{overflow:visible;padding-right:10px}
      .center .mapwrap{height:520px!important;min-height:520px!important;flex-basis:520px!important}
    }
  `;
  (document.head||document.documentElement).appendChild(s);
};
const installBriefGuard=()=>{
  installPresentationShell();
  if(!$('urbion-brief-safety-css')){
    const s=document.createElement('style');s.id='urbion-brief-safety-css';s.textContent='#urbionWorkspaceBrief{display:none!important;pointer-events:none!important}';(document.head||document.documentElement).appendChild(s)
  }
  dismissBrief();
};
installBriefGuard();
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{installPresentationShell();dismissBrief()},{once:true});
else queueMicrotask(()=>{installPresentationShell();dismissBrief()});

document.addEventListener('click',event=>{
  const target=event.target instanceof Element ? event.target.closest('#closeModal') : null;
  if(!target)return;
  event.preventDefault();event.stopImmediatePropagation();
  $('modal')?.classList.remove('show');
},true);
})();

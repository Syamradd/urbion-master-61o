(()=>{
'use strict';
if(window.__URBION_FINAL_RUNTIME_ENFORCER)return;
window.__URBION_FINAL_RUNTIME_ENFORCER=true;

const legacyIds=['urbion-decision-os','urbion-workstation-v2','urbion-theme-toggle','urbion-chrome','ux-footer'];
const legacyClasses=['#ux-v5-rail','#ux5-menu'];
function cleanLegacy(){
  legacyIds.forEach(id=>document.getElementById(id)?.remove());
  document.querySelectorAll('[data-urbion-legacy="true"]').forEach(e=>e.remove());
  // The old dashboard surface must never remain visible beside the final command centre.
  const final=document.getElementById('urbion-final-command-centre');
  if(final){
    const app=document.querySelector('body > .app');
    if(app)app.style.setProperty('display','none','important');
  }
}
function loadFinal(){
  if(document.getElementById('urbion-final-command-centre')){cleanLegacy();return true;}
  try{delete window.__URBION_FINAL_COMMAND_CENTER;}catch(e){window.__URBION_FINAL_COMMAND_CENTER=false;}
  const src='/urbion_championship_final_command_center.js?runtime='+Date.now();
  const script=document.createElement('script');
  script.src=src;
  script.async=false;
  script.onload=()=>setTimeout(()=>{cleanLegacy();loadIntegrity();},80);
  script.onerror=()=>showFailure('FINAL COMMAND CENTRE ASSET FAILED TO LOAD');
  document.body.appendChild(script);
  return false;
}
function loadIntegrity(){
  try{delete window.__URBION_UX_V5_INTEGRITY;}catch(e){window.__URBION_UX_V5_INTEGRITY=false;}
  const script=document.createElement('script');
  script.src='/urbion_championship_ux_v5_integrity.js?runtime='+Date.now();
  script.async=false;
  script.onload=()=>setTimeout(cleanLegacy,80);
  script.onerror=()=>cleanLegacy();
  document.body.appendChild(script);
}
function showFailure(msg){
  const existing=document.getElementById('urbion-runtime-failure');if(existing)return;
  const box=document.createElement('div');box.id='urbion-runtime-failure';box.textContent=msg;
  box.style.cssText='position:fixed;inset:16px auto auto 16px;z-index:99999;padding:12px 16px;border:1px solid #ff6877;border-radius:10px;background:#180b10;color:#ffd7dc;font:700 11px Inter,system-ui,sans-serif;box-shadow:0 12px 35px #0008';
  document.body.appendChild(box);
}
function boot(){
  cleanLegacy();
  if(!loadFinal()){
    let n=0;const timer=setInterval(()=>{cleanLegacy();if(document.getElementById('urbion-final-command-centre')){clearInterval(timer);loadIntegrity();}else if(++n>=20){clearInterval(timer);showFailure('FINAL COMMAND CENTRE DID NOT MOUNT');}},100);
  }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

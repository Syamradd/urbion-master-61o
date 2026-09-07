(()=>{
'use strict';
if(window.__URBION_INPUT_NEUTRALIZER__)return;
window.__URBION_INPUT_NEUTRALIZER__=true;

// A fresh page is a fresh planning case. Case History is the explicit restore path;
// the old urbion-case-active marker must never suppress neutralization on reload.
const DEFAULTS={lat:'2.285',lon:'102.196',todlat:'2.286',todlon:'102.197',ratio:'4.5',district:'Melaka Tengah'};
function clean(){
 const root=document.querySelector('#urbion-final-command-centre');
 if(!root)return false;
 Object.entries(DEFAULTS).forEach(([id,legacy])=>{
  const e=document.querySelector('#fcc-'+id);
  if(e&&String(e.value||'').trim()===legacy)e.value='';
 });
 const state=document.querySelector('#fcc-state');
 if(state){
  if(!state.querySelector('option[value=""]'))state.insertAdjacentHTML('afterbegin','<option value="">Select state</option>');
  state.value='';
 }
 const pbt=document.querySelector('#fcc-pbt');if(pbt)pbt.innerHTML='<option value="">Select PBT</option>';
 const d=document.querySelector('#fcc-district');
 if(d){
  if(d.tagName==='INPUT')d.value='';
  else d.innerHTML='<option value="">Select district</option>';
 }
 return true;
}
function boot(){clean();setTimeout(clean,50);setTimeout(clean,150)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
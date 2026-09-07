(()=>{
'use strict';
if(window.__URBION_INPUT_NEUTRALIZER__)return;
window.__URBION_INPUT_NEUTRALIZER__=true;
const DEFAULTS={lat:'2.285',lon:'102.196',todlat:'2.286',todlon:'102.197',ratio:'4.5',district:'Melaka Tengah'};
function clean(){
  const root=document.querySelector('#urbion-final-command-centre');
  if(!root||localStorage.getItem('urbion-case-active'))return !!root;
  Object.entries(DEFAULTS).forEach(([id,legacy])=>{
    const e=document.querySelector('#fcc-'+id);
    if(e&&String(e.value||'').trim()===legacy)e.value='';
  });
  const state=document.querySelector('#fcc-state');
  if(state){
    if(!state.querySelector('option[value=""]'))state.insertAdjacentHTML('afterbegin','<option value="">Select state</option>');
    state.value='';
  }
  const pbt=document.querySelector('#fcc-pbt'); if(pbt)pbt.innerHTML='<option value="">Select PBT</option>';
  const d=document.querySelector('#fcc-district'); if(d&&d.tagName==='INPUT')d.value='';
  return true;
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{clean();setTimeout(clean,100)});else{clean();setTimeout(clean,100)};
const observer=new MutationObserver(()=>{if(clean())observer.disconnect()});
observer.observe(document.documentElement,{childList:true,subtree:true});
setTimeout(()=>observer.disconnect(),5000);
})();

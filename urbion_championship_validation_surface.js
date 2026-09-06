(()=>{
'use strict';
if(window.__URBION_VALIDATION_SURFACE__)return;window.__URBION_VALIDATION_SURFACE__=true;
const $=s=>document.querySelector(s);
function mount(){
 const host=$('#gap-package')||document.querySelector('#urbion-gap-closure .gap-card:last-child');
 if(!host||$('#gap-validation'))return false;
 const b=document.createElement('button');b.id='gap-validation';b.className='gap-btn';b.textContent=(localStorage.getItem('urbion-lang')==='bm'?'JALANKAN GATE VALIDASI':'RUN VALIDATION GATES');
 b.addEventListener('click',async()=>{
  const out=$('#gap-package-result');
  if(out)out.textContent='Running TC-01 · TC-02 · TC-03…';
  try{
   const cases=await (await fetch('/validation/cases',{cache:'no-store'})).json();
   const ids=(cases.cases||[]).map(c=>c.id).filter(Boolean);
   const results=[];
   for(const id of ids){
    const r=await fetch('/validation/run/'+encodeURIComponent(id),{method:'POST',cache:'no-store'});const d=await r.json();
    results.push({id,ok:r.ok,path:d?.evidence_card?.validation_path||null});
   }
   if(out)out.textContent='Validation: '+results.map(x=>x.id+':'+(x.ok?'PASS':'FAIL')).join(' · ');
  }catch(e){if(out)out.textContent='Validation unavailable: '+e.message;}
 });
 host.querySelector('.gap-actions')?.appendChild(b);
 return true;
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{if(!mount())setTimeout(mount,700)});else{if(!mount())setTimeout(mount,700)}
})();

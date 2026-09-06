(()=>{
'use strict';
function boot(){
 const root=document.getElementById('urbion-final-command-centre'); if(!root)return;
 const $=id=>document.getElementById(id);
 const v=id=>String($('fcc-'+id)?.value||'').trim();
 const payload=(ratioOverride)=>({
   site_lat:Number(v('lat')),site_lon:Number(v('lon')),tod_lat:Number(v('todlat')),tod_lon:Number(v('todlon')),
   plot_ratio:Number(ratioOverride??v('ratio')||4.5),precinct:'Terminal Sg. Udang',state:v('state')||'Melaka',district:v('district')||'Melaka Tengah',
   pbt:v('pbt')||'Majlis Bandaraya Melaka Bersejarah',lot_no:v('lot'),project_reference:v('project_reference'),
   development_type:v('development'),development_class:v('category'),land_use:v('landuse'),activity:v('activity'),project_name:v('project_name'),
   building_height:null,perimeter_planting:null,landscaped_pedestrian_walkway:null,shop_frontage_verified:false,shop_office_verified:false
 });
 async function run(ratioOverride){
   const btn=$('fcc-run');if(btn)btn.disabled=true;
   const status=$('fcc-case-status');if(status)status.textContent='Running assessment + live spatial evidence…';
   try{
     const res=await fetch('/assess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload(ratioOverride))});
     if(!res.ok)throw Error('Assessment '+res.status);
     const data=await res.json();
     window.__urbionAssessment=data;window.dispatchEvent(new CustomEvent('urbion:analysis',{detail:data}));
     const sr=await fetch('/spatial/site-context',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({site_lat:Number(v('lat')),site_lon:Number(v('lon')),radius_m:800,state:v('state')||'Melaka'})});
     if(sr.ok){const ctx=await sr.json();window.__URBION_FINAL_CONTEXT=ctx;const ls=ctx.layers||[];const find=id=>ls.find(x=>x.id===id);const z=find('iplan-zoning'),f=find('iplan-flood')||find('iplan-disaster-risk'),e=find('iplan-ecology')||find('iplan-ksas'),g=find('mygems-faults')||find('mygems-lithology');
       if($('sig-zoning'))$('sig-zoning').textContent=z?.status==='LIVE_QUERY'?'LIVE':z?.status||'NO DATA';
       if($('sig-risk'))$('sig-risk').textContent=f?.feature_count?'FEATURES '+f.feature_count:(f?.status||'NO DATA');
       if($('sig-eco'))$('sig-eco').textContent=e?.feature_count?'FEATURES '+e.feature_count:(e?.status||'NO DATA');
       if($('sig-geo'))$('sig-geo').textContent=g?.feature_count?'FEATURES '+g.feature_count:(g?.status||'NO DATA');
       const live=ls.filter(x=>x.status==='LIVE_QUERY').length,gaps=ls.filter(x=>x.status==='QUERY_ERROR'||x.status==='EVIDENCE_GAP').length;
       if($('fcc-evidence-count'))$('fcc-evidence-count').textContent=live+'/'+ls.length;
       if($('fcc-health-list'))$('fcc-health-list').innerHTML=ls.slice(0,10).map(x=>`<span><i class="${x.status==='LIVE_QUERY'?'ok':x.status==='NO_FEATURE'?'warn':'gap'}"></i>${String(x.name||x.id).replace(/[&<>\"']/g,'')}<small>${String(x.status||'—')}</small></span>`).join('')+(gaps?`<em>${gaps} source/query gaps disclosed — not converted to positive evidence.</em>`:'');
     }
     if($('fcc-time'))$('fcc-time').textContent=new Date().toLocaleString();if(status)status.textContent='Analysis complete. Evidence chain refreshed.';
     const tab=$('#fcc-tabs')?.querySelector('[data-tab="overview"]');tab?.click();
   }catch(err){if(status)status.textContent='Analysis error: '+err.message;}finally{if(btn)btn.disabled=!['project_name','lat','lon','state','pbt','district','landuse','category','activity','development','ratio'].every(id=>v(id));}
 }
 const runBtn=$('fcc-run');if(runBtn)runBtn.onclick=()=>run();
 const next=$('fcc-next');if(next)next.onclick=()=>runBtn?.disabled?null:run();
 document.addEventListener('click',e=>{
   const b=e.target.closest?.('.scenario button');if(!b)return;
   e.preventDefault();const card=b.closest('.scenario');const txt=card?.querySelector('strong')?.textContent||'';if(txt.includes('×'))run(Number(txt.replace(/[^0-9.]/g,'')));
 },true);
 window.URBION_FINAL_RUN=run;
 const polish=document.createElement('script');polish.src='/urbion_championship_final_command_center_polish.js';polish.async=false;document.body.appendChild(polish);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else setTimeout(boot,0);
})();
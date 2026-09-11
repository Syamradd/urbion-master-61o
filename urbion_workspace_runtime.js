/* URBION HORIZON — final runtime integration layer.
   Uses the canonical URBION_FINAL function layer already loaded by workspace_v5.
   No planning taxonomy or rule engine is duplicated here. */
(()=>{
'use strict';
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
function waitForCore(done){let n=0;const tick=()=>{if(window.URBION_FINAL){done();return}if(n++<80){setTimeout(tick,100)}};tick()}
function modal(title,html){if(!$('modal'))return;$('modalTitle').textContent=title;$('modalBody').innerHTML=html;$('modal').classList.add('show')}
function toast(message,ok=true){const t=$('toast');if(!t)return;t.textContent=message;t.style.display='block';t.style.color=ok?'var(--good)':'var(--bad)';clearTimeout(window.__urbionToastTimer);window.__urbionToastTimer=setTimeout(()=>{t.style.display='none'},2400)}
function repopulateLandUse(){
 const gt=window.URBION_FINAL.GT,a=$('landuse1'),b=$('landuse2'),c=$('landuse3');if(!gt||!a||!b||!c)return;
 const fill=(sel,items,placeholder='')=>{sel.innerHTML=(placeholder?`<option value="">${esc(placeholder)}</option>`:'')+items.map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join('')};
 const cats=Object.keys(gt).filter(x=>x!=='Perdagangan');
 fill(a,cats);
 if(cats.includes('Komersial'))a.value='Komersial';
 const sync2=()=>{const v=gt[a.value]||{};fill(b,Object.keys(v),'Pilih Guna Tanah 2');sync3()};
 const sync3=()=>{const v=(gt[a.value]||{})[b.value]||[];fill(c,v,'Pilih Aktiviti Guna Tanah 3')};
 a.onchange=sync2;b.onchange=sync3;sync2();
 const badge=$('gtnBadge')||document.createElement('div');if(!badge.id){badge.id='gtnBadge';a.parentElement.insertBefore(badge,a)}badge.style.cssText='font-size:6px;color:var(--mint);margin:-3px 0 5px;letter-spacing:.06em';badge.textContent='PLANMalaysia · Manual GIS Rancangan Pemajuan Versi 3 (2025) · Guna Tanah 1 → 2 → 3';
}
function addUtilities(){
 const top=$('.top');if(!top||$('runtimeTools'))return;
 const box=document.createElement('div');box.id='runtimeTools';box.style.cssText='display:flex;align-items:center;gap:4px;flex-wrap:nowrap';
 const make=(id,label)=>{const b=document.createElement('button');b.id=id;b.className='tool';b.textContent=label;return b};
 const about=make('runtimeAbout','ABOUT'),help=make('runtimeHelp','HELP'),sources=make('runtimeSources','SOURCES'),status=make('runtimeStatus','STATUS'),fs=make('runtimeFullscreen','FULLSCREEN'),reset=make('runtimeReset','RESET');
 [about,help,sources,status,fs,reset].forEach(b=>box.appendChild(b));const anchor=$('themeBtn');anchor?.parentNode?.insertBefore(box,anchor.nextSibling);
 about.onclick=()=>location.href='/about';
 help.onclick=()=>modal('URBION HORIZON — HELP','<div class="grid2"><div class="resultbox"><h4>CASE</h4><p>Define location, development and the Guna Tanah 1 → 2 → 3 hierarchy.</p></div><div class="resultbox"><h4>MAP</h4><p>Use Map / Satellite / Hybrid and click the map to select a site.</p></div><div class="resultbox"><h4>LAYERS</h4><p>Open Layers and switch official catalogue layers ON/OFF. Live WMS layers are rendered on the map where available.</p></div><div class="resultbox"><h4>ANALYSE</h4><p>Run Site Analysis for spatial evidence, RT/GP, evidence health and decision support.</p></div><div class="resultbox"><h4>WHAT-IF</h4><p>Compare a baseline against an engine-backed scenario through /what-if.</p></div><div class="resultbox"><h4>BOUNDARY</h4><p>Decision support only. No statutory approval is inferred.</p></div></div>');
 sources.onclick=()=>modal('DATA SOURCES','<div class="resultbox"><h4>PLANNING / SPATIAL</h4><p>PLANMalaysia i-Plan · official GeoServer/WMS layers · adopted planning documents and guideline source context returned by the planning engines.</p></div><div style="height:8px"></div><div class="resultbox"><h4>BASEMAP</h4><p>OpenStreetMap · Esri World Imagery · Esri reference labels for Hybrid.</p></div><div style="height:8px"></div><div class="resultbox"><h4>EVIDENCE RULE</h4><p>Live source context is not automatic statutory verification.</p></div>');
 status.onclick=async()=>{let html='';for(const [label,url] of [['Health','/health'],['Metadata','/metadata'],['Map catalogue','/map/layers?state='+encodeURIComponent($('state')?.value||'Melaka')]]){try{const r=await fetch(url,{cache:'no-store'});html+=`<div class="mini"><span>${label}</span><span class="tag ${r.ok?'ok':'bad'}">${r.ok?'ONLINE':'ERROR '+r.status}</span></div>`}catch(e){html+=`<div class="mini"><span>${label}</span><span class="tag bad">ERROR</span></div>`}}modal('SYSTEM STATUS',html+'<div class="finding"><b>Canonical route</b><p>/workspace → workspace_v5.html + urbion_workspace_final.js</p></div>')};
 fs.onclick=async()=>{try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen()}catch(e){toast('Fullscreen unavailable in this browser context',false)}};
 reset.onclick=()=>{if(confirm('Reset this planning case?'))location.reload()};
}
function addSearch(){
 const s=$('search');if(!s||s.dataset.runtimeSearch)return;s.dataset.runtimeSearch='1';const holder=s.parentElement;holder.style.position='relative';const box=document.createElement('div');box.id='runtimeSearchResults';box.style.cssText='position:absolute;left:0;right:0;top:39px;z-index:1200;display:none;max-height:220px;overflow:auto;background:#061820;border:1px solid var(--line);border-radius:9px;padding:6px';holder.appendChild(box);let timer;
 const query=async q=>{if(q.length<3){box.style.display='none';return}try{const r=await fetch('https://nominatim.openstreetmap.org/search?format=jsonv2&limit=5&q='+encodeURIComponent(q),{headers:{Accept:'application/json'}});if(!r.ok)throw new Error('search HTTP '+r.status);const d=await r.json();box.innerHTML=d.length?d.map((x,i)=>`<button data-i="${i}" style="display:block;width:100%;text-align:left;background:transparent;border:0;color:inherit;padding:7px;font-size:8px;border-bottom:1px solid rgba(45,85,100,.18)">${esc(x.display_name)}</button>`).join(''):'<div style="padding:7px;font-size:8px;color:var(--muted)">No location found</div>';box.style.display='block';box.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>{const x=d[+b.dataset.i];$('site_lat').value=(+x.lat).toFixed(6);$('site_lon').value=(+x.lon).toFixed(6);$('coords').textContent=(+x.lat).toFixed(6)+', '+(+x.lon).toFixed(6);$('locate').click();s.value=x.display_name;box.style.display='none';toast('Location selected from search')})}catch(e){box.innerHTML='<div style="padding:7px;font-size:8px;color:var(--bad)">Search unavailable</div>';box.style.display='block'}};
 s.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>query(s.value.trim()),350)});document.addEventListener('click',e=>{if(!holder.contains(e.target))box.style.display='none'});
}
function enforceNoLegacyCopy(){document.querySelectorAll('#landuse1 option,#landuse2 option,#landuse3 option').forEach(o=>{if(o.textContent.trim().toLowerCase()==='perdagangan')o.remove()})}
function boot(){repopulateLandUse();addUtilities();addSearch();enforceNoLegacyCopy();setTimeout(()=>{window.URBION_FINAL.refreshMap?.();window.URBION_FINAL.loadLayers?.();},350);}
waitForCore(boot);
})();

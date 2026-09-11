/* URBION HORIZON — canonical runtime takeover.
   Removes competing inline handlers after the canonical core loads, then
   binds one authoritative handler per visible control. */
(()=>{
'use strict';
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function waitForCore(done){let n=0;const tick=()=>{if(window.URBION_FINAL){done();return}if(n++<120){setTimeout(tick,100)}else console.warn('URBION_FINAL not available')};tick()}
function toast(message,ok=true){const t=$('toast');if(!t)return;t.textContent=message;t.style.display='block';t.style.color=ok?'var(--good)':'var(--bad)';clearTimeout(window.__urbionToastTimer);window.__urbionToastTimer=setTimeout(()=>{t.style.display='none'},2400)}
function modal(title,html){const m=$('modal');if(!m)return;$('modalTitle').textContent=title;$('modalBody').innerHTML=html;$('modal').classList.add('show')}
function replaceNode(el){if(!el||!el.parentNode)return el;const clone=el.cloneNode(true);el.parentNode.replaceChild(clone,el);return clone}
function takeoverControls(){
  document.querySelectorAll('button').forEach(replaceNode);
  ['landuse1','landuse2','landuse3','state','roadCtx','roadCtxMap','context400','context800','context1000','ring400','ring800','ring1000','search'].forEach(id=>{const e=$(id);if(e)replaceNode(e)});
  document.querySelectorAll('.sec .sechead button').forEach(b=>b.addEventListener('click',()=>b.parentElement.parentElement.classList.toggle('collapsed')));
}
function setupLandUse(){
  const gt=window.URBION_FINAL?.GT,a=$('landuse1'),b=$('landuse2'),c=$('landuse3');
  if(!gt||!a||!b||!c)return;
  const fill=(sel,items,placeholder)=>{sel.innerHTML=(placeholder?`<option value="">${esc(placeholder)}</option>`:'')+items.map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join('')};
  const cats=Object.keys(gt).filter(x=>x.toLowerCase()!=='perdagangan');
  fill(a,cats);if(cats.includes('Komersial'))a.value='Komersial';
  const sync3=()=>{const acts=(gt[a.value]||{})[b.value]||[];fill(c,acts,'Pilih Aktiviti Guna Tanah 3')};
  const sync2=()=>{fill(b,Object.keys(gt[a.value]||{}),'Pilih Guna Tanah 2');sync3()};
  a.addEventListener('change',sync2);b.addEventListener('change',sync3);sync2();
  let badge=$('gtnBadge');if(!badge){badge=document.createElement('div');badge.id='gtnBadge';a.parentElement.insertBefore(badge,a)}
  badge.style.cssText='font-size:6px;color:var(--mint);margin:-3px 0 5px;letter-spacing:.06em';
  badge.textContent='PLANMalaysia · Manual GIS Rancangan Pemajuan Versi 3.0 (2025) · GT1 → GT2 → GT3';
}
function bindMapControls(){
  document.querySelectorAll('[data-base]').forEach(b=>b.addEventListener('click',()=>window.URBION_FINAL.setBase?.(b.dataset.base)));
  $('layerBtn')?.addEventListener('click',()=>{$('layers')?.classList.toggle('open');window.URBION_FINAL.loadLayers?.()});
  $('run')?.addEventListener('click',()=>window.URBION_FINAL.analyse?.());
  $('evidenceBtn')?.addEventListener('click',()=>openCore('evidence'));
  $('whatifBtn')?.addEventListener('click',()=>openCore('whatif'));
  $('decisionBtn')?.addEventListener('click',()=>openCore('decision'));
  $('outputBtn')?.addEventListener('click',()=>openCore('output'));
  $('generateOutput')?.addEventListener('click',()=>openCore('output'));
  $('printBtn')?.addEventListener('click',()=>window.print());
  $('closeModal')?.addEventListener('click',()=>$('modal')?.classList.remove('show'));
  $('useMap')?.addEventListener('click',()=>toast('Click the map to choose the site'));
  $('locate')?.addEventListener('click',()=>{window.URBION_FINAL.refreshMap?.();toast('Map recentered to selected site')});
  ['context400','context800','context1000'].forEach((id,i)=>$(id)?.addEventListener('change',e=>{const obj=window[['r400','r800','r1000'][i]];if(obj&&window.map){e.target.checked?obj.addTo(window.map):obj.removeFrom(window.map)}}));
  [['ring400','context400'],['ring800','context800'],['ring1000','context1000']].forEach(([button,check])=>$(button)?.addEventListener('click',()=>{const c=$(check);if(c)c.checked=!c.checked;c?.dispatchEvent(new Event('change'))}));
  $('roadCtx')?.addEventListener('change',e=>{if(!window.map||!window.L)return;if(!window.__urbionRoadLayer)window.__urbionRoadLayer=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{opacity:.42,maxZoom:19,attribution:'© OpenStreetMap'});e.target.checked?window.__urbionRoadLayer.addTo(window.map):window.map.removeLayer(window.__urbionRoadLayer)});
  $('roadCtxMap')?.addEventListener('change',e=>{$('roadCtx').checked=e.target.checked;$('roadCtx').dispatchEvent(new Event('change'))});
}
async function searchBinding(){
  const s=$('search');if(!s)return;const holder=s.parentElement;holder.style.position='relative';const box=document.createElement('div');box.id='runtimeSearchResults';box.style.cssText='position:absolute;left:0;right:0;top:39px;z-index:1200;display:none;max-height:220px;overflow:auto;background:#061820;border:1px solid var(--line);border-radius:9px;padding:6px';holder.appendChild(box);let timer;
  const query=async q=>{if(q.length<3){box.style.display='none';return}try{const r=await fetch('https://nominatim.openstreetmap.org/search?format=jsonv2&limit=5&q='+encodeURIComponent(q),{headers:{Accept:'application/json'}});if(!r.ok)throw new Error('search HTTP '+r.status);const d=await r.json();box.innerHTML=d.length?d.map((x,i)=>`<button type="button" data-i="${i}" style="display:block;width:100%;text-align:left;background:transparent;border:0;color:inherit;padding:7px;font-size:8px;border-bottom:1px solid rgba(45,85,100,.18)">${esc(x.display_name)}</button>`).join(''):'<div style="padding:7px;font-size:8px;color:var(--muted)">No location found</div>';box.style.display='block';box.querySelectorAll('[data-i]').forEach(btn=>btn.onclick=()=>{const x=d[+btn.dataset.i],lat=+x.lat,lon=+x.lon;$('site_lat').value=lat.toFixed(6);$('site_lon').value=lon.toFixed(6);$('coords').textContent=`${lat.toFixed(6)}, ${lon.toFixed(6)}`;window.URBION_FINAL.refreshMap?.();s.value=x.display_name;box.style.display='none';toast('Location selected')})}catch(e){box.innerHTML='<div style="padding:7px;font-size:8px;color:var(--bad)">Search unavailable</div>';box.style.display='block'}};
  s.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>query(s.value.trim()),350)});s.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();query(s.value.trim())}});document.addEventListener('click',e=>{if(!holder.contains(e.target))box.style.display='none'});
}
function openCore(kind){
  if(kind==='evidence')return evidenceView();
  if(kind==='whatif')return window.URBION_FINAL.whatif?.();
  if(kind==='decision')return window.URBION_FINAL.decision?.();
  if(kind==='output')return window.URBION_FINAL.output?.();
}
function evidenceView(){
  const r=window.URBION_LAST||{};const items=Array.isArray(r.evidence_register)?r.evidence_register:(Array.isArray(r.evidence?.evidence_register)?r.evidence.evidence_register:[]);const gaps=Array.isArray(r.review_gaps)?r.review_gaps:[];
  const rows=items.slice(0,15).map(x=>`<tr><td>${esc(x.source||x.name||'Source')}</td><td>${esc(x.status||x.evidence_status||'—')}</td><td>${esc(x.finding||x.summary||'—')}</td><td>${esc(x.implication||x.reason||'—')}</td></tr>`).join('')||'<tr><td colspan="4">No structured evidence register returned.</td></tr>';
  modal('EVIDENCE CHAIN',`<div class="resultbox"><h4>BOUNDARY</h4><p>Live source context, calculated evidence and verification status remain distinct. No statutory approval is inferred.</p></div><div style="height:8px"></div><table class="table"><thead><tr><th>SOURCE</th><th>STATUS</th><th>FINDING</th><th>IMPLICATION</th></tr></thead><tbody>${rows}</tbody></table><div class="resultbox" style="margin-top:8px"><h4>REVIEW GAPS (${gaps.length})</h4><p>${esc(gaps.map(x=>x.title||x).join(' · ')||'None returned')}</p></div>`);
}
function bindNav(){
  document.querySelectorAll('.nav button').forEach(b=>b.addEventListener('click',()=>{
    document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('active'));b.classList.add('active');
    const m=b.dataset.mode;if(m==='whatif')window.URBION_FINAL.whatif?.();else if(m==='decision')window.URBION_FINAL.decision?.();else if(m==='output')window.URBION_FINAL.output?.();else if(m==='evidence')evidenceView();else{$('modal')?.classList.remove('show');window.scrollTo(0,0);toast('Planning workspace active')}
  }));
}
function bindUtility(){
  $('themeBtn')?.addEventListener('click',()=>document.body.classList.toggle('light'));
  $('langBtn')?.addEventListener('click',()=>{const bm=$('langBtn').textContent==='EN';$('langBtn').textContent=bm?'BM':'EN';document.documentElement.lang=bm?'ms':'en';const dict=bm?{'PLAN':'PELAN','EVIDENCE':'BUKTI','WHAT-IF':'BAGAIMANA JIKA','DECISION':'KEPUTUSAN','OUTPUT':'OUTPUT','Map':'Peta','Satellite':'Satelit','Hybrid':'Hibrid','Layers':'Lapisan','Planning Case':'Kes Perancangan'}:{'PELAN':'PLAN','BUKTI':'EVIDENCE','BAGAIMANA JIKA':'WHAT-IF','KEPUTUSAN':'DECISION','Peta':'Map','Satelit':'Satellite','Hibrid':'Hybrid','Lapisan':'Layers','Kes Perancangan':'Planning Case'};document.querySelectorAll('button,.lab,.sechead button,.dock h3,.card h3,.maptag').forEach(el=>{const t=el.textContent.trim();if(dict[t])el.textContent=dict[t]});toast(bm?'BM mode':'EN mode')});
  $('runtimeAbout')?.addEventListener('click',()=>location.href='/about');
}
function addUtilities(){
  const top=$('.top');if(!top||$('runtimeTools'))return;const box=document.createElement('div');box.id='runtimeTools';box.style.cssText='display:flex;align-items:center;gap:4px;margin-left:4px';
  const make=(id,label)=>{const b=document.createElement('button');b.id=id;b.className='tool';b.type='button';b.textContent=label;return b};
  const about=make('runtimeAbout','ABOUT'),help=make('runtimeHelp','HELP'),sources=make('runtimeSources','SOURCES'),status=make('runtimeStatus','STATUS'),fs=make('runtimeFullscreen','FULLSCREEN'),reset=make('runtimeReset','RESET');[about,help,sources,status,fs,reset].forEach(b=>box.appendChild(b));$('themeBtn')?.parentNode?.insertBefore(box,$('themeBtn').nextSibling);
  help.onclick=()=>modal('URBION HORIZON — HELP','<div class="grid2"><div class="resultbox"><h4>CASE</h4><p>Define location, development and the Guna Tanah 1 → 2 → 3 hierarchy.</p></div><div class="resultbox"><h4>MAP</h4><p>Use Map / Satellite / Hybrid and click the map to select a site.</p></div><div class="resultbox"><h4>LAYERS</h4><p>Open Layers and switch official catalogue layers ON/OFF. Source/type state is shown alongside the layer.</p></div><div class="resultbox"><h4>ANALYSE</h4><p>Run Site Analysis to populate spatial evidence, RT/GP, evidence health and decision support.</p></div></div>');
  sources.onclick=()=>modal('DATA SOURCES','<div class="resultbox"><h4>PLANNING / SPATIAL</h4><p>PLANMalaysia i-Plan · official map/service context returned by the workspace catalogue · planning documents and guideline context.</p></div><div style="height:8px"></div><div class="resultbox"><h4>BASEMAP</h4><p>OpenStreetMap · Esri World Imagery · Esri reference labels.</p></div>');
  status.onclick=async()=>{let html='';for(const [label,url] of [['Health','/health'],['Metadata','/metadata'],['Map catalogue','/map/layers?state='+encodeURIComponent($('state')?.value||'Melaka')]]){try{const r=await fetch(url,{cache:'no-store'});html+=`<div class="mini"><span>${label}</span><span class="tag ${r.ok?'ok':'bad'}">${r.ok?'ONLINE':'ERROR '+r.status}</span></div>`}catch(e){html+=`<div class="mini"><span>${label}</span><span class="tag bad">ERROR</span></div>`}}modal('SYSTEM STATUS',html)};
  fs.onclick=async()=>{try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen()}catch(e){toast('Fullscreen unavailable',false)}};
  reset.onclick=()=>{if(confirm('Reset this planning case?'))location.reload()};
}
async function boot(){await sleep(50);takeoverControls();setupLandUse();bindMapControls();bindNav();addUtilities();bindUtility();await searchBinding();setTimeout(()=>{window.URBION_FINAL.refreshMap?.();window.URBION_FINAL.loadLayers?.()},250)}
waitForCore(()=>boot().catch(e=>console.error('URBION runtime boot failed',e)));
})();

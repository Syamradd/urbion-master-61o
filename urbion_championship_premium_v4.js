(()=>{
'use strict';
if(window.__URBION_PREMIUM_V4)return;
window.__URBION_PREMIUM_V4=true;
const root=()=>document.getElementById('urbion-final-command-centre');
const map=()=>window.__URBION_FCC_MAP__||null;
const fmtRadius=r=>r>=1000?`${r/1000} km`:`${r} m`;
function logoSync(){const r=root(),img=r?.querySelector('.fcc-brand img');if(img)img.src=document.body.classList.contains('fcc-light')?'/urbion_logo_light.svg':'/urbion_logo_dark.svg';}
function drawRelations(){
 const m=map(); if(!m||!window.L)return;
 const slat=Number(document.getElementById('fcc-lat')?.value),slon=Number(document.getElementById('fcc-lon')?.value),tlat=Number(document.getElementById('fcc-todlat')?.value),tlon=Number(document.getElementById('fcc-todlon')?.value);
 window.__URBION_FCC_RELATION_LINE__&&m.removeLayer(window.__URBION_FCC_RELATION_LINE__);
 if([slat,slon,tlat,tlon].every(Number.isFinite)){
  window.__URBION_FCC_RELATION_LINE__=L.polyline([[slat,slon],[tlat,tlon]],{weight:2.2,color:'#67e6c5',opacity:.9,dashArray:'6 6',interactive:false}).addTo(m);
 }
}
function groupLayers(){
 const d=document.getElementById('fcc-layer-drawer');if(!d||d.dataset.v4Grouped)return;
 const rows=[...d.querySelectorAll('.fcc-layer-row')]; if(!rows.length)return;
 const groups={
  'PLANNING & LAND USE':/i-Plan · (Current|Zoning|Committed|RFN)/,
  'ENVIRONMENT & RISK':/i-Plan · (Flood|Disaster Risk|KSAS)|MyEQMS/,
  'ECOLOGY · HERITAGE · HOUSING':/i-Plan · (CFS|Ecological Network|Heritage|Affordable Housing)/,
  'TERRAIN · GEOLOGY':/i-Plan · Topography|MyGEMS/,
  'HYDROLOGY':/JPS · Public Infobanjir/,
  'CADASTRAL':/JUPEM MyLot/
 };
 const wrap=document.createDocumentFragment();
 const used=new Set();
 for(const [title,re] of Object.entries(groups)){
  const matched=rows.filter(r=>re.test(r.textContent||'')); if(!matched.length)continue;
  const sec=document.createElement('div');sec.className='fcc-layer-group';sec.innerHTML=`<div class="fcc-layer-group-title">${title}</div>`;
  matched.forEach(r=>{sec.appendChild(r);used.add(r)});wrap.appendChild(sec);
 }
 rows.filter(r=>!used.has(r)).forEach(r=>wrap.appendChild(r));
 d.replaceChildren(wrap);d.dataset.v4Grouped='1';
}
function openSettings(){
 let p=document.getElementById('urbion-v4-settings');if(p){p.remove();return;}
 p=document.createElement('div');p.id='urbion-v4-settings';p.className='urbion-v4-settings';
 p.innerHTML=`<button data-x class="sv-x">×</button><span class="sv-kicker">URBION HORIZON · WORKSPACE CONTROL</span><h3>Workspace Settings</h3><p>Control the presentation without changing the planning engine or statutory authority boundary.</p><section><b>LANGUAGE</b><div><button data-lang="en">ENGLISH</button><button data-lang="bm">BAHASA MELAYU</button></div></section><section><b>THEME</b><div><button data-theme="dark">DARK</button><button data-theme="light">LIGHT</button></div></section><section><b>MAP BASE</b><div><button data-base="street">STREET</button><button data-base="dark">DARK MAP</button></div></section><section><b>SCREENING WINDOW</b><div><button data-radius="400">400 m</button><button data-radius="800">800 m</button><button data-radius="1000">1 km</button><button data-radius="1500">1.5 km</button></div></section><section><b>MOTION</b><div><button data-motion="normal">NORMAL</button><button data-motion="reduced">REDUCED</button></div></section><small class="sv-foot">GIS layers are source-context evidence. Radius bands are screening/context aids, not statutory buffers.</small>`;
 document.body.appendChild(p);
 p.querySelector('[data-x]').onclick=()=>p.remove();
 p.querySelectorAll('[data-lang]').forEach(b=>b.onclick=()=>{localStorage.setItem('urbion-lang',b.dataset.lang);document.getElementById('fcc-lang')?.click();});
 p.querySelectorAll('[data-theme]').forEach(b=>b.onclick=()=>{const light=b.dataset.theme==='light';if(light!==document.body.classList.contains('fcc-light'))document.getElementById('fcc-theme')?.click();logoSync();});
 p.querySelectorAll('[data-base]').forEach(b=>b.onclick=()=>{
  const m=map();if(!m||!window.L)return;
  window.__URBION_FCC_DARK_BASE__=window.__URBION_FCC_DARK_BASE__||L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{maxZoom:20,attribution:'© OpenStreetMap © CARTO'});
  const street=window.__URBION_FCC_BASE_TILE__,dark=window.__URBION_FCC_DARK_BASE__;
  if(b.dataset.base==='dark'){if(street&&m.hasLayer(street))m.removeLayer(street);if(!m.hasLayer(dark))dark.addTo(m);}else{if(dark&&m.hasLayer(dark))m.removeLayer(dark);if(street&&!m.hasLayer(street))street.addTo(m);}
 });
 p.querySelectorAll('[data-radius]').forEach(b=>b.onclick=()=>refreshRadius(Number(b.dataset.radius),p));
 p.querySelectorAll('[data-motion]').forEach(b=>b.onclick=()=>{document.documentElement.dataset.urbionMotion=b.dataset.motion;p.classList.toggle('reduced',b.dataset.motion==='reduced');});
}
async function refreshRadius(radius,panel){
 const lat=Number(document.getElementById('fcc-lat')?.value),lon=Number(document.getElementById('fcc-lon')?.value),state=document.getElementById('fcc-state')?.value||'Melaka';
 if(!map()||!Number.isFinite(lat)||!Number.isFinite(lon))return;
 const note=panel.querySelector('.sv-foot');note.textContent=`Refreshing ${fmtRadius(radius)} spatial context…`;
 try{const r=await fetch('/spatial/site-context',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({site_lat:lat,site_lon:lon,radius_m:radius,state})});if(!r.ok)throw new Error(`HTTP ${r.status}`);const d=await r.json();const n=(d.layers||d.results||[]).length;note.textContent=`${fmtRadius(radius)} context refreshed · ${n} source records · source-labelled evidence.`;}catch(e){note.textContent=`${fmtRadius(radius)} context returned an evidence gap; existing map remains unchanged.`;}
}
function outputBridge(){
 const out=document.getElementById('fcc-export');if(!out||out.dataset.v4Export)return;out.dataset.v4Export='1';
 out.onclick=(e)=>{e.preventDefault();const unified=window.URBION_FINAL_RUN?.package||window.URBION_FINAL_RUN?.packet||window.URBION_FINAL_RUN?.case_package||window.URBION_FINAL_RUN;if(unified&&typeof unified==='object')download(unified,'urbion-horizon-unified-case-package.json');else document.getElementById('fcc-export-legacy')?.click?.();};
}
function download(obj,name){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify(obj,null,2)],{type:'application/json'}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function footerBrand(){const f=root()?.querySelector('.fcc-footer');if(!f||f.dataset.v4)return;f.dataset.v4='1';const meta=document.createElement('div');meta.className='fcc-footer-meta';meta.textContent='URBION HORIZON · MASTER-132 · PHASE-E.8 · PLANNER DECISION SUPPORT ONLY';f.appendChild(meta);}
function css(){if(document.getElementById('urbion-premium-v4-style'))return;const s=document.createElement('style');s.id='urbion-premium-v4-style';s.textContent=`
#urbion-final-command-centre .fcc-case,#urbion-final-command-centre .fcc-rail{box-shadow:inset 0 0 0 1px rgba(103,230,197,.025)}
#urbion-final-command-centre .fcc-card,#urbion-final-command-centre .fcc-map-card{box-shadow:0 20px 55px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.018)!important}
#urbion-final-command-centre .fcc-head-actions button,#urbion-final-command-centre .fcc-map-actions button{transition:transform .15s ease,border-color .15s ease,box-shadow .15s ease}
#urbion-final-command-centre .fcc-head-actions button:active,#urbion-final-command-centre .fcc-map-actions button:active{transform:translateY(1px)}
#urbion-final-command-centre button:focus-visible,#urbion-final-command-centre input:focus-visible,#urbion-final-command-centre select:focus-visible{outline:2px solid #67e6c5;outline-offset:2px}
.fcc-layer-group-title{padding:9px 7px 5px;color:#67e6c5;font-size:8px;font-weight:900;letter-spacing:.12em;border-top:1px solid #1b3442;margin-top:3px}
.fcc-layer-group:first-child .fcc-layer-group-title{border-top:0;margin-top:0}
.urbion-v4-settings{position:fixed;top:82px;right:24px;width:min(430px,calc(100vw - 32px));z-index:12000;padding:20px;border:1px solid #2d5160;border-radius:18px;background:linear-gradient(150deg,#0a1c28,#06111a);color:#eaf6f9;box-shadow:0 30px 90px rgba(0,0,0,.52)}
.urbion-v4-settings .sv-x{position:absolute;right:13px;top:11px;border:0;background:transparent;color:#7896a3;font-size:20px}.urbion-v4-settings .sv-kicker{font-size:8px;letter-spacing:.16em;color:#58c9e8;font-weight:900}.urbion-v4-settings h3{margin:6px 0 4px;font:700 24px 'Space Grotesk'}.urbion-v4-settings p{margin:0 0 14px;color:#8fa9b4;font-size:10px;line-height:1.65}.urbion-v4-settings section{padding:11px 0;border-top:1px solid #193441}.urbion-v4-settings section>b{display:block;color:#6f8996;font-size:8px;letter-spacing:.12em;margin-bottom:7px}.urbion-v4-settings section>div{display:flex;gap:6px;flex-wrap:wrap}.urbion-v4-settings section button{border:1px solid #294b5b;border-radius:9px;background:#091722;color:#9bb0ba;padding:8px 10px;font-size:9px;font-weight:800}.urbion-v4-settings section button:hover{border-color:#67e6c5;color:#67e6c5}.urbion-v4-settings .sv-foot{display:block;margin-top:12px;padding:9px;border:1px dashed #294856;border-radius:9px;color:#78929e;font-size:8px;line-height:1.55}
.urbion-v4-settings.reduced~#urbion-final-command-centre *{animation:none!important;transition:none!important}
#urbion-final-command-centre .fcc-footer-meta{grid-column:1/-1;color:#527280;font-size:7px;letter-spacing:.1em;padding-top:3px}
@media(max-width:900px){.urbion-v4-settings{right:12px;top:74px}}
@media(prefers-reduced-motion:reduce){.urbion-v4-settings{scroll-behavior:auto}.urbion-v4-settings *{transition:none!important;animation:none!important}}
`;
document.head.appendChild(s);}
function boot(){const r=root();if(!r)return;css();const more=document.getElementById('fcc-more');if(more&&!more.dataset.v4){more.dataset.v4='1';more.onclick=openSettings;}groupLayers();drawRelations();footerBrand();outputBridge();['fcc-lat','fcc-lon','fcc-todlat','fcc-todlon'].forEach(id=>document.getElementById(id)?.addEventListener('change',drawRelations));}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(boot,80),{once:true});else setTimeout(boot,80);
})();

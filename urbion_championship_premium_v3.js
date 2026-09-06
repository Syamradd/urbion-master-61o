(()=>{
'use strict';
if(window.__URBION_PREMIUM_V3)return;
window.__URBION_PREMIUM_V3=true;

/*
 * Premium V3 = presentation + controlled map enhancements only.
 * No polling, MutationObserver loops, background timers, or automatic API storms.
 * The map hook runs before the final command centre so the final Leaflet instance
 * can be enhanced without duplicating the map itself.
 */
function hookLeaflet(){
 if(window.L && !window.__URBION_FCC_LEAFLET_HOOKED){
  const originalMap=window.L.map;
  window.L.map=function(){
   const m=originalMap.apply(this,arguments);
   window.__URBION_FCC_MAP__=m;
   return m;
  };
  const originalTile=window.L.tileLayer;
  window.L.tileLayer=function(){
   const layer=originalTile.apply(this,arguments);
   if(arguments[0]&&String(arguments[0]).includes('openstreetmap.org'))window.__URBION_FCC_BASE_TILE__=layer;
   return layer;
  };
  window.__URBION_FCC_LEAFLET_HOOKED=true;
 }
}

function boot(){
 hookLeaflet();
 const root=document.getElementById('urbion-final-command-centre');
 if(!root)return;
 if(!document.getElementById('urbion-premium-v3-style')){
  const s=document.createElement('style');
  s.id='urbion-premium-v3-style';
  s.textContent=`
#urbion-final-command-centre{font-family:Inter,ui-sans-serif,system-ui,sans-serif;font-size:14px;color:#eaf5f7;position:relative;isolation:isolate}
#urbion-final-command-centre:before{content:"";position:absolute;inset:0;pointer-events:none;z-index:0;background:radial-gradient(circle at 76% 8%,rgba(74,205,235,.12),transparent 26%),radial-gradient(circle at 13% 89%,rgba(78,225,189,.09),transparent 25%),linear-gradient(90deg,transparent 0 12%,rgba(66,196,223,.018) 12% 12.3%,transparent 12.3% 100%),repeating-linear-gradient(0deg,rgba(81,210,202,.018) 0 1px,transparent 1px 44px),repeating-linear-gradient(90deg,rgba(81,210,202,.018) 0 1px,transparent 1px 44px);opacity:.95}
#urbion-final-command-centre>*{position:relative;z-index:1}
#urbion-final-command-centre .fcc-kicker{font-size:10px!important;letter-spacing:.14em!important;font-weight:800!important;color:#67d9c0}
#urbion-final-command-centre .fcc-muted{font-size:12px!important;line-height:1.7!important;color:#8fa8b5!important}
#urbion-final-command-centre .fcc-header{height:72px!important;padding:0 28px!important;background:#06111add!important;backdrop-filter:none!important}
#urbion-final-command-centre .fcc-brand img{width:192px!important}
#urbion-final-command-centre .fcc-brand b{font-size:15px!important;font-weight:750!important}
#urbion-final-command-centre .fcc-brand small{font-size:8px!important;letter-spacing:.16em!important}
#urbion-final-command-centre .fcc-system{font-size:9px!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-head-actions button{font-size:12px!important;min-width:36px!important;height:34px!important;border-radius:10px!important;background:linear-gradient(180deg,#0c1d2a,#08141e)!important;border-color:#264655!important}
#urbion-final-command-centre .fcc-head-actions button:hover{border-color:#67e6c5!important;color:#67e6c5!important;box-shadow:0 0 0 1px rgba(103,230,197,.12)}
#urbion-final-command-centre .fcc-case h1,#urbion-final-command-centre .fcc-rail h2{font-size:26px!important;font-weight:750!important;letter-spacing:-.035em!important}
#urbion-final-command-centre .fcc-step{margin-top:20px!important;margin-bottom:10px!important;font-size:11px!important}
#urbion-final-command-centre .fcc-step b{font-size:10px!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-case label{font-size:10px!important;font-weight:650!important;letter-spacing:.01em!important}
#urbion-final-command-centre .fcc-case input,#urbion-final-command-centre .fcc-case select{font-size:12px!important;min-height:40px!important;padding:10px 12px!important}
#urbion-final-command-centre .fcc-readiness span{font-size:9px!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-readiness b{font-size:19px!important}
#urbion-final-command-centre .fcc-readiness small{font-size:10px!important;line-height:1.5!important}
#urbion-final-command-centre .fcc-run{font-size:10px!important;font-weight:850!important;letter-spacing:.08em!important}
#urbion-final-command-centre .fcc-reset{font-size:9px!important;letter-spacing:.06em!important}
#urbion-final-command-centre .fcc-status{font-size:10px!important;line-height:1.6!important}
#urbion-final-command-centre .fcc-commandbar h2{font-size:31px!important;font-weight:700!important;letter-spacing:-.04em!important;max-width:880px}
#urbion-final-command-centre .fcc-tabs{gap:6px!important;padding:4px!important;border:1px solid rgba(110,172,190,.18)!important;border-radius:12px!important;background:rgba(5,16,25,.62)!important}
#urbion-final-command-centre .fcc-tabs button{font-size:10px!important;font-weight:750!important;letter-spacing:.02em!important;padding:10px 13px!important;border-radius:8px!important;border-color:transparent!important;background:transparent!important}
#urbion-final-command-centre .fcc-tabs button.active{background:linear-gradient(180deg,rgba(103,230,197,.18),rgba(88,201,232,.07))!important;border-color:rgba(103,230,197,.28)!important;color:#8ff0d5!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.03)}
#urbion-final-command-centre .fcc-map-card,#urbion-final-command-centre .fcc-card{border-color:#213a48!important;background:linear-gradient(150deg,rgba(12,28,41,.97),rgba(6,16,25,.98))!important;box-shadow:0 18px 52px rgba(0,0,0,.22)!important}
#urbion-final-command-centre .fcc-map-head{padding:13px 15px!important}
#urbion-final-command-centre .fcc-map-head b{font-size:10px!important;letter-spacing:.04em!important}
#urbion-final-command-centre .fcc-map-head span{font-size:10px!important}
#urbion-final-command-centre .fcc-map-actions{gap:6px!important}
#urbion-final-command-centre .fcc-map-actions button{font-size:9px!important;font-weight:700!important;padding:8px 10px!important;border-radius:8px!important;background:#081721!important;border-color:#254353!important}
#urbion-final-command-centre .fcc-map-actions button:hover{border-color:#67e6c5!important;color:#67e6c5!important}
#urbion-final-command-centre .fcc-layer-drawer{background:rgba(6,17,26,.98)!important;backdrop-filter:none!important}
#urbion-final-command-centre .fcc-layer-row b{font-size:10px!important}.fcc-layer-row small{font-size:9px!important}
#urbion-final-command-centre .fcc-card-head span{font-size:10px!important;letter-spacing:.06em!important}.fcc-card-head>b{font-size:17px!important}
#urbion-final-command-centre .fcc-card strong{font-size:19px!important}.fcc-card p{font-size:11px!important;line-height:1.7!important}
#urbion-final-command-centre .fcc-chain span{font-size:10px!important;padding:12px!important}.fcc-chain small{font-size:9px!important;line-height:1.55!important}
#urbion-final-command-centre .fcc-signal{font-size:10px!important}.fcc-signal b{font-size:8px!important}.fcc-health-list span{font-size:9px!important}.fcc-health-list small{font-size:8px!important}
#urbion-final-command-centre .fcc-next strong{font-size:15px!important}
#urbion-final-command-centre .e-row{padding:12px 0!important}.e-row b{font-size:10px!important}.e-row small{font-size:9px!important}.e-row>strong,.e-row>span{font-size:9px!important}
#urbion-final-command-centre .scenario strong{font-size:32px!important}.scenario span{font-size:10px!important}.scenario button{font-size:9px!important}
#urbion-final-command-centre .fcc-decision-list div{font-size:10px!important;padding:10px!important}.output-grid strong{font-size:10px!important}.output-grid span{font-size:8px!important}
#urbion-final-command-centre .fcc-footer{font-size:9px!important;padding:20px 2px 6px!important;border-top:1px solid rgba(117,168,183,.12)!important;margin-top:8px!important}.fcc-footer b{font-size:10px!important;color:#a8c2cc!important}.fcc-footer button{font-size:9px!important;padding:5px 2px!important}
#urbion-final-command-centre .fcc-modal-box{max-width:660px!important;background:linear-gradient(145deg,#0a1b27,#06111a)!important;border-color:#2a4b5b!important;box-shadow:0 32px 90px rgba(0,0,0,.48)!important}
#urbion-final-command-centre .fcc-modal-box h2{font-size:30px!important}.fcc-modal-box p{font-size:11px!important;line-height:1.8!important}
.urbion-v3-settings{position:fixed;top:82px;right:24px;z-index:12000;width:min(390px,calc(100vw - 32px));padding:16px;border:1px solid #2a4b5b;border-radius:16px;background:linear-gradient(145deg,#081823,#050f17);box-shadow:0 24px 70px rgba(0,0,0,.5)}
.urbion-v3-settings h3{margin:0 0 4px;font:700 20px 'Space Grotesk';color:#eef8fb}.urbion-v3-settings p{margin:0 0 14px;color:#8da6b3;font-size:10px;line-height:1.6}.urbion-v3-settings .sv-row{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:10px 0;border-top:1px solid #19323f}.urbion-v3-settings .sv-row span{font-size:10px;color:#b4c6ce}.urbion-v3-settings button{border:1px solid #264655;border-radius:8px;background:#091721;color:#9ab2bd;padding:7px 9px;font-size:8px;font-weight:800}.urbion-v3-settings button.active{border-color:#67e6c5;color:#67e6c5;background:#67e6c50e}.urbion-v3-settings .sv-radios{display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end}.urbion-v3-settings .sv-note{margin-top:12px;padding:9px;border:1px dashed #274653;border-radius:9px;color:#7893a1;font-size:8px;line-height:1.55}
.urbion-v3-radius-legend{position:absolute;left:14px;bottom:14px;z-index:900;background:rgba(5,14,22,.92);border:1px solid #294a58;border-radius:11px;padding:9px 10px;min-width:150px;box-shadow:0 12px 30px rgba(0,0,0,.3);font-size:8px;color:#b4c8cf}.urbion-v3-radius-legend b{display:block;color:#67e6c5;font-size:9px;margin-bottom:5px}.urbion-v3-radius-legend span{display:flex;gap:7px;align-items:center;margin:3px 0}.urbion-v3-dot{width:7px;height:7px;border-radius:50%;display:inline-block;border:1px solid #7ae7d1;background:rgba(103,230,197,.08)}
@media(max-width:900px){#urbion-final-command-centre .fcc-commandbar h2{font-size:27px!important}.urbion-v3-settings{right:12px;top:74px}}
@media(max-width:600px){#urbion-final-command-centre .fcc-commandbar h2{font-size:23px!important}.urbion-v3-settings{width:calc(100vw - 24px);right:12px}.urbion-v3-radius-legend{left:8px;bottom:8px}}
@media(prefers-reduced-motion:reduce){#urbion-final-command-centre *{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
`;
  document.head.appendChild(s);
 }

 const more=document.getElementById('fcc-more');
 if(more&&!more.dataset.v3Bound){
  more.dataset.v3Bound='1';
  more.onclick=()=>openSettings(root);
 }
 const logo=root.querySelector('.fcc-brand img');
 const syncLogo=()=>{if(logo)logo.src=document.body.classList.contains('fcc-light')?'/urbion_logo_light.svg':'/urbion_logo_dark.svg';};
 if(logo&&!logo.dataset.v3Theme){logo.dataset.v3Theme='1';syncLogo();}
 addSpatialEnhancements(root);
}

function mapReady(){return window.__URBION_FCC_MAP__&&window.L;}
function openSettings(root){
 let panel=document.getElementById('urbion-v3-settings');
 if(panel){panel.remove();return;}
 panel=document.createElement('div');panel.id='urbion-v3-settings';panel.className='urbion-v3-settings';
 panel.innerHTML=`<button data-close style="float:right;border:0;background:transparent;font-size:18px;padding:2px;color:#7893a1">×</button><span style="font-size:8px;letter-spacing:.16em;color:#58c9e8;font-weight:900">URBION HORIZON · CONTROL SURFACE</span><h3>Workspace Settings</h3><p>Presentation controls are local to this browser. Live GIS evidence remains source-labelled and is never promoted to statutory approval.</p><div class="sv-row"><span>Interface language</span><div class="sv-radios"><button data-lang="en">EN</button><button data-lang="bm">BM</button></div></div><div class="sv-row"><span>Workspace mode</span><div class="sv-radios"><button data-theme="dark">DARK</button><button data-theme="light">LIGHT</button></div></div><div class="sv-row"><span>Map display</span><div class="sv-radios"><button data-mapmode="street">STREET</button><button data-mapmode="dark">DARK MAP</button></div></div><div class="sv-row"><span>Screening radius</span><div class="sv-radios"><button data-radius="400">400m</button><button data-radius="800">800m</button><button data-radius="1000">1km</button><button data-radius="1500">1.5km</button></div></div><div class="sv-row"><span>Browser motion</span><div class="sv-radios"><button data-motion="normal">NORMAL</button><button data-motion="reduced">REDUCED</button></div></div><div class="sv-note" id="urbion-v3-setting-note">Four planning screening bands are supported: 400 m, 800 m, 1 km and 1.5 km. The selected radius refreshes source-context screening only.</div>`;
 document.body.appendChild(panel);
 const close=panel.querySelector('[data-close]');close.onclick=()=>panel.remove();
 panel.querySelectorAll('[data-lang]').forEach(b=>b.onclick=()=>{localStorage.setItem('urbion-lang',b.dataset.lang);document.getElementById('fcc-lang')?.click();});
 panel.querySelectorAll('[data-theme]').forEach(b=>b.onclick=()=>{const light=b.dataset.theme==='light';const body=document.body;if(light!==body.classList.contains('fcc-light'))document.getElementById('fcc-theme')?.click();syncLogo();});
 panel.querySelectorAll('[data-mapmode]').forEach(b=>b.onclick=()=>setMapMode(b.dataset.mapmode));
 panel.querySelectorAll('[data-radius]').forEach(b=>b.onclick=()=>runRadiusScreening(Number(b.dataset.radius),panel));
 panel.querySelectorAll('[data-motion]').forEach(b=>b.onclick=()=>{document.documentElement.dataset.urbionMotion=b.dataset.motion;panel.querySelector('#urbion-v3-setting-note').textContent=b.dataset.motion==='reduced'?'Reduced motion is active for the command centre.':'Normal motion is active for the command centre.';});
}
function setMapMode(mode){
 const m=window.__URBION_FCC_MAP__; if(!m||!window.L)return;
 window.__URBION_FCC_DARK_BASE__=window.__URBION_FCC_DARK_BASE__||L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{maxZoom:20,attribution:'© OpenStreetMap © CARTO'});
 const street=window.__URBION_FCC_BASE_TILE__,dark=window.__URBION_FCC_DARK_BASE__;
 if(mode==='dark'){if(street&&m.hasLayer(street))m.removeLayer(street);if(dark&&!m.hasLayer(dark))dark.addTo(m);}else{if(dark&&m.hasLayer(dark))m.removeLayer(dark);if(street&&!m.hasLayer(street))street.addTo(m);}
}
async function runRadiusScreening(radius,panel){
 const m=mapReady();if(!m){panel.querySelector('#urbion-v3-setting-note').textContent='Map not ready yet.';return;}
 const lat=Number(document.getElementById('fcc-lat')?.value),lon=Number(document.getElementById('fcc-lon')?.value),state=document.getElementById('fcc-state')?.value||'Melaka';
 if(!Number.isFinite(lat)||!Number.isFinite(lon))return;
 panel.querySelector('#urbion-v3-setting-note').textContent=`Refreshing ${radius>=1000?(radius/1000)+' km':radius+' m'} source-context screening…`;
 try{
  const r=await fetch('/spatial/site-context',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({site_lat:lat,site_lon:lon,radius_m:radius,state})});
  if(!r.ok)throw new Error('HTTP '+r.status);
  const d=await r.json();
  const n=(d.layers||d.results||[]).length;
  panel.querySelector('#urbion-v3-setting-note').textContent=`${radius>=1000?(radius/1000)+' km':radius+' m'} screening refreshed: ${n} source-context records. Evidence remains source-labelled.`;
  drawRadiusBands(lat,lon);
 }catch(e){panel.querySelector('#urbion-v3-setting-note').textContent=`Radius ${radius} m query returned an evidence gap. Existing map context remains unchanged.`;}
}
function drawRadiusBands(lat,lon){
 const m=mapReady();if(!m)return;
 window.__URBION_FCC_RING_LAYERS__?.forEach(x=>m.removeLayer(x));
 const specs=[[400,'400 m','0.32'],[800,'800 m','0.22'],[1000,'1 km','0.15'],[1500,'1.5 km','0.10']];
 const layers=specs.map(([r,label,fill])=>L.circle([lat,lon],{radius:r,weight:1.3,color:'#67e6c5',opacity:r===400?.72:.42,fillColor:'#67e6c5',fillOpacity:Number(fill),interactive:false})).map((c,i)=>{c.bindTooltip(specs[i][1],{permanent:false,direction:'center',className:'urbion-radius-tooltip'});c.addTo(m);return c;});
 window.__URBION_FCC_RING_LAYERS__=layers;
 let legend=document.getElementById('urbion-v3-radius-legend');
 if(!legend){legend=document.createElement('div');legend.id='urbion-v3-radius-legend';legend.className='urbion-v3-radius-legend';document.getElementById('fcc-map')?.appendChild(legend);}
 legend.innerHTML='<b>SCREENING RADII</b>'+specs.map(x=>`<span><i class="urbion-v3-dot"></i>${x[1]} screening / context</span>`).join('');
}
function addSpatialEnhancements(root){
 if(!mapReady()||root.dataset.v3Spatial)return;
 root.dataset.v3Spatial='1';
 const m=window.__URBION_FCC_MAP__;
 const lat=Number(document.getElementById('fcc-lat')?.value),lon=Number(document.getElementById('fcc-lon')?.value);
 if(Number.isFinite(lat)&&Number.isFinite(lon))drawRadiusBands(lat,lon);
 const mapBtn=document.getElementById('fcc-map');
 if(mapBtn)mapBtn.setAttribute('data-spatial-overlay','screening-radii-400m-800m-1km-1.5km');
 const fit=document.getElementById('fcc-fit');
 if(fit&&!fit.dataset.v3Radius){fit.dataset.v3Radius='1';}
 const onInput=()=>{const la=Number(document.getElementById('fcc-lat')?.value),lo=Number(document.getElementById('fcc-lon')?.value);if(Number.isFinite(la)&&Number.isFinite(lo))drawRadiusBands(la,lo);};
 ['fcc-lat','fcc-lon'].forEach(id=>document.getElementById(id)?.addEventListener('change',onInput,{passive:true}));
}

hookLeaflet();
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(boot,0),{once:true});else setTimeout(boot,0);
})();

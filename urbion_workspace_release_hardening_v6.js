/* URBION HORIZON — release hardening for the existing canonical V5 workspace.
   This layer does not add a planning engine or a second map. It takes ownership
   only of the visible GIS controls after the canonical layer manager renders them,
   adding reliable imagery fallbacks, opacity controls, diagnostics, and road-map
   presentation while preserving source/evidence boundaries. */
(()=>{
'use strict';
if(window.__URBION_RELEASE_HARDENING_V6__)return;
window.__URBION_RELEASE_HARDENING_V6__=true;
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>\"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[m]));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

function style(){
 if($('urbionReleaseHardeningStyle'))return;
 const s=document.createElement('style');s.id='urbionReleaseHardeningStyle';s.textContent=`
/* Keep Leaflet imagery above the decorative map veil. */
.mapwrap>#map{position:relative;z-index:2}
.mapwrap>.mapveil{z-index:1!important}
.mapwrap>.maptop,.mapwrap>.mapbottom{z-index:700!important}
.urbion-layer-tools-v6{display:flex;gap:5px;margin:0 0 7px}
.urbion-layer-tools-v6 button{flex:1;border:1px solid var(--line);background:#061923;color:var(--text);border-radius:7px;padding:6px 7px;font-size:6.5px}
.urbion-layer-tools-v6 button:hover{border-color:rgba(47,225,233,.45)}
.urbion-layer-row-v6{display:grid;grid-template-columns:16px minmax(0,1fr);gap:6px;padding:7px 1px 5px;border-bottom:1px solid rgba(45,85,100,.18);font-size:7.5px}
.urbion-layer-row-v6:last-child{border-bottom:0}
.urbion-layer-row-v6 input[type=checkbox]{accent-color:var(--cyan);margin-top:2px}
.urbion-layer-name-v6{display:flex;justify-content:space-between;gap:5px;align-items:center;min-width:0}
.urbion-layer-name-v6 b{font-size:7.2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.urbion-layer-source-v6{display:block;color:var(--muted);font-size:5.7px;margin-top:2px}
.urbion-layer-state-v6{font-size:5.8px;margin-top:4px;color:var(--muted)}
.urbion-layer-state-v6.ok{color:var(--good)}.urbion-layer-state-v6.loading{color:var(--warn)}.urbion-layer-state-v6.error{color:var(--bad)}
.urbion-opacity-v6{display:grid;grid-template-columns:auto 1fr auto;gap:5px;align-items:center;margin-top:4px;color:var(--muted);font-size:5.5px}
.urbion-opacity-v6 input{width:100%;accent-color:var(--cyan)}
.urbion-layer-legend-v6{font-size:5.5px;color:var(--muted);padding:5px 0 1px;line-height:1.35}
.urbion-road-map-note-v6{position:absolute;z-index:710;right:11px;bottom:11px;padding:6px 8px;border:1px solid rgba(47,225,233,.25);border-radius:8px;background:rgba(4,18,27,.92);color:var(--muted);font-size:5.8px;pointer-events:none}
.urbion-road-hierarchy-v6{display:grid;gap:4px;margin-top:7px}
.urbion-road-level-v6{display:grid;grid-template-columns:1fr auto;gap:7px;align-items:center;padding:6px 7px;border:1px solid rgba(45,85,100,.22);border-radius:7px}
.urbion-road-level-v6 b{font-size:6.6px}.urbion-road-level-v6 span{font-size:5.8px;color:var(--muted);text-align:right}
`;
 document.head.appendChild(s);
}
function mapObj(){try{return (typeof map!=='undefined'&&map)||window.__URBION_MAP__||null}catch(_){return null}}
function ensurePane(){const m=mapObj();if(!m)return null;let pane=m.getPane('urbionDataV6');if(!pane){pane=m.createPane('urbionDataV6');pane.style.zIndex='430';}return pane}
function mercatorBounds(x,y,z){const n=2**z,s=40075016.68557849/n;return[x*s-20037508.342789244,20037508.342789244-(y+1)*s,((x+1)*s)-20037508.342789244,20037508.342789244-y*s]}
function arcgisLayer(info){
 const pane=ensurePane();
 const Base=L.GridLayer.extend({createTile(c,done){
   const t=document.createElement('img');t.width=256;t.height=256;t.alt='';t.crossOrigin='anonymous';
   const b=mercatorBounds(c.x,c.y,c.z);const service=String(info.url||'').replace(/\/$/,'');
   const lid=info.layerId??info.layer_id??0;const u=location.origin+'/map/arcgis?service='+encodeURIComponent(service)+'&bbox='+b.join(',')+'&bboxSR=3857&imageSR=3857&size=256,256&imageDisplay=256,256,96&dpi=96&format=png32&transparent=true&f=image&layers=show:'+encodeURIComponent(lid);
   t.src=u;t.onload=()=>done(null,t);t.onerror=e=>done(e,t);return t;}});
 const l=new Base({tileSize:256,opacity:Number(info.opacity??.82),updateWhenIdle:false,keepBuffer:2,pane:pane?pane.name:undefined});
 l.__urbionInfo=info;return l;
}
function wmsLayer(info){
 const pane=ensurePane();
 const l=L.tileLayer.wms(location.origin+'/map/wms',{layers:info.layers,styles:'',format:'image/png',transparent:true,version:'1.1.1',opacity:Number(info.opacity??.78),tiled:true,pane:pane?pane.name:'overlayPane'});
 l.__urbionInfo=info;return l;
}
function tileLayer(info){const pane=ensurePane();const l=L.tileLayer(info.url,{maxZoom:19,opacity:Number(info.opacity??.78),attribution:info.name||info.source||'Source',pane:pane?pane.name:'overlayPane'});l.__urbionInfo=info;return l}
function criticalArcgis(info){
 const id=String(info.id||'');if(id==='iplan-current'){return {...info,type:'ARCGIS_MAP',url:'https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTsemasa_04/MapServer',layerId:0,source:'PLANMalaysia i-Plan / ArcGIS'}}
 if(id==='iplan-zoning'){return {...info,type:'ARCGIS_MAP',url:'https://scharms.planmalaysia.gov.my/arcgis/rest/services/iPLAN/GTzoning_04/MapServer',layerId:0,source:'PLANMalaysia i-Plan / ArcGIS'}}
 return info;
}
function makeLayer(info){const x=criticalArcgis(info);const type=String(x.type||'').toUpperCase();if(type==='GEOSERVER_WMS')return wmsLayer(x);if(type==='ARCGIS_MAP')return arcgisLayer(x);if(type==='TILE')return tileLayer(x);return null}
function layerRegistry(){window.__URBION_HARDENED_LAYERS__=window.__URBION_HARDENED_LAYERS__||{};return window.__URBION_HARDENED_LAYERS__}
function stateEl(id){return document.querySelector('[data-layer-state-v6="'+CSS.escape(id)+'"]')}
function setState(id,text,kind=''){const e=stateEl(id);if(e){e.textContent=text;e.className='urbion-layer-state-v6 '+kind}}
function removeLayer(id){const m=mapObj(),store=layerRegistry(),old=store[id];if(old&&m?.hasLayer(old))m.removeLayer(old);delete store[id]}
function renderLayer(info,on){const m=mapObj();if(!m)return;const store=layerRegistry();if(!on){removeLayer(info.id);setState(info.id,'OFF · HIDDEN');return}removeLayer(info.id);const resolved=criticalArcgis(info);setState(info.id,'LOADING · '+String(resolved.type||'SOURCE'),'loading');try{const layer=makeLayer(resolved);if(!layer)throw Error('Unsupported render type');layer.on?.('load',()=>setState(info.id,'ON · RENDERED','ok'));layer.on?.('tileload',()=>setState(info.id,'ON · RENDERED','ok'));layer.on?.('tileerror',()=>{setState(info.id,'ERROR · SOURCE','error')});layer.addTo(m);store[info.id]=layer;setTimeout(()=>{if(m.hasLayer(layer)&&!stateEl(info.id)?.textContent.includes('RENDERED'))setState(info.id,'ON · SOURCE CONNECTED','ok')},9000)}catch(e){setState(info.id,'ERROR · '+(e.message||'render failed'),'error')}}
function currentInfo(id){const arr=window.__URBION_LAYER_CATALOG__||[];return arr.find(x=>x&&x.id===id)||null}
function addOpacityUi(wrapper,info,checked){
 let box=wrapper.querySelector('.urbion-opacity-v6');if(!box){box=document.createElement('div');box.className='urbion-opacity-v6';box.innerHTML='<span>OPACITY</span><input type="range" min="0" max="100" step="5" value="78"><b>78%</b>';wrapper.appendChild(box)}
 const slider=box.querySelector('input'),label=box.querySelector('b');const store=layerRegistry();const old=store[info.id];const defaultOpacity=Math.round(Number(info.opacity??.78)*100);slider.value=String(old?Math.round((old.options?.opacity??Number(info.opacity??.78))*100):defaultOpacity);label.textContent=slider.value+'%';slider.oninput=()=>{const v=Number(slider.value)/100;label.textContent=slider.value+'%';if(store[info.id]?.setOpacity)store[info.id].setOpacity(v)};
}
function claimCheckboxes(){
 const list=$('layerList');if(!list)return false;
 list.querySelectorAll('input[data-urbion-layer]').forEach(oldCb=>{
   const id=oldCb.dataset.urbionLayer||oldCb.dataset.layer;if(!id)return;
   const wrapper=oldCb.closest('.urbion-layer-row')||oldCb.parentElement;const info=currentInfo(id);if(!wrapper||!info)return;
   if(oldCb.dataset.v6Claimed==='1'){addOpacityUi(wrapper,info,oldCb.checked);return}
   const cb=oldCb.cloneNode(true);cb.dataset.v6Claimed='1';oldCb.replaceWith(cb);
   cb.addEventListener('change',()=>renderLayer(info,cb.checked));
   addOpacityUi(wrapper,info,cb.checked);
   if(cb.checked&&!(layerRegistry()[id]))renderLayer(info,true);
 });
 return true;
}
function enhanceLayerPanel(){
 const list=$('layerList');if(!list)return;
 let tools=list.querySelector('.urbion-layer-tools-v6');if(!tools){tools=document.createElement('div');tools.className='urbion-layer-tools-v6';tools.innerHTML='<button type="button" id="urbionLayerClearV6">CLEAR OVERLAYS</button><button type="button" id="urbionLayerRefreshV6">REFRESH CATALOGUE</button>';list.prepend(tools);$('urbionLayerClearV6').onclick=()=>{Object.keys(layerRegistry()).forEach(removeLayer);list.querySelectorAll('input[data-urbion-layer]').forEach(x=>x.checked=false);list.querySelectorAll('.urbion-layer-state-v6').forEach(x=>x.textContent='OFF · HIDDEN')};$('urbionLayerRefreshV6').onclick=()=>void window.URBION_LAYER_MANAGER?.refresh?.()}
 const rows=list.querySelectorAll('.urbion-layer-row');rows.forEach(row=>{const cb=row.querySelector('input[data-urbion-layer]');if(cb)row.classList.add('urbion-layer-row-v6');});claimCheckboxes();
}
function observePanel(){const list=$('layerList');if(!list||list.dataset.v6Observed)return;list.dataset.v6Observed='1';new MutationObserver(()=>{enhanceLayerPanel()}).observe(list,{childList:true,subtree:true});}
function autoCriticalLayers(){const list=$('layerList');if(!list)return;for(const id of ['iplan-current','iplan-zoning']){const cb=list.querySelector('input[data-urbion-layer="'+id+'"]');if(cb&&!cb.checked){cb.dataset.autoCritical='1';cb.click();}}}
function roadOverlayFromData(data){
 const m=mapObj();if(!m||typeof L==='undefined')return;
 window.__URBION_ROAD_V6__=window.__URBION_ROAD_V6__||{layer:L.layerGroup().addTo(m)};const group=window.__URBION_ROAD_V6__.layer;group.clearLayers();
 const roads=Array.isArray(data?.road_access?.roads)?data.road_access.roads:[];
 roads.slice(0,25).forEach((r,i)=>{if(!Number.isFinite(Number(r.lat))||!Number.isFinite(Number(r.lon)))return;const marker=L.circleMarker([Number(r.lat),Number(r.lon)],{radius:i===0?6:4,weight:1,fillOpacity:.55,pane:'markerPane'}).addTo(group);marker.bindTooltip((r.name||'Road')+' · '+(r.hierarchy||r.highway||'OSM'),{direction:'top'});});
 let note=$('urbionRoadMapNoteV6');if(!note){note=document.createElement('div');note.id='urbionRoadMapNoteV6';note.className='urbion-road-map-note-v6';note.textContent='ROAD CONTEXT · OSM SOURCE';document.querySelector('.mapwrap')?.appendChild(note)}
}
function roadRender(data){
 const body=$('urbionRoadBody');if(!body)return;const levels=Array.isArray(data?.road_access?.hierarchy_levels)?data.road_access.hierarchy_levels:[];
 const existing=document.querySelector('.urbion-road-hierarchy-v6');existing?.remove();
 const host=document.createElement('div');host.className='urbion-road-hierarchy-v6';
 if(levels.length)host.innerHTML=levels.map(x=>`<div class="urbion-road-level-v6"><b>${esc(x.hierarchy||x.highway||'Road')}</b><span>${esc(x.nearest_name||'—')} · ${x.distance_km!=null?esc(x.distance_km+' km'):'—'}</span></div>`).join('');
 else host.innerHTML='<div class="urbion-road-level-v6"><b>Hierarchy</b><span>Awaiting source context</span></div>';
 body.appendChild(host);
 roadOverlayFromData(data);
}
async function refreshRoad(){
 const body=$('urbionRoadBody');if(!body)return;body.innerHTML='<div class="urbion-road-spinner">Loading live road hierarchy & accessibility context…</div>';
 try{const lat=Number($('site_lat')?.value),lon=Number($('site_lon')?.value);if(!Number.isFinite(lat)||!Number.isFinite(lon))throw Error('Valid site coordinates are required');const r=await fetch('/road-intelligence',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({site_lat:lat,site_lon:lon})});const d=await r.json();if(!r.ok)throw Error(d?.message||d?.detail||'Road intelligence unavailable');window.URBION_ROAD_LAST=d;roadRender(d);if(window.__URBION_ROAD_OWNER_RENDER__)window.__URBION_ROAD_OWNER_RENDER__(d);else if(typeof window.URBION_ROAD_RENDER==='function')window.URBION_ROAD_RENDER(d);}
 catch(e){body.innerHTML='<div class="urbion-road-error">'+esc(e.message||e)+'</div>'}
}
function enhanceRoadButton(){const b=$('urbionRoadOpen');if(!b||b.dataset.v6Bound)return;b.dataset.v6Bound='1';b.onclick=()=>{const d=$('urbionRoadDrawer');d?.classList.add('open');void refreshRoad()}}
function diagnostics(){
 const m=mapObj();if(!m)return false;const mapwrap=document.querySelector('.mapwrap');mapwrap?.setAttribute('data-gis-visual-hardened','true');
 if(!mapwrap?.querySelector('[data-urbion-map-hardened]')){const x=document.createElement('span');x.dataset.urbionMapHardened='1';x.style.display='none';mapwrap?.appendChild(x)}return true;
}
async function boot(){style();for(let i=0;i<160;i++){if(mapObj()&&L&&$('layerList'))break;await sleep(100)}observePanel();enhanceLayerPanel();diagnostics();setTimeout(()=>{enhanceLayerPanel();autoCriticalLayers()},700);enhanceRoadButton();setInterval(()=>{enhanceLayerPanel();enhanceRoadButton()},2500)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>void boot(),{once:true});else void boot();
})();

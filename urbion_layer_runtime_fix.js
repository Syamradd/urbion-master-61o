/* URBION HORIZON — resilient live GIS layer renderer */
(()=>{
'use strict';
if(window.__URBION_LAYER_RUNTIME_FIX__)return;
window.__URBION_LAYER_RUNTIME_FIX__=true;
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function getMap(){try{return (typeof map!=='undefined'&&map)||window.__URBION_MAP__||window.URBION_FCC_MAP||null}catch(_){return window.__URBION_MAP__||null}}
function stateName(){return String($('state')?.value||'Melaka').trim()||'Melaka'}
function escAttr(s){return esc(s).replace(/`/g,'&#96;')}
function setMsg(id,msg,good=true){const el=document.querySelector(`[data-layer-state="${CSS.escape(id)}"]`);if(el){el.textContent=msg;el.style.color=good?'var(--good)':'var(--bad)'}}
function webMercatorBounds(x,y,z){const n=2**z,s=40075016.68557849/n;const minx=x*s-20037508.342789244,maxx=(x+1)*s-20037508.342789244;const maxy=20037508.342789244-y*s,miny=20037508.342789244-(y+1)*s;return [minx,miny,maxx,maxy]}
function arcgisGridLayer(info){
  const Base=L.GridLayer.extend({
    createTile(coords,done){
      const tile=document.createElement('img');tile.width=256;tile.height=256;tile.alt='';tile.setAttribute('role','presentation');tile.crossOrigin='anonymous';
      const [xmin,ymin,xmax,ymax]=webMercatorBounds(coords.x,coords.y,coords.z);
      const u=String(info.url||'').replace(/\\/$/,'')+'/export?bbox='+[xmin,ymin,xmax,ymax].join(',')+'&bboxSR=3857&imageSR=3857&size=256,256&imageDisplay=256,256,96&dpi=96&format=png32&transparent=true&f=image&layers=show:0';
      tile.onload=()=>done(null,tile);tile.onerror=e=>done(e,tile);tile.src=u;return tile;
    }
  });
  return new Base({tileSize:256,updateWhenIdle:false,keepBuffer:2,opacity:.82});
}
function buildLayer(info){
  const type=String(info.type||'').toUpperCase();
  if(type==='GEOSERVER_WMS'){
    if(!info.url||!info.layers)throw new Error('WMS endpoint/layer missing');
    const l=L.tileLayer.wms(info.url,{layers:info.layers,format:'image/png',transparent:true,version:'1.1.1',opacity:.78,tiled:true,uppercase:false,crossOrigin:true});
    l.on('tileerror',e=>console.warn('URBION WMS tile error',info.id,e));return l;
  }
  if(type==='TILE')return L.tileLayer(info.url,{maxZoom:19,opacity:.78,attribution:info.name||info.source||'Source'});
  if(type==='ARCGIS_MAP')return arcgisGridLayer(info);
  return null;
}
async function fetchCatalog(){
  for(let i=0;i<18;i++){
    try{const r=await fetch(location.origin+'/map/layers?state='+encodeURIComponent(stateName())+'&_='+Date.now(),{cache:'no-store'});if(r.ok){const d=await r.json();if(Array.isArray(d.layers))return d.layers.filter(x=>x.id!=='osm')} }catch(_){ }
    await sleep(500);
  }
  throw new Error('Layer catalogue unavailable');
}
function renderCatalog(layers){
  const list=$('layerList');if(!list)return;
  const groups={};layers.forEach(x=>(groups[x.group||'OTHER']??=[]).push(x));
  list.innerHTML=Object.entries(groups).map(([g,arr])=>`<div class="lg">${esc(g)}</div>`+arr.map(x=>`<div class="layerrow"><input type="checkbox" data-layer-fix="${escAttr(x.id)}"><span>${esc(x.name||x.id)}</span><small>${esc(x.source||x.type||'')}</small></div><div class="layerstate" data-layer-state="${escAttr(x.id)}">OFF · ${esc(x.type||'SOURCE')}</div>`).join('')).join('')||'<div class="tiny">No live layers returned.</div>';
  layers.forEach(x=>{const cb=list.querySelector(`[data-layer-fix="${CSS.escape(x.id)}"]`);cb?.addEventListener('change',()=>toggle(x,cb.checked))});
}
async function toggle(info,on){
  const m=getMap();if(!m||typeof L==='undefined')return;
  try{
    window.__URBION_LIVE_LAYERS__=window.__URBION_LIVE_LAYERS__||{};
    const old=window.__URBION_LIVE_LAYERS__[info.id];
    if(!on){if(old&&m.hasLayer(old))m.removeLayer(old);delete window.__URBION_LIVE_LAYERS__[info.id];setMsg(info.id,'OFF');return}
    if(old&&m.hasLayer(old)){setMsg(info.id,'ON · RENDERED');return}
    const layer=buildLayer(info);if(!layer){setMsg(info.id,'PORTAL · SOURCE');return}
    layer.addTo(m);window.__URBION_LIVE_LAYERS__[info.id]=layer;
    setMsg(info.id,'ON · RENDERED');
    if(layer.once)layer.once('load',()=>setMsg(info.id,'ON · RENDERED'));layer.on?.('tileerror',()=>setMsg(info.id,'ERROR · TILE',false));
  }catch(e){setMsg(info.id,'ERROR · '+e.message,false);console.error('URBION layer failed',info,e)}
}
async function refresh(){const m=getMap();if(!m)return false;try{const layers=await fetchCatalog();renderCatalog(layers);return true}catch(e){const list=$('layerList');if(list)list.innerHTML=`<div class="tiny" style="color:var(--bad)">Live layer catalogue error · ${esc(e.message)}</div>`;return false}}
async function boot(){for(let i=0;i<80;i++){if(typeof L!=='undefined'&&getMap()&&$('layerList')){await refresh();const btn=$('layerBtn');if(btn&&!btn.dataset.layerFixBound){btn.dataset.layerFixBound='1';btn.addEventListener('click',e=>{e.stopImmediatePropagation();$('layers')?.classList.toggle('open');void refresh()},true)}$('state')?.addEventListener('change',()=>void refresh());return}await sleep(250)}}
window.URBION_LAYER_FIX={refresh,toggle};void boot();
})();

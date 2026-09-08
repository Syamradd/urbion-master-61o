(()=>{
'use strict';
/* Phase 1 frontend repair: preserve the canonical shell/map/state model and repair
   command-centre geometry, Leaflet sizing, and existing map-selection interaction. */
const $=(s,r=document)=>r.querySelector(s);

function phase1Style(){
  if($('#urbion-phase1-style'))return;
  const s=document.createElement('style');
  s.id='urbion-phase1-style';
  s.textContent=`
/* Phase 1A — compact three-column Planning Command Centre */
#urbion-championship-shell .app-shell{padding-top:0}
#urbion-championship-shell .workspace-head{padding:9px 0 8px;align-items:center;gap:16px}
#urbion-championship-shell .workspace-head h1{font-size:clamp(27px,2.55vw,40px);margin:4px 0 3px}
#urbion-championship-shell .workspace-head p{font-size:9px}
#urbion-championship-shell .workstation{grid-template-columns:minmax(250px,24%) minmax(0,52%) minmax(250px,24%);gap:10px;align-items:stretch}
#urbion-championship-shell .case-panel,#urbion-championship-shell .intel-panel{min-height:0}
#urbion-championship-shell .map-panel-canonical{min-width:0;min-height:0;display:flex;flex-direction:column;align-self:start}

/* Phase 1B — one stable Leaflet viewport owned by the map panel */
#urbion-championship-shell .map-toolbar{flex:0 0 auto;min-height:66px}
#urbion-championship-shell .map-stage{height:clamp(520px,calc(100vh - 245px),650px);min-height:520px;max-height:none;position:relative;overflow:hidden;flex:0 0 clamp(520px,calc(100vh - 245px),650px)}
#urbion-championship-shell .map-stage #cs-map,
#urbion-championship-shell .map-stage .leaflet-container{width:100%;height:100%}
#urbion-championship-shell .map-stage #cs-map{position:absolute;inset:0;min-height:0;overflow:hidden}

/* Keep the workstation itself compact; its panels scroll internally when needed. */
#urbion-championship-shell .case-panel,
#urbion-championship-shell .intel-panel{overflow:auto;scrollbar-gutter:stable}

/* Phase 1C — explicit map-selection state without changing the assessment model */
#urbion-championship-shell #cs-pick-map{transition:border-color .15s ease,background-color .15s ease,color .15s ease,box-shadow .15s ease}
#urbion-championship-shell #cs-pick-map.phase1-select-active{color:#dffff9;border-color:#5ee2cf;background:rgba(88,223,208,.12);box-shadow:0 0 0 2px rgba(88,223,208,.08),0 0 18px rgba(88,223,208,.08)}

@media(max-width:1320px){
  #urbion-championship-shell .workstation{grid-template-columns:minmax(235px,27%) minmax(0,46%) minmax(235px,27%)}
}
@media(max-width:1100px){
  #urbion-championship-shell .workstation{grid-template-columns:1fr}
  #urbion-championship-shell .case-panel{order:1;overflow:visible}
  #urbion-championship-shell .map-panel-canonical{order:2}
  #urbion-championship-shell .intel-panel{order:3;overflow:visible}
  #urbion-championship-shell .map-stage{height:560px;min-height:560px;flex-basis:560px}
}
@media(max-width:720px){
  #urbion-championship-shell .workspace-head{display:block;padding:8px 0}
  #urbion-championship-shell .workspace-head h1{font-size:26px}
  #urbion-championship-shell .map-stage{height:520px;min-height:520px;flex-basis:520px}
}
@media(max-height:760px) and (min-width:1101px){
  #urbion-championship-shell .map-stage{height:500px;min-height:500px;flex-basis:500px}
}
`;
  document.head.appendChild(s);
}

function toast(message,type='info'){
  const e=$('#cs-toast');
  if(!e)return;
  e.textContent=message;
  e.dataset.type=type;
  e.classList.add('show');
  window.clearTimeout(window.__URBION_PHASE1_TOAST__);
  window.__URBION_PHASE1_TOAST__=window.setTimeout(()=>e.classList.remove('show'),2200);
}

function syncField(name,value){
  const e=$('#cs-'+name);
  if(!e)return false;
  e.value=value;
  e.dispatchEvent(new Event('input',{bubbles:true}));
  return true;
}

function setSelectMode(active){
  const b=$('#cs-pick-map');
  if(!b)return;
  b.classList.toggle('phase1-select-active',active);
  b.setAttribute('aria-pressed',active?'true':'false');
  b.setAttribute('aria-label',active?'Map selection active. Click the map to place the site.':'Use map selection to place the site.');
  b.textContent=active?'⌖ Select on Map':'⌖ Use Map Selection';
}

function wireMapSelection(){
  const m=window.__URBION_FCC_MAP__,b=$('#cs-pick-map');
  if(!m||!b||m.__urbionPhase1SelectionWired)return;
  m.__urbionPhase1SelectionWired=true;
  const state=window.__URBION_PHASE1_SELECTION__||(window.__URBION_PHASE1_SELECTION__={active:false,lat:null,lon:null});

  b.onclick=()=>{
    state.active=!state.active;
    setSelectMode(state.active);
    toast(state.active?'Click the map to place the site.':'Map selection cancelled.');
  };

  m.on('click',e=>{
    if(!state.active)return;
    const lat=Number(e?.latlng?.lat),lon=Number(e?.latlng?.lng);
    if(!Number.isFinite(lat)||!Number.isFinite(lon)){
      toast('Invalid map selection.','error');
      return;
    }
    const okLat=syncField('lat',lat.toFixed(6));
    const okLon=syncField('lon',lon.toFixed(6));
    if(!(okLat&&okLon)){
      toast('Site coordinate fields are unavailable.','error');
      return;
    }
    state.lat=lat;
    state.lon=lon;
    state.active=false;
    setSelectMode(false);
    toast(`Site selected · ${lat.toFixed(6)}, ${lon.toFixed(6)}`,'success');
  });

  document.addEventListener('keydown',e=>{
    if(e.key!=='Escape'||!state.active)return;
    state.active=false;
    setSelectMode(false);
    toast('Map selection cancelled.');
  });
}

/* Avoid redundant Leaflet view resets. The canonical shell calls setView from
   updateMap() on every form input, including TOD edits. When the requested view
   already equals the live map view, skipping the no-op setView preserves Leaflet's
   existing tile footprint/render state while allowing real view changes through. */
function wireStableMapView(){
  const m=window.__URBION_FCC_MAP__;
  if(!m||m.__urbionPhase1StableSetViewWired)return;
  m.__urbionPhase1StableSetViewWired=true;
  const originalSetView=m.setView;
  m.setView=function(center,zoom,options){
    const current=m.getCenter?.();
    const targetLat=Array.isArray(center)?Number(center[0]):Number(center?.lat);
    const targetLon=Array.isArray(center)?Number(center[1]):Number(center?.lng);
    const targetZoom=zoom==null?m.getZoom?.():Number(zoom);
    if(current&&Number.isFinite(targetLat)&&Number.isFinite(targetLon)&&Number.isFinite(targetZoom)&&Number.isFinite(m.getZoom?.())&&Math.abs(current.lat-targetLat)<1e-9&&Math.abs(current.lng-targetLon)<1e-9&&m.getZoom()===targetZoom)return m;
    return originalSetView.call(this,center,zoom,options);
  };
}

function wireMapResize(){
  const m=window.__URBION_FCC_MAP__,stage=$('.map-stage');
  if(!m||!stage||m.__urbionPhase1ResizeWired)return;
  m.__urbionPhase1ResizeWired=true;
  let frame=0;
  const invalidate=()=>{
    if(frame)return;
    frame=requestAnimationFrame(()=>{
      frame=0;
      m.invalidateSize({pan:false,animate:false});
    });
  };
  if(window.ResizeObserver){
    const ro=new ResizeObserver(invalidate);
    ro.observe(stage);
    m.__urbionPhase1ResizeObserver=ro;
  }
  window.addEventListener('resize',invalidate,{passive:true});
  document.addEventListener('fullscreenchange',invalidate,{passive:true});
  invalidate();
}

function install(){
  phase1Style();
  wireMapSelection();
  wireStableMapView();
  wireMapResize();
}

if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
else install();

/* Shared status helper used by Premium V7 official i-Plan integration. */
window.syncLayerState=function syncLayerState(r,id,active,text){
  const input=r?.querySelector(`#cs-layer-drawer input[data-layer="${id}"]`);
  const row=input?.closest?.('.fcc-layer-row');
  const small=row?.querySelector?.('span small')||row?.querySelector?.('small');
  if(small&&text!=null)small.textContent=String(text);
  if(row)row.classList.toggle('is-on',!!active);
};
})();

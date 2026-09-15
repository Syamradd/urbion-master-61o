/* URBION HORIZON — compatibility bootstrap only.
   Canonical V5 planning/map/navigation controls remain the owners.
   This bootstrap only restores safe defaults and visual readiness after the
   canonical owners have initialised; it does not register competing control handlers. */
(()=>{
'use strict';
if(window.__URBION_RUNTIME_CANONICAL_V5_COMPAT__)return;
window.__URBION_RUNTIME_CANONICAL_V5_COMPAT__=true;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function defaultSelect(id){const e=document.getElementById(id);if(!e||e.value)return false;const opts=[...e.options].filter(x=>x.value&&x.value!=='__UNSPECIFIED__');if(opts[0]){e.value=opts[0].value;e.dispatchEvent(new Event('change',{bubbles:true}));return true}return false}
function safeDefaults(){defaultSelect('landuse1');defaultSelect('landuse2');defaultSelect('landuse3');const p=document.getElementById('perimeter_planting');const w=document.getElementById('landscaped_pedestrian_walkway');if(p&&['yes','no'].includes(String(p.value).toLowerCase()))p.value='';if(w&&['yes','no'].includes(String(w.value).toLowerCase()))w.value='';}
function ensurePlanningLayers(){const list=document.getElementById('layerList');if(!list)return;for(const id of ['iplan-current','iplan-zoning']){const cb=list.querySelector(`input[data-urbion-layer="${id}"]`);if(cb&&!cb.checked&&!cb.dataset.autoEnabled){cb.dataset.autoEnabled='1';cb.click();}}
const mapWrap=document.querySelector('.mapwrap');if(mapWrap&&!mapWrap.querySelector('[data-urbion-critical-layer-badge]')){const badge=document.createElement('div');badge.dataset.urbionCriticalLayerBadge='1';badge.style.cssText='position:absolute;z-index:710;left:11px;top:43px;background:rgba(4,18,27,.90);border:1px solid rgba(72,223,170,.24);border-radius:8px;padding:6px 8px;color:var(--good);font-size:6px;font-weight:800;letter-spacing:.06em;pointer-events:none';badge.textContent='LAND USE + ZONING · SOURCE CONTEXT';mapWrap.appendChild(badge)}}
function compactRightRail(){if(document.getElementById('urbionRightRailStyle'))return;const s=document.createElement('style');s.id='urbionRightRailStyle';s.textContent='.right .card{margin-bottom:6px;padding:9px}.right .urbion-story-card{margin-bottom:6px;padding:9px}.right .finding{padding:7px}.right .udi-grid{gap:4px}.right .udi-domain{padding:6px}.right .udi-metrics{max-height:120px;overflow:auto}.right .udi-gap{max-width:100%}.right .actionsgrid{gap:4px}.right .quick{gap:4px}';document.head.appendChild(s)}
async function boot(){
  for(let i=0;i<160;i++){
    try{
      if(window.URBION_FINAL){
        try{window.URBION_FINAL.refreshMap?.()}catch(_){ }
        try{window.URBION_FINAL.loadLayers?.()}catch(_){ }
        safeDefaults();compactRightRail();ensurePlanningLayers();
        await sleep(250);safeDefaults();ensurePlanningLayers();
        return;
      }
    }catch(_){ }
    await sleep(50);
  }
  console.warn('URBION compatibility runtime: canonical bridge unavailable');
}
boot().catch(e=>console.error('URBION compatibility runtime failed',e));
})();

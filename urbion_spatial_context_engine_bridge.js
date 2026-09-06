(()=>{
'use strict';
if(window.__URBION_SPATIAL_CONTEXT_ENGINE_BRIDGE)return;window.__URBION_SPATIAL_CONTEXT_ENGINE_BRIDGE=true;
const $=id=>document.getElementById(id);
async function bind(data){
  if(!data?.site)return;
  const lat=Number(data.site.latitude),lon=Number(data.site.longitude);
  const todlat=Number.parseFloat($('todlat')?.value),todlon=Number.parseFloat($('todlon')?.value);
  try{
    const r=await fetch('/spatial/intelligence',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({site_lat:lat,site_lon:lon,tod_lat:Number.isFinite(todlat)?todlat:undefined,tod_lon:Number.isFinite(todlon)?todlon:undefined,radii:[400,800],constraints:{},environmental_context:data})});
    const intelligence=await r.json();
    if(!r.ok)throw Error(intelligence.detail?.message||intelligence.detail||r.status);
    window.__urbionSpatialIntelligence=intelligence;
    window.dispatchEvent(new CustomEvent('urbion:spatial-intelligence',{detail:intelligence}));
  }catch(e){console.warn('URBION spatial intelligence bridge',e)}
}
window.addEventListener('urbion:spatial-context',e=>bind(e.detail));
if(window.__urbionSpatialContext)bind(window.__urbionSpatialContext);
})();
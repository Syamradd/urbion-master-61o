(()=>{
'use strict';
if(window.__URBION_SPATIAL_CONTEXT_INTELLIGENCE)return;window.__URBION_SPATIAL_CONTEXT_INTELLIGENCE=true;
const $=id=>document.getElementById(id);
const fmt=m=>m==null?'—':m<1000?`${Math.round(m)} m`:`${(m/1000).toFixed(2)} km`;
function render(data){
  if(!data)return;
  window.__urbionSpatialContext=data;
  const layers=data.layers||[],live=layers.filter(x=>x.status==='LIVE_QUERY'),hits=layers.filter(x=>x.status==='LIVE_QUERY'&&x.feature_count>0),gaps=layers.filter(x=>x.status==='QUERY_ERROR'||x.status==='NOT_CONFIGURED');
  const count=$('ux5-source-count');if(count)count.textContent=`${live.length}/${layers.length}`;
  const state=$('ux5-evidence-state');if(state)state.textContent=hits.length?`GIS ${hits.length} HIT${hits.length===1?'':'S'}`:gaps.length?'GIS REVIEW':'GIS SCANNED';
  const tod=$('ux5-tod');if(tod&&hits.length){const flood=hits.find(x=>x.id==='iplan-flood');const geology=hits.find(x=>x.id==='mygems-lithology');tod.textContent=[flood?`Flood ${fmt(flood.nearest_distance_m)}`:'',geology?`Geology ${fmt(geology.nearest_distance_m)}`:''].filter(Boolean).join(' · ')||tod.textContent||'Spatial context loaded'}
  const list=$('ux5-source-list');if(list){const rows=[];hits.slice(0,5).forEach(x=>rows.push(`<span>${x.name}${x.inside_count?` · ${x.inside_count} site hit`:''}${x.nearest_distance_m!=null?` · ${fmt(x.nearest_distance_m)}`:''}</span>`));if(gaps.length)rows.push(`<span>Evidence gaps · ${gaps.length}</span>`);if(!rows.length)rows.push('<span>No mapped feature hit in current radius</span>');list.innerHTML=rows.join('')}
  const next=$('ux5-next-copy');if(next&&hits.length)next.textContent=`${hits.length} GIS source${hits.length===1?'':'s'} returned geometry. Review the mapped relationships before testing What-If.`;
  window.dispatchEvent(new CustomEvent('urbion:spatial-context-ready',{detail:data}));
}
window.addEventListener('urbion:spatial-context',e=>render(e.detail));
if(window.__urbionSpatialContext)render(window.__urbionSpatialContext);
})();
(()=>{
'use strict';
if(window.__URBION_MAP_IDENTIFY_RUNTIME__)return;
window.__URBION_MAP_IDENTIFY_RUNTIME__=true;

const state={version:2,active:false,last:null,pending:0};
window.__URBION_MAP_IDENTIFY__=state;
const $=(s,r=document)=>r.querySelector(s);

function map(){return window.__URBION_FCC_MAP__||window.URBION_FCC_MAP||window.__URBION_MAP__||null;}
function visibleOfficialLayers(){
  const m=map();
  if(!m)return [];
  const store=window.__URBION_OFFICIAL_LAYERS__||{};
  const candidates=[...Object.entries(store).map(([id,layer])=>[id,layer])];
  if(m._layers){
    Object.values(m._layers).forEach(layer=>{
      if(!layer?.__urbionSource)return;
      const id=layer.__urbionLayerId||layer.__urbionId||layer.__urbionSource;
      candidates.push([id,layer]);
    });
  }
  const seen=new Set();
  return candidates.filter(([id,layer])=>{
    if(!layer||!layer.__urbionSource||!m.hasLayer?.(layer))return false;
    const key=String(layer.__urbionSource)+'|'+String(id);
    if(seen.has(key))return false;
    seen.add(key);return true;
  });
}
function esc(v){return String(v??'').replace(/[&<>\\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}[c]));}
function ensurePanel(){
  let panel=$('#urbion-map-identify');
  if(panel)return panel;
  const host=$('.map-panel')||document.body;
  panel=document.createElement('aside');
  panel.id='urbion-map-identify';
  panel.setAttribute('aria-live','polite');
  panel.innerHTML='<div class="umi-head"><b>MAP INTELLIGENCE</b><button type="button" data-umi-close aria-label="Close">×</button></div><div data-umi-body><span>Click a live map feature to identify it.</span></div>';
  const style=document.createElement('style');
  style.textContent='#urbion-map-identify{position:absolute;z-index:1500;right:14px;bottom:14px;width:min(360px,calc(100% - 28px));max-height:48%;overflow:auto;padding:11px;border:1px solid rgba(99,228,194,.22);border-radius:12px;background:rgba(6,15,23,.94);backdrop-filter:blur(12px);box-shadow:0 12px 34px rgba(0,0,0,.35);color:#d8eef0;font:12px/1.45 Inter,system-ui,sans-serif}.umi-head{display:flex;justify-content:space-between;align-items:center;font-size:9px;letter-spacing:.14em;color:#69e2c0}.umi-head button{border:0;background:transparent;color:#9bb8c0;font-size:18px;cursor:pointer}.umi-meta{display:grid;grid-template-columns:88px 1fr;gap:4px 8px;margin:9px 0}.umi-meta dt{color:#75909a}.umi-meta dd{margin:0;color:#e6f7f7;overflow-wrap:anywhere}.umi-state{margin:8px 0;padding:7px;border-radius:8px;background:rgba(82,146,167,.12);font-size:10px}.umi-props{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:7px}.umi-prop{padding:6px;border:1px solid rgba(109,211,210,.1);border-radius:7px}.umi-prop small{display:block;color:#6f8b95;font-size:8px}.umi-prop b{display:block;margin-top:2px;font-size:10px;word-break:break-word}.umi-actions{display:flex;gap:6px;margin-top:9px}.umi-actions button{flex:1;padding:7px 8px;border-radius:7px;border:1px solid rgba(99,228,194,.25);background:rgba(99,228,194,.08);color:#bfeee1;font-size:9px;font-weight:700;cursor:pointer}.umi-muted{color:#718991;font-size:10px}';
  document.head.appendChild(style);host.appendChild(panel);panel.querySelector('[data-umi-close]').onclick=()=>panel.remove();return panel;
}
function render(payload){
  const panel=ensurePanel(),body=panel.querySelector('[data-umi-body]');
  if(!body)return;
  if(!payload){body.innerHTML='<span class="umi-muted">No feature identified at this location.</span>';return;}
  const p=payload.properties||{};
  const entries=Object.entries(p).filter(([k,v])=>v!==null&&v!==undefined&&v!=='').slice(0,18);
  body.innerHTML='<dl class="umi-meta"><dt>Layer</dt><dd>'+esc(payload.layer_name||payload.layer_id||'Unknown')+'</dd><dt>Feature</dt><dd>'+esc(payload.feature_id||'Not exposed')+'</dd><dt>Source</dt><dd>'+esc(payload.source||'Not established')+'</dd><dt>Query</dt><dd>'+esc(payload.query_status||'UNKNOWN')+'</dd></dl><div class="umi-state">Evidence: <b>'+esc(payload.evidence_state||'REVIEW')+'</b> · Decision-safe: <b>NO</b></div>'+(entries.length?'<div class="umi-props">'+entries.map(([k,v])=>'<div class="umi-prop"><small>'+esc(k)+'</small><b>'+esc(v)+'</b></div>').join('')+'</div>':'<div class="umi-muted">No scalar attributes returned by the source.</div>')+'<div class="umi-actions"><button type="button" data-umi-evidence>USE AS EVIDENCE</button><button type="button" data-umi-source>VIEW SOURCE</button></div>';
  panel.querySelector('[data-umi-evidence]').onclick=()=>{state.last={...payload,evidence_handoff:{decision_safe:false,rule_binding_required:true,statutory_approval_claim:false}};window.dispatchEvent(new CustomEvent('urbion-map-evidence',{detail:state.last}));};
  panel.querySelector('[data-umi-source]').onclick=()=>{if(payload.source)window.open(payload.source,'_blank','noopener');};
}
function identify(service,latlng,mapInstance){
  const b=mapInstance.getBounds(),size=mapInstance.getSize();
  const params=new URLSearchParams({f:'json',geometry:JSON.stringify({x:latlng.lng,y:latlng.lat,spatialReference:{wkid:4326}}),geometryType:'esriGeometryPoint',sr:'4326',layers:'all',tolerance:'8',mapExtent:[b.getWest(),b.getSouth(),b.getEast(),b.getNorth()].join(','),imageDisplay:[size.x,size.y,96].join(','),returnGeometry:'false'});
  return fetch(service.replace(/\/$/,'')+'/identify?'+params.toString(),{credentials:'omit'}).then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()});
}
async function onClick(e){
  const m=map(),layers=visibleOfficialLayers();if(!m||!layers.length)return;
  state.active=true;state.pending=layers.length;const panel=ensurePanel();panel.querySelector('[data-umi-body]').innerHTML='<span>Identifying live source features…</span>';
  const results=[];
  for(const [layerId,layer] of layers){
    try{const data=await identify(layer.__urbionSource,e.latlng,m);for(const r of (data.results||[])){results.push({layer_id:layerId,layer_name:r.layerName||layerId,feature_id:r.value||r.attributes?.OBJECTID||r.attributes?.objectid||null,source:layer.__urbionSource,query_status:'LIVE_QUERY',evidence_state:'SOURCE_CONTEXT',decision_safe:false,requires_rule_binding:true,properties:r.attributes||{}})}}catch(err){results.push({layer_id:layerId,layer_name:layerId,source:layer.__urbionSource,query_status:'QUERY_ERROR',evidence_state:'REVIEW',decision_safe:false,requires_rule_binding:true,properties:{error:String(err.message||err)}})}
    state.pending--;
  }
  state.last=results[0]||null;render(state.last);
  window.dispatchEvent(new CustomEvent('urbion-map-identify',{detail:{point:e.latlng,results}}));
}
function boot(){const m=map();if(!m||m.__urbionIdentifyWired)return false;m.__urbionIdentifyWired=true;m.on('click',onClick);state.mapReady=true;return true;}
let tries=0;const timer=setInterval(()=>{tries++;if(boot()||tries>120)clearInterval(timer)},250);
})();

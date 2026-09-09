(()=>{
'use strict';
if(window.__URBION_MAP_IDENTIFY_RUNTIME__)return;
window.__URBION_MAP_IDENTIFY_RUNTIME__=true;

const state={version:7,active:false,last:null,lastResults:[],selectedIndex:0,pending:0,cadastralLayer:null,binding:null};
window.__URBION_MAP_IDENTIFY__=state;
const $=(s,r=document)=>r.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>\\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}[c]));
function map(){return window.__URBION_FCC_MAP__||window.URBION_FCC_MAP||window.__URBION_MAP__||null;}
function selectedState(){return String($('#cs-state')?.value||window.__URBION_SELECTED_STATE__||'Melaka').trim()||'Melaka';}
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
function ensurePanel(){
  let panel=$('#urbion-map-identify');
  if(panel)return panel;
  const host=$('.map-panel')||document.body;
  panel=document.createElement('aside');
  panel.id='urbion-map-identify';
  panel.setAttribute('aria-live','polite');
  panel.innerHTML='<div class="umi-head"><b>MAP INTELLIGENCE</b><button type="button" data-umi-close aria-label="Close">×</button></div><div data-umi-body><span>Click a live map feature to identify it.</span></div>';
  const style=document.createElement('style');
  style.textContent='#urbion-map-identify{position:absolute;z-index:1500;right:14px;bottom:14px;width:min(390px,calc(100% - 28px));max-height:62%;overflow:auto;padding:11px;border:1px solid rgba(99,228,194,.22);border-radius:12px;background:rgba(6,15,23,.94);backdrop-filter:blur(12px);box-shadow:0 12px 34px rgba(0,0,0,.35);color:#d8eef0;font:12px/1.45 Inter,system-ui,sans-serif}.umi-head{display:flex;justify-content:space-between;align-items:center;font-size:9px;letter-spacing:.14em;color:#69e2c0}.umi-head button{border:0;background:transparent;color:#9bb8c0;font-size:18px;cursor:pointer}.umi-summary{margin:8px 0;padding:8px 9px;border-radius:9px;background:rgba(99,228,194,.08);border:1px solid rgba(99,228,194,.14);font-size:10px}.umi-cards{display:grid;gap:6px}.umi-card{width:100%;text-align:left;padding:8px 9px;border:1px solid rgba(109,211,210,.12);border-radius:9px;background:rgba(255,255,255,.025);color:#dceff0;cursor:pointer}.umi-card:hover,.umi-card.is-selected{border-color:rgba(99,228,194,.38);background:rgba(99,228,194,.07)}.umi-card-top{display:flex;justify-content:space-between;gap:8px}.umi-card b{font-size:10px}.umi-card small{color:#78929a;font-size:8px}.umi-detail{margin-top:8px;padding-top:8px;border-top:1px solid rgba(109,211,210,.1)}.umi-meta{display:grid;grid-template-columns:88px 1fr;gap:4px 8px;margin:0 0 8px}.umi-meta dt{color:#75909a}.umi-meta dd{margin:0;color:#e6f7f7;overflow-wrap:anywhere}.umi-state{margin:8px 0;padding:7px;border-radius:8px;background:rgba(82,146,167,.12);font-size:10px}.umi-props{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:7px}.umi-prop{padding:6px;border:1px solid rgba(109,211,210,.1);border-radius:7px}.umi-prop small{display:block;color:#6f8b95;font-size:8px}.umi-prop b{display:block;margin-top:2px;font-size:10px;word-break:break-word}.umi-actions{display:flex;gap:6px;margin-top:9px}.umi-actions button{flex:1;padding:7px 8px;border-radius:7px;border:1px solid rgba(99,228,194,.25);background:rgba(99,228,194,.08);color:#bfeee1;font-size:9px;font-weight:700;cursor:pointer}.umi-muted{color:#718991;font-size:10px}.umi-bind{margin-top:7px;padding:7px 8px;border-radius:8px;border:1px solid rgba(99,228,194,.16);background:rgba(99,228,194,.05);font-size:9px}';
  document.head.appendChild(style);host.appendChild(panel);panel.querySelector('[data-umi-close]').onclick=()=>panel.remove();return panel;
}
function evidenceHandoff(payload){return {...payload,evidence_handoff:{decision_safe:false,rule_binding_required:true,statutory_approval_claim:false}};}
function clearCadastralOverlay(){const m=map();if(m&&state.cadastralLayer){m.removeLayer(state.cadastralLayer);state.cadastralLayer=null;}}
function renderCadastral(features){
  const m=map();if(!m||!window.L||!Array.isArray(features)||!features.length)return;
  clearCadastralOverlay();
  state.cadastralLayer=window.L.geoJSON({type:'FeatureCollection',features},{style:()=>({color:'#69e2c0',weight:2,opacity:.95,fillOpacity:.06}),onEachFeature:(feature,layer)=>{
    const p=feature?.properties||{};
    const title=p.LOT?`Lot ${esc(p.LOT)}`:'i-Plan Cadastral Parcel';
    const details=[p.UPI&&`UPI: ${esc(p.UPI)}`,p.KELUASAN!==undefined&&`Luas: ${esc(p.KELUASAN)}`].filter(Boolean).join('<br>');
    layer.bindPopup('<b>'+title+'</b>'+(details?'<br>'+details:''));
  }}).addTo(m);
}
async function bindEvidence(payload){
  const developmentType=String($('#cs-development')?.value||payload?.development_type||'').trim();
  const authority=String($('#cs-pbt')?.value||'MBMB').trim()||'MBMB';
  const response=await fetch('/spatial/feature-evidence/bind',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({feature:evidenceHandoff(payload),development_type:developmentType,authority})});
  if(!response.ok)throw new Error('HTTP '+response.status);
  const data=await response.json();
  state.binding=data;
  window.dispatchEvent(new CustomEvent('urbion-map-evidence-bound',{detail:data}));
  return data;
}
function renderSelected(){
  const panel=ensurePanel(),body=panel.querySelector('[data-umi-body]');
  if(!body)return;
  const results=state.lastResults||[];
  if(!results.length){body.innerHTML='<span class="umi-muted">No feature identified at this location.</span>';return;}
  const selected=Math.max(0,Math.min(state.selectedIndex,results.length-1));
  state.selectedIndex=selected;
  const payload=results[selected]||null;
  const cards=results.map((item,i)=>'<button type="button" class="umi-card '+(i===selected?'is-selected':'')+'" data-umi-result="'+i+'"><span class="umi-card-top"><b>'+esc(item.layer_name||item.layer_id||'Unknown layer')+'</b><small>'+esc(item.query_status||'UNKNOWN')+'</small></span><small>'+esc(item.feature_id||'Feature identified')+'</small></button>').join('');
  const p=payload.properties||{};
  const entries=Object.entries(p).filter(([k,v])=>v!==null&&v!==undefined&&v!=='').slice(0,18);
  const bindingLabel=state.binding&&state.binding.evidence?.feature_id===payload.feature_id?`<div class="umi-bind">Binding: <b>${esc(state.binding.binding_status)}</b> · ${state.binding.rules?.length||0} candidate rule(s) · decision-safe: NO</div>`:'';
  body.innerHTML='<div class="umi-summary"><b>'+results.length+'</b> FEATURE'+(results.length===1?'':'S')+' IDENTIFIED · click a layer card to inspect</div><div class="umi-cards">'+cards+'</div><div class="umi-detail"><dl class="umi-meta"><dt>Layer</dt><dd>'+esc(payload.layer_name||payload.layer_id||'Unknown')+'</dd><dt>Feature</dt><dd>'+esc(payload.feature_id||'Not exposed')+'</dd><dt>Source</dt><dd>'+esc(payload.source||'Not established')+'</dd><dt>Query</dt><dd>'+esc(payload.query_status||'UNKNOWN')+'</dd></dl><div class="umi-state">Evidence: <b>'+esc(payload.evidence_state||'REVIEW')+'</b> · Decision-safe: <b>NO</b></div>'+(entries.length?'<div class="umi-props">'+entries.map(([k,v])=>'<div class="umi-prop"><small>'+esc(k)+'</small><b>'+esc(v)+'</b></div>').join('')+'</div>':'<div class="umi-muted">No scalar attributes returned by the source.</div>')+bindingLabel+'<div class="umi-actions"><button type="button" data-umi-evidence>USE AS EVIDENCE</button><button type="button" data-umi-source>VIEW SOURCE</button></div></div>';
  panel.querySelectorAll('[data-umi-result]').forEach(button=>button.onclick=()=>{state.selectedIndex=Number(button.dataset.umiResult)||0;state.last=state.lastResults[state.selectedIndex]||null;renderSelected();});
  panel.querySelector('[data-umi-evidence]').onclick=async()=>{state.last=evidenceHandoff(payload);window.dispatchEvent(new CustomEvent('urbion-map-evidence',{detail:state.last}));const button=panel.querySelector('[data-umi-evidence]');button.disabled=true;button.textContent='BINDING…';try{await bindEvidence(state.last);renderSelected();}catch(err){button.disabled=false;button.textContent='BIND FAILED';const note=document.createElement('div');note.className='umi-bind';note.textContent='Rule binding unavailable: '+String(err.message||err);body.appendChild(note);}};
  panel.querySelector('[data-umi-source]').onclick=()=>{if(payload.source)window.open(payload.source,'_blank','noopener');};
}
function featureId(feature){
  const p=feature?.properties||feature?.attributes||{};
  return String(feature?.id??p.id??p.OBJECTID??p.objectid??p.fid??'Not exposed');
}
async function identifyAtPoint(layerIds,latlng){
  const params=new URLSearchParams({site_lat:String(latlng.lat),site_lon:String(latlng.lng),radius_m:'120',state:selectedState(),layers:layerIds.join(',')});
  const response=await fetch('/spatial/site-context?'+params.toString(),{credentials:'same-origin',headers:{Accept:'application/json'}});
  if(!response.ok)throw new Error('HTTP '+response.status);
  const data=await response.json();
  const results=[];
  for(const item of (data.layers||[])){
    const candidates=Array.isArray(item.features)?item.features:[];
    const feature=candidates.find(f=>{const props=f?.properties||f?.attributes||{};return props?.OBJECTID!==undefined||props?.objectid!==undefined||props?.id!==undefined||f?.id!==undefined;})||candidates[0];
    if(feature){results.push({layer_id:item.id,layer_name:item.name_ms||item.name||item.id,feature_id:featureId(feature),source:item.source,query_status:item.status==='LIVE_QUERY'?'LIVE_QUERY':item.status,evidence_state:item.evidence||'EVIDENCE_GAP',decision_safe:false,requires_rule_binding:true,properties:feature.properties||feature.attributes||{},geometry:feature.geometry||null,features:item.id==='iplan-cadastral'?candidates:null});}
    else if(item.status==='QUERY_ERROR'){results.push({layer_id:item.id,layer_name:item.name_ms||item.name||item.id,source:item.source,query_status:'QUERY_ERROR',evidence_state:'REVIEW',decision_safe:false,requires_rule_binding:true,properties:{error:item.error||'Source query failed'}});}
  }
  return results;
}
async function onClick(e){
  const m=map(),layers=visibleOfficialLayers();if(!m||!layers.length)return;
  state.active=true;state.pending=layers.length;state.selectedIndex=0;state.lastResults=[];state.binding=null;const panel=ensurePanel();panel.querySelector('[data-umi-body]').innerHTML='<span>Identifying live source features…</span>';
  const ids=[...new Set([...layers.map(([id])=>String(id)),'iplan-cadastral'])];
  try{
    const results=await identifyAtPoint(ids,e.latlng);
    state.pending=0;state.lastResults=results;state.last=results[0]||null;
    const cadastralResult=results.find(item=>item.layer_id==='iplan-cadastral');
    if(cadastralResult?.features)renderCadastral(cadastralResult.features);
    renderSelected();
    window.dispatchEvent(new CustomEvent('urbion-map-identify',{detail:{point:e.latlng,results}}));
  }catch(err){
    state.pending=0;
    const payload={layer_id:'map',layer_name:'Map Intelligence',source:'/spatial/site-context',query_status:'QUERY_ERROR',evidence_state:'REVIEW',decision_safe:false,requires_rule_binding:true,properties:{error:String(err.message||err)}};
    state.last=payload;state.lastResults=[payload];renderSelected();window.dispatchEvent(new CustomEvent('urbion-map-identify',{detail:{point:e.latlng,results:[payload]}}));
  }
}
function boot(){const m=map();if(!m||m.__urbionIdentifyWired)return false;m.__urbionIdentifyWired=true;m.on('click',onClick);state.mapReady=true;return true;}
let tries=0;const timer=setInterval(()=>{tries++;if(boot()||tries>120)clearInterval(timer)},250);
})();

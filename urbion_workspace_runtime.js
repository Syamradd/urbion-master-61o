/* URBION HORIZON — canonical runtime compatibility bootstrap + presentation fallback. */
(()=>{'use strict';
if(window.__URBION_RUNTIME_CANONICAL_V5_COMPAT__)return;
window.__URBION_RUNTIME_CANONICAL_V5_COMPAT__=true;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const $=id=>document.getElementById(id);
const root=()=>document.querySelector('.right')||document.querySelector('.layout > :last-child');
const packet=()=>window.URBION_LAST?.canonical_evidence_packet||null;
const esc=v=>String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));

function mapVisualStack(){
  if($('urbionCanonicalRuntimeStyle'))return;
  const s=document.createElement('style');s.id='urbionCanonicalRuntimeStyle';s.textContent=`
    .mapwrap>#map{position:relative!important;z-index:2!important}
    .mapwrap>.mapveil{z-index:1!important}
    .mapwrap .leaflet-pane.leaflet-tile-pane{z-index:200!important}
    .mapwrap .leaflet-pane.leaflet-overlay-pane{z-index:450!important}
    .mapwrap .leaflet-pane.urbionDataV6{z-index:520!important}
    .urbion-runtime-impact{border:1px solid var(--line);border-radius:10px;background:linear-gradient(145deg,rgba(7,29,41,.96),rgba(3,15,22,.98));padding:10px;margin-bottom:7px}
    .light .urbion-runtime-impact{background:#fff}
    .uri-head{display:flex;justify-content:space-between;align-items:center;gap:8px}.uri-title{font-size:8px;font-weight:900;letter-spacing:.07em}.uri-sub{font-size:5.8px;color:var(--muted)}
    .uri-note{font-size:6.1px;color:var(--muted);line-height:1.4;margin-top:6px}
    .uri-grid{display:grid;grid-template-columns:1fr;gap:4px;margin-top:7px}.uri-row{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:6px;padding:6px 7px;border:1px solid rgba(45,85,100,.22);border-radius:7px;background:rgba(255,255,255,.015)}.uri-row b{font-size:6.8px}.uri-count{font-size:6px;color:var(--muted)}.uri-state{font-size:5.6px;font-weight:800;padding:3px 5px;border:1px solid rgba(255,203,93,.28);border-radius:5px;color:var(--warn)}.uri-state.ready{color:var(--good);border-color:rgba(72,223,170,.28)}
    .urbion-runtime-opacity{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:5px;margin:4px 0 2px 22px;color:var(--muted);font-size:5.6px}.urbion-runtime-opacity input{width:100%;accent-color:var(--cyan)}
  `;document.head.appendChild(s);
}

function mountImpact(){
  const r=root();if(!r)return false;
  let card=document.querySelector('[data-testid="development-impact"]');
  if(!card){card=document.createElement('section');card.className='urbion-runtime-impact';card.dataset.testid='development-impact';card.dataset.owner='canonical-runtime-fallback';r.prepend(card)}
  const p=packet();const impact=p?.evidence?.development_impact||p?.development_impact||null;const summary=impact?.impact_summary||{};
  const domains=['physical','social','economic'];
  const rows=domains.map(d=>{const s=summary[d]||{};const count=Number(s.metric_count||0);const ready=!!impact&&count>0&&!s.review_required;return `<div class="uri-row"><b>${d.toUpperCase()}</b><span class="uri-count">${count} metrics</span><span class="uri-state ${ready?'ready':''}">${!impact?'WAITING':ready?'READY':'REVIEW'}</span></div>`}).join('');
  card.innerHTML=`<div class="uri-head"><span class="uri-title">DEVELOPMENT IMPACT</span><span class="uri-sub">DECISION SUPPORT</span></div><div class="uri-note">Physical · Social · Economic screening · statutory verification ${esc(impact?.statutory_verification||p?.statutory_verification||'NOT_CLAIMED')}</div><div class="uri-grid">${rows}</div>`;
  return true;
}

function siteCoords(){
  const ids=[['site_lat','site_lon'],['cs-lat','cs-lon'],['cs_lat','cs_lon']];
  for(const [a,b] of ids){const la=Number($(a)?.value),lo=Number($(b)?.value);if(Number.isFinite(la)&&Number.isFinite(lo))return{lat:la,lon:lo}}
  const p=packet()?.site||{};const la=Number(p.latitude),lo=Number(p.longitude);return Number.isFinite(la)&&Number.isFinite(lo)?{lat:la,lon:lo}:null;
}

function roadSelectorPatch(){
  window.URBION_SITE_COORDS=siteCoords;
  const open=$('urbionRoadOpen');if(!open||open.dataset.runtimeCoordPatch==='1')return false;
  open.dataset.runtimeCoordPatch='1';
  const original=window.URBION_ROAD_OPEN_PATCH;
  if(original)return true;
  window.URBION_ROAD_OPEN_PATCH=()=>siteCoords();
  return true;
}

function opacityControls(){
  const list=$('layerList');if(!list)return;
  const live=window.__URBION_LIVE_LAYERS__||{};
  list.querySelectorAll('input[data-urbion-layer]').forEach(cb=>{
    const row=cb.closest('.urbion-layer-row')||cb.parentElement;if(!row)return;
    if(row.querySelector('.urbion-runtime-opacity'))return;
    const id=cb.dataset.urbionLayer||cb.dataset.layer;if(!id)return;
    const box=document.createElement('div');box.className='urbion-runtime-opacity';box.innerHTML='<span>OPACITY</span><input type="range" min="0" max="100" step="5" value="78"><b>78%</b>';row.appendChild(box);
    const slider=box.querySelector('input'),label=box.querySelector('b');const base=live[id]?.options?.opacity??0.78;slider.value=String(Math.round(base*100));label.textContent=slider.value+'%';slider.oninput=()=>{const v=Number(slider.value)/100;label.textContent=slider.value+'%';const layer=(window.__URBION_LIVE_LAYERS__||{})[id];if(layer?.setOpacity)layer.setOpacity(v)};
  });
}

async function hardeningScript(){
  if(document.querySelector('script[data-urbion-release-hardening="v6"]'))return;
  const s=document.createElement('script');s.src='/urbion_workspace_release_hardening_v6.js';s.dataset.urbionReleaseHardening='v6';s.async=false;
  s.onerror=()=>console.warn('URBION GIS visual hardening asset unavailable; canonical runtime fallback remains active');
  document.body.appendChild(s);
}

function bootFallbacks(){
  mapVisualStack();mountImpact();roadSelectorPatch();opacityControls();hardeningScript();
}

(async()=>{
  for(let i=0;i<120;i++){
    try{if(document.body){bootFallbacks();if($('layerList'))opacityControls();if(root())mountImpact();if(siteCoords())roadSelectorPatch();return}}catch(_){ }
    await sleep(100);
  }
})();
window.addEventListener('urbion:assessment-ready',()=>{mountImpact();roadSelectorPatch();},{passive:true});
window.addEventListener('urbion:analysis-ready',()=>{mountImpact();roadSelectorPatch();},{passive:true});
setInterval(()=>{try{mapVisualStack();mountImpact();opacityControls();roadSelectorPatch()}catch(_){ }},1000);
})();
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

wms = ROOT / "urbion_wms_proxy.py"
text = wms.read_text(encoding="utf-8")
needle = '''    if layers in WMTS_FALLBACK_LAYERS:\n        fallback = await _wmts_rest_fallback(layers, params)\n        if fallback is not None: return fallback\n        fallback = await _tms_tile_fallback(layers, params)\n        if fallback is not None: return fallback\n'''
replacement = '''    # Prefer an authoritative ArcGIS fallback that has already passed preflight\n    # over slow GWC/WMTS/TMS paths for known-problematic i-Plan layers. This is\n    # a routing optimization, not a data substitution: the fallback remains an\n    # official PLANMalaysia GIS service.\n    if layers in WMS_ARCGIS_FALLBACKS:\n        fallback = await _arcgis_wms_fallback(layers, params)\n        if fallback is not None: return fallback\n    if layers in WMTS_FALLBACK_LAYERS:\n        fallback = await _wmts_rest_fallback(layers, params)\n        if fallback is not None: return fallback\n        fallback = await _tms_tile_fallback(layers, params)\n        if fallback is not None: return fallback\n'''
if needle not in text:
    raise SystemExit("WMS routing anchor not found")
text = text.replace(needle, replacement, 1)
wms.write_text(text, encoding="utf-8")

bridge = ROOT / "urbion_workspace_bridge.js"
text = bridge.read_text(encoding="utf-8")
needle = """          canonicalLast=null;\n          canonicalAnalysisError=null;\n          try{if(typeof lastResult!=='undefined')lastResult=null;}catch(_){ }\n"""
replacement = """          canonicalLast=null;\n          canonicalAnalysisError=null;\n          try{window.dispatchEvent(new CustomEvent('urbion:analysis-start',{detail:{startedAt:Date.now()}}));}catch(_){ }\n          try{if(typeof lastResult!=='undefined')lastResult=null;}catch(_){ }\n"""
if needle not in text:
    raise SystemExit("analysis reset anchor not found")
text = text.replace(needle, replacement, 1)
bridge.write_text(text, encoding="utf-8")

lifecycle = ROOT / "urbion_workspace_lifecycle_hardening.js"
lifecycle.write_text(r'''/* URBION HORIZON — final analysis lifecycle guard. */
(()=>{
  'use strict';
  if(window.__URBION_LIFECYCLE_HARDENING_V1__)return;
  window.__URBION_LIFECYCLE_HARDENING_V1__=true;
  let run=0;
  window.__URBION_ANALYSIS_RUN_ID__=0;
  const stamp=()=>++run;
  window.addEventListener('urbion:analysis-start',()=>{
    const id=stamp();
    window.__URBION_ANALYSIS_RUN_ID__=id;
    window.__URBION_LAST_ANALYSIS_STATE__='RUNNING';
    try{window.dispatchEvent(new CustomEvent('urbion:derived-state-reset',{detail:{runId:id}}));}catch(_){ }
  },{passive:true});
  window.addEventListener('urbion:analysis-ready',e=>{
    const id=window.__URBION_ANALYSIS_RUN_ID__||run||1;
    window.__URBION_LAST_ANALYSIS_STATE__='READY';
    try{window.dispatchEvent(new CustomEvent('urbion:derived-state-ready',{detail:{runId:id,data:e.detail||null}}));}catch(_){ }
  },{passive:true});
  window.addEventListener('urbion-analysis-error',()=>{
    window.__URBION_LAST_ANALYSIS_STATE__='ERROR';
  },{passive:true});
})();
''', encoding="utf-8")

needle = """  function loadOwners(){
    loadOwner('/urbion_workspace_lcp_readiness_owner.js','__URBION_LCP_READINESS_OWNER_V1__');
    loadOwner('/urbion_workspace_concurrency_guard.js','__URBION_CONCURRENCY_GUARD_V1__');
  }
"""
replacement = """  function loadOwners(){
    loadOwner('/urbion_workspace_lcp_readiness_owner.js','__URBION_LCP_READINESS_OWNER_V1__');
    loadOwner('/urbion_workspace_concurrency_guard.js','__URBION_CONCURRENCY_GUARD_V1__');
    loadOwner('/urbion_workspace_lifecycle_hardening.js','__URBION_LIFECYCLE_HARDENING_V1__');
  }
"""
text = bridge.read_text(encoding="utf-8")
if needle not in text:
    raise SystemExit("owner-loader anchor not found")
bridge.write_text(text.replace(needle, replacement, 1), encoding="utf-8")

# The release automation itself is intentionally ephemeral; the workflow removes it after use.

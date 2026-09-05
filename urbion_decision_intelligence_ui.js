/* URBION HORIZON — explainable decision intelligence panel. */
(function(){
  'use strict';
  function esc(v){return String(v==null?'—':v).replace(/[&<>\"]/g,function(c){return({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'})[c]||c;});}
  function mount(){
    if(document.getElementById('urbion-di-panel')) return;
    var panel=document.createElement('section');
    panel.id='urbion-di-panel';
    panel.style.cssText='position:fixed;left:18px;bottom:18px;z-index:1300;width:min(420px,calc(100vw - 36px));max-height:54vh;overflow:auto;background:#09131deF;border:1px solid #294052;border-radius:16px;padding:14px;color:#eff8ff;font:12px Inter,system-ui;box-shadow:0 18px 60px #0008;display:none;';
    panel.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center"><strong>DECISION INTELLIGENCE</strong><button id="urbion-di-close" style="background:none;border:0;color:#9eb5c7;font-size:18px">×</button></div><div id="urbion-di-body" style="margin-top:10px;color:#b9cbd7">Run an assessment to generate evidence-weighted priorities.</div>';
    document.body.appendChild(panel);
    document.getElementById('urbion-di-close').onclick=function(){panel.style.display='none';};
    window.urbionDecisionIntelligence=function(payload){
      panel.style.display='block';
      var body=document.getElementById('urbion-di-body');
      body.innerHTML='<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0"><div><small>STATUS</small><br><b>'+esc(payload.decision_intelligence&&payload.decision_intelligence.decision_status)+'</b></div><div><small>CONFIDENCE</small><br><b>'+esc(payload.decision_intelligence&&payload.decision_intelligence.confidence&&payload.decision_intelligence.confidence.band)+'</b></div></div>';
      var actions=(payload.decision_intelligence&&payload.decision_intelligence.priority_actions)||[];
      body.innerHTML+='<div style="font-weight:800;margin:8px 0">PRIORITY ACTIONS</div>'+(actions.length?actions.map(function(a){return '<div style="padding:8px 0;border-top:1px solid #203443"><b>'+esc(a.priority)+' · '+esc(a.rule_id)+'</b><br><span style="color:#b9cbd7">'+esc(a.reason)+'</span></div>';}).join(''):'<div style="padding:8px 0">No mapped priority actions.</div>');
      body.innerHTML+='<div style="margin-top:10px;font-size:10px;color:#8299aa">DECISION-SUPPORT ONLY · STATUTORY VERIFICATION NOT CLAIMED</div>';
    };
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount); else mount();
})();

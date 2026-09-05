(()=>{
  if(location.pathname!=='/'&&!location.pathname.endsWith('/index.html')&&!location.pathname.endsWith('/championship.html'))return;
  const esc=v=>String(v??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
  const groups=[
    ['PLANNING',/I-PLAN|RFN|ZONING|LAND USE/,'Check land-use and statutory-plan context before forming a planning view.'],
    ['RISK',/FLOOD|DISASTER|FAULT|QUARRY|SEISMIC|GEOHAZARD/,'Screen constraints and risk exposure; escalate to the relevant technical source where required.'],
    ['ENVIRONMENT',/KSAS|ECOLOG|CFS|HERITAGE|GROUNDWATER|LITHOLOGY|MINERAL|GEOHERITAGE|TOPO/,'Review environmental, heritage and physical-context constraints before site suitability is concluded.']
  ];
  function inject(){
    const panel=document.querySelector('#spatial-studio .ss-panel');
    if(!panel||document.getElementById('ss-implications'))return;
    const sec=document.createElement('div');sec.id='ss-implications';sec.className='ss-section';
    sec.innerHTML='<b>SPATIAL → PLANNING IMPLICATION</b><div id="ss-implication-list" class="ss-layers"></div><div class="ss-note" style="margin-top:7px">Implications are planner prompts derived from the active layer names. They are not statutory determinations and do not replace source or authority verification.</div>';
    panel.insertBefore(sec,panel.querySelector('.ss-note'));render();
  }
  function render(){
    const host=document.getElementById('ss-implication-list');if(!host)return;
    const rows=[...document.querySelectorAll('#ss-layers input[data-i]:checked')].map(cb=>cb.closest('.ss-layer')?.textContent||'').join(' | ').toUpperCase();
    const active=groups.filter(([,rx])=>rx.test(rows));
    host.innerHTML=active.length?active.map(([name,,text])=>`<div class="ss-layer"><span><strong>${esc(name)}</strong><small>${esc(text)}</small></span><small>REVIEW</small></div>`).join(''):'<div class="ss-layer"><span><strong>NO ACTIVE GROUP</strong><small>Enable Planning, Risk or Environment layers to generate planner prompts.</small></span><small>WAIT</small></div>';
  }
  function boot(){inject();render();const h=document.getElementById('ss-layers');if(h)new MutationObserver(render).observe(h,{childList:true,subtree:true,attributes:true,attributeFilter:['checked']});}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();setTimeout(boot,700);
})();

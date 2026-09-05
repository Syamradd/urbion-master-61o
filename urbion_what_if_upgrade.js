(function(){
  if(location.pathname!=='/what-if.html' && !location.pathname.endsWith('/what-if.html')) return;
  const API=location.origin;
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function addStyles(){if(document.getElementById('urbion-wi-upgrade-style'))return;const s=document.createElement('style');s.id='urbion-wi-upgrade-style';s.textContent='.wi-presets{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:12px}.wi-preset{border:1px solid #28435e;border-radius:9px;padding:9px;background:#081727;color:#cfe0f2;cursor:pointer;text-align:left}.wi-preset:hover{border-color:#6caaf2}.wi-preset b{display:block;font-size:10px}.wi-preset span{display:block;font-size:8px;color:#8298b2;margin-top:3px}.wi-experiment{margin-top:12px;padding:12px;border:1px solid #315679;border-radius:11px;background:linear-gradient(135deg,#0b1d30,#091522)}.wi-experiment h3{margin:0 0 5px;font-size:11px}.wi-experiment p{margin:0;color:#8298b2;font-size:9px;line-height:1.5}@media(max-width:850px){.wi-presets{grid-template-columns:1fr}}';document.head.appendChild(s)}
  function inject(){
    addStyles();
    const panel=document.querySelector('.grid .card'); if(!panel||document.getElementById('wiExperiment'))return;
    const box=document.createElement('div');box.id='wiExperiment';box.className='wi-experiment';box.innerHTML='<h3>EXPERIMENT PRESETS</h3><p>Run the same assessment engine under a controlled planning change. Presets are screening experiments, not approval recommendations.</p><div class="wi-presets"><button class="wi-preset" data-w="1.5"><b>ACCESS UPGRADE</b><span>Walkway → 1.5 m</span></button><button class="wi-preset" data-w="2.0"><b>STRONG ACCESS</b><span>Walkway → 2.0 m</span></button><button class="wi-preset" data-w="0.5"><b>BASELINE</b><span>Keep current walkway</span></button></div>';
    const run=document.getElementById('run'); run&&run.parentNode.insertBefore(box,run);
    box.querySelectorAll('.wi-preset').forEach(b=>b.onclick=()=>{document.getElementById('variantWalk').value=b.dataset.w;document.getElementById('run').click()});
  }
  function boot(){inject();const h=document.getElementById('health');if(h)h.title='Same-origin URBION assessment engine';}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
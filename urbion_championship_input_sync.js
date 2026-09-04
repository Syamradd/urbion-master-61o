(()=>{
  const ids=['lat','lon','todlat','todlon','state','pbt','devtype','devclass','ratio','lot'];
  const $=id=>document.getElementById(id);
  const finite=v=>Number.isFinite(parseFloat(v));
  const snapshot=()=>Object.fromEntries(ids.map(id=>[id,$(id)?.value??'']));
  let timer;
  function status(text){
    const el=$('side-status');
    if(el) el.textContent=text;
  }
  function publish(source){
    const s=snapshot();
    const coords=['lat','lon','todlat','todlon'];
    if(!coords.every(id=>finite(s[id]))) return;
    window.dispatchEvent(new CustomEvent('urbion:site-change',{detail:{
      latitude:parseFloat(s.lat),longitude:parseFloat(s.lon),
      tod_latitude:parseFloat(s.todlat),tod_longitude:parseFloat(s.todlon),
      source,inputs:s
    }}));
    window.dispatchEvent(new CustomEvent('urbion:inputs-change',{detail:{source,inputs:s}}));
    status('Site inputs changed. Run analysis to refresh the decision chain.');
  }
  function schedule(source){
    clearTimeout(timer);
    timer=setTimeout(()=>publish(source),180);
  }
  function bind(){
    ids.forEach(id=>{
      const el=$(id); if(!el) return;
      el.addEventListener('input',()=>schedule(`input:${id}`));
      el.addEventListener('change',()=>schedule(`change:${id}`));
    });
    window.addEventListener('urbion:site-change',e=>{
      if(e.detail?.source?.startsWith('input:')||e.detail?.source?.startsWith('change:')) return;
      status('Site changed on map. Run analysis to refresh the decision chain.');
    });
    window.addEventListener('urbion:analysis',()=>status('Analysis complete. Decision chain refreshed.'));
    window.dispatchEvent(new CustomEvent('urbion:inputs-ready',{detail:{inputs:snapshot()}}));
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',bind); else bind();
})();

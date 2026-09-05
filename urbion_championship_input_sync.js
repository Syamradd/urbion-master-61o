(()=>{
  const ids=['lat','lon','todlat','todlon','state','pbt','devtype','devclass','ratio','lot'];
  const $=id=>document.getElementById(id);
  const finite=v=>Number.isFinite(parseFloat(v));
  const snapshot=()=>Object.fromEntries(ids.map(id=>[id,$(id)?.value??'']));
  const basePayload=()=>{const s=snapshot();return {site_lat:+s.lat,site_lon:+s.lon,tod_lat:+s.todlat,tod_lon:+s.todlon,plot_ratio:+s.ratio||4.5,precinct:$('precinct')?.value||'Terminal Sg. Udang',development_type:s.devtype||'TOD Development / Mixed Use',development_class:s.devclass||'Mixed Use',state:s.state||'Melaka',district:$('district')?.value||'Melaka Tengah',pbt:s.pbt||'Majlis Bandaraya Melaka Bersejarah',lot_no:s.lot||'',building_height:null,perimeter_planting:null,landscaped_pedestrian_walkway:null,shop_frontage_verified:false,shop_office_verified:false};};
  const payloadKey=payload=>JSON.stringify(payload);
  const nativeFetch=window.fetch.bind(window);
  let timer,version=0,cachedVersion=-1,cachedKey='',cached=null,inflight=null,assessCount=0;
  function status(text){const el=$('side-status');if(el)el.textContent=text;}
  function persistInputs(){try{localStorage.setItem('urbion:assessment-inputs',JSON.stringify(basePayload()))}catch(e){}}
  function invalidate(source){version+=1;cached=null;cachedVersion=-1;cachedKey='';window.dispatchEvent(new CustomEvent('urbion:assessment-invalidated',{detail:{version,source}}));}
  async function sharedAssess(extra={}){
    const payload={...basePayload(),...extra};
    const key=payloadKey(payload);
    if(cachedVersion===version&&cachedKey===key&&cached) return cached;
    if(inflight&&inflight.version===version&&inflight.key===key) return inflight.promise;
    assessCount+=1;
    const requestVersion=version;
    const requestKey=key;
    const promise=nativeFetch('/assess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(r=>{if(!r.ok)throw Error(`Assessment ${r.status}`);return r.json()}).then(data=>{if(version===requestVersion&&inflight?.version===requestVersion&&inflight?.key===requestKey){cached=data;cachedVersion=requestVersion;cachedKey=requestKey;window.__urbionAssessment=data;try{localStorage.setItem('urbion:assessment',JSON.stringify(data));localStorage.setItem('urbion:assessment-inputs',JSON.stringify(payload))}catch(e){}window.dispatchEvent(new CustomEvent('urbion:analysis',{detail:data}));}return data}).finally(()=>{if(inflight?.version===requestVersion&&inflight?.key===requestKey)inflight=null});
    inflight={version:requestVersion,key:requestKey,promise};
    return promise;
  }
  window.URBION=window.URBION||{};
  window.URBION.getSiteSnapshot=()=>snapshot();
  window.URBION.getAssessmentPayload=()=>basePayload();
  window.URBION.invalidateAssessment=source=>invalidate(source||'unknown');
  window.URBION.assess=sharedAssess;
  window.URBION.getAssessmentStats=()=>({version,assessCount,cached:Boolean(cached),cachedKey});
  function publish(source){
    const s=snapshot();
    const coords=['lat','lon','todlat','todlon'];
    if(!coords.every(id=>finite(s[id]))) return;
    persistInputs();
    invalidate(source);
    window.dispatchEvent(new CustomEvent('urbion:site-change',{detail:{latitude:parseFloat(s.lat),longitude:parseFloat(s.lon),tod_latitude:parseFloat(s.todlat),tod_longitude:parseFloat(s.todlon),source,inputs:s}}));
    window.dispatchEvent(new CustomEvent('urbion:inputs-change',{detail:{source,inputs:s}}));
    status('Site inputs changed. Run analysis to refresh the decision chain.');
  }
  function schedule(source){clearTimeout(timer);timer=setTimeout(()=>publish(source),180);}
  function bind(){
    ids.forEach(id=>{const el=$(id);if(!el)return;el.addEventListener('input',()=>schedule(`input:${id}`));el.addEventListener('change',()=>schedule(`change:${id}`));});
    window.addEventListener('urbion:site-change',e=>{if(e.detail?.source?.startsWith('input:')||e.detail?.source?.startsWith('change:'))return;persistInputs();invalidate(e.detail?.source||'map');status('Site changed on map. Run analysis to refresh the decision chain.');});
    window.addEventListener('urbion:analysis',()=>status('Analysis complete. Decision chain refreshed.'));
    window.dispatchEvent(new CustomEvent('urbion:inputs-ready',{detail:{inputs:snapshot()}}));
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind);else bind();
})();

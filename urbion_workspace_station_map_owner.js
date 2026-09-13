/* URBION HORIZON — live station map overlay owner.
   Renders map markers from the canonical mobility evidence packet. It only
   performs a direct query when no canonical station snapshot exists yet. */
(()=>{
'use strict';
if(window.__URBION_STATION_MAP_OWNER_V2__)return;
window.__URBION_STATION_MAP_OWNER_V2__=true;
const $=id=>document.getElementById(id);
function mapObj(){try{return (typeof map!=='undefined'&&map)||window.__URBION_MAP__||window.__URBION_FCC_MAP__||null}catch(_){return null}}
function packet(){return window.URBION_LAST?.canonical_evidence_packet||null}
function cachedStations(){const p=packet();return p?.evidence?.stations||window.URBION_LAST?.live_station_evidence||null}
function esc(s){return String(s??'').replace(/[&<>\"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[m]))}
function style(){if($('urbionStationMapStyle'))return;const s=document.createElement('style');s.id='urbionStationMapStyle';s.textContent='.urbion-station-btn{width:100%;margin-top:6px;padding:7px 9px;border:1px solid rgba(47,225,233,.22);background:rgba(47,225,233,.05);border-radius:8px;text-align:left;font-size:6.5px}.urbion-station-btn.on{border-color:rgba(72,223,170,.5);color:var(--good)}';document.head.appendChild(s)}
function popup(item,domain){
 const parts=[];
 if(domain==='JPS RAINFALL'){const reading=item.rainfall_1h_mm??item.daily_rainfall_mm??null;parts.push(reading==null?'No reading':`${esc(reading)} mm`)}
 else if(domain==='MYEQMS WATER'){if(item.ph!=null)parts.push(`pH ${esc(item.ph)}`);if(item.turbidity_ntu!=null)parts.push(`Turbidity ${esc(item.turbidity_ntu)} NTU`);if(item.conductivity_us_cm!=null)parts.push(`Conductivity ${esc(item.conductivity_us_cm)} µS/cm`)}
 else {const reading=item.reading??item.api??null;parts.push(reading==null?'No reading':`${esc(reading)} ${esc(item.unit||'')}`)}
 return `<b>${esc(item.name||item.station_id||'Station')}</b><br>${esc(domain)} · ${parts.join(' · ')}<br>${item.distance_m!=null?esc(Math.round(item.distance_m)+' m from site'):''}<br><small>SOURCE_CONTEXT · ${esc(item.last_updated||item.last_updated_rainfall||item.observed_at||'time not supplied')}</small>`}
let layer=null;
async function loadStations(){
 const cached=cachedStations();
 if(cached)return cached;
 const lat=Number($('site_lat')?.value),lon=Number($('site_lon')?.value),state=String($('state')?.value||'Melaka');
 if(!Number.isFinite(lat)||!Number.isFinite(lon))throw Error('Site coordinates unavailable');
 const r=await fetch(`/mobility/stations?site_lat=${encodeURIComponent(lat)}&site_lon=${encodeURIComponent(lon)}&state=${encodeURIComponent(state)}&limit=10`,{cache:'no-store'});
 const d=await r.json();if(!r.ok)throw Error(d?.detail||`HTTP ${r.status}`);return d}
function toggleMarkers(data,on){const m=mapObj();if(!m||typeof L==='undefined')throw Error('Map engine unavailable');if(layer){try{m.removeLayer(layer)}catch(_){}layer=null}if(!on)return;layer=L.layerGroup();const feeds=[['JPS RAINFALL',data?.jps_rainfall?.stations||[]],['MYEQMS WATER',data?.eqmp_water?.stations||[]],['AIR QUALITY',data?.air_quality?.stations||[]]];for(const [domain,items] of feeds){for(const item of items){const lat=Number(item.latitude??item.lat),lon=Number(item.longitude??item.lon);if(!Number.isFinite(lat)||!Number.isFinite(lon))continue;const marker=L.circleMarker([lat,lon],{radius:6,weight:2,fillOpacity:.8});marker.bindPopup(popup(item,domain));marker.addTo(layer)}}layer.addTo(m)}
function stationCount(data){return (data?.jps_rainfall?.stations||[]).length+(data?.eqmp_water?.stations||[]).length+(data?.air_quality?.stations||[]).length}
function mount(){style();const root=document.querySelector('.right');if(!root)return false;if($('urbionStationMapCard'))return true;const card=document.createElement('section');card.id='urbionStationMapCard';card.className='card';card.innerHTML='<div class="cardhead"><h3>MAP · LIVE STATIONS</h3><span class="tiny">OBSERVATION</span></div><div class="tiny">JPS rainfall · MyEQMS water stations · DOE air-quality stations when source data is available.</div><button type="button" class="urbion-station-btn" id="urbionStationToggle">SHOW STATIONS ON MAP</button><div class="tiny" id="urbionStationStatus" style="margin-top:5px">OFF · no station markers rendered</div>';root.appendChild(card);$('urbionStationToggle').addEventListener('click',async()=>{const b=$('urbionStationToggle'),st=$('urbionStationStatus');const on=b.dataset.on==='1';if(on){toggleMarkers(null,false);b.dataset.on='0';b.textContent='SHOW STATIONS ON MAP';b.classList.remove('on');st.textContent='OFF · no station markers rendered';return}b.disabled=true;st.textContent='LOADING · canonical/live station coordinates';try{const d=await loadStations();toggleMarkers(d,true);b.dataset.on='1';b.textContent='HIDE STATIONS FROM MAP';b.classList.add('on');const total=stationCount(d);const eqmp=(d?.eqmp_water?.stations||[]).length;st.textContent=total?`ON · ${total} source-backed station markers · MyEQMS ${eqmp}`:'ON · no station geometry returned';}catch(e){st.textContent='UNAVAILABLE · '+e.message}finally{b.disabled=false}});return true}
function boot(){let n=0;const t=setInterval(()=>{if(mount()||++n>=300)clearInterval(t)},100)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

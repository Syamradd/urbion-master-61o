(()=>{
'use strict';
if(window.__URBION_VISUAL_CLEANUP)return;window.__URBION_VISUAL_CLEANUP=true;
let baseLayers={};
function mapFor(){const map=document.getElementById('ss-map');return map?.__urbionMap||(window.__URBION_MAPS||[]).find(x=>x&&x.getContainer&&x.getContainer()===map)}
function basemapDefinitions(){return {
 'STREET · OSM':L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap contributors'}),
 'SATELLITE · ESRI':L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Tiles © Esri'}),
 'HYBRID · ESRI':L.layerGroup([
   L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Tiles © Esri'}),
   L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,opacity:.95,attribution:'Labels © Esri'})
 ]),
 'TOPO · ESRI':L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Tiles © Esri'}),
 'LIGHT · CARTO':L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{maxZoom:20,subdomains:'abcd',attribution:'© OpenStreetMap © CARTO'}),
 'DARK · CARTO':L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{maxZoom:20,subdomains:'abcd',attribution:'© OpenStreetMap © CARTO'}),
 'TERRAIN · OTM':L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',{maxZoom:17,subdomains:'abc',attribution:'© OpenStreetMap contributors © OpenTopoMap'})
}}
function addBasemapDock(m){
 if(document.getElementById('urbion-basemap-dock'))return;
 const mapNode=document.getElementById('ss-map');if(!mapNode)return;
 const dock=document.createElement('div');dock.id='urbion-basemap-dock';
 dock.innerHTML='<div class="ubd-head"><b>BASEMAP</b><span>VISUAL MODE</span></div><div class="ubd-buttons"></div>';
 dock.style.cssText='position:absolute;z-index:800;top:12px;left:52px;padding:9px;border:1px solid rgba(35,68,85,.9);border-radius:12px;background:rgba(6,19,28,.90);backdrop-filter:blur(12px);box-shadow:0 10px 30px rgba(0,0,0,.24);font:700 8px Inter,system-ui,sans-serif;color:#edf8fb;max-width:calc(100% - 64px)';
 dock.querySelector('.ubd-head').style.cssText='display:flex;gap:8px;align-items:center;margin-bottom:6px;letter-spacing:.08em;color:#43e5bd';
 dock.querySelector('.ubd-head span').style.cssText='color:#89a5b4;font-size:7px';
 const btns=dock.querySelector('.ubd-buttons');btns.style.cssText='display:flex;gap:4px;flex-wrap:wrap';
 Object.keys(baseLayers).forEach(name=>{const b=document.createElement('button');b.type='button';b.textContent=name;b.dataset.basemap=name;b.style.cssText='border:1px solid #234455;border-radius:7px;padding:6px 8px;background:#0b1c27;color:#d9eef2;font:800 7px Inter;cursor:pointer';b.onclick=()=>setBasemap(m,name);btns.appendChild(b)});
 mapNode.appendChild(dock);
}
function setBasemap(m,name){
 Object.values(baseLayers).forEach(l=>{try{if(m.hasLayer(l))m.removeLayer(l)}catch(e){}});
 const next=baseLayers[name];if(!next)return;next.addTo(m);
 document.querySelectorAll('#urbion-basemap-dock button').forEach(b=>{const active=b.dataset.basemap===name;b.style.background=active?'#43e5bd':'#0b1c27';b.style.color=active?'#06131c':'#d9eef2';b.style.borderColor=active?'#43e5bd':'#234455'});
 const label=document.querySelector('#urbion-basemap-dock .ubd-head span');if(label)label.textContent=name;
}
function run(){
 const m=mapFor();if(!m)return false;
 m.eachLayer(layer=>{if(layer instanceof L.TileLayer || layer instanceof L.LayerGroup)return;m.removeLayer(layer)});
 ['urbion-workstation-v2','urbion-decision-os'].forEach(id=>document.getElementById(id)?.remove());
 baseLayers=basemapDefinitions();
 addBasemapDock(m);
 setBasemap(m,'STREET · OSM');
 return true;
}
function wait(n=80){if(run()||n<=0)return;setTimeout(()=>wait(n-1),100)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>wait());else wait();
})();
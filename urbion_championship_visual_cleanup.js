(()=>{
'use strict';
if(window.__URBION_VISUAL_CLEANUP)return;window.__URBION_VISUAL_CLEANUP=true;
function run(){
 const map=document.getElementById('ss-map');
 const m=map?.__urbionMap||(window.__URBION_MAPS||[]).find(x=>x&&x.getContainer&&x.getContainer()===map);
 if(!m)return false;
 m.eachLayer(layer=>{if(layer instanceof L.TileLayer)return;m.removeLayer(layer)});
 ['urbion-workstation-v2','urbion-decision-os'].forEach(id=>document.getElementById(id)?.remove());
 return true;
}
function wait(n=80){if(run()||n<=0)return;setTimeout(()=>wait(n-1),100)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>wait());else wait();
})();
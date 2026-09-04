/* MASTER-279 loader: preserve the reliability bridge while layering MASTER-280. */
(()=>{
'use strict';
if(window.__URBION_CHAMPIONSHIP_V279_LOADER__)return;
window.__URBION_CHAMPIONSHIP_V279_LOADER__=1;
const load=src=>new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src;s.async=false;s.onload=resolve;s.onerror=reject;document.head.appendChild(s)});
load('/urbion_championship_reliability_279.js').then(()=>load('/urbion_championship_v280.js')).catch(e=>console.error('URBION championship layer load failed',e));
})();
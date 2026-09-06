(()=>{
'use strict';
/*
 * Compatibility asset kept for the championship acceptance contract.
 * The canonical championship_server.py now owns the single frontend path and
 * the final command centre owns its own mount lifecycle, so this file must not
 * start duplicate loaders, MutationObservers, or 100ms polling loops.
 */
if(window.__URBION_FINAL_RUNTIME_ENFORCER)return;
window.__URBION_FINAL_RUNTIME_ENFORCER=true;
const app=document.querySelector('body > .app');
if(app)app.style.display='none';
})();

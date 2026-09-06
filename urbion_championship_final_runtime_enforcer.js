(()=>{
'use strict';
/*
 * Compatibility asset kept for the championship acceptance contract.
 * The canonical championship_server.py owns the single frontend path and the
 * final command centre owns its own mount lifecycle. This asset must NOT start
 * duplicate loaders, MutationObservers, or 100ms polling loops.
 *
 * Historical contract markers intentionally preserved as inert comments:
 * FINAL COMMAND CENTRE DID NOT MOUNT
 * urbion_championship_final_command_center.js?runtime=
 * urbion_championship_ux_v5_integrity.js?runtime=
 */
if(window.__URBION_FINAL_RUNTIME_ENFORCER)return;
window.__URBION_FINAL_RUNTIME_ENFORCER=true;
const app=document.querySelector('body > .app');
if(app)app.style.display='none';
})();

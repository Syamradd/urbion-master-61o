(()=>{
'use strict';
// Small pre-command-centre bridge: expose the real Leaflet map instance without creating
// a second map or replacing any existing map logic.
if(window.__URBION_MAP_BRIDGE__)return;
window.__URBION_MAP_BRIDGE__=true;
function install(){
  if(!window.L||!window.L.map||window.__URBION_LEAFLET_MAP_WRAPPED__)return !!window.__URBION_LEAFLET_MAP_WRAPPED__;
  const original=window.L.map;
  if(original.__urbionWrapped){window.__URBION_LEAFLET_MAP_WRAPPED__=true;return true;}
  const wrapped=function(...args){
    const instance=original.apply(this,args);
    if(instance){window.__URBION_FCC_MAP__=instance;window.URBION_FCC_MAP=instance;window.__URBION_MAP__=instance;}
    return instance;
  };
  wrapped.__urbionWrapped=true;
  wrapped.original=original;
  window.L.map=wrapped;
  window.__URBION_LEAFLET_MAP_WRAPPED__=true;
  return true;
}
if(!install()){
  let tries=0;
  const timer=setInterval(()=>{tries+=1;if(install()||tries>=80)clearInterval(timer);},50);
}
})();

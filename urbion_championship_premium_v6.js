(()=>{
'use strict';
/* Retired compatibility asset. The canonical command shell owns the UI and map;
   Premium V7 owns official i-Plan layer integration. This file intentionally
   performs no DOM, CSS, map or event mutation. */
})();

/* Shared status helper used by Premium V7 official i-Plan integration. */
function syncLayerState(r,id,active,text){
  const input=r?.querySelector(`#cs-layer-drawer input[data-layer="${id}"]`);
  const row=input?.closest?.('.fcc-layer-row');
  const small=row?.querySelector?.('span small')||row?.querySelector?.('small');
  if(small&&text!=null)small.textContent=String(text);
  if(row)row.classList.toggle('is-on',!!active);
}

/* URBION HORIZON — canonical modal close owner. */
(()=>{
'use strict';
if(window.__URBION_MODAL_OWNER_V1__) return;
window.__URBION_MODAL_OWNER_V1__=true;
document.addEventListener('click',event=>{
  const target=event.target instanceof Element ? event.target.closest('#closeModal') : null;
  if(!target) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  document.getElementById('modal')?.classList.remove('show');
},true);
})();

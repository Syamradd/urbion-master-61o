/* URBION HORIZON — canonical modal close owner.
   One delegated handler guarantees the current modal can always be dismissed,
   even after modal body content is replaced dynamically. */
(()=>{
'use strict';
if(window.__URBION_MODAL_OWNER_V1__) return;
window.__URBION_MODAL_OWNER_V1__=true;
document.addEventListener('click',event=>{
  const target=event.target instanceof Element ? event.target.closest('#closeModal') : null;
  if(!target) return;
  event.preventDefault();
  event.stopPropagation();
  document.getElementById('modal')?.classList.remove('show');
});
})();

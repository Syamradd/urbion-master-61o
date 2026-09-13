/* URBION HORIZON — workspace utility control owner.
   Uses delegated capture so utility actions survive canonical/runtime control
   replacement without creating another planning engine. */
(()=>{
'use strict';
if(window.__URBION_UTILITY_OWNER_V1__) return;
window.__URBION_UTILITY_OWNER_V1__=true;
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const CONTENT={
  runtimeAbout:{title:'ABOUT URBION HORIZON',html:'<p><b>URBION HORIZON</b> is an AI-assisted spatial planning decision-support workspace.</p><p>The platform combines site context, GIS layers, planning evidence, scenario analysis and explainable decision support.</p><small>Decision support only · not statutory approval.</small>'},
  runtimeHelp:{title:'WORKSPACE HELP',html:'<p><b>Assess → Map → Evidence → What-If → Decide</b></p><p>Complete the planning case, run Site Analysis, inspect evidence, test scenarios and review the recommendation before KM/OSC action.</p>'},
  runtimeSources:{title:'SOURCES & PROVENANCE',html:'<p>URBION combines official planning-source registry context with live GIS decision-support layers.</p><p>Source availability does not by itself establish statutory currency or applicability. Verify authoritative records before formal planning decisions.</p>'},
  runtimeStatus:{title:'SYSTEM STATUS',html:'<p><b>Workspace:</b> ONLINE</p><p><b>Analysis:</b> '+(window.URBION_LAST?'READY / RESULT STORED':'PRE-RUN / AWAITING CASE')+'</p><p><b>AI:</b> '+(window.URBION_AI_LAST?'NARRATIVE AVAILABLE':'ON DEMAND')+'</p><small>Deterministic planning packet remains the source of truth.</small>'}
};
function open(id){const def=CONTENT[id];if(!def)return false;const modal=$('modal');const title=$('modalTitle');const body=$('modalBody');if(!modal||!body)return false;if(title)title.textContent=def.title;body.innerHTML=def.html;modal.classList.add('show');return true}
document.addEventListener('click',e=>{const btn=e.target.closest?.('#runtimeAbout,#runtimeHelp,#runtimeSources,#runtimeStatus');if(!btn)return;const id=btn.id;if(!CONTENT[id])return;e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();open(id)},true);
})();

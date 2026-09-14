/* URBION HORIZON — workspace utility control owner.
   Creates and owns utility controls, then handles them through one delegated
   capture path. It does not bind planning/map/navigation controls. */
(()=>{
'use strict';
if(window.__URBION_UTILITY_OWNER_V2__) return;
window.__URBION_UTILITY_OWNER_V2__=true;
const $=id=>document.getElementById(id);
const CONTENT={
  runtimeAbout:{title:'ABOUT URBION HORIZON',html:'<p><b>URBION HORIZON</b> is an AI-assisted spatial planning decision-support workspace.</p><p>The platform combines site context, GIS layers, planning evidence, scenario analysis and explainable decision support.</p><small>Decision support only · not statutory approval.</small>'},
  runtimeHelp:{title:'WORKSPACE HELP',html:'<p><b>Assess → Map → Evidence → What-If → Decide</b></p><p>Complete the planning case, run Site Analysis, inspect evidence, test scenarios and review the recommendation before KM/OSC action.</p>'},
  runtimeSources:{title:'SOURCES & PROVENANCE',html:'<p>URBION combines official planning-source registry context with live GIS decision-support layers.</p><p>Source availability does not by itself establish statutory currency or applicability. Verify authoritative records before formal planning decisions.</p>'},
  runtimeStatus:{title:'SYSTEM STATUS',html:'<p><b>Workspace:</b> ONLINE</p><p><b>Analysis:</b> '+(window.URBION_LAST?'READY / RESULT STORED':'PRE-RUN / AWAITING CASE')+'</p><p><b>AI:</b> '+(window.URBION_AI_LAST?'NARRATIVE AVAILABLE':'ON DEMAND')+'</p><small>Deterministic planning packet remains the source of truth.</small>'}
};
function modal(title,html){const m=$('modal'),h=$('modalTitle'),b=$('modalBody');if(!m||!b)return false;if(h)h.textContent=title;b.innerHTML=html;m.classList.add('show');return true}
function toast(message,ok=true){const t=$('toast');if(!t)return;t.textContent=message;t.style.display='block';t.style.color=ok?'var(--good)':'var(--bad)';clearTimeout(window.__urbionUtilityToast);window.__urbionUtilityToast=setTimeout(()=>{t.style.display='none'},2400)}
function createUtilities(){
  const top=document.querySelector('.top');
  if(!top||$('urbionUtilityTools'))return;
  const box=document.createElement('div');box.id='urbionUtilityTools';box.style.cssText='display:flex;align-items:center;gap:4px;margin-left:4px;flex-shrink:0';
  const make=(id,label)=>{const b=document.createElement('button');b.id=id;b.className='tool';b.type='button';b.textContent=label;return b};
  const about=make('runtimeAbout','ABOUT');
  const help=make('runtimeHelp','HELP');
  const sources=make('runtimeSources','SOURCES');
  const status=make('runtimeStatus','STATUS');
  const fullscreen=make('runtimeFullscreen','FULLSCREEN');
  const reset=make('runtimeReset','RESET');
  [about,help,sources,status,fullscreen,reset].forEach(b=>box.appendChild(b));
  top.appendChild(box);
}
function openUtility(id){const def=CONTENT[id];if(!def)return false;return modal(def.title,def.html)}
async function toggleFullscreen(){try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen()}catch(e){toast('Fullscreen unavailable',false)}}
function handleClick(e){
  const btn=e.target.closest?.('#runtimeAbout,#runtimeHelp,#runtimeSources,#runtimeStatus,#runtimeFullscreen,#runtimeReset');
  if(!btn)return;
  e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();
  if(btn.id==='runtimeFullscreen'){void toggleFullscreen();return}
  if(btn.id==='runtimeReset'){if(window.confirm('Reset this planning case?'))window.location.reload();return}
  openUtility(btn.id);
}
function boot(){createUtilities();document.addEventListener('click',handleClick,true)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

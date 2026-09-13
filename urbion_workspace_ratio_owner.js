/* URBION HORIZON — plot ratio presentation owner.
   Keeps the deterministic numeric denominator used by the engine while
   presenting the planning convention explicitly as 1 : X to the planner. */
(()=>{
'use strict';
if(window.__URBION_RATIO_OWNER_V3__) return;
window.__URBION_RATIO_OWNER_V3__=true;
const $=id=>document.getElementById(id);
function style(){
  if($('urbionRatioOwnerStyle')) return;
  const s=document.createElement('style');s.id='urbionRatioOwnerStyle';
  s.textContent='.urbion-ratio-fallback{border:1px solid var(--line);border-radius:10px;background:linear-gradient(145deg,rgba(8,31,43,.96),rgba(3,15,22,.98));margin-bottom:6px;overflow:hidden}.urbion-ratio-fallback .body{padding:8px 9px}.urbion-ratio-control{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:7px}.urbion-ratio-prefix{font:800 10px Space Grotesk,system-ui,sans-serif;color:var(--cyan);white-space:nowrap;border:1px solid rgba(47,225,233,.22);background:rgba(47,225,233,.06);padding:7px 8px;border-radius:8px}.urbion-ratio-hint{font-size:6px;color:var(--muted);line-height:1.45;margin-top:3px}';
  document.head.appendChild(s);
}
function locate(){
  const direct=$('plot_ratio'); if(direct) return direct;
  for(const row of document.querySelectorAll('.sec .row')){
    const label=row.querySelector('.lab');
    if(label&&/PLOT\s*RATIO/i.test(label.textContent)){
      const control=row.querySelector('input,select,textarea');
      if(control){control.id='plot_ratio';return control;}
    }
  }
  return null;
}
function injectFallback(){
  let input=$('plot_ratio'); if(input) return input;
  const host=document.querySelector('.leftscroll');
  if(!host) return null;
  const sec=document.createElement('section');
  sec.className='urbion-ratio-fallback sec';
  sec.innerHTML='<div class="sechead"><span class="num">PR</span><button type="button">PLOT RATIO · 1 : X</button></div><div class="body"><div class="row"><label class="lab" for="plot_ratio">PLOT RATIO · 1 : X</label><div class="urbion-ratio-control"><span class="urbion-ratio-prefix">1 :</span><input id="plot_ratio" class="field" type="number" min="0.1" step="0.1" value="4.5" inputmode="decimal" autocomplete="off"></div><div class="urbion-ratio-hint">Enter X only · e.g. 4.5 → 1 : 4.5. The planning engine continues to use the numeric denominator.</div></div></div>';
  host.appendChild(sec);
  sec.querySelector('.sechead button')?.addEventListener('click',()=>sec.classList.toggle('collapsed'));
  return $('plot_ratio');
}
function apply(){
  let input=locate();
  if(!input) input=injectFallback();
  if(!input) return;
  style();
  const row=input.closest('.row');
  if(row){const label=row.querySelector('.lab');if(label)label.textContent='PLOT RATIO · 1 : X';}
  input.dataset.ratioOwner='1';
  input.type='number';input.min='0.1';input.step='0.1';
  input.title='Enter the denominator only. Example: 4.5 means a plot ratio of 1 : 4.5.';
  if(!String(input.value||'').trim()) input.value='4.5';
  if(!input.closest('.urbion-ratio-control')){
    const wrap=document.createElement('div');wrap.className='urbion-ratio-control';
    const prefix=document.createElement('span');prefix.className='urbion-ratio-prefix';prefix.textContent='1 :';
    wrap.append(prefix);input.parentNode.insertBefore(wrap,input);wrap.appendChild(input);
    const hint=document.createElement('div');hint.className='urbion-ratio-hint';hint.textContent='Enter X only · e.g. 4.5 → 1 : 4.5. The planning engine continues to use the numeric denominator.';
    wrap.parentNode.appendChild(hint);
  }
}
function boot(){
  style();apply();
  let tries=0;const timer=setInterval(()=>{apply();if(++tries>=160)clearInterval(timer)},100);
  console.info('URBION PLOT RATIO OWNER READY · 1:X presentation');
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

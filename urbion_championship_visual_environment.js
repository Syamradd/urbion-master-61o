(()=>{
'use strict';
if(window.__URBION_VISUAL_ENVIRONMENT__)return;
window.__URBION_VISUAL_ENVIRONMENT__=true;
function boot(){
  if(document.documentElement.dataset.urbionVisualEnvironment==='ready')return;
  document.documentElement.dataset.urbionVisualEnvironment='ready';
  const root=document.body;
  if(!root)return;
  const scene=document.createElement('div');
  scene.id='urbion-visual-environment';
  scene.setAttribute('aria-hidden','true');
  scene.innerHTML='<div class="uve-sky"></div><div class="uve-grid"></div><div class="uve-skyline"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="uve-orbit uve-orbit-a"></div><div class="uve-orbit uve-orbit-b"></div><div class="uve-pulse uve-pulse-a"></div><div class="uve-pulse uve-pulse-b"></div>';
  const css=document.createElement('style');
  css.textContent=`#urbion-visual-environment{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;background:linear-gradient(180deg,#06131e 0%,#0a202a 48%,#07141d 100%)}#urbion-visual-environment .uve-sky{position:absolute;inset:0;background:radial-gradient(ellipse at 72% 12%,rgba(105,226,192,.20),transparent 34%),radial-gradient(ellipse at 18% 8%,rgba(53,168,195,.16),transparent 30%),linear-gradient(180deg,rgba(7,27,39,.05),rgba(5,14,22,.82));}.uve-grid{position:absolute;left:-8%;right:-8%;bottom:-22%;height:64%;opacity:.18;background-image:linear-gradient(rgba(105,226,192,.22) 1px,transparent 1px),linear-gradient(90deg,rgba(105,226,192,.22) 1px,transparent 1px);background-size:42px 42px;transform:perspective(520px) rotateX(62deg);transform-origin:center bottom}.uve-skyline{position:absolute;left:0;right:0;bottom:0;height:29%;display:flex;align-items:flex-end;gap:2px;padding:0 3%;opacity:.46;background:linear-gradient(180deg,transparent 0%,rgba(5,16,24,.2) 40%,rgba(4,11,17,.78) 100%)}.uve-skyline i{display:block;flex:1;max-width:68px;min-width:12px;height:var(--h,42%);background:linear-gradient(180deg,rgba(43,117,132,.32),rgba(5,16,24,.92));border:1px solid rgba(105,226,192,.08);clip-path:polygon(8% 0,92% 0,100% 100%,0 100%)}.uve-skyline i:nth-child(2n){--h:68%;}.uve-skyline i:nth-child(3n){--h:36%;}.uve-skyline i:nth-child(5n){--h:84%;}.uve-orbit{position:absolute;border:1px solid rgba(105,226,192,.12);border-radius:50%;filter:blur(.2px);}.uve-orbit-a{width:360px;height:160px;right:-90px;top:10%;transform:rotate(-18deg)}.uve-orbit-b{width:300px;height:120px;left:-110px;top:22%;transform:rotate(17deg)}.uve-pulse{position:absolute;width:8px;height:8px;border-radius:50%;background:rgba(105,226,192,.75);box-shadow:0 0 0 6px rgba(105,226,192,.04),0 0 24px rgba(105,226,192,.38)}.uve-pulse-a{right:18%;top:22%}.uve-pulse-b{left:22%;top:38%}body>#urbion-championship-shell,body>.map-panel,body>.fcc-workspace,body>.leaflet-container,body>main{position:relative;z-index:1}.leaflet-container{background:transparent}.fcc-workspace,.map-panel{isolation:isolate}`;
  document.head.appendChild(css);root.insertBefore(scene,root.firstChild||null);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

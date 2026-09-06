(()=>{'use strict';
if(window.__URBION_FINAL_COMMAND_CENTER)return;window.__URBION_FINAL_COMMAND_CENTER=true;
const $=s=>document.querySelector(s);
const $$=s=>Array.from(document.querySelectorAll(s));
const LEGACY_IDS=['urbion-decision-os','urbion-workstation-v2','urbion-theme-toggle'];
function removeLegacy(){
  LEGACY_IDS.forEach(id=>document.getElementById(id)?.remove());
  $$('body *').forEach(el=>{
    if(el===document.body||el.id==='ux-v5-rail'||el.closest('#ux-v5-rail'))return;
    const t=(el.textContent||'').trim();
    if(t==='PLANNER HANDOFF'&&el.children.length===0)el.remove();
  });
}
function brand(){
  const logo=$('.header .logo');
  if(!logo)return;
  logo.textContent='';
  logo.setAttribute('aria-label','URBION HORIZON');
  logo.style.width='190px';logo.style.height='48px';logo.style.border='0';logo.style.borderRadius='0';logo.style.background='none';
  logo.style.backgroundImage="url('/urbion_logo_dark.svg')";logo.style.backgroundRepeat='no-repeat';logo.style.backgroundPosition='left center';logo.style.backgroundSize='contain';
  const apply=()=>{logo.style.backgroundImage=document.body.classList.contains('urbion-light')?"url('/urbion_logo_light.svg')":"url('/urbion_logo_dark.svg')"};
  apply();
  if(!logo.dataset.themeWatch){logo.dataset.themeWatch='1';new MutationObserver(apply).observe(document.body,{attributes:true,attributeFilter:['class']})}
}
function css(){
 if($('#urbion-final-ui-style'))return;
 const s=document.createElement('style');s.id='urbion-final-ui-style';s.textContent=`
 #urbion-decision-os,#urbion-workstation-v2,#urbion-theme-toggle{display:none!important}
 body{overflow-x:hidden}
 .header{height:74px!important;padding:0 24px!important;position:sticky!important;top:0!important;z-index:5000!important;background:rgba(4,13,21,.94)!important;backdrop-filter:blur(20px)!important}
 .header .logo{flex:0 0 190px!important}
 .brand strong{font-size:15px!important}.brand small{font-size:7px!important;letter-spacing:.13em!important}
 .layout{grid-template-columns:280px minmax(0,1fr) 318px!important;min-height:calc(100vh - 74px)!important}
 .sidebar{top:74px!important;height:calc(100vh - 74px)!important;padding:18px 15px!important}
 .main{padding:16px 18px 30px!important}
 #ux-v5-rail{display:grid!important;position:sticky!important;top:74px!important;height:calc(100vh - 74px)!important;z-index:100!important}
 .nav{position:sticky!important;top:6px!important;z-index:200!important}
 .hero-card:first-child{padding:20px 22px!important;min-height:180px!important}
 .hero-card:first-child h1{font-size:clamp(32px,3.2vw,48px)!important}
 .hero-card:first-child p{font-size:10px!important;max-width:820px!important}
 .kpis{gap:8px!important}.kpi{min-height:82px!important;padding:12px!important}
 .dashboard{gap:12px!important}.card{padding:13px!important}
 .map{height:min(60vh,620px)!important;min-height:440px!important}
 #spatial-studio{margin-top:12px!important}
 @media(max-width:1050px){.layout{grid-template-columns:250px minmax(0,1fr)!important}#ux-v5-rail{position:relative!important;top:auto!important;height:auto!important;border-left:0!important;border-top:1px solid var(--ux5-line)!important}.main{grid-column:2}.sidebar{grid-row:1 / span 2}}
 @media(max-width:760px){.layout{display:block!important}.sidebar{position:relative!important;top:auto!important;height:auto!important}.main{padding:12px!important}.header{padding:0 14px!important}.header .logo{flex-basis:155px!important;width:155px!important}.health{display:none!important}.map{min-height:360px!important;height:55vh!important}}
 `;document.head.appendChild(s)
}
function boot(){css();removeLegacy();brand();let n=0;const timer=setInterval(()=>{removeLegacy();brand();if(++n>40)clearInterval(timer)},250);new MutationObserver(()=>{removeLegacy();brand()}).observe(document.body,{childList:true,subtree:true});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
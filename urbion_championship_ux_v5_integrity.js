(()=>{'use strict';if(window.__URBION_UX_V5_INTEGRITY)return;window.__URBION_UX_V5_INTEGRITY=true;const $=s=>document.querySelector(s);const $$=s=>Array.from(document.querySelectorAll(s));
function reconcile(){
 const legacy=['urbion-decision-os','urbion-workstation-v2','urbion-theme-toggle'];
 legacy.forEach(id=>document.getElementById(id)?.remove());
 document.getElementById('urbion-chrome')?.remove();
 document.getElementById('ux-footer')?.remove();
 $$('body *').forEach(el=>{if(el===document.body||el.id==='ux-v5-rail'||el.id==='ux5-menu'||el.closest('#ux-v5-rail')||el.closest('#ux5-menu'))return;const t=(el.textContent||'').trim();if(t==='PLANNER HANDOFF'&&el.children.length===0)el.remove()});
 const logo=$('.header .logo');
 if(logo){logo.textContent='';logo.setAttribute('aria-label','URBION HORIZON');logo.style.cssText+=';width:190px!important;height:48px!important;border:0!important;border-radius:0!important;background:transparent url(/urbion_logo_dark.svg) left center/contain no-repeat!important;color:transparent!important;';if(!logo.dataset.urbionTheme){logo.dataset.urbionTheme='1';new MutationObserver(()=>{logo.style.backgroundImage=document.body.classList.contains('urbion-light')?'url(/urbion_logo_light.svg)':'url(/urbion_logo_dark.svg)'}).observe(document.body,{attributes:true,attributeFilter:['class']})}}
 if(!document.getElementById('urbion-final-integrity-style')){const s=document.createElement('style');s.id='urbion-final-integrity-style';s.textContent=`
 #urbion-decision-os,#urbion-workstation-v2,#urbion-theme-toggle,#ux-footer{display:none!important}
 body{overflow-x:hidden!important}
 .header{height:74px!important;padding:0 24px!important;background:rgba(4,13,21,.94)!important;backdrop-filter:blur(20px)!important;z-index:5000!important}
 .header .logo{flex:0 0 190px!important}
 #ux5-tools{display:flex!important;align-items:center!important;gap:5px!important}
 #ux5-tools button{width:32px!important;height:30px!important;border:1px solid #234151!important;border-radius:8px!important;background:#081722!important;color:#9db4c0!important;font-size:8px!important;font-weight:900!important}
 #ux5-tools button:hover{border-color:#5ee7c2!important;color:#5ee7c2!important}
 .layout{grid-template-columns:280px minmax(0,1fr) 318px!important;min-height:calc(100vh - 74px)!important}
 .sidebar{top:74px!important;height:calc(100vh - 74px)!important;padding:18px 15px!important}
 .main{padding:16px 18px 30px!important;min-width:0!important}
 #ux-v5-rail{display:grid!important;position:sticky!important;top:74px!important;height:calc(100vh - 74px)!important;z-index:100!important}
 .nav{position:sticky!important;top:6px!important;z-index:200!important}
 .hero{grid-template-columns:minmax(0,1fr)!important;gap:10px!important}
 .hero-card:first-child{padding:20px 22px!important;min-height:180px!important}
 .hero-card:first-child h1{font-size:clamp(32px,3.2vw,48px)!important}
 .hero-card:first-child p{font-size:10px!important;max-width:820px!important}
 .hero-card.hero-side{display:none!important}
 .kpis{gap:8px!important}.kpi{min-height:82px!important;padding:12px!important}
 .dashboard{gap:12px!important}.card{padding:13px!important}
 .map{height:min(60vh,620px)!important;min-height:440px!important}
 @media(max-width:1050px){.layout{grid-template-columns:250px minmax(0,1fr)!important}#ux-v5-rail{position:relative!important;top:auto!important;height:auto!important;border-left:0!important;border-top:1px solid var(--ux5-line)!important}.main{grid-column:2}.sidebar{grid-row:1 / span 2}}
 @media(max-width:760px){.layout{display:block!important}.sidebar{position:relative!important;top:auto!important;height:auto!important}.main{padding:12px!important}.header{padding:0 14px!important}.header .logo{flex-basis:155px!important;width:155px!important}.health{display:none!important}.map{min-height:360px!important;height:55vh!important}}
 `;document.head.appendChild(s)}}
function boot(){reconcile();let n=0;const timer=setInterval(()=>{reconcile();if(++n>48)clearInterval(timer)},250);new MutationObserver(()=>reconcile()).observe(document.body,{childList:true,subtree:true})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
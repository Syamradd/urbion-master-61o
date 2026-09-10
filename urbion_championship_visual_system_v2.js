(()=>{
'use strict';
if(window.__URBION_VISUAL_SYSTEM_V2__) return;
window.__URBION_VISUAL_SYSTEM_V2__=true;
const style=document.createElement('style');
style.id='urbion-visual-system-v2';
style.textContent=`
:root{--v2-cyan:#43e7ee;--v2-mint:#61efc6;--v2-blue:#62a9ff;--v2-violet:#9a7cff;--v2-line:rgba(83,209,224,.18);--v2-text:#effbff;--v2-body:#bfd3db;--v2-muted:#7f9eab}
html{scroll-behavior:smooth!important}
body.horizon-ui{overflow-x:hidden!important;background:radial-gradient(1100px 650px at 74% -8%,rgba(42,203,235,.13),transparent 62%),radial-gradient(900px 620px at 8% 88%,rgba(44,221,193,.08),transparent 60%),#020b13!important}
body.horizon-ui .app-shell{max-width:1740px!important;padding:0 22px 34px!important}
body.horizon-ui .workstation{grid-template-columns:minmax(300px,345px) minmax(0,1fr) minmax(380px,420px)!important;gap:16px!important;align-items:stretch!important;min-height:0!important}
body.horizon-ui .case-panel{height:calc(100vh - 290px)!important;min-height:560px!important;max-height:840px!important;overflow-y:auto!important;overflow-x:hidden!important;scroll-behavior:smooth!important;scrollbar-width:thin!important;scrollbar-color:rgba(73,210,222,.46) transparent!important}
body.horizon-ui .map-panel-canonical{height:100%!important;min-height:560px!important;display:flex!important;flex-direction:column!important;min-width:0!important}
body.horizon-ui .map-stage{flex:1 1 auto!important;height:auto!important;min-height:520px!important;max-height:none!important}
body.horizon-ui .intel-panel{height:calc(100vh - 290px)!important;max-height:840px!important;min-height:560px!important;overflow-y:auto!important;overflow-x:hidden!important;scroll-behavior:smooth!important;scrollbar-width:thin!important;scrollbar-color:rgba(73,210,222,.46) transparent!important;padding-right:3px!important}
body.horizon-ui .intel-card{padding:18px!important;border-radius:18px!important}
body.horizon-ui .intel-card .eyebrow{font-size:10px!important;letter-spacing:.15em!important}
body.horizon-ui .intel-card .muted,body.horizon-ui .intel-card p{font-size:11px!important;line-height:1.6!important}
body.horizon-ui .card-row{min-height:42px!important}
body.horizon-ui .card-row>b{font-size:23px!important;line-height:1.05!important}
body.horizon-ui .readiness-main{grid-template-columns:118px minmax(0,1fr)!important;gap:16px!important}
body.horizon-ui .readiness-main strong{font-size:64px!important;line-height:.88!important;letter-spacing:-.05em!important}
body.horizon-ui .readiness-main b{font-size:14px!important}
body.horizon-ui .readiness-main p{font-size:10px!important;line-height:1.55!important}
body.horizon-ui .metrics span{font-size:10px!important;color:#89a7b4!important}.metrics b{font-size:10px!important}
body.horizon-ui .site-summary b{font-size:22px!important}.site-summary span{font-size:10px!important}
body.horizon-ui .signals div{font-size:10px!important;line-height:1.35!important;padding:10px 0!important}.signals b{font-size:9px!important}
body.horizon-ui .next-card h3{font-size:20px!important}.next-card p{font-size:10px!important}
body.horizon-ui .tool-grid{grid-template-columns:1fr 1fr!important}.tool-grid button{font-size:9px!important;min-height:42px!important}
body.horizon-ui .tool-result{font-size:10px!important;line-height:1.55!important}
body.horizon-ui .case-panel .case-body{padding-bottom:22px!important}
body.horizon-ui .case-panel .field>span{font-size:8.5px!important;letter-spacing:.13em!important;margin-bottom:5px!important}
body.horizon-ui .case-panel .field input,body.horizon-ui .case-panel .field select,body.horizon-ui .case-panel .field textarea{font-size:12.5px!important;min-height:40px!important;height:40px!important;padding:8px 11px!important}
body.horizon-ui .case-panel .case-body summary{font-size:9px!important;letter-spacing:.10em!important;min-height:38px!important}
body.horizon-ui .case-panel .panel-title h2{font-size:18px!important}.case-panel .panel-title p{font-size:10px!important}
body.horizon-ui .workspace-head{margin-bottom:2px!important}
body.horizon-ui .workspace-head:after{content:"01 CASE  ›  02 SPATIAL EVIDENCE  ›  03 ASSESS  ›  04 WHAT-IF  ›  05 DECIDE  ›  06 OUTPUT";display:block;margin-top:13px;color:#64838f;font:800 8px/1.2 Inter,sans-serif;letter-spacing:.10em;opacity:.9}
body.horizon-ui .workspace-head h1{font-size:clamp(40px,3.4vw,58px)!important;line-height:1.08!important;height:auto!important;min-height:0!important;overflow:visible!important}
body.horizon-ui .workspace-head p{font-size:12px!important;line-height:1.55!important}
body.horizon-ui .workspace-actions .primary{min-height:44px!important;font-size:11px!important}
body.horizon-ui .map-toolbar{min-height:76px!important}.map-toolbar h2{font-size:17px!important}.map-toolbar .eyebrow{font-size:10px!important}
body.horizon-ui .map-search{width:min(310px,42%)!important}.map-search input{font-size:10px!important}
body.horizon-ui #cs-layer-drawer{width:min(385px,42%)!important;top:12px!important;right:12px!important;bottom:12px!important;height:auto!important;max-height:none!important;overflow:hidden!important;box-shadow:0 30px 90px rgba(0,0,0,.62),0 0 34px rgba(63,214,225,.07)!important}
body.horizon-ui #cs-layer-drawer .layers-head{padding:14px 14px!important}.layers-head h3{font-size:14px!important}.layers-head p{font-size:9px!important}
body.horizon-ui #cs-layer-drawer .layer-list,body.horizon-ui #cs-layer-drawer .layers-list,body.horizon-ui #cs-layer-drawer .drawer-body,body.horizon-ui #cs-layer-drawer .layer-drawer-body,body.horizon-ui #cs-layer-drawer .layer-drawer-content,body.horizon-ui #cs-layer-drawer .drawer-content{overflow-y:auto!important;min-height:0!important;flex:1 1 auto!important;padding-bottom:10px!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row{min-height:47px!important;grid-template-columns:18px minmax(0,1fr) 58px!important;font-size:11px!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row span{font-size:11px!important}.fcc-layer-row small{font-size:9px!important}
body.horizon-ui #cs-layer-drawer .group-toggle{font-size:10px!important;min-height:42px!important}
body.horizon-ui .card,.body.horizon-ui .panel,body.horizon-ui .hero-card{transition:transform .18s ease,box-shadow .24s ease,border-color .24s ease!important}
body.horizon-ui .card:hover,body.horizon-ui .hero-card:hover{transform:translateY(-1px)!important;box-shadow:0 24px 58px rgba(0,0,0,.34),0 0 24px rgba(57,214,225,.04)!important;border-color:rgba(76,211,225,.28)!important}
body.horizon-ui .btn,body.horizon-ui button{transition:transform .16s ease,box-shadow .20s ease,border-color .20s ease,background .20s ease!important}
body.horizon-ui .kpi,body.horizon-ui .metric-box{background:linear-gradient(145deg,rgba(8,29,43,.92),rgba(3,14,23,.96))!important;border-color:rgba(74,199,216,.16)!important}
body.horizon-ui .kpi strong,body.horizon-ui .metric-box b{font-variant-numeric:tabular-nums!important}
/* Deduplicate visually identical layer controls without changing the underlying data/engine. */
body.horizon-ui #cs-layer-drawer .fcc-layer-row[data-v2-duplicate="true"]{display:none!important}
@media(max-width:1340px){body.horizon-ui .workstation{grid-template-columns:minmax(285px,315px) minmax(0,1fr) minmax(340px,370px)!important}}
@media(max-width:1120px){body.horizon-ui .workstation{grid-template-columns:1fr!important;align-items:start!important}.case-panel,.intel-panel{height:auto!important;max-height:none!important;min-height:0!important;overflow:visible!important}.map-panel-canonical{height:auto!important}.map-stage{height:600px!important;min-height:520px!important}.intel-panel{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important}.intel-head{grid-column:1/-1!important}.tool-card{grid-column:1/-1!important}}
@media(max-width:760px){body.horizon-ui .app-shell{padding:0 12px 22px!important}.workspace-head:after{white-space:normal!important;line-height:1.5!important}.workstation{display:block!important}.case-panel,.map-panel-canonical,.intel-panel{margin-bottom:12px!important}.intel-panel{display:block!important}.map-stage{height:540px!important;min-height:0!important}.map-search{width:calc(100% - 28px)!important}.map-tabs{flex-wrap:wrap!important}.base-tab{font-size:8px!important}.case-panel .field input,.case-panel .field select,.case-panel .field textarea{font-size:12px!important}.case-panel .panel-title h2{font-size:17px!important}.readiness-main{grid-template-columns:92px 1fr!important}.readiness-main strong{font-size:52px!important}body.horizon-ui #cs-layer-drawer{left:10px!important;right:10px!important;top:auto!important;bottom:10px!important;width:auto!important;height:min(66vh,460px)!important;max-height:460px!important}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}*,*::before,*::after{animation:none!important;transition:none!important}}
`;
document.head.appendChild(style);
function dedupeLayers(){const d=document.querySelector('#cs-layer-drawer');if(!d)return;const seen=new Set();d.querySelectorAll('.fcc-layer-row').forEach(row=>{const id=row.getAttribute('data-layer')||row.querySelector('input[data-layer]')?.getAttribute('data-layer')||'';if(!id)return;if(seen.has(id))row.setAttribute('data-v2-duplicate','true');else{row.removeAttribute('data-v2-duplicate');seen.add(id);}})}
function normalize(){const m=document.querySelector('.map-stage');if(m&&m.offsetHeight>1000)m.style.maxHeight='700px';dedupeLayers();}
normalize();
new MutationObserver(normalize).observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class','aria-hidden']});
})();

(()=>{
'use strict';
if(window.__URBION_HORIZON_UI__)return;
window.__URBION_HORIZON_UI__=true;

const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>Array.from(r.querySelectorAll(s));

const NAV=[
  ['command','01','Gambaran Keseluruhan','Command Centre','⌂'],
  ['evidence','02','Kecerdasan Tapak','Site Intelligence','⌖'],
  ['scenarios','03','Bagaimana Jika','What-If Studio','◈'],
  ['decision','04','Pusat Keputusan','Decision Centre','✓'],
  ['judge','05','Mod Penilai','Judge View','◆']
];

const STYLE=`
:root{
  --h-bg:#03101a;--h-bg2:#061a29;--h-panel:rgba(7,24,36,.88);--h-panel2:rgba(10,31,47,.92);
  --h-line:rgba(91,212,226,.20);--h-line-strong:rgba(73,220,232,.46);
  --h-text:#effaff;--h-muted:#8ea8b8;--h-blue:#38a9ff;--h-cyan:#26d9e7;--h-mint:#51e0bd;
  --h-violet:#9c83ff;--h-amber:#ffc857;--h-red:#ff727d;--h-shadow:0 24px 70px rgba(0,0,0,.38);
}
html{background:var(--h-bg)}
body.horizon-ui{background:radial-gradient(1000px 550px at 72% 0%,rgba(39,168,255,.16),transparent 64%),radial-gradient(850px 520px at 16% 76%,rgba(42,224,191,.10),transparent 64%),linear-gradient(180deg,#03101a 0%,#061827 50%,#03101a 100%)!important;color:var(--h-text)!important;overflow-x:hidden}
body.horizon-ui:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background-image:linear-gradient(rgba(79,196,229,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(79,196,229,.035) 1px,transparent 1px);background-size:64px 64px;mask-image:linear-gradient(to bottom,rgba(0,0,0,.85),transparent 84%)}
#urbion-horizon-visual{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
#urbion-horizon-visual .horizon-sky{position:absolute;inset:-10%;background:radial-gradient(ellipse at 70% 8%,rgba(57,191,255,.22),transparent 30%),radial-gradient(ellipse at 25% 20%,rgba(47,125,255,.13),transparent 28%),linear-gradient(180deg,rgba(4,22,35,.1),rgba(3,13,23,.84))}
#urbion-horizon-visual .horizon-stars{position:absolute;inset:0;opacity:.72}
.h-star{position:absolute;width:2px;height:2px;border-radius:50%;background:rgba(204,246,255,.78);box-shadow:0 0 9px rgba(76,211,255,.48)}
#urbion-horizon-visual .h-city{position:absolute;left:0;right:0;bottom:-2px;height:28%;display:flex;align-items:flex-end;gap:3px;padding:0 2%;opacity:.46;background:linear-gradient(180deg,transparent,rgba(2,10,17,.75) 46%,rgba(2,8,14,.98))}
.h-building{flex:1;max-width:74px;min-width:8px;height:var(--bh,42%);border:1px solid rgba(93,208,232,.10);background:linear-gradient(180deg,rgba(27,73,96,.38),rgba(2,10,17,.96));clip-path:polygon(8% 0,92% 0,100% 100%,0 100%)}
.h-building:nth-child(2n){--bh:68%}.h-building:nth-child(3n){--bh:36%}.h-building:nth-child(5n){--bh:82%}
#urbion-horizon-visual .h-floor{position:absolute;left:-10%;right:-10%;bottom:-24%;height:58%;opacity:.15;background-image:linear-gradient(rgba(79,224,207,.32) 1px,transparent 1px),linear-gradient(90deg,rgba(79,224,207,.32) 1px,transparent 1px);background-size:46px 46px;transform:perspective(520px) rotateX(61deg);transform-origin:center bottom}
#urbion-horizon-visual .h-orbit{position:absolute;border:1px solid rgba(85,218,231,.13);border-radius:50%;box-shadow:0 0 38px rgba(32,188,255,.06)}
.h-orbit-a{width:520px;height:190px;right:-160px;top:14%;transform:rotate(-18deg)}.h-orbit-b{width:380px;height:140px;left:-180px;top:28%;transform:rotate(17deg)}
body.horizon-ui>*:not(#urbion-horizon-visual){position:relative;z-index:1}
body.horizon-ui .header,body.horizon-ui .topbar,body.horizon-ui .main-nav{backdrop-filter:blur(18px)!important;background:rgba(3,15,24,.84)!important;border-color:var(--h-line)!important}
body.horizon-ui .header{box-shadow:0 12px 40px rgba(0,0,0,.24)}
body.horizon-ui .nav{display:flex;gap:9px;align-items:stretch;overflow:auto;padding:7px 3px 10px;margin-bottom:14px;border-bottom:1px solid rgba(88,206,226,.08)}
body.horizon-ui .nav button{display:grid;grid-template-columns:auto auto 1fr auto;align-items:center;gap:8px;min-height:54px;padding:9px 12px;border:1px solid rgba(74,171,203,.20)!important;border-radius:13px!important;background:linear-gradient(145deg,rgba(8,27,41,.92),rgba(4,17,28,.86))!important;color:#9db4c0!important;box-shadow:0 8px 22px rgba(0,0,0,.16)!important;font-size:11px!important;font-weight:800!important;letter-spacing:.02em!important;transition:transform .18s,border-color .18s,box-shadow .18s,color .18s,background .18s;flex:0 0 auto}
body.horizon-ui .nav button:hover{transform:translateY(-2px);color:#eefaff!important;border-color:rgba(65,213,231,.48)!important;box-shadow:0 14px 28px rgba(4,18,28,.45),0 0 24px rgba(45,196,231,.10)!important}
body.horizon-ui .nav button.active{background:linear-gradient(135deg,rgba(25,130,180,.34),rgba(44,225,199,.18))!important;border-color:rgba(61,224,231,.75)!important;color:#f3ffff!important;box-shadow:0 14px 35px rgba(23,171,208,.16),inset 0 0 0 1px rgba(255,255,255,.04)!important}
body.horizon-ui .nav button .h-nav-num{font:900 10px Inter;color:#5da9c4;letter-spacing:.12em}.h-nav-icon{font-size:14px;color:var(--h-cyan);filter:drop-shadow(0 0 8px rgba(38,217,231,.28))}.h-nav-copy{display:flex;flex-direction:column;align-items:flex-start;min-width:max-content}.h-nav-copy b{font-size:11px}.h-nav-copy small{margin-top:2px;color:#6f8999;font-size:8px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}.h-nav-arrow{font-size:13px;color:#55798c;transition:transform .18s}.nav button:hover .h-nav-arrow{transform:translateX(2px);color:#9eeff2}
body.horizon-ui .hero-card,body.horizon-ui .card{background:linear-gradient(145deg,rgba(10,31,47,.92),rgba(4,16,27,.94))!important;border-color:var(--h-line)!important;box-shadow:var(--h-shadow)!important}
body.horizon-ui .hero-card{overflow:hidden}
body.horizon-ui .hero-card:before{content:"";position:absolute;right:-10%;top:-40%;width:60%;height:160%;background:radial-gradient(circle,rgba(44,197,236,.09),transparent 63%);transform:rotate(25deg);pointer-events:none}
body.horizon-ui .hero h1{font-size:clamp(44px,5.2vw,68px)!important;letter-spacing:-.055em!important;text-shadow:0 8px 30px rgba(0,0,0,.28)}
body.horizon-ui .hero p{font-size:13px!important;line-height:1.75!important;max-width:800px!important}
body.horizon-ui .eyebrow{font-size:9px!important;letter-spacing:.20em!important}
body.horizon-ui .card h2{font-size:20px!important}.card h3{font-size:15px!important}
body.horizon-ui .muted,.hero p,.site-meta{font-size:10px!important;line-height:1.65!important}
body.horizon-ui .kpi strong{font-size:25px!important}.kpi label{font-size:8px!important}
body.horizon-ui .btn{padding:11px 14px!important;border-radius:11px!important;font-size:10px!important;box-shadow:0 10px 24px rgba(0,0,0,.18)}
body.horizon-ui .btn.primary{background:linear-gradient(135deg,#2fd7e5,#47dfbd)!important;color:#03131a!important;border-color:transparent!important;box-shadow:0 12px 30px rgba(32,214,209,.20)!important}
body.horizon-ui input,body.horizon-ui select{font-size:11px!important;padding:11px 12px!important;border-radius:10px!important;background:rgba(4,19,29,.84)!important;border-color:rgba(81,177,205,.24)!important}
body.horizon-ui .label{font-size:8px!important;color:#7ea2b4!important}
body.horizon-ui .sidebar{background:rgba(4,18,28,.76)!important;border-color:var(--h-line)!important;box-shadow:20px 0 50px rgba(0,0,0,.12)}
body.horizon-ui .run{font-size:11px!important;padding:13px!important;background:linear-gradient(135deg,#32d7e4,#4ce0bb)!important;box-shadow:0 12px 26px rgba(41,213,207,.16)}
body.horizon-ui .reset{font-size:10px!important;padding:11px!important}

/* MAP / LAYER DRAWER FIX */
body.horizon-ui .map-panel{position:relative!important;overflow:hidden!important;border-radius:20px!important;border:1px solid var(--h-line-strong)!important;box-shadow:0 24px 60px rgba(0,0,0,.34)!important;background:rgba(4,16,25,.94)!important}
body.horizon-ui .map-panel .leaflet-container{height:100%!important;min-height:520px!important;background:#061d2a!important}
body.horizon-ui #cs-layer-drawer{position:absolute!important;top:14px!important;right:14px!important;bottom:14px!important;width:min(360px,40%)!important;max-width:calc(100% - 28px)!important;height:auto!important;max-height:none!important;display:flex!important;flex-direction:column!important;overflow:hidden!important;z-index:1400!important;border:1px solid rgba(82,211,226,.28)!important;border-radius:18px!important;background:linear-gradient(180deg,rgba(4,18,29,.94),rgba(3,12,21,.97))!important;box-shadow:0 22px 55px rgba(0,0,0,.42),0 0 34px rgba(38,197,229,.07)!important;backdrop-filter:blur(16px)!important}
body.horizon-ui #cs-layer-drawer .layer-drawer-header,body.horizon-ui #cs-layer-drawer .drawer-header,body.horizon-ui #cs-layer-drawer > .layer-head{flex:0 0 auto}
body.horizon-ui #cs-layer-drawer .layer-group{overflow:hidden!important;border-color:rgba(74,162,188,.20)!important;background:rgba(6,22,33,.72)!important;border-radius:12px!important}
body.horizon-ui #cs-layer-drawer .group-toggle{font-size:10px!important;padding:10px!important;min-height:38px!important;background:linear-gradient(90deg,rgba(12,36,51,.88),rgba(7,22,34,.92))!important;color:#d9eef3!important}
body.horizon-ui #cs-layer-drawer .group-body{overflow:visible!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row{min-height:47px!important;padding:8px 10px!important;border-color:rgba(67,141,164,.16)!important;background:rgba(5,18,28,.72)!important;color:#d9eef3!important;font-size:10px!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row span{font-size:10px!important;line-height:1.2!important}.fcc-layer-row small{font-size:8px!important}
body.horizon-ui #cs-layer-drawer .layer-opacity{height:18px!important}
body.horizon-ui #cs-layer-drawer .legend-inline,body.horizon-ui #urbion-map-legend{font-size:9px!important}
body.horizon-ui #cs-layer-drawer{scrollbar-width:thin;scrollbar-color:rgba(76,204,224,.55) rgba(255,255,255,.04)}
body.horizon-ui #cs-layer-drawer::-webkit-scrollbar{width:8px}body.horizon-ui #cs-layer-drawer::-webkit-scrollbar-thumb{background:rgba(76,204,224,.48);border-radius:999px}
body.horizon-ui .leaflet-bottom{z-index:900!important}.leaflet-control-attribution{font-size:9px!important;background:rgba(4,14,22,.76)!important;color:#9ab2be!important;border-radius:7px 0 0 0;padding:4px 7px!important}.leaflet-control-attribution a{color:#72d4e4!important}
body.horizon-ui .uo-layer-row{min-height:46px!important;font-size:10px!important}

/* contextual status bar */
#horizon-status{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 13px;margin:0 0 12px;border:1px solid rgba(80,198,219,.20);border-radius:14px;background:linear-gradient(90deg,rgba(30,174,213,.10),rgba(54,218,194,.04));box-shadow:0 10px 25px rgba(0,0,0,.18)}
#horizon-status .live{display:flex;align-items:center;gap:8px;color:#79efe0;font-size:9px;font-weight:900;letter-spacing:.09em;text-transform:uppercase}.h-dot{width:7px;height:7px;border-radius:50%;background:#51e0bd;box-shadow:0 0 14px #51e0bd}
#horizon-status .hint{color:#7893a2;font-size:9px}

/* floating map HUD, without covering map footer */
#horizon-map-hud{position:absolute;left:14px;top:14px;z-index:1300;display:flex;gap:7px;flex-wrap:wrap;max-width:54%;pointer-events:none}.h-hud{padding:7px 9px;border:1px solid rgba(66,206,224,.22);border-radius:999px;background:rgba(3,17,27,.84);backdrop-filter:blur(10px);color:#dffaff;font-size:8px;font-weight:900;letter-spacing:.04em;box-shadow:0 8px 20px rgba(0,0,0,.18)}.h-hud b{color:#56e1db}

/* visual mode tags */
body.horizon-ui .fcc-layer-row.is-on{background:linear-gradient(90deg,rgba(44,192,210,.12),rgba(8,25,38,.80))!important;box-shadow:inset 2px 0 0 #4bded0}
body.horizon-ui .fcc-layer-row[data-live-recovered="1"]{box-shadow:inset 2px 0 0 #51e0bd,0 0 16px rgba(81,224,189,.05)!important}
body.horizon-ui .fcc-layer-row[data-source-error="1"]{box-shadow:inset 2px 0 0 #ff727d!important}

@media(max-width:1050px){body.horizon-ui #cs-layer-drawer{width:min(330px,46%)!important}}
@media(max-width:780px){body.horizon-ui #cs-layer-drawer{left:12px!important;right:12px!important;width:auto!important;top:auto!important;bottom:12px!important;height:min(52%,390px)!important}.horizon-ui .nav button{min-height:48px}}
`;

function addStyle(){if($('#horizon-ui-style'))return;const s=document.createElement('style');s.id='horizon-ui-style';s.textContent=STYLE;document.head.appendChild(s)}
function addVisual(){if($('#urbion-horizon-visual'))return;const v=document.createElement('div');v.id='urbion-horizon-visual';const stars=Array.from({length:70},(_,i)=>{const x=(i*37)%100,y=(i*61+11)%70,size=i%8===0?3:2;return `<i class="h-star" style="left:${x}%;top:${y}%;width:${size}px;height:${size}px;opacity:${(.28+(i%7)*.09).toFixed(2)}"></i>`}).join('');const buildings=Array.from({length:22},()=>'<i class="h-building"></i>').join('');v.innerHTML=`<div class="horizon-sky"></div><div class="horizon-stars">${stars}</div><div class="h-orbit h-orbit-a"></div><div class="h-orbit h-orbit-b"></div><div class="h-floor"></div><div class="h-city">${buildings}</div>`;document.body.insertBefore(v,document.body.firstChild)}
function enhanceNav(){
  const nav=$('#nav');if(nav){$$('button',nav).forEach(btn=>{if(btn.dataset.horizonNav)return;const view=btn.dataset.view||'';const meta=NAV.find(x=>x[0]===view);if(!meta)return;btn.dataset.horizonNav='1';btn.innerHTML=`<span class="h-nav-num">${meta[1]}</span><span class="h-nav-icon">${meta[4]}</span><span class="h-nav-copy"><b>${meta[2]}</b><small>${meta[3]}</small></span><span class="h-nav-arrow">→</span>`;});}
  $$('.main-nav a,.main-nav button,.top-nav a,.top-nav button').forEach(el=>{el.classList.add('horizon-nav-item')});
}
function addStatus(){if($('#horizon-status'))return;const nav=$('#nav');if(!nav)return;const e=document.createElement('div');e.id='horizon-status';e.innerHTML='<div class="live"><span class="h-dot"></span> LIVE SPATIAL PLANNING</div><div class="hint">Evidence-aware · source-aware · planner in the loop</div>';nav.insertAdjacentElement('afterend',e)}
function fixLayerDrawer(){const d=$('#cs-layer-drawer');const map=d?.closest('.map-panel');if(!d||!map)return;map.style.position='relative';map.style.overflow='hidden';d.style.position='absolute';d.style.top='14px';d.style.right='14px';d.style.bottom='14px';d.style.width='min(360px,40%)';d.style.maxHeight='none';d.style.height='auto';d.style.display='flex';d.style.flexDirection='column';d.style.overflow='auto';d.style.zIndex='1400';const scrollables=d.querySelectorAll('.layer-list,.layers-list,.drawer-body,.layer-drawer-body,.layer-drawer-content,.drawer-content');scrollables.forEach(e=>{e.style.overflowY='auto';e.style.minHeight='0';e.style.flex='1 1 auto'});}
function addMapHud(){const map=$('.map-panel');if(!map||$('#horizon-map-hud'))return;const h=document.createElement('div');h.id='horizon-map-hud';h.innerHTML='<span class="h-hud">SPATIAL ENGINE <b>ONLINE</b></span><span class="h-hud">EVIDENCE <b>LIVE</b></span><span class="h-hud">MAP <b>INTERACTIVE</b></span>';map.appendChild(h)}
function observe(){const root=$('#urbion-championship-shell');if(!root)return;const mo=new MutationObserver(()=>{enhanceNav();fixLayerDrawer();addMapHud()});mo.observe(root,{subtree:true,childList:true});setInterval(()=>{enhanceNav();fixLayerDrawer();},1500)}
function boot(){
  document.body.classList.add('horizon-ui');
  addStyle();addVisual();enhanceNav();addStatus();fixLayerDrawer();addMapHud();observe();
  window.addEventListener('resize',fixLayerDrawer,{passive:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

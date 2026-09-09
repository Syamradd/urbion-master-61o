(()=>{
'use strict';
if(window.__URBION_HORIZON_UI__)return;
window.__URBION_HORIZON_UI__=true;

const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>Array.from(r.querySelectorAll(s));

const NAV_COPY={
  command:['01','Command Centre','Overview & Workflow','⌂','Pusat Kawalan','Gambaran Keseluruhan & Aliran Kerja'],
  evidence:['02','Site Intelligence','Spatial Analysis & Evidence','⌖','Kecerdasan Tapak','Analisis Ruang & Bukti'],
  ai:['03','AI Assessment','Planning Evaluation','◈','Penilaian AI','Penilaian Perancangan'],
  scenarios:['04','What-If Studio','Scenario Comparison','↗','Studio What-If','Perbandingan Senario'],
  decision:['05','Decision Centre','Decision & Compliance','✓','Pusat Keputusan','Keputusan & Pematuhan'],
  lcp:['06','LCP Intelligence','Submission & Documentation','▤','Kecerdasan LCP','Penyerahan & Dokumentasi'],
  judge:['06','Judge View','Evaluation Workspace','◆','Paparan Penilai','Ruang Kerja Penilaian']
};

const TEXT_PAIRS={
  'Gambaran Keseluruhan':'Overview','Overview':'Gambaran Keseluruhan',
  'Kecerdasan Tapak':'Site Intelligence','Site Intelligence':'Kecerdasan Tapak',
  'Penilaian AI':'AI Assessment','AI Assessment':'Penilaian AI',
  'Bagaimana Jika':'What-If Studio','What-If Studio':'Bagaimana Jika',
  'Pusat Keputusan':'Decision Centre','Decision Centre':'Pusat Keputusan',
  'Kecerdasan LCP':'LCP Intelligence','LCP Intelligence':'Kecerdasan LCP',
  'Mod Penilai':'Judge View','Judge View':'Mod Penilai',
  'New planning case':'Kes perancangan baharu',
  'Kes perancangan baharu':'New planning case',
  'Define planning case':'Takrif kes perancangan',
  'Takrif kes perancangan':'Define planning case',
  'Location':'Lokasi','Lokasi':'Location',
  'Site / Project Name':'Nama Tapak / Projek','Nama Tapak / Projek':'Site / Project Name',
  'State':'Negeri','Negeri':'State',
  'Local Authority (PBT)':'Pihak Berkuasa Tempatan (PBT)','Pihak Berkuasa Tempatan (PBT)':'Local Authority (PBT)',
  'District':'Daerah','Daerah':'District',
  'Site / Parcel':'Tapak / Lot','Tapak / Lot':'Site / Parcel',
  'Project Reference':'Rujukan Projek','Rujukan Projek':'Project Reference',
  'Development Proposal':'Cadangan Pemajuan','Cadangan Pemajuan':'Development Proposal',
  'Development Intensity':'Intensiti Pemajuan','Intensiti Pemajuan':'Development Intensity',
  'TOD / Transit Context':'Konteks TOD / Transit','Konteks TOD / Transit':'TOD / Transit Context',
  'Use Map Selection':'Gunakan Pilihan Peta','Gunakan Pilihan Peta':'Use Map Selection',
  'Locate Me':'Lokasi Saya','Lokasi Saya':'Locate Me',
  'Resolve Lot':'Selesaikan Lot','Selesaikan Lot':'Resolve Lot',
  'RUN SITE ANALYSIS':'JALANKAN ANALISIS TAPAK','JALANKAN ANALISIS TAPAK':'RUN SITE ANALYSIS',
  'Spatial Intelligence Map':'Peta Kecerdasan Ruang','Peta Kecerdasan Ruang':'Spatial Intelligence Map',
  'Explore spatial context, constraints and opportunities.':'Explore spatial context, constraints and opportunities.',
  'Planning Intelligence':'Kecerdasan Perancangan','Kecerdasan Perancangan':'Planning Intelligence',
  'Decision Readiness':'Kesediaan Keputusan','Kesediaan Keputusan':'Decision Readiness',
  'Key Insights':'Penemuan Utama','Penemuan Utama':'Key Insights',
  'Quick Actions':'Tindakan Pantas','Tindakan Pantas':'Quick Actions',
  'Evidence Health':'Kesihatan Bukti','Kesihatan Bukti':'Evidence Health',
  'MAP LAYERS':'LAPISAN PETA','LAPISAN PETA':'MAP LAYERS',
  'Official':'Rasmi','Rasmi':'Official',
  'Live':'Langsung','Langsung':'Live',
  'Analysis':'Analisis','Analisis':'Analysis',
  'Custom':'Tersuai','Tersuai':'Custom',
  'Planning':'Perancangan','Perancangan':'Planning',
  'Parcel':'Lot','Lot':'Parcel',
  'Transport':'Pengangkutan','Pengangkutan':'Transport',
  'Environment / Risk':'Alam Sekitar / Risiko','Alam Sekitar / Risiko':'Environment / Risk',
  'Terrain':'Bentuk Muka Bumi','Bentuk Muka Bumi':'Terrain',
  'Geology':'Geologi','Geologi':'Geology',
  'Hydrology':'Hidrologi','Hidrologi':'Hydrology',
  'Sources':'Sumber','Sumber':'Sources',
  'Print':'Cetak','Cetak':'Print',
  'Export':'Eksport','Eksport':'Export',
  'About':'Tentang','Tentang':'About',
  'Help':'Bantuan','Bantuan':'Help',
  'System Online':'Sistem Dalam Talian','Sistem Dalam Talian':'System Online'
};

const STYLE=`
:root{
  --uh-bg:#020b13;--uh-bg2:#061927;--uh-panel:rgba(5,20,31,.90);--uh-panel-2:rgba(8,29,43,.92);
  --uh-line:rgba(72,194,221,.20);--uh-line-2:rgba(55,218,225,.42);--uh-line-3:rgba(101,226,237,.68);
  --uh-text:#eefaff;--uh-body:#c5d7df;--uh-muted:#7e9aaa;--uh-dim:#55717f;
  --uh-cyan:#27d8e7;--uh-blue:#46a9ff;--uh-mint:#55e3bf;--uh-violet:#a48bff;--uh-amber:#ffc95b;--uh-red:#ff717d;
  --uh-radius:18px;--uh-shadow:0 24px 70px rgba(0,0,0,.34);
}
*,*::before,*::after{box-sizing:border-box}
html{background:var(--uh-bg)!important}
body.horizon-ui{
  margin:0!important;background:
  radial-gradient(1100px 600px at 74% -2%,rgba(35,163,255,.18),transparent 62%),
  radial-gradient(900px 560px at 12% 78%,rgba(36,223,196,.09),transparent 65%),
  linear-gradient(180deg,#020b13 0%,#051623 48%,#020b13 100%)!important;
  color:var(--uh-text)!important;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;
  overflow-x:hidden!important;
}
body.horizon-ui::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.72;
  background-image:linear-gradient(rgba(75,200,228,.038) 1px,transparent 1px),linear-gradient(90deg,rgba(75,200,228,.038) 1px,transparent 1px);
  background-size:52px 52px;mask-image:linear-gradient(to bottom,#000 0%,rgba(0,0,0,.92) 48%,transparent 96%);
}
body.horizon-ui>*.horizon-pro-stage~*{position:relative;z-index:2}
body.horizon-ui #urbion-championship-shell{position:relative;z-index:2}

/* PREMIUM ATMOSPHERE */
#horizon-pro-stage{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
#horizon-pro-stage .pro-sky{position:absolute;inset:-10%;background:
 radial-gradient(ellipse 520px 220px at 77% 8%,rgba(54,211,255,.24),transparent 72%),
 radial-gradient(ellipse 420px 180px at 35% 16%,rgba(60,107,255,.11),transparent 72%),
 radial-gradient(ellipse 680px 260px at 50% 100%,rgba(24,205,187,.07),transparent 70%)}
#horizon-pro-stage .pro-stars{position:absolute;inset:0;opacity:.74}
.pro-star{position:absolute;width:2px;height:2px;border-radius:50%;background:rgba(205,246,255,.76);box-shadow:0 0 10px rgba(68,208,255,.48)}
#horizon-pro-stage .pro-horizon-glow{position:absolute;left:0;right:0;bottom:20%;height:3px;background:linear-gradient(90deg,transparent,rgba(52,212,226,.36),rgba(89,227,198,.46),transparent);box-shadow:0 0 34px rgba(45,213,226,.22)}
#horizon-pro-stage .pro-city{position:absolute;left:0;right:0;bottom:-1px;height:29%;display:flex;align-items:flex-end;gap:3px;padding:0 1.8%;opacity:.48;background:linear-gradient(180deg,transparent 0%,rgba(2,10,16,.70) 45%,rgba(2,8,14,.98) 100%)}
.pro-building{flex:1;min-width:7px;max-width:64px;height:var(--bh,42%);position:relative;border:1px solid rgba(73,204,226,.11);background:linear-gradient(180deg,rgba(17,62,84,.34),rgba(2,11,18,.98));clip-path:polygon(7% 0,93% 0,100% 100%,0 100%)}
.pro-building::after{content:"";position:absolute;inset:9% 18%;background:repeating-linear-gradient(180deg,rgba(107,228,240,.28) 0 2px,transparent 2px 11px);opacity:.32}
.pro-building:nth-child(2n){--bh:64%}.pro-building:nth-child(3n){--bh:38%}.pro-building:nth-child(5n){--bh:78%}.pro-building:nth-child(7n){--bh:54%}
#horizon-pro-stage .pro-floor{position:absolute;left:-12%;right:-12%;bottom:-28%;height:57%;opacity:.16;background-image:linear-gradient(rgba(69,215,208,.28) 1px,transparent 1px),linear-gradient(90deg,rgba(69,215,208,.28) 1px,transparent 1px);background-size:48px 48px;transform:perspective(620px) rotateX(60deg);transform-origin:center bottom}
.pro-orbit{position:absolute;border:1px solid rgba(64,210,232,.16);border-radius:50%;box-shadow:0 0 48px rgba(51,198,231,.07)}
.pro-orbit.a{width:650px;height:220px;right:-220px;top:13%;transform:rotate(-17deg)}
.pro-orbit.b{width:440px;height:160px;left:-260px;top:27%;transform:rotate(16deg)}
.pro-orbit::after{content:"";position:absolute;right:18%;top:12%;width:7px;height:7px;border-radius:50%;background:var(--uh-cyan);box-shadow:0 0 20px rgba(39,216,231,.9)}
#horizon-pro-stage .pro-scanline{position:absolute;inset:0;background:linear-gradient(180deg,transparent 0%,rgba(40,201,223,.025) 52%,transparent 55%);background-size:100% 8px;opacity:.22}

/* TOP HEADER */
body.horizon-ui .header,body.horizon-ui .topbar,body.horizon-ui .main-nav{
  background:rgba(2,13,21,.82)!important;border-color:rgba(74,196,219,.16)!important;backdrop-filter:blur(18px) saturate(130%)!important;
}
body.horizon-ui .header{box-shadow:0 12px 45px rgba(0,0,0,.22)!important}
body.horizon-ui .header *{min-width:0}
body.horizon-ui .header h1,body.horizon-ui .header h2{letter-spacing:-.03em!important}

/* NAVIGATION — clean, compact, readable */
body.horizon-ui #nav{display:flex!important;gap:8px!important;align-items:stretch!important;overflow-x:auto!important;overflow-y:visible!important;padding:8px 2px 10px!important;margin:0!important;border-bottom:1px solid rgba(75,200,222,.08)!important;scrollbar-width:none}
body.horizon-ui #nav::-webkit-scrollbar{display:none}
body.horizon-ui #nav button{
  display:grid!important;grid-template-columns:auto auto minmax(0,1fr)!important;align-items:center!important;gap:9px!important;
  min-height:58px!important;padding:8px 13px!important;flex:0 0 auto!important;border:1px solid rgba(68,165,196,.20)!important;border-radius:14px!important;
  background:linear-gradient(145deg,rgba(7,27,41,.94),rgba(3,15,25,.92))!important;color:#a7bbc5!important;
  box-shadow:0 8px 22px rgba(0,0,0,.16)!important;font:700 12px/1.15 Inter,sans-serif!important;letter-spacing:.01em!important;white-space:normal!important;
  transition:transform .18s,border-color .18s,background .18s,color .18s,box-shadow .18s!important;
}
body.horizon-ui #nav button:hover{transform:translateY(-2px)!important;color:#f2ffff!important;border-color:rgba(58,215,227,.55)!important;box-shadow:0 14px 28px rgba(4,20,31,.42),0 0 18px rgba(39,201,225,.08)!important}
body.horizon-ui #nav button.active,body.horizon-ui #nav button[aria-selected="true"]{
  color:#f7ffff!important;border-color:rgba(54,224,229,.86)!important;background:linear-gradient(135deg,rgba(22,112,153,.46),rgba(36,218,193,.22))!important;
  box-shadow:0 12px 32px rgba(27,189,214,.14),inset 0 0 0 1px rgba(255,255,255,.035),0 0 24px rgba(38,209,224,.10)!important;
}
.h-nav-num{font:900 10px/1 Inter,sans-serif;color:#5faac1;letter-spacing:.12em}.h-nav-icon{font-size:16px!important;line-height:1;color:var(--uh-cyan);filter:drop-shadow(0 0 8px rgba(39,216,231,.26))}.h-nav-copy{display:flex;flex-direction:column;align-items:flex-start;min-width:0!important}.h-nav-copy b{font:800 12px/1.15 Inter,sans-serif!important;white-space:normal!important}.h-nav-copy small{margin-top:4px;color:#6f8c9b;font:700 8px/1.15 Inter,sans-serif!important;letter-spacing:.04em;white-space:normal!important}.h-nav-arrow{display:none!important}

/* TYPOGRAPHIC SYSTEM */
body.horizon-ui h1,body.horizon-ui h2,body.horizon-ui h3,body.horizon-ui .hero h1,body.horizon-ui .card h2,body.horizon-ui .card h3{font-family:"Space Grotesk",Inter,system-ui,sans-serif!important;color:var(--uh-text)!important}
body.horizon-ui .hero h1{font-size:clamp(38px,4.1vw,56px)!important;line-height:1.02!important;letter-spacing:-.048em!important;max-width:980px!important;margin:0!important}
body.horizon-ui .hero p{font-size:14px!important;line-height:1.65!important;color:#98b1bd!important;max-width:760px!important}
body.horizon-ui .eyebrow{font-size:10px!important;line-height:1.2!important;letter-spacing:.17em!important;color:var(--uh-mint)!important;font-weight:900!important}
body.horizon-ui .card h2{font-size:21px!important;line-height:1.2!important;letter-spacing:-.02em!important}
body.horizon-ui .card h3{font-size:15px!important;line-height:1.3!important}
body.horizon-ui .muted,body.horizon-ui .site-meta{font-size:12px!important;line-height:1.55!important;color:var(--uh-muted)!important}
body.horizon-ui .label{font-size:10px!important;line-height:1.3!important;color:#8fb0bf!important;font-weight:800!important;letter-spacing:.04em!important}
body.horizon-ui .kpi strong{font-size:24px!important}.kpi label{font-size:10px!important}

/* WORKSTATION PANELS */
body.horizon-ui .hero-card,body.horizon-ui .card,body.horizon-ui .sidebar,body.horizon-ui .intel-card,body.horizon-ui .map-panel{
  background:linear-gradient(145deg,rgba(7,27,41,.94),rgba(3,14,24,.96))!important;
  border:1px solid rgba(72,194,221,.18)!important;border-radius:var(--uh-radius)!important;box-shadow:var(--uh-shadow)!important;
}
body.horizon-ui .hero-card{position:relative;overflow:visible!important}
body.horizon-ui .hero-card::after{content:"";position:absolute;right:4%;top:14%;width:240px;height:86px;border:1px solid rgba(59,209,229,.16);border-radius:50%;transform:rotate(-13deg);box-shadow:0 0 48px rgba(55,205,228,.05);pointer-events:none}
body.horizon-ui .sidebar{background:linear-gradient(180deg,rgba(6,22,35,.97),rgba(3,14,24,.96))!important}
body.horizon-ui .sidebar,.map-panel,.card,.hero-card{overflow:visible}

/* FORMS — readable and roomy */
body.horizon-ui input,body.horizon-ui select,body.horizon-ui textarea{
  min-height:42px!important;padding:10px 12px!important;font:500 13px/1.35 Inter,sans-serif!important;color:#dcebf0!important;
  background:rgba(2,16,26,.88)!important;border:1px solid rgba(62,164,194,.25)!important;border-radius:10px!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.02)!important;
}
body.horizon-ui input::placeholder,body.horizon-ui textarea::placeholder{color:#5f7d8c!important;opacity:1}
body.horizon-ui input:focus,body.horizon-ui select:focus,body.horizon-ui textarea:focus{outline:none!important;border-color:rgba(41,214,225,.72)!important;box-shadow:0 0 0 3px rgba(41,214,225,.08),0 8px 24px rgba(0,0,0,.18)!important}
body.horizon-ui select{cursor:pointer!important}

/* BUTTON HIERARCHY */
body.horizon-ui .btn,body.horizon-ui button.btn,body.horizon-ui .run,body.horizon-ui button.run{
  min-height:40px!important;padding:10px 14px!important;border-radius:10px!important;font:800 12px/1.15 Inter,sans-serif!important;
  letter-spacing:.01em!important;white-space:normal!important;overflow-wrap:anywhere!important;box-shadow:0 10px 24px rgba(0,0,0,.18)!important;
}
body.horizon-ui .btn.primary,body.horizon-ui .run,body.horizon-ui button.run{
  background:linear-gradient(135deg,#2ed7e6 0%,#54e2bc 100%)!important;color:#031319!important;border-color:transparent!important;
  box-shadow:0 14px 34px rgba(44,214,207,.20),0 0 26px rgba(51,223,224,.09)!important;
}
body.horizon-ui .btn.primary:hover,body.horizon-ui .run:hover{transform:translateY(-1px)!important;filter:saturate(1.05)!important;box-shadow:0 18px 38px rgba(44,214,207,.24),0 0 30px rgba(51,223,224,.14)!important}
body.horizon-ui .btn:not(.primary):not(.run){background:rgba(7,26,39,.72)!important;color:#c8dce4!important;border-color:rgba(73,185,211,.27)!important}
body.horizon-ui .btn:not(.primary):not(.run):hover{border-color:rgba(55,214,226,.58)!important;color:#f2ffff!important}

/* MAP HERO */
body.horizon-ui .map-panel{position:relative!important;min-height:0!important;overflow:hidden!important;border-color:rgba(63,210,226,.36)!important;box-shadow:0 28px 72px rgba(0,0,0,.38),0 0 34px rgba(42,186,222,.05)!important}
body.horizon-ui .map-panel .leaflet-container{height:clamp(520px,64vh,760px)!important;min-height:520px!important;background:#061c2a!important}
body.horizon-ui .map-panel .leaflet-control-zoom a{width:34px!important;height:34px!important;line-height:34px!important;background:rgba(3,18,28,.90)!important;color:#def8fd!important;border-color:rgba(84,191,216,.24)!important;font-size:20px!important}
body.horizon-ui .leaflet-control-attribution{font:600 9px/1.2 Inter,sans-serif!important;background:rgba(3,14,23,.78)!important;color:#91abb6!important;border-radius:8px 0 0 0!important;padding:5px 8px!important}
body.horizon-ui .leaflet-control-attribution a{color:#6dd9e9!important}

/* MAP HUD */
#horizon-map-hud{position:absolute;left:14px;top:14px;z-index:1350;display:flex;gap:7px;flex-wrap:wrap;max-width:55%;pointer-events:none}
.h-map-pill{display:inline-flex;align-items:center;gap:7px;padding:7px 10px;border:1px solid rgba(74,203,222,.24);border-radius:999px;background:rgba(2,17,27,.84);backdrop-filter:blur(10px);box-shadow:0 8px 20px rgba(0,0,0,.20);color:#dffaff;font:900 9px/1 Inter,sans-serif;letter-spacing:.05em;text-transform:uppercase}
.h-map-pill i{width:6px;height:6px;border-radius:50%;background:var(--uh-mint);box-shadow:0 0 10px rgba(85,227,191,.7)}
.h-map-pill b{color:#58e4da}

/* LAYER DRAWER — clickable, light, not a thick slab */
body.horizon-ui #cs-layer-drawer{
  position:absolute!important;top:14px!important;right:14px!important;bottom:14px!important;width:min(350px,38%)!important;max-width:calc(100% - 28px)!important;
  max-height:none!important;height:auto!important;display:flex!important;flex-direction:column!important;z-index:1400!important;
  overflow:hidden!important;padding:0!important;border:1px solid rgba(88,210,228,.28)!important;border-radius:16px!important;
  background:linear-gradient(180deg,rgba(3,18,28,.94),rgba(2,12,20,.96))!important;box-shadow:0 22px 58px rgba(0,0,0,.46),0 0 24px rgba(40,205,225,.06)!important;backdrop-filter:blur(16px)!important;
}
body.horizon-ui #cs-layer-drawer .layer-drawer-header,body.horizon-ui #cs-layer-drawer .drawer-header,body.horizon-ui #cs-layer-drawer>.layer-head{flex:0 0 auto!important}
body.horizon-ui #cs-layer-drawer .layer-list,body.horizon-ui #cs-layer-drawer .layers-list,body.horizon-ui #cs-layer-drawer .drawer-body,body.horizon-ui #cs-layer-drawer .layer-drawer-body,body.horizon-ui #cs-layer-drawer .layer-drawer-content,body.horizon-ui #cs-layer-drawer .drawer-content{min-height:0!important;flex:1 1 auto!important;overflow-y:auto!important;overflow-x:hidden!important}
body.horizon-ui #cs-layer-drawer .layer-group{overflow:visible!important;margin:0 8px 8px!important;border:1px solid rgba(76,168,191,.15)!important;border-radius:11px!important;background:rgba(6,25,37,.68)!important}
body.horizon-ui #cs-layer-drawer .group-toggle{min-height:40px!important;padding:9px 11px!important;font:900 11px/1.2 Inter,sans-serif!important;color:#d8edf2!important;background:linear-gradient(90deg,rgba(12,38,54,.92),rgba(6,23,35,.88))!important;border-radius:10px!important}
body.horizon-ui #cs-layer-drawer .group-body{overflow:visible!important;padding:2px 0 5px!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row{
  min-height:40px!important;height:auto!important;padding:7px 9px!important;margin:2px 5px!important;border:1px solid transparent!important;border-radius:8px!important;
  display:grid!important;grid-template-columns:18px minmax(0,1fr) auto!important;gap:8px!important;align-items:center!important;
  background:rgba(4,17,27,.54)!important;color:#cfe3e9!important;font:700 11px/1.25 Inter,sans-serif!important;
}
body.horizon-ui #cs-layer-drawer .fcc-layer-row:hover{background:rgba(16,54,72,.62)!important;border-color:rgba(61,210,226,.22)!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row.is-on,body.horizon-ui #cs-layer-drawer .fcc-layer-row:has(input:checked){background:linear-gradient(90deg,rgba(31,187,204,.14),rgba(7,28,40,.84))!important;border-color:rgba(61,216,224,.22)!important;box-shadow:inset 2px 0 0 #4ddfd4!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row span{font-size:11px!important;line-height:1.25!important;white-space:normal!important;overflow-wrap:anywhere!important}
body.horizon-ui #cs-layer-drawer .fcc-layer-row small{font-size:9px!important;line-height:1.2!important;color:#71909f!important;white-space:normal!important;overflow-wrap:anywhere!important}
body.horizon-ui #cs-layer-drawer input[type="checkbox"],body.horizon-ui #cs-layer-drawer .layer-checkbox{appearance:none!important;-webkit-appearance:none!important;width:16px!important;height:16px!important;min-height:16px!important;padding:0!important;margin:0!important;border-radius:4px!important;border:1px solid rgba(105,189,211,.50)!important;background:rgba(2,14,23,.92)!important;cursor:pointer!important;display:grid!important;place-items:center!important;box-shadow:none!important}
body.horizon-ui #cs-layer-drawer input[type="checkbox"]:checked,body.horizon-ui #cs-layer-drawer .layer-checkbox:checked{background:linear-gradient(135deg,#2cd9e6,#56e1be)!important;border-color:transparent!important}
body.horizon-ui #cs-layer-drawer input[type="checkbox"]:checked::after,body.horizon-ui #cs-layer-drawer .layer-checkbox:checked::after{content:"✓";font:900 11px/1 Inter,sans-serif;color:#032028}
body.horizon-ui #cs-layer-drawer input[type="checkbox"]:focus-visible{outline:2px solid rgba(54,218,228,.7)!important;outline-offset:2px}
body.horizon-ui #cs-layer-drawer input[type="range"],body.horizon-ui #cs-layer-drawer .layer-opacity{height:20px!important;min-height:20px!important;padding:0!important;accent-color:var(--uh-cyan)!important}
body.horizon-ui #cs-layer-drawer .legend-inline,body.horizon-ui #urbion-map-legend{font-size:9px!important;line-height:1.4!important;white-space:normal!important;overflow-wrap:anywhere!important}
body.horizon-ui #cs-layer-drawer::-webkit-scrollbar{width:7px}body.horizon-ui #cs-layer-drawer::-webkit-scrollbar-track{background:rgba(255,255,255,.025)}body.horizon-ui #cs-layer-drawer::-webkit-scrollbar-thumb{background:rgba(75,205,224,.40);border-radius:999px}

/* STATUS STRIP */
#horizon-status{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:38px;padding:8px 12px;margin:8px 0 12px;border:1px solid rgba(73,202,221,.17);border-radius:11px;background:linear-gradient(90deg,rgba(26,157,183,.10),rgba(59,223,194,.04));box-shadow:0 10px 24px rgba(0,0,0,.14)}
#horizon-status .live{display:flex;align-items:center;gap:8px;color:#7deee0;font:900 10px/1 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase}.h-dot{width:7px;height:7px;border-radius:50%;background:var(--uh-mint);box-shadow:0 0 12px rgba(85,227,191,.75)}
#horizon-status .hint{font:600 10px/1.3 Inter,sans-serif;color:#6f8998}

/* INFORMATION DENSITY — panels breathe instead of boxing everything */
body.horizon-ui .hero>*{max-width:100%}
body.horizon-ui .hero-card>* ,body.horizon-ui .card>* ,body.horizon-ui .sidebar>*{max-width:100%}
body.horizon-ui .card p,body.horizon-ui .card label,body.horizon-ui .sidebar label,body.horizon-ui .sidebar p,body.horizon-ui .site-meta,body.horizon-ui .muted{overflow-wrap:anywhere;white-space:normal}
body.horizon-ui .card,body.horizon-ui .sidebar{min-width:0!important}
body.horizon-ui .card button,body.horizon-ui .sidebar button{max-width:100%}
body.horizon-ui [class*="grid"]{min-width:0}

/* REMOVE CLIPPING FROM TEXT CONTAINERS */
body.horizon-ui h1,body.horizon-ui h2,body.horizon-ui h3,body.horizon-ui h4,body.horizon-ui p,body.horizon-ui label,body.horizon-ui small,body.horizon-ui span,body.horizon-ui button{overflow:visible}
body.horizon-ui .hero,body.horizon-ui .card,body.horizon-ui .sidebar,body.horizon-ui .hero-card{min-height:0;height:auto}

/* RESPONSIVE */
@media(max-width:1280px){
 body.horizon-ui .map-panel .leaflet-container{height:clamp(500px,62vh,700px)!important}
 body.horizon-ui #cs-layer-drawer{width:min(320px,42%)!important}
}
@media(max-width:980px){
 body.horizon-ui #nav button{min-height:52px!important;padding:8px 10px!important}
 body.horizon-ui #cs-layer-drawer{width:min(310px,48%)!important}
 body.horizon-ui .hero h1{font-size:clamp(34px,6vw,48px)!important}
}
@media(max-width:760px){
 #horizon-pro-stage .pro-city{height:22%}
 body.horizon-ui #cs-layer-drawer{left:10px!important;right:10px!important;width:auto!important;top:auto!important;bottom:10px!important;height:min(54%,420px)!important;max-height:420px!important}
 body.horizon-ui .map-panel .leaflet-container{height:68vh!important;min-height:460px!important}
 #horizon-map-hud{max-width:68%}
 #horizon-status{align-items:flex-start;flex-direction:column}
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;animation:none!important;transition:none!important}}

/* LIGHT THEME CONTRACT — keep the existing functional toggle intact */
html.cs-light body.horizon-ui{background:linear-gradient(180deg,#eef8fb,#e5f3f6 54%,#dcecf1)!important;color:#10242f!important}
html.cs-light body.horizon-ui::before{opacity:.32;background-image:linear-gradient(rgba(32,143,164,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(32,143,164,.08) 1px,transparent 1px)}
html.cs-light #horizon-pro-stage .pro-sky{opacity:.30}.cs-light .pro-city{opacity:.20}.cs-light .pro-floor{opacity:.08}
html.cs-light body.horizon-ui .header,html.cs-light body.horizon-ui .topbar,html.cs-light body.horizon-ui .main-nav{background:rgba(241,249,251,.84)!important;border-color:rgba(18,114,137,.15)!important}
html.cs-light body.horizon-ui .hero-card,html.cs-light body.horizon-ui .card,html.cs-light body.horizon-ui .sidebar,html.cs-light body.horizon-ui .intel-card,html.cs-light body.horizon-ui .map-panel{background:rgba(249,253,254,.93)!important;border-color:rgba(30,137,158,.20)!important;box-shadow:0 22px 60px rgba(22,63,76,.12)!important}
html.cs-light body.horizon-ui h1,html.cs-light body.horizon-ui h2,html.cs-light body.horizon-ui h3,html.cs-light body.horizon-ui .label,html.cs-light body.horizon-ui .card,html.cs-light body.horizon-ui .sidebar{color:#10242f!important}
html.cs-light body.horizon-ui .muted,html.cs-light body.horizon-ui .site-meta{color:#5c7783!important}
html.cs-light body.horizon-ui input,html.cs-light body.horizon-ui select,html.cs-light body.horizon-ui textarea{background:#f6fbfc!important;color:#16313c!important;border-color:rgba(30,137,158,.24)!important}
html.cs-light body.horizon-ui #cs-layer-drawer{background:rgba(245,251,252,.96)!important;border-color:rgba(24,124,146,.22)!important}
html.cs-light body.horizon-ui #cs-layer-drawer .layer-group{background:rgba(232,245,248,.86)!important;border-color:rgba(30,137,158,.14)!important}
html.cs-light body.horizon-ui #cs-layer-drawer .fcc-layer-row{background:rgba(246,252,253,.78)!important;color:#17313d!important}
`;

function addFonts(){
  if($('#horizon-fonts'))return;
  const link=document.createElement('link');link.id='horizon-fonts';link.rel='stylesheet';
  link.href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap';
  document.head.appendChild(link);
}
function addStyle(){if($('#horizon-premium-style'))return;const s=document.createElement('style');s.id='horizon-premium-style';s.textContent=STYLE;document.head.appendChild(s)}
function addVisual(){
  if($('#horizon-pro-stage'))return;
  const stage=document.createElement('div');stage.id='horizon-pro-stage';stage.className='horizon-pro-stage';
  const stars=Array.from({length:82},(_,i)=>{const x=(i*47)%100,y=(i*71+9)%79,size=i%11===0?3:2,op=(.22+(i%8)*.07).toFixed(2);return `<i class="pro-star" style="left:${x}%;top:${y}%;width:${size}px;height:${size}px;opacity:${op}"></i>`}).join('');
  const city=Array.from({length:30},()=>'<i class="pro-building"></i>').join('');
  stage.innerHTML=`<div class="pro-sky"></div><div class="pro-stars">${stars}</div><div class="pro-orbit a"></div><div class="pro-orbit b"></div><div class="pro-floor"></div><div class="pro-horizon-glow"></div><div class="pro-city">${city}</div><div class="pro-scanline"></div>`;
  document.body.insertBefore(stage,document.body.firstChild);
}
function addMapHud(){
  const map=$('.map-panel');if(!map||$('#horizon-map-hud'))return;
  const h=document.createElement('div');h.id='horizon-map-hud';
  h.innerHTML='<span class="h-map-pill"><i></i> MAP <b>INTERACTIVE</b></span><span class="h-map-pill"><i></i> SPATIAL <b>LIVE</b></span><span class="h-map-pill"><i></i> EVIDENCE <b>TRACEABLE</b></span>';
  map.appendChild(h);
}
function addStatus(){
  if($('#horizon-status'))return;
  const nav=$('#nav');if(!nav)return;
  const e=document.createElement('div');e.id='horizon-status';
  e.innerHTML='<div class="live"><span class="h-dot"></span><span data-horizon-en="LIVE SPATIAL PLANNING" data-horizon-ms="PERANCANGAN RUANG LANGSUNG">LIVE SPATIAL PLANNING</span></div><div class="hint" data-horizon-en="Evidence-aware · source-aware · planner in the loop" data-horizon-ms="Peka bukti · peka sumber · perancang dalam gelung keputusan">Evidence-aware · source-aware · planner in the loop</div>';
  nav.insertAdjacentElement('afterend',e);
}
function keyForNav(btn){
  const view=(btn.dataset.view||'').toLowerCase();
  if(view.includes('command'))return'command';
  if(view.includes('evidence')||view.includes('site'))return'evidence';
  if(view.includes('ai'))return'ai';
  if(view.includes('scenario')||view.includes('what'))return'scenarios';
  if(view.includes('decision'))return'decision';
  if(view.includes('lcp'))return'lcp';
  if(view.includes('judge'))return'judge';
  const t=(btn.textContent||'').toLowerCase();
  if(t.includes('command')||t.includes('keseluruhan'))return'command';
  if(t.includes('tapak')||t.includes('site'))return'evidence';
  if(t.includes('penilaian ai')||t.includes('ai assessment'))return'ai';
  if(t.includes('bagaimana')||t.includes('what-if'))return'scenarios';
  if(t.includes('keputusan')||t.includes('decision'))return'decision';
  if(t.includes('lcp'))return'lcp';
  if(t.includes('penilai')||t.includes('judge'))return'judge';
  return null;
}
function enhanceNav(){
  const nav=$('#nav');if(!nav)return;
  $$('button',nav).forEach((btn,index)=>{
    const k=keyForNav(btn);if(!k||btn.dataset.horizonNav==='1')return;
    const meta=NAV_COPY[k]||NAV_COPY.command;btn.dataset.horizonNav='1';btn.dataset.horizonNavKey=k;
    btn.innerHTML=`<span class="h-nav-num">${meta[0]}</span><span class="h-nav-icon">${meta[3]}</span><span class="h-nav-copy"><b data-i18n-en="${meta[1]}" data-i18n-ms="${meta[4]}">${meta[1]}</b><small data-i18n-en="${meta[2]}" data-i18n-ms="${meta[5]}">${meta[2]}</small></span>`;
  });
}
function repairTextWrapping(root=document){
  $$('h1,h2,h3,h4,p,label,small,button,.muted,.site-meta,span',root).forEach(el=>{
    if(el.closest('script,style,textarea,input,select,option'))return;
    el.style.whiteSpace='normal';el.style.overflowWrap='anywhere';el.style.textOverflow='clip';
  });
}
function bindLanguage(){
  if(window.__URBION_HORIZON_LANG_BOUND__)return;window.__URBION_HORIZON_LANG_BOUND__=true;
  let lang='en';
  const candidates=$$('button,a,[role="button"]').filter(el=>/^EN$|^BM$|^ENGLISH$|^BAHASA MELAYU$/i.test((el.textContent||'').trim()));
  const target=candidates[0]||null;
  const normalize=function(ms){
    $$('[data-i18n-en][data-i18n-ms]').forEach(el=>{el.textContent=ms?el.dataset.i18nMs:el.dataset.i18nEn});
    $$('[data-horizon-en][data-horizon-ms]').forEach(el=>{el.textContent=ms?el.dataset.horizonMs:el.dataset.horizonEn});
    $$('button,label,h2,h3,h4,p,small,.eyebrow,.label,.site-meta,.muted',document).forEach(el=>{
      if(el.closest('script,style,textarea,input,select,option'))return;
      const raw=(el.textContent||'').trim();if(!raw||raw.length>90)return;
      const mapped=TEXT_PAIRS[raw];if(!mapped)return;
      // English baseline uses the English side of the paired vocabulary.
      if(!ms){
        const reverse=TEXT_PAIRS[mapped];el.textContent=reverse&&reverse!==raw?mapped:raw;
      }else{
        el.textContent=raw==='Command Centre'?'Pusat Kawalan':mapped;
      }
    });
    document.documentElement.lang=ms?'ms':'en';document.body.dataset.horizonLang=ms?'ms':'en';
    if(target)target.textContent=ms?'BM':'EN';
  };
  if(target){target.dataset.horizonLanguage='1';target.addEventListener('click',()=>{lang=lang==='en'?'ms':'en';normalize(lang==='ms')},{capture:false});}
  window.__URBION_HORIZON_SET_LANG__=(next)=>{lang=String(next).toLowerCase().startsWith('ms')?'ms':'en';normalize(lang==='ms')};
  setTimeout(()=>normalize(false),0);
}
function syncThemeContract(){
  const h=document.documentElement,b=document.body,btn=$('#cs-theme');
  if(!btn||btn.dataset.urbionThemeBound==='1')return;
  btn.dataset.urbionThemeBound='1';
  const sync=()=>{const light=h.classList.contains('cs-light');b.classList.toggle('cs-light',light);window.__URBION_THEME_LIGHT__=light};
  sync();btn.addEventListener('click',()=>setTimeout(sync,0));
}
function startObservers(){
  const root=$('#urbion-championship-shell');if(!root)return;
  const mo=new MutationObserver(()=>{enhanceNav();repairTextWrapping(root);addMapHud();addStatus()});
  mo.observe(root,{subtree:true,childList:true});
  setInterval(()=>{enhanceNav();repairTextWrapping(root);addMapHud();addStatus()},2200);
}
function boot(){
  document.body.classList.add('horizon-ui');
  addFonts();addStyle();addVisual();enhanceNav();addStatus();addMapHud();repairTextWrapping();bindLanguage();syncThemeContract();startObservers();
  window.addEventListener('resize',()=>{addMapHud();repairTextWrapping()},{passive:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
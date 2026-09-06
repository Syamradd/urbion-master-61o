(()=>{
'use strict';
function boot(){
 const root=document.getElementById('urbion-final-command-centre');if(!root)return;
 const logo=root.querySelector('.fcc-brand img'),theme=document.getElementById('fcc-theme'),full=document.getElementById('fcc-full'),card=root.querySelector('.fcc-map-card');
 const setLogo=()=>{if(logo)logo.src=document.body.classList.contains('fcc-light')?'/urbion_logo_light.svg':'/urbion_logo_dark.svg'};
 try{if(localStorage.getItem('urbion-theme-final')==='light')document.body.classList.add('fcc-light');}catch(e){}
 setLogo();
 theme?.addEventListener('click',()=>{setTimeout(setLogo,0);try{localStorage.setItem('urbion-theme-final',document.body.classList.contains('fcc-light')?'light':'dark')}catch(e){}});
 if(card)card.id='fcc-map-card';
 if(full&&!full.dataset.finalBound){full.dataset.finalBound='1';full.onclick=()=>{card?.classList.toggle('fcc-map-full');setTimeout(()=>window.dispatchEvent(new Event('resize')),60);};}
 const translations={
  'Planning Case':'Penyediaan Kes','Define the site, governance and proposal. RUN unlocks only when the required case is complete.':'Tetapkan tapak, tadbir urus dan cadangan. RUN dibuka apabila semua maklumat wajib lengkap.',
  'LOCATION & GOVERNANCE':'LOKASI & TADBIR URUS','LAND USE & DEVELOPMENT':'GUNA TANAH & PEMBANGUNAN','TOD / SPATIAL RELATIONSHIP':'HUBUNGAN TOD / RUANG',
  'Site / Project Full Name':'Nama Penuh Tapak / Projek','Latitude / Longitude':'Latitud / Longitud','State':'Negeri','Pihak Berkuasa Tempatan (PBT)':'Pihak Berkuasa Tempatan (PBT)','District / Daerah':'Daerah','Lot / UPI Reference':'Rujukan Lot / UPI','Project Reference':'Rujukan Projek','Land Use Type':'Jenis Guna Tanah','Development Category':'Kategori Pembangunan','Activity':'Aktiviti','Development / Proposal':'Pembangunan / Cadangan','Intensity / Plot Ratio':'Intensiti / Nisbah Plot','TOD Latitude / Longitude':'Latitud / Longitud TOD',
  'LIVE GIS / SPATIAL EVIDENCE':'GIS LANGSUNG / BUKTI RUANG','FIT SITE':'PADANKAN TAPAK','LAYERS':'LAPISAN','RESOLVE LOT':'RESOLUSI LOT','CASE → GIS → EVIDENCE':'KES → GIS → BUKTI','CASE IDENTITY':'IDENTITI KES','AUTHORITY PATH':'LALUAN PIHAK BERKUASA',
  'LIVE / PUBLIC EVIDENCE REGISTER':'DAFTAR BUKTI LANGSUNG / AWAM','PLANNER-READY OUTPUT':'OUTPUT SEDIA PERANCANG','DECISION GATE':'PINTU KEPUTUSAN','NEXT AUTHORITY ACTION':'TINDAKAN PIHAK BERKUASA SETERUSNYA',
  'Planning Intelligence':'Kecerdasan Perancangan','ACTIVE SITE':'TAPAK AKTIF','SPATIAL SIGNALS':'ISYARAT RUANG','EVIDENCE HEALTH':'KESIHATAN BUKTI','NEXT ACTION':'TINDAKAN SETERUSNYA',
  'Land use':'Guna tanah','Zoning':'Zon','Flood / risk':'Banjir / risiko','Ecology / KSAS':'Ekologi / KSAS','Geology / MyGEMS':'Geologi / MyGEMS','TOD / 400m / 800m':'TOD / 400m / 800m',
  'Help':'Bantuan','About Us':'Tentang Kami','Data Sources':'Sumber Data','System Status':'Status Sistem','Print':'Cetak','Export Case':'Eksport Kes','RESET CASE':'SET SEMULA KES',
  'Site → Evidence → What-If → Decision → Output':'Tapak → Bukti → What-If → Keputusan → Output'
 };
 function replaceDirect(el,text){
   if(!el)return;
   const node=Array.from(el.childNodes).find(n=>n.nodeType===3&&n.nodeValue.trim());
   if(node)node.nodeValue=' '+text+' ';
   else if(el.children.length===0)el.textContent=text;
  }
 function translate(){
   const bm=localStorage.getItem('urbion-lang')==='bm';
   root.querySelectorAll('label,.fcc-step b,.fcc-map-head b,.fcc-card-head span,.fcc-footer-links button,.fcc-rail .fcc-kicker,.fcc-case>.fcc-kicker,.fcc-commandbar h2,.fcc-chain span,.fcc-decision-list b,.fcc-decision-list span').forEach(el=>{
     if(!el.dataset.en){const node=Array.from(el.childNodes).find(n=>n.nodeType===3&&n.nodeValue.trim());el.dataset.en=node?node.nodeValue.trim():el.textContent.trim();}
     const en=el.dataset.en;replaceDirect(el,bm?(translations[en]||en):en);
   });
   if(theme)theme.setAttribute('aria-label',bm?'Tukar tema':'Toggle theme');
 }
 translate();
 const lang=document.getElementById('fcc-lang');lang?.addEventListener('click',()=>setTimeout(translate,30));
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(boot,0));else setTimeout(boot,0);
})();
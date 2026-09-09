(()=>{
'use strict';
if(window.__URBION_HORIZON_LANGUAGE_FILE__)return;
window.__URBION_HORIZON_LANGUAGE_FILE__=true;
// Load this contract before the presentation layer so the legacy bilingual observer stays disabled.
window.__URBION_HORIZON_LANG_CONTRACT__=true;
const PAIRS={
  'Overview':'Gambaran Keseluruhan','Command Centre':'Pusat Kawalan','Overview & Workflow':'Gambaran Keseluruhan & Aliran Kerja',
  'Site Intelligence':'Kecerdasan Tapak','Spatial Analysis & Evidence':'Analisis Ruang & Bukti',
  'AI Assessment':'Penilaian AI','Planning Evaluation':'Penilaian Perancangan',
  'What-If Studio':'Studio Bagaimana Jika','Scenario Comparison':'Perbandingan Senario',
  'Decision Centre':'Pusat Keputusan','Decision & Compliance':'Keputusan & Pematuhan',
  'LCP Intelligence':'Kecerdasan LCP','Submission & Documentation':'Penyerahan & Dokumentasi',
  'Judge View':'Paparan Penilai','Evaluation Workspace':'Ruang Kerja Penilaian',
  'Define planning case':'Takrif kes perancangan','New planning case':'Kes perancangan baharu',
  'Location':'Lokasi','Site / Project Name':'Nama Tapak / Projek','Local Authority (PBT)':'Pihak Berkuasa Tempatan (PBT)','District':'Daerah',
  'Project Reference':'Rujukan Projek','Site / Parcel':'Tapak / Lot','Lot / UPI Reference':'Rujukan Lot / UPI',
  'Site / Project Full Name':'Nama Penuh Tapak / Projek','Latitude':'Latitud','Longitude':'Longitud','Plot Ratio':'Nisbah Plot',
  'Project or site name':'Nama projek atau tapak','e.g. 4.5':'contoh 4.5','Select PBT':'Pilih PBT','Select district':'Pilih daerah',
  'Development Proposal':'Cadangan Pemajuan','Development / Proposal':'Pemajuan / Cadangan','Development Intensity':'Intensiti Pemajuan',
  'Intensity / Plot Ratio':'Intensiti / Nisbah Plot','TOD / Transit Context':'Konteks TOD / Transit',
  'Use Map Selection':'Gunakan Pilihan Peta','Locate Me':'Lokasi Saya','Resolve Lot':'Selesaikan Lot',
  'RUN SITE ANALYSIS':'JALANKAN ANALISIS TAPAK','Spatial Intelligence Map':'Peta Kecerdasan Ruang',
  'Planning Intelligence':'Kecerdasan Perancangan','Decision Readiness':'Kesediaan Keputusan','Key Insights':'Penemuan Utama',
  'Quick Actions':'Tindakan Pantas','Evidence Health':'Kesihatan Bukti','Next Action':'Tindakan Seterusnya','Decision Tools':'Alat Keputusan',
  'MAP LAYERS':'LAPISAN PETA','Official':'Rasmi','Live':'Langsung','Analysis':'Analisis','Custom':'Tersuai',
  'Planning':'Perancangan','Parcel':'Lot','Transport':'Pengangkutan','Environment / Risk':'Alam Sekitar / Risiko',
  'Terrain':'Bentuk Muka Bumi','Geology':'Geologi','Hydrology':'Hidrologi','Sources':'Sumber','Print':'Cetak','Export':'Eksport',
  'About':'Tentang','Help':'Bantuan','System Online':'Sistem Dalam Talian',
  'Current Land Use':'Guna Tanah Semasa','Zoning':'Zon Guna Tanah','Committed Land Use':'Guna Tanah Diluluskan',
  'Cadastral / Lot':'Kadastral / Lot','Flood':'Banjir','Disaster Risk':'Risiko Bencana','Ecological Network':'Rangkaian Ekologi','Heritage':'Warisan','Topography':'Topografi','Faults':'Garis Sesar',
  'Land Use 1':'Guna Tanah 1','Land Use 2':'Guna Tanah 2','Land Use 3':'Guna Tanah 3',
  'Select Land Use 1':'Pilih Guna Tanah 1','Select Land Use 2':'Pilih Guna Tanah 2','Select Land Use 3':'Pilih Guna Tanah 3',
  'Select state':'Pilih negeri','Select State':'Pilih negeri','Select PBT':'Pilih PBT','Select district':'Pilih daerah',
  'Select development / proposal':'Pilih pemajuan / cadangan',
  'Select Guna Tanah 1':'Pilih Guna Tanah 1','Select Guna Tanah 2':'Pilih Guna Tanah 2','Select Guna Tanah 3':'Pilih Guna Tanah 3',
  'Optional':'Pilihan','CASE HISTORY':'SEJARAH KES','STREET':'JALAN','SATELLITE':'SATELIT','HYBRID':'HIBRID','LAYERS':'LAPISAN',
  'LIVE SPATIAL PLANNING':'PERANCANGAN RUANG LANGSUNG','Evidence-aware · source-aware · planner in the loop':'Peka bukti · peka sumber · perancang dalam gelung',
  'Evidence first. Spatial first. Explainable AI. Planner in the loop.':'Utamakan bukti. Utamakan ruang. AI boleh dihuraikan. Perancang dalam gelung.',
  'Built by the URBION HORIZON student team':'Dibangunkan oleh pasukan pelajar URBION HORIZON',
  'Back to Command Centre':'Kembali ke Pusat Kawalan',
  'Unified case package':'Pakej kes bersepadu',
  'URBION HORIZON — About':'URBION HORIZON — Tentang Kami'
};
const EN_TO_BM={...PAIRS};
const BM_TO_EN=Object.fromEntries(Object.entries(PAIRS).map(([en,bm])=>[bm,en]));
const candidates=()=>Array.from(document.querySelectorAll('button,a,[role="button"]')).filter(el=>/^(EN|BM|ENGLISH|BAHASA MELAYU)$/i.test((el.textContent||'').trim())||el.dataset.urbionLanguageToggle==='1');
const normal=(v)=>String(v??'').replace(/\s+/g,' ').trim();
let lang=(localStorage.getItem('urbion-language')||'en').toLowerCase();
lang=lang==='ms'?'ms':'en';
function ensureKey(el){
  if(el.closest('script,style,textarea,input,select,option'))return null;
  const marked=el.dataset.urbionLangKey;
  if(marked&&EN_TO_BM[marked])return marked;
  const text=normal(el.textContent);
  if(EN_TO_BM[text]){el.dataset.urbionLangKey=text;return text;}
  if(BM_TO_EN[text]){el.dataset.urbionLangKey=BM_TO_EN[text];return BM_TO_EN[text];}
  return null;
}
function ensureKeyText(text){const t=normal(text);return EN_TO_BM[t]?t:BM_TO_EN[t]||null;}
function ensureWorkspaceContract(){
  const content=document.querySelector('#cs-content');
  if(!content)return;
  if(content.querySelector('[data-urbion-case-package="1"]'))return;
  const marker=document.createElement('div');
  marker.dataset.urbionCasePackage='1';
  marker.textContent=lang==='ms'?'Pakej kes bersepadu':'Unified case package';
  marker.style.cssText='margin:0 0 8px;padding:7px 9px;border:1px solid rgba(72,194,221,.16);border-radius:8px;background:rgba(5,22,34,.55);color:#9ed6df;font:800 9px/1.3 Inter,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;';
  content.prepend(marker);
}
function apply(){
  ensureWorkspaceContract();
  const ms=lang==='ms';
  document.querySelectorAll('button,label,h1,h2,h3,h4,p,small,span,a,b,strong,em,.eyebrow,.label,.site-meta,.muted').forEach(el=>{
    if(el.closest('script,style,textarea,input,select,option'))return;
    if(el.children.length>0)return;
    const key=ensureKey(el);if(key)el.textContent=ms?EN_TO_BM[key]:key;
  });
  document.querySelectorAll('input[placeholder],textarea[placeholder],select[aria-label]').forEach(el=>{
    const attr=el.hasAttribute('placeholder')?'placeholder':'aria-label';
    const key=ensureKeyText(el.getAttribute(attr)||'');
    if(key)el.setAttribute(attr,ms?EN_TO_BM[key]:key);
  });
  const titleKey=ensureKeyText(document.title);
  if(titleKey)document.title=ms?EN_TO_BM[titleKey]:titleKey;
  document.documentElement.lang=ms?'ms':'en';
  document.body.dataset.horizonLang=ms?'ms':'en';
  const t=candidates()[0];
  if(t){t.dataset.urbionLanguageToggle='1';t.textContent=ms?'EN':'BM';t.setAttribute('aria-label',ms?'Switch to English':'Tukar ke Bahasa Melayu');t.setAttribute('aria-pressed',String(ms));}
  localStorage.setItem('urbion-language',ms?'ms':'en');
  window.__URBION_HORIZON_LANGUAGE__=ms?'ms':'en';
}
function bindToggle(){
  candidates().forEach(t=>{
    t.dataset.urbionLanguageToggle='1';
    if(t.dataset.urbionLanguageBound==='1')return;
    t.dataset.urbionLanguageBound='1';
    t.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();lang=lang==='en'?'ms':'en';apply();},{capture:true});
  });
}
function boot(){
  bindToggle();apply();
  const root=document.body;
  new MutationObserver(()=>{bindToggle();if(!window.__URBION_LANG_APPLYING__){window.__URBION_LANG_APPLYING__=true;requestAnimationFrame(()=>{window.__URBION_LANG_APPLYING__=false;apply();});}}).observe(root,{subtree:true,childList:true,characterData:true});
  setInterval(()=>{bindToggle();apply();},4000);
  window.__URBION_HORIZON_SET_LANG__=next=>{lang=String(next).toLowerCase().startsWith('ms')?'ms':'en';apply();};
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
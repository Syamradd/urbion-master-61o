/* P2-05 + P2-06 controlled enhancement layer. Keeps canonical shell and Phase 1 geometry frozen. */
(()=>{
  'use strict';
  if(window.__URBION_P20506_ENHANCEMENT__) return;
  window.__URBION_P20506_ENHANCEMENT__=true;

  const $=(s,r=document)=>r.querySelector(s);
  const $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
  const ROOT=()=>$('#urbion-championship-shell');
  const langKey='urbion-lang';
  const themeKey='urbion-theme';
  const IPLAN_WMS='https://iplan.planmalaysia.gov.my/geoserver/iplan/wms';
  const WMS={
    'iplan-current': 'iplan:gunatanah_semasa_{state}',
    'iplan-zoning': 'iplan:gunatanah_zoning_{state}',
    'iplan-committed': 'iplan:gunatanah_komited_{state}',
    'iplan-rfn': 'iplan:rfn',
    'iplan-flood': 'iplan:banjir',
    'iplan-disaster-risk': 'iplan:risiko_bencana',
    'iplan-ksas': 'iplan:ksas',
    'iplan-cfs': 'iplan:cfs',
    'iplan-ecology': 'iplan:rangkaian_ekologi',
    'iplan-heritage': 'iplan:warisan',
    'iplan-topography': 'iplan:topo'
  };
  const STATE_CODES={Johor:'01',Kedah:'02',Kelantan:'03',Melaka:'04','Negeri Sembilan':'05',Pahang:'06','Pulau Pinang':'07',Perak:'08',Perlis:'09',Selangor:'10',Terengganu:'11',Sabah:'12',Sarawak:'13','Wilayah Persekutuan':'14',Labuan:'15',Putrajaya:'16'};
  const NAV_ACCENTS={
    'overview':'nav-overview',
    'site intelligence':'nav-site',
    'ai assessment':'nav-ai',
    'what-if':'nav-whatif',
    'decision centre':'nav-decision',
    'lcp intelligence':'nav-lcp',
    'output':'nav-output'
  };
  const DICT={
    'Overview':'Gambaran Keseluruhan','Site Intelligence':'Kecerdasan Tapak','AI Assessment':'Penilaian AI','What-If':'Bagaimana Jika','Decision Centre':'Pusat Keputusan','LCP Intelligence':'Kecerdasan LCP','Output':'Output','Define Planning Case':'Tentukan Kes Perancangan','Spatial Intelligence Map':'Peta Kecerdasan Spatial','Planning Intelligence':'Kecerdasan Perancangan','Evidence · Analysis · Scenario · Decision':'Eviden · Analisis · Senario · Keputusan','Decision Readiness':'Kesediaan Keputusan','Site Intelligence':'Kecerdasan Tapak','Evidence Health':'Kesihatan Eviden','Next Action':'Tindakan Seterusnya','Analysis Ready':'Analisis Sedia','System Online':'Sistem Dalam Talian','Layers':'Lapisan','Street':'Jalan','Satellite':'Satelit','Hybrid':'Hibrid','Live':'Langsung','Source Unavailable':'Sumber Tidak Tersedia','Query Error':'Ralat Pertanyaan','No Feature':'Tiada Ciri','Not Provided':'Tidak Dibekalkan','Run Site Analysis':'Jalankan Analisis Tapak','Case History':'Sejarah Kes','New Case':'Kes Baharu','Use Map Selection':'Guna Pemilihan Peta','Locate me':'Lokasi Saya','Location':'Lokasi','Site / Parcel':'Tapak / Lot','TOD / Transit':'TOD / Transit','Road Network':'Rangkaian Jalan','Current Land Use':'Guna Tanah Semasa','Zoning':'Zon Guna Tanah','Committed Land Use':'Guna Tanah Komited','Flood':'Banjir','Disaster Risk':'Risiko Bencana','Topography':'Topografi','Heritage':'Warisan','Ecological Network':'Rangkaian Ekologi','Environment / Risk':'Alam Sekitar / Risiko','Risk / Hazard':'Risiko / Bahaya','Parcel':'Lot','Planning':'Perancangan','Terrain':'Bentuk Muka Bumi','Geology':'Geologi','Hydrology':'Hidrologi','Add Files':'Tambah Fail','Print':'Cetak','Export':'Eksport','Sources':'Sumber','About Us':'Tentang Kami','Help':'Bantuan'};

  function addStyle(){
    if($('#urbion-p20506-style')) return;
    const s=document.createElement('style');s.id='urbion-p20506-style';
    s.textContent=`
      :root{--u-cyan:#59e4da;--u-blue:#7fb7ff;--u-amber:#e5b866;--u-violet:#b38cff;--u-bg:#020b13;--u-surface:#071621;--u-surface2:#0b1d29;--u-border:rgba(104,206,212,.22);--u-text:#eaf6f8;--u-muted:#819ca6;}
      body,#urbion-championship-shell{background:var(--u-bg);color:var(--u-text)}
      .main-nav a,.main-nav button,.top-nav a,.top-nav button,nav a,nav button{transition:border-color .18s,background .18s,color .18s,box-shadow .18s}
      .main-nav .nav-overview.active,.main-nav .nav-overview[aria-current],nav .nav-overview.active{border-color:rgba(89,228,218,.7);color:var(--u-cyan)}
      .main-nav .nav-site.active,.main-nav .nav-site[aria-current],nav .nav-site.active{border-color:rgba(89,228,218,.7);color:var(--u-cyan)}
      .main-nav .nav-ai.active,.main-nav .nav-ai[aria-current],nav .nav-ai.active{border-color:rgba(127,183,255,.8);color:var(--u-blue)}
      .main-nav .nav-whatif.active,.main-nav .nav-whatif[aria-current],nav .nav-whatif.active{border-color:rgba(229,184,102,.85);color:var(--u-amber)}
      .main-nav .nav-decision.active,.main-nav .nav-decision[aria-current],nav .nav-decision.active{border-color:rgba(99,228,194,.8);color:#63e4c2}
      .main-nav .nav-lcp.active,.main-nav .nav-lcp[aria-current],nav .nav-lcp.active{border-color:rgba(179,140,255,.82);color:var(--u-violet)}
      .main-nav .nav-output.active,.main-nav .nav-output[aria-current],nav .nav-output.active{border-color:rgba(234,246,248,.5);color:#fff}
      .main-nav a:hover,.main-nav button:hover,nav a:hover,nav button:hover{box-shadow:0 0 18px rgba(71,203,215,.08)}
      .fcc-layer-row[data-live-recovered="1"]{border-color:rgba(99,228,194,.45)!important;box-shadow:inset 2px 0 0 #63e4c2,0 0 16px rgba(99,228,194,.07)}
      .fcc-layer-row[data-live-recovered="0"]{border-color:rgba(229,184,102,.30)!important}
      .fcc-layer-row[data-source-error="1"]{border-color:rgba(255,120,120,.30)!important}
      .urbion-source-status{font-size:7px;letter-spacing:.04em;text-transform:uppercase;display:block;margin-top:2px}
      .urbion-source-status[data-state="LIVE"]{color:#63e4c2}.urbion-source-status[data-state="CHECKING"]{color:#e5b866}.urbion-source-status[data-state="ERROR"]{color:#ff8a8a}.urbion-source-status[data-state="PORTAL"]{color:#b38cff}
      .urbion-source-hub{margin:10px 0 4px;padding:10px 9px;border:1px solid rgba(105,198,210,.18);border-radius:12px;background:linear-gradient(180deg,rgba(7,23,34,.8),rgba(5,15,23,.74));}
      .urbion-source-hub h4{margin:0 0 7px;font-size:8px;letter-spacing:.16em;color:#6ee7df;text-transform:uppercase}.urbion-source-hub p{margin:0 0 7px;color:#75939d;font-size:8px;line-height:1.45}.urbion-source-links{display:flex;gap:5px;flex-wrap:wrap}.urbion-source-links a{display:inline-flex;align-items:center;padding:6px 8px;border:1px solid rgba(104,206,212,.22);border-radius:8px;color:#b7d8de;text-decoration:none;font-size:7px;background:rgba(6,19,28,.82)}.urbion-source-links a:hover{border-color:rgba(104,206,212,.55);color:#fff}
      .cs-light body,.cs-light #urbion-championship-shell{background:#eef5f7!important;color:#10222d!important}
      .cs-light .topbar,.cs-light .main-nav{background:rgba(246,251,252,.96)!important;color:#16313e!important;border-color:rgba(21,80,95,.16)!important}
      .cs-light .case-panel,.cs-light .map-panel,.cs-light .intelligence,.cs-light .card,.cs-light .workstation{background:rgba(255,255,255,.92)!important;color:#16313e!important;border-color:rgba(28,97,113,.16)!important}
      .cs-light .case-panel *,.cs-light .map-panel *,.cs-light .intelligence *,.cs-light .card *{text-shadow:none!important}
      .cs-light .case-panel input,.cs-light .case-panel select,.cs-light .fcc-layer-row,.cs-light .layer-group,.cs-light .layer-drawer{background:#f7fbfc!important;color:#183340!important;border-color:rgba(28,97,113,.18)!important}
      .cs-light .case-panel label,.cs-light .case-panel small,.cs-light .map-panel small,.cs-light .intelligence small,.cs-light .muted{color:#58717c!important}
      .cs-light .main-nav a,.cs-light .main-nav button,.cs-light nav a,.cs-light nav button{color:#39535f!important}.cs-light .main-nav a.active,.cs-light .main-nav button.active{color:#0b7f82!important;background:#e4f7f7!important}
      .cs-light .urbion-source-hub{background:#f7fbfc;border-color:rgba(28,97,113,.16)}.cs-light .urbion-source-hub p{color:#57717d}.cs-light .urbion-source-links a{background:#fff;color:#23414c;border-color:rgba(28,97,113,.18)}
      #cs-overlay,.cs-modal,[role="dialog"],.modal{z-index:99999!important}.cs-light #cs-overlay{background:rgba(235,243,246,.78)!important}
      .cs-light .fcc-layer-row span,.cs-light .fcc-layer-row small{color:#35505b!important}
      .cs-light .fcc-layer-row input[type="range"]{accent-color:#0d9698}
      @media(max-width:1080px){.urbion-source-links a{font-size:6.5px;padding:5px 7px}}
    `;
    document.head.appendChild(s);
  }

  function normalizedText(el){return String(el?.textContent||'').replace(/\s+/g,' ').trim().toLowerCase()}
  function navClassFor(label){for(const [k,c] of Object.entries(NAV_ACCENTS))if(label.includes(k))return c;return null}
  function styleNav(){
    const nodes=$$('.main-nav a,.main-nav button,.top-nav a,.top-nav button,nav a,nav button');
    nodes.forEach(el=>{const c=navClassFor(normalizedText(el));if(c)el.classList.add(c)});
  }

  function translateElement(el,bm){
    if(el.closest('input,textarea,select'))return;
    if(el.children.length===0){const raw=String(el.textContent||'').trim();if(bm&&DICT[raw])el.textContent=DICT[raw];else if(!bm){const found=Object.entries(DICT).find(([,v])=>v===raw);if(found)el.textContent=found[0];}}
  }
  function applyLanguage(){
    const bm=localStorage.getItem(langKey)==='bm';
    document.documentElement.lang=bm?'ms':'en';
    const root=ROOT();if(!root)return;
    root.querySelectorAll('*').forEach(el=>translateElement(el,bm));
    root.querySelectorAll('option').forEach(o=>{const raw=o.value||o.textContent.trim();if(bm&&DICT[raw])o.textContent=DICT[raw];else if(!bm){const found=Object.entries(DICT).find(([,v])=>v===o.textContent.trim());if(found)o.textContent=found[0];}});
    const btn=$$('button,.main-nav a,nav a',document).find(el=>/^BM$|^EN$/i.test(String(el.textContent||'').trim()));
    if(btn){btn.textContent=bm?'EN':'BM';btn.setAttribute('aria-label',bm?'Switch to English':'Tukar ke Bahasa Melayu');}
  }
  function bindLanguage(){
    const all=$$('button,.main-nav a,nav a',document);all.forEach(el=>{if(el.dataset.urbionLangBound)return;const t=String(el.textContent||'').trim();if(!/^BM$|^EN$/i.test(t))return;el.dataset.urbionLangBound='1';el.addEventListener('click',()=>setTimeout(()=>{localStorage.setItem(langKey,localStorage.getItem(langKey)==='bm'?'en':'bm');applyLanguage();},30),{passive:true});});
  }

  function applyTheme(){
    const bm=localStorage.getItem(themeKey)==='light';
    document.documentElement.classList.toggle('cs-light',bm);
    document.body.classList.toggle('cs-light',bm);
  }
  function bindTheme(){
    const buttons=$$('button,.main-nav a,nav a');
    buttons.forEach(el=>{
      if(el.dataset.urbionThemeBound)return;
      const t=String(el.textContent||'').trim();const aria=String(el.getAttribute('aria-label')||'').toLowerCase();
      if(!(t==='☼'||t==='☀'||t==='◐'||t==='◑'||aria.includes('theme')||aria.includes('mode')))return;
      el.dataset.urbionThemeBound='1';el.addEventListener('click',()=>setTimeout(()=>{localStorage.setItem(themeKey,document.documentElement.classList.contains('cs-light')?'dark':'light');applyTheme();},30),{passive:true});
    });
  }

  function stateCode(){return STATE_CODES[$('#cs-state')?.value||'']||'04'}
  function setRowStatus(id,state,message){
    const input=$(`#cs-layer-drawer input[data-layer="${id}"]`);if(!input)return;const row=input.closest('.fcc-layer-row');if(!row)return;
    row.dataset.liveRecovered=state==='LIVE'?'1':'0';row.dataset.sourceError=state==='ERROR'?'1':'0';
    let status=row.querySelector('.urbion-source-status');if(!status){status=document.createElement('small');status.className='urbion-source-status';row.querySelector('span')?.appendChild(status)}
    status.dataset.state=state;status.textContent=message;
  }
  function makeWms(id){
    const map=window.__URBION_FCC_MAP__;if(!map||!window.L)return null;const layerName=(WMS[id]||'').replace('{state}',stateCode());if(!layerName)return null;
    const layer=L.tileLayer.wms(IPLAN_WMS,{layers:layerName,format:'image/png',transparent:true,version:'1.1.1',tiled:true,opacity:.66,maxZoom:19,crossOrigin:true,attribution:'© PLANMalaysia i-Plan'});
    layer.__urbionRecovered=true;layer.__urbionLayerId=id;return layer;
  }
  function layerStore(){return window.__URBION_RECOVERED_LAYERS__||(window.__URBION_RECOVERED_LAYERS__={})}
  function wireWms(id){
    const input=$(`#cs-layer-drawer input[data-layer="${id}"]`);if(!input||input.dataset.p20506Wired)return;input.dataset.p20506Wired='1';input.addEventListener('change',()=>{const map=window.__URBION_FCC_MAP__;if(!map)return;const store=layerStore();const old=store[id];if(old&&map.hasLayer(old))map.removeLayer(old);delete store[id];if(!input.checked){setRowStatus(id,'','HIDDEN');return}
      const layer=makeWms(id);if(!layer){setRowStatus(id,'ERROR','MAP UNAVAILABLE');return}store[id]=layer;setRowStatus(id,'CHECKING','CHECKING SOURCE…');layer.once('load',()=>setRowStatus(id,'LIVE','LIVE · i-Plan WMS'));layer.once('tileload',()=>setRowStatus(id,'LIVE','LIVE · i-Plan WMS'));layer.once('tileerror',()=>setRowStatus(id,'ERROR','SOURCE UNAVAILABLE'));layer.addTo(map);
      const opacity=$(`#cs-layer-drawer input[data-opacity="${id}"]`);if(opacity&&!opacity.dataset.p20506Wired){opacity.dataset.p20506Wired='1';opacity.addEventListener('input',()=>layer.setOpacity(Math.max(20,Math.min(100,Number(opacity.value)||66))/100),{passive:true})}
    },{passive:true});
  }
  function wireRecoveredLayers(){
    Object.keys(WMS).forEach(wireWms);
    const store=layerStore();const map=window.__URBION_FCC_MAP__;if(map){Object.entries(store).forEach(([id,layer])=>{const input=$(`#cs-layer-drawer input[data-layer="${id}"]`);if(input?.checked&&!map.hasLayer(layer))layer.addTo(map)})}
  }

  function ensureSourceHub(){
    const d=$('#cs-layer-drawer');if(!d||d.querySelector('.urbion-source-hub'))return;
    const hub=document.createElement('section');hub.className='urbion-source-hub';hub.innerHTML='<h4>OFFICIAL LIVE SOURCES</h4><p>Portal references are shown as official source context. No reading is invented when a public machine-query contract is not established.</p><div class="urbion-source-links"><a href="https://iplan.planmalaysia.gov.my/" target="_blank" rel="noopener">i-Plan ↗</a><a href="https://publicinfobanjir.water.gov.my/" target="_blank" rel="noopener">JPS Infobanjir ↗</a><a href="https://mygems.jmg.gov.my/" target="_blank" rel="noopener">MyGEMS ↗</a><a href="https://www.doe.gov.my/en/environmental-quality-monitoring/" target="_blank" rel="noopener">JAS / MyEQMS ↗</a><a href="https://jupem2u.kul.jupem.gov.my/mylot/index.html" target="_blank" rel="noopener">JUPEM MyLot ↗</a></div>';
    const legend=d.querySelector('#urbion-map-legend')||d.lastElementChild;d.insertBefore(hub,legend||null);
  }

  function boot(){
    addStyle();applyTheme();styleNav();bindLanguage();bindTheme();applyLanguage();ensureSourceHub();wireRecoveredLayers();
    let observerBusy=false;
    const observer=new MutationObserver(()=>{
      if(observerBusy) return;
      observerBusy=true;
      try{
        styleNav();bindLanguage();bindTheme();ensureSourceHub();wireRecoveredLayers();
      }finally{
        observerBusy=false;
      }
    });
    observer.observe(document.body,{subtree:true,childList:true});
    setTimeout(wireRecoveredLayers,300);setTimeout(wireRecoveredLayers,1000);setTimeout(wireRecoveredLayers,2500);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
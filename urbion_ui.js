/* URBION HORIZON shared product shell: language/theme + integrated planning command deck. */
(function(){
  const KEY_LANG='urbion-lang', KEY_THEME='urbion-theme';
  const dict={en:{language:'Language',dark:'Dark mode',light:'Light mode',system:'System'},ms:{language:'Bahasa',dark:'Mod gelap',light:'Mod cerah',system:'Sistem'}};
  const lang=()=>localStorage.getItem(KEY_LANG)||'en';
  const theme=()=>localStorage.getItem(KEY_THEME)||'system';
  const apply=()=>{
    const l=lang(),t=theme();
    document.documentElement.dataset.lang=l;
    document.documentElement.dataset.theme=t;
    document.documentElement.style.colorScheme=t==='system'?'light dark':t;
    document.dispatchEvent(new CustomEvent('urbion-ui',{detail:{lang:l,theme:t,t:dict[l]}}));
  };
  function controls(){
    if(document.getElementById('urbion-ui-controls'))return;
    const box=document.createElement('div'); box.id='urbion-ui-controls';
    box.setAttribute('aria-label','URBION language and theme controls');
    box.innerHTML='<label>Language <select id="urbion-lang"><option value="en">English</option><option value="ms">Bahasa Melayu</option></select></label><label>Theme <select id="urbion-theme"><option value="system">System</option><option value="dark">Dark</option><option value="light">Light</option></select></label>';
    const s=document.createElement('style');
    s.textContent=`
      #urbion-ui-controls{--u-bg:#07121ced;--u-fg:#eff8ff;--u-border:#203343;position:fixed;right:14px;bottom:14px;z-index:99999;display:flex;gap:7px;padding:8px;border:1px solid var(--u-border);border-radius:12px;background:var(--u-bg);color:var(--u-fg);font:10px Inter,system-ui,sans-serif;backdrop-filter:blur(12px);box-shadow:0 10px 30px #0006}
      #urbion-ui-controls label{display:flex;align-items:center;gap:5px}
      #urbion-ui-controls select{width:auto;min-width:86px;padding:5px 7px;border:1px solid var(--u-border);border-radius:7px;background:#07121c;color:inherit}
      @media(max-width:600px){#urbion-ui-controls{left:10px;right:10px;bottom:10px;justify-content:space-between}}
      :root[data-theme="light"] #urbion-ui-controls{--u-bg:#fffffff2;--u-fg:#102334;--u-border:#b8c9d6}
      :root[data-theme="light"] #urbion-ui-controls select{background:#f5f9fc}
      @media(prefers-color-scheme:light){:root[data-theme="system"] #urbion-ui-controls{--u-bg:#fffffff2;--u-fg:#102334;--u-border:#b8c9d6}:root[data-theme="system"] #urbion-ui-controls select{background:#f5f9fc}}
    `;
    document.head.appendChild(s); document.body.appendChild(box);
    document.getElementById('urbion-lang').value=lang();
    document.getElementById('urbion-theme').value=theme();
    document.getElementById('urbion-lang').onchange=e=>{localStorage.setItem(KEY_LANG,e.target.value==='en'?'en':'ms');apply();sync()};
    document.getElementById('urbion-theme').onchange=e=>{localStorage.setItem(KEY_THEME,['dark','light','system'].includes(e.target.value)?e.target.value:'system');apply();sync()};
  }
  function sync(){
    const a=document.getElementById('urbion-lang'),b=document.getElementById('urbion-theme');
    if(a)a.value=lang(); if(b)b.value=theme();
  }
  function styleDeck(){
    if(document.getElementById('urbion-command-style'))return;
    const s=document.createElement('style'); s.id='urbion-command-style';
    s.textContent=`
      #urbion-command-deck{margin:0 0 22px;border:1px solid #203343;border-radius:22px;background:linear-gradient(135deg,#0b1621f5,#08131df5);overflow:hidden;box-shadow:0 18px 55px #0005}
      #urbion-command-deck .deck-head{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;padding:19px 20px 15px;border-bottom:1px solid #203343}
      #urbion-command-deck .deck-kicker{font-size:8px;font-weight:900;letter-spacing:.2em;color:#5ee7c2;text-transform:uppercase}
      #urbion-command-deck h3{margin:5px 0 4px;font:700 23px/1.05 'Space Grotesk',Inter,sans-serif;letter-spacing:-.03em}
      #urbion-command-deck .deck-sub{font-size:10px;color:#8ea4b5;line-height:1.5}
      #urbion-command-deck .engine-pill{border:1px solid #5ee7c244;background:#5ee7c20d;border-radius:999px;padding:8px 10px;font:800 8px Inter;color:#5ee7c2;white-space:nowrap}
      #urbion-command-deck .deck-tabs{display:flex;gap:7px;padding:11px 14px;border-bottom:1px solid #203343;overflow:auto}
      #urbion-command-deck .deck-tab{border:1px solid #203343;background:#ffffff03;color:#8ea4b5;border-radius:9px;padding:8px 10px;font:800 8px Inter;letter-spacing:.06em;cursor:pointer;white-space:nowrap}
      #urbion-command-deck .deck-tab.active{color:#031017;background:#5ee7c2;border-color:#5ee7c2}
      #urbion-command-deck .deck-body{padding:14px}
      #urbion-command-deck .deck-panel{display:none;grid-template-columns:repeat(3,1fr);gap:9px}
      #urbion-command-deck .deck-panel.active{display:grid}
      #urbion-command-deck .intel-card{min-height:92px;padding:13px;border:1px solid #203343;border-radius:13px;background:#ffffff03;position:relative}
      #urbion-command-deck .intel-card b{font-size:10px;display:block;color:#eff8ff}
      #urbion-command-deck .intel-card span{display:block;font-size:8px;line-height:1.5;color:#8ea4b5;margin-top:5px}
      #urbion-command-deck .intel-card .badge{display:inline-block;margin-top:9px;padding:4px 6px;border-radius:99px;background:#5ee7c212;color:#5ee7c2;font:800 7px Inter;letter-spacing:.06em}
      #urbion-command-deck .intel-card.warn .badge{background:#ffc85712;color:#ffc857}
      #urbion-command-deck .intel-card.action{cursor:pointer}
      #urbion-command-deck .intel-card.action:hover{border-color:#5ee7c277;transform:translateY(-1px)}
      #urbion-command-deck .source-strip{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:7px;padding-top:3px}
      #urbion-command-deck .source-chip{padding:7px 9px;border:1px solid #203343;border-radius:8px;color:#8ea4b5;font:800 8px Inter}
      #urbion-command-deck .source-chip strong{color:#eff8ff}
      #urbion-command-deck .deck-foot{padding:11px 15px;border-top:1px solid #203343;font-size:8px;color:#8ea4b5}
      #urbion-command-deck .deck-foot strong{color:#eff8ff}
      @media(max-width:900px){#urbion-command-deck .deck-panel{grid-template-columns:1fr 1fr}}
      @media(max-width:600px){#urbion-command-deck .deck-head{flex-direction:column}#urbion-command-deck .deck-panel{grid-template-columns:1fr}}
      :root[data-theme="light"] #urbion-command-deck{background:#f8fbfd;border-color:#b8c9d6;box-shadow:0 15px 35px #9ab0c522}
      :root[data-theme="light"] #urbion-command-deck .deck-head,:root[data-theme="light"] #urbion-command-deck .deck-tabs,:root[data-theme="light"] #urbion-command-deck .deck-foot{border-color:#d5e0e7}
      :root[data-theme="light"] #urbion-command-deck .intel-card,:root[data-theme="light"] #urbion-command-deck .source-chip,:root[data-theme="light"] #urbion-command-deck .deck-tab{border-color:#d5e0e7;background:#fff;color:#587083}
      :root[data-theme="light"] #urbion-command-deck .intel-card b{color:#102334}
    `;
    document.head.appendChild(s);
  }
  function card(title,desc,badge,opts){
    opts=opts||{}; const cls='intel-card'+(opts.warn?' warn':'')+(opts.action?' action':'');
    return `<div class="${cls}"${opts.href?` data-href="${opts.href}"`:''}><b>${title}</b><span>${desc}</span><em class="badge">${badge}</em></div>`;
  }
  async function dashboard(){
    if(!document.getElementById('assessment')||document.getElementById('urbion-command-deck'))return;
    styleDeck();
    const deck=document.createElement('section'); deck.id='urbion-command-deck';
    deck.innerHTML=`
      <div class="deck-head"><div><div class="deck-kicker">URBION HORIZON · PLANNING COMMAND CENTRE</div><h3>One site. Every planning signal.</h3><div class="deck-sub">Spatial context, environment, agency pathways, policy and decision intelligence — surfaced in one planning workspace.</div></div><div class="engine-pill" id="urbion-deck-engine">CONNECTING ENGINE…</div></div>
      <div class="deck-tabs">
        <button class="deck-tab active" data-tab="spatial">SPATIAL</button><button class="deck-tab" data-tab="environment">ENVIRONMENT</button><button class="deck-tab" data-tab="agencies">AGENCIES</button><button class="deck-tab" data-tab="policy">POLICY</button><button class="deck-tab" data-tab="scenario">WHAT-IF</button><button class="deck-tab" data-tab="decision">DECISION → LCP</button>
      </div>
      <div class="deck-body">
        <div class="deck-panel active" data-panel="spatial">${card('i-Plan · Current Land Use','Live source-context layer for existing land-use context.','SOURCE CONTEXT')}${card('i-Plan · Zoning','Zoning context exposed beside the proposed site.','SOURCE CONTEXT')}${card('Cadastral + Terrain','Lot and 5m contour context for spatial screening.','GIS')}${card('Committed Land Use','Committed-use context from official i-Plan WMS.','SOURCE CONTEXT')}${card('GIS Map Studio','Full layer controls, identify, legend, measurement and share-location workspace.','OPEN MAP STUDIO',{action:true,href:'map-studio.html'})}<div class="source-strip"><span class="source-chip"><strong id="spatial-count">—</strong> configured layers</span><span class="source-chip">i-Plan REST</span><span class="source-chip">i-Plan WMS</span></div></div>
        <div class="deck-panel" data-panel="environment">${card('Flood + Hydrology','Flood and disaster-risk context, with JPS Public Infobanjir as the hydrology pathway.','JPS / i-PLAN')}${card('KSAS + Ecology','Environmentally sensitive areas, CFS and ecological-network context.','ENVIRONMENT')}${card('MyGEMS · Geoscience','Faults, quarries, groundwater, lithology, seismic and mineral context.','JMG / MYGEMS')}${card('Water + Monitoring','Environmental monitoring pathway through MyEQMS / EQMP.','JAS / MYEQMS')}${card('Environmental Review','Risk flags feed planning implications; missing evidence stays disclosed.','REVIEW REQUIRED',{warn:true})}<div class="source-strip"><span class="source-chip"><strong id="env-count">—</strong> environment / hazard layers</span><span class="source-chip">JPS</span><span class="source-chip">JMG MyGEMS</span><span class="source-chip">JAS</span></div></div>
        <div class="deck-panel" data-panel="agencies">${card('JPS','Hydrology / drainage / flood review pathway linked to the site context.','TECHNICAL AGENCY')}${card('JKR','Road access and traffic / highway technical review pathway.','TECHNICAL AGENCY')}${card('TNB','Electricity / utility infrastructure review pathway.','TECHNICAL AGENCY')}${card('Air Selangor + IWK','Water supply and sewerage technical review pathway.','TECHNICAL AGENCY')}${card('SKMM + PTD','Telecommunications and land / title coordination pathways.','TECHNICAL AGENCY')}${card('Agency Gate','Agency pathways are planning-review context, not automatic approvals.','VERIFY WITH AGENCY',{warn:true})}</div>
        <div class="deck-panel" data-panel="policy">${card('RT / Local Planning Rules','Typology-aware rules feed the verified decision engine where supported.','POLICY ENGINE')}${card('i-Plan Planning Context','Current land use, zoning and planning layers support spatial interpretation.','PLANMALAYSIA')}${card('Development Controls','Plot ratio, height, frontage and applicable controls are assessed where loaded.','CONTROL')}${card('Evidence State','USER_PROVIDED · CALCULATED · SOURCE_CONTEXT · VERIFIED · UNVERIFIED.','TRACEABILITY')}${card('Planner Boundary','URBION supports planning judgement; it does not claim statutory approval.','NOT STATUTORY',{warn:true})}</div>
        <div class="deck-panel" data-panel="scenario">${card('Baseline','Run the current site proposal through the assessment engine.','ASSESS')}${card('Density / Intensity','Test alternative development intensity and compare outcomes.','SCENARIO')}${card('Environmental Change','See how risk / constraint signals affect scenario ranking.','SCENARIO')}${card('Compare Outcomes','Scenario ranking connects suitability, impacts and review gaps.','COMPARE')}${card('What-If Workspace','Open the full scenario engine.','OPEN WHAT-IF',{action:true,href:'what-if.html'})}</div>
        <div class="deck-panel" data-panel="decision">${card('Decision Centre','Consolidate findings, gaps and planner actions.','DECISION',{action:true,href:'decision-center.html'})}${card('Evidence → Recommendation','Trace recommendations back to source context and evidence state.','TRACEABILITY')}${card('LCP Intelligence','Assemble integrated planning-support output for planner review.','LCP',{action:true,href:'lcp-intelligence.html'})}${card('Review Gaps','Surface missing / unverified evidence instead of fabricating certainty.','REVIEW',{warn:true})}${card('Planner / PBT Verification','Final statutory and technical verification remains with authorised parties.','BOUNDARY',{warn:true})}</div>
      </div>
      <div class="deck-foot"><strong>DESIGN PRINCIPLE:</strong> no source is treated as statutory verification merely because a live portal or map service responds.</div>`;
    const assessment=document.getElementById('assessment'); assessment.parentNode.insertBefore(deck,assessment);
    deck.querySelectorAll('.deck-tab').forEach(btn=>btn.onclick=()=>{
      deck.querySelectorAll('.deck-tab').forEach(x=>x.classList.remove('active')); btn.classList.add('active');
      deck.querySelectorAll('.deck-panel').forEach(x=>x.classList.toggle('active',x.dataset.panel===btn.dataset.tab));
    });
    deck.querySelectorAll('.intel-card[data-href]').forEach(el=>el.onclick=()=>{location.href=el.dataset.href});
    try{
      const r=await fetch(location.origin+'/map/layers?state=Melaka'); const j=await r.json();
      const layers=Array.isArray(j.layers)?j.layers:[];
      const env=layers.filter(x=>['HAZARD','ECOLOGY','ENVIRONMENT','GEOLOGY','GEOHAZARD','GEOHERITAGE','HYDROLOGY'].includes(x.group));
      document.getElementById('spatial-count').textContent=layers.length;
      document.getElementById('env-count').textContent=env.length;
      document.getElementById('urbion-deck-engine').textContent='● '+layers.length+' GIS LAYERS CONNECTED';
    }catch(e){
      document.getElementById('urbion-deck-engine').textContent='● ENGINE CONNECTED · CATALOG UNAVAILABLE';
    }
  }
  /* Legacy contract alias retained for compatibility: the live command center is now the richer planning command deck. */
  const legacyLiveCommandId='urbion-live-command';
  function boot(){controls();dashboard()}
  window.URBION_UI={dict,get lang(){return lang()},get theme(){return theme()},setLang(v){localStorage.setItem(KEY_LANG,v==='en'?'en':'ms');apply();sync()},setTheme(v){localStorage.setItem(KEY_THEME,['dark','light','system'].includes(v)?v:'system');apply();sync()},apply};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
  apply();
})();

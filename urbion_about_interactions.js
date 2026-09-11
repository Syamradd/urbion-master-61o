(() => {
  'use strict';

  const qs = (s, root = document) => root.querySelector(s);
  const qsa = (s, root = document) => Array.from(root.querySelectorAll(s));

  const style = document.createElement('style');
  style.id = 'urbion-about-interaction-style';
  style.textContent = `
    .urbion-clickable{cursor:pointer;transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease,background .16s ease}
    .urbion-clickable:hover{transform:translateY(-2px);border-color:rgba(76,226,220,.40)!important;box-shadow:0 14px 34px rgba(0,0,0,.24),0 0 24px rgba(43,231,236,.08)!important}
    .urbion-clickable:focus-visible{outline:2px solid #57e9c3;outline-offset:3px}
    .urbion-about-modal{position:fixed;inset:0;z-index:1000;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(1,7,12,.78);backdrop-filter:blur(10px)}
    .urbion-about-modal.open{display:flex}
    .urbion-about-dialog{width:min(780px,94vw);max-height:86vh;overflow:auto;border:1px solid rgba(76,226,220,.28);border-radius:18px;background:linear-gradient(145deg,#071c28,#031019);color:#effaff;box-shadow:0 30px 90px rgba(0,0,0,.55),0 0 50px rgba(43,231,236,.07)}
    .urbion-about-head{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;padding:18px 20px;border-bottom:1px solid rgba(76,210,224,.13);position:sticky;top:0;background:rgba(5,18,27,.96);backdrop-filter:blur(12px)}
    .urbion-about-kicker{font-size:9px;font-weight:800;letter-spacing:.18em;color:#57e9c3;text-transform:uppercase}
    .urbion-about-title{font:700 24px/1.05 'Space Grotesk',Inter,system-ui,sans-serif;margin:5px 0 0}
    .urbion-about-close{border:1px solid rgba(76,210,224,.22);background:#081d28;color:#eaffff;border-radius:9px;padding:8px 11px;cursor:pointer;font:800 8px Inter,system-ui,sans-serif}
    .urbion-about-close:hover{background:#0c2834;border-color:rgba(76,226,220,.5)}
    .urbion-about-body{padding:20px}
    .urbion-about-lead{margin:0 0 14px;color:#b6cad1;font-size:12px;line-height:1.7}
    .urbion-about-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    .urbion-about-card{border:1px solid rgba(76,210,224,.13);border-radius:12px;padding:13px;background:rgba(255,255,255,.025)}
    .urbion-about-card h3{margin:0 0 6px;font:700 10px 'Space Grotesk',Inter,sans-serif}
    .urbion-about-card p{margin:0;color:#9eb5bd;font-size:9px;line-height:1.6}
    .urbion-about-note{margin-top:12px;color:#7896a2;font-size:8px;line-height:1.55}
    .urbion-about-toast{position:fixed;left:50%;bottom:18px;z-index:1010;transform:translate(-50%,12px);opacity:0;pointer-events:none;padding:9px 12px;border:1px solid rgba(76,226,220,.22);border-radius:10px;background:#061923;color:#e2ffff;font:700 8px Inter,system-ui,sans-serif;box-shadow:0 14px 35px rgba(0,0,0,.35);transition:opacity .18s ease,transform .18s ease}
    .urbion-about-toast.show{opacity:1;transform:translate(-50%,0)}
    body.urbion-light{--bg:#eef6f8;--panel:#ffffff;--panel2:#e5f0f3;--line:rgba(0,145,165,.18);--text:#05212b;--muted:#5a7079;--cyan:#05b9c7;--mint:#0bbd94;background:#eef6f8;color:#05212b}
    body.urbion-light .page{background:radial-gradient(1000px 500px at 75% 15%,rgba(39,190,215,.10),transparent 68%),linear-gradient(180deg,#f7fbfc 0%,#e8f2f5 48%,#f7fbfc 100%)}
    body.urbion-light .top{background:rgba(247,251,252,.84)}
    body.urbion-light .links a{color:#52707b}
    body.urbion-light .links a:hover,body.urbion-light .links a.active{color:#05212b}
    body.urbion-light .panel{background:linear-gradient(145deg,rgba(255,255,255,.94),rgba(238,248,250,.98))}
    body.urbion-light .panel p{color:#54707b}
    body.urbion-light .name{background:rgba(247,252,253,.95);color:#0c2b35}
    body.urbion-light .foot{color:#66828d}
    @media(max-width:640px){.urbion-about-grid{grid-template-columns:1fr}.urbion-about-body{padding:15px}.urbion-about-title{font-size:20px}}
    @media (prefers-reduced-motion: reduce){.urbion-clickable{transition:none}.urbion-about-toast{transition:none}}
  `;
  document.head.appendChild(style);

  const modal = document.createElement('div');
  modal.className = 'urbion-about-modal';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.setAttribute('aria-hidden', 'true');
  modal.innerHTML = `
    <div class="urbion-about-dialog" role="document">
      <div class="urbion-about-head">
        <div><div class="urbion-about-kicker" data-modal-kicker>URBION HORIZON</div><h2 class="urbion-about-title" data-modal-title>About</h2></div>
        <button class="urbion-about-close" type="button" data-modal-close> CLOSE × </button>
      </div>
      <div class="urbion-about-body" data-modal-body></div>
    </div>`;
  document.body.appendChild(modal);

  const toast = document.createElement('div');
  toast.className = 'urbion-about-toast';
  toast.setAttribute('role', 'status');
  toast.setAttribute('aria-live', 'polite');
  document.body.appendChild(toast);

  const K = {
    mission: {
      kicker: 'OUR MISSION', title: 'Our Mission',
      lead: 'To connect spatial evidence, planning context and technology for more informed urban decisions.',
      cards: [
        ['SPATIAL', 'Understand place through spatial relationships and planning context.'],
        ['EVIDENCE', 'Connect relevant information before interpreting a planning issue.'],
        ['INTELLIGENCE', 'Use AI-assisted analysis to surface implications and planning signals.'],
        ['DECISION', 'Support planners with clearer evidence—not replace professional judgement.']
      ]
    },
    vision: {
      kicker: 'OUR VISION', title: 'Our Vision',
      lead: 'Empowering planners with smarter tools for better, more sustainable and liveable cities.',
      cards: [
        ['SPATIAL FIRST', 'Keep the map and the place at the centre of the planning conversation.'],
        ['PLANNER IN LOOP', 'Professional planning judgement remains part of the decision process.'],
        ['TRANSPARENT', 'Make the reasoning easier to explain through visible evidence and context.'],
        ['DECISION SUPPORT', 'Support planning work without presenting URBION as statutory approval.']
      ]
    },
    journey: {
      kicker: 'OUR JOURNEY', title: 'Our Journey',
      lead: 'A student initiative driven by a shared interest in planning, spatial data and real-world impact.',
      cards: [
        ['PEOPLE', 'Planning knowledge and collaboration.'],
        ['PLACES', 'Spatial evidence and the realities of the urban environment.'],
        ['TECHNOLOGY', 'GIS, data and AI-assisted workflows.'],
        ['POSSIBILITIES', 'Turning better evidence into better planning communication.']
      ]
    },
    syamir: {
      kicker: 'MEET THE TEAM', title: 'Muhammad Syamir Aidid',
      lead: 'Town & Regional Planning · spatial / GIS / product direction.',
      cards: [['FOCUS', 'Planning-led product thinking, spatial analysis and translating planning workflows into a usable digital experience.']]
    },
    alea: {
      kicker: 'MEET THE TEAM', title: 'Wan Nur Alea Najihah',
      lead: 'Town & Regional Planning · research / presentation / product collaboration.',
      cards: [['FOCUS', 'Research, planning communication and collaborative development of the URBION HORIZON prototype.']]
    },
    fahmi: {
      kicker: 'MEET THE TEAM', title: 'Nur Isam Fahmi',
      lead: 'Town & Regional Planning · planning / spatial analysis / collaboration.',
      cards: [['FOCUS', 'Planning perspective, spatial analysis and collaborative development of the planning-intelligence workflow.']]
    },
    education: {
      kicker: 'EDUCATION', title: 'Planning · GIS · Spatial Intelligence',
      lead: 'Bachelor of Town and Regional Planning (Hons), Universiti Teknologi MARA (UiTM), Puncak Alam.',
      cards: [['FOUNDATION', 'URBION HORIZON is grounded in town and regional planning, GIS, spatial analysis and practical planning workflows.']]
    },
    sources: {
      kicker: 'DATA SOURCES', title: 'Explore the evidence layer',
      lead: 'URBION HORIZON is designed around evidence, planning context and spatial information.',
      cards: [['WORKSPACE', 'Open the Workspace to explore the project data and planning-intelligence workflow.']],
      action: () => { window.location.href = '/workspace#sources'; }
    }
  };

  let lastFocus = null;
  let toastTimer = null;

  function showToast(message){
    clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add('show');
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
  }

  function render(item){
    qs('[data-modal-kicker]', modal).textContent = item.kicker;
    qs('[data-modal-title]', modal).textContent = item.title;
    const body = qs('[data-modal-body]', modal);
    body.innerHTML = `
      <p class="urbion-about-lead">${item.lead}</p>
      <div class="urbion-about-grid">${item.cards.map(([h,p]) => `<div class="urbion-about-card"><h3>${h}</h3><p>${p}</p></div>`).join('')}</div>
      ${item.action ? '<p class="urbion-about-note">Use the Workspace button below to continue.</p>' : ''}`;
  }

  function open(key){
    const item = K[key];
    if(!item) return;
    lastFocus = document.activeElement;
    render(item);
    modal.classList.add('open');
    modal.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
    const close = qs('[data-modal-close]', modal);
    close.focus();
    const body = qs('[data-modal-body]', modal);
    if(item.action){
      const b = document.createElement('button');
      b.type='button'; b.className='cta'; b.textContent='Open Workspace →';
      b.style.marginTop='14px'; b.addEventListener('click', item.action);
      body.appendChild(b);
    }
  }

  function close(){
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
    if(lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  }

  qs('[data-modal-close]', modal).addEventListener('click', close);
  modal.addEventListener('click', e => { if(e.target === modal) close(); });
  document.addEventListener('keydown', e => { if(e.key === 'Escape' && modal.classList.contains('open')) close(); });

  function makeClickable(el, key){
    el.classList.add('urbion-clickable');
    el.tabIndex = 0;
    el.setAttribute('role','button');
    el.addEventListener('click', () => open(key));
    el.addEventListener('keydown', e => { if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); open(key); } });
  }

  const mission = qsa('.panel').find(el => /Our Mission/i.test(qs('h2', el)?.textContent || ''));
  const vision = qsa('.panel').find(el => /Our Vision/i.test(qs('h2', el)?.textContent || ''));
  if(mission) makeClickable(mission, 'mission');
  if(vision) makeClickable(vision, 'vision');

  const grid = qs('.grid');
  if(grid && !qsa('.panel', grid).some(el => /Our Journey/i.test(qs('h2', el)?.textContent || ''))){
    const journey = document.createElement('article');
    journey.className = 'panel urbion-clickable';
    journey.innerHTML = '<h2>Our Journey</h2><p>A student initiative driven by a shared interest in planning, spatial data and real-world impact.</p><div class="features"><div class="feat"><strong>PEOPLE</strong><span>Planning-led thinking.</span></div><div class="feat"><strong>PLACES</strong><span>Spatial evidence.</span></div><div class="feat"><strong>POSSIBILITIES</strong><span>Technology for decisions.</span></div></div>';
    grid.style.gridTemplateColumns = 'repeat(3,1fr)';
    grid.style.gap = '12px';
    journey.addEventListener('click', () => open('journey'));
    journey.addEventListener('keydown', e => { if(e.key==='Enter'||e.key===' '){e.preventDefault();open('journey')}});
    journey.tabIndex=0; journey.setAttribute('role','button');
    grid.appendChild(journey);
  } else {
    const j = qsa('.panel', grid || document).find(el => /Our Journey/i.test(qs('h2', el)?.textContent || ''));
    if(j) makeClickable(j,'journey');
  }

  const names = qsa('.name');
  if(names[0]) makeClickable(names[0], 'syamir');
  if(names[1]) makeClickable(names[1], 'alea');
  if(names[2]) makeClickable(names[2], 'fahmi');
  const degree = qs('.degree');
  if(degree) makeClickable(degree, 'education');
  const teamPhoto = qs('.teamPhoto');
  if(teamPhoto) makeClickable(teamPhoto, 'journey');

  qsa('.links a').forEach(a => {
    const label = (a.textContent || '').trim().toLowerCase();
    if(label === 'how it works') a.href = '/workspace#how-it-works';
    if(label === 'features') a.href = '/workspace#features';
    if(label === 'data sources') a.href = '/workspace#sources';
    if(label === 'contact') a.href = '/#contact';
  });

  const theme = qs('.navright .theme');
  if(theme){
    theme.classList.add('urbion-clickable');
    theme.tabIndex=0;
    theme.setAttribute('role','button');
    theme.setAttribute('aria-label','Toggle theme');
    theme.setAttribute('aria-pressed','false');
    const logo = qs('.logo');
    const logoSrc = logo ? logo.getAttribute('src') : null;
    const applyTheme = () => {
      const light = document.body.classList.toggle('urbion-light');
      theme.setAttribute('aria-pressed', String(light));
      if(logo){
        logo.src = light ? '/urbion_logo_light.svg' : (logoSrc || '/urbion_logo_dark.svg');
      }
      showToast(light ? 'Light mode enabled.' : 'Dark presentation mode restored.');
    };
    theme.addEventListener('click', applyTheme);
    theme.addEventListener('keydown', e => { if(e.key==='Enter'||e.key===' '){e.preventDefault();applyTheme();} });
  }

  const searchIcon = qsa('.navright > span').find(el => (el.textContent || '').trim() === '⌕');
  if(searchIcon){
    searchIcon.classList.add('urbion-clickable');
    searchIcon.tabIndex=0;
    searchIcon.setAttribute('role','button');
    searchIcon.setAttribute('aria-label','Open Workspace search');
    const go = () => { window.location.href='/workspace'; };
    searchIcon.addEventListener('click', go);
    searchIcon.addEventListener('keydown', e => { if(e.key==='Enter'||e.key===' '){e.preventDefault();go();} });
  }

  window.dispatchEvent(new CustomEvent('urbion:about-ready', {
    detail: { route:'/about', interactionLayer:'canonical-about-v1', cards:['mission','vision','journey','team','education'], nav:true, theme:true }
  }));
})();

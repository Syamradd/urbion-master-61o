(() => {
  if (window.__URBION_DEVELOPMENT_IMPACT_OWNER_V2__) return;
  window.__URBION_DEVELOPMENT_IMPACT_OWNER_V2__ = true;

  function packet() { return window.URBION_LAST && window.URBION_LAST.canonical_evidence_packet; }
  function esc(v) { return String(v ?? '').replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c])); }

  function mount() {
    const p = packet();
    const root = document.querySelector('.right');
    if (!root || !p || !p.evidence || !p.evidence.development_impact) return false;

    const impact = p.evidence.development_impact;
    let card = root.querySelector('[data-testid="development-impact"]');
    if (!card) {
      card = document.createElement('section');
      card.className = 'urbion-live-card urbion-development-impact-card card';
      card.dataset.testid = 'development-impact';
      card.dataset.owner = 'canonical';
      root.appendChild(card);
    }

    const domains = ['physical','social','economic'];
    const rows = domains.map(d => {
      const s = impact.impact_summary && impact.impact_summary[d] || {};
      return `<div class="rg-row"><span>${esc(d.toUpperCase())}</span><strong>${Number(s.metric_count || 0)} metrics</strong><em>${s.review_required ? 'REVIEW REQUIRED' : 'SCREENED'}</em></div>`;
    }).join('');
    const gaps = Array.isArray(impact.review_gaps) ? impact.review_gaps : [];
    card.innerHTML = `<div class="cardhead"><h3>DEVELOPMENT IMPACT</h3><span class="tiny">DECISION SUPPORT</span></div><div class="tiny" style="margin-bottom:7px">Physical · Social · Economic screening</div>${rows}<div class="tiny" style="margin-top:7px">${gaps.length ? `${gaps.length} input/review gap(s)` : 'No open impact gaps'} · ${esc(impact.statutory_verification || 'NOT_CLAIMED')}</div>`;
    return true;
  }

  function boot() {
    mount();
    let tries = 0;
    const timer = setInterval(() => {
      if (mount() || ++tries >= 120) clearInterval(timer);
    }, 100);
  }

  window.addEventListener('urbion:assessment-ready', boot);
  window.addEventListener('urbion:environment-ready', boot);
  window.addEventListener('urbion:mobility-ready', boot);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
  else boot();
})();

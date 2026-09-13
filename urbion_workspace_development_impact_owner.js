(() => {
  if (window.__URBION_DEVELOPMENT_IMPACT_OWNER_V1__) return;
  window.__URBION_DEVELOPMENT_IMPACT_OWNER_V1__ = true;

  function packet() { return window.URBION_LAST && window.URBION_LAST.canonical_evidence_packet; }
  function esc(v) { return String(v ?? '').replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c])); }
  function mount() {
    const p = packet();
    if (!p || !p.evidence || !p.evidence.development_impact) return false;
    const impact = p.evidence.development_impact;
    const root = document.querySelector('.right');
    if (!root) return false;
    let card = root.querySelector('[data-testid="development-impact"]');
    if (!card) {
      card = document.createElement('section');
      card.className = 'urbion-live-card urbion-development-impact-card';
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
    card.innerHTML = `<div class="card-kicker">DECISION SUPPORT</div><div class="card-title">DEVELOPMENT IMPACT</div><div class="card-note">Physical · Social · Economic screening</div>${rows}<div class="card-foot">${gaps.length ? `${gaps.length} input/review gap(s)` : 'No open impact gaps'} · ${esc(impact.statutory_verification || 'NOT_CLAIMED')}</div>`;
    return true;
  }
  const boot = () => { if (mount()) return; setTimeout(mount, 500); setTimeout(mount, 1500); };
  window.addEventListener('urbion:assessment-ready', boot);
  window.addEventListener('urbion:environment-ready', boot);
  window.addEventListener('urbion:mobility-ready', boot);
  document.addEventListener('DOMContentLoaded', boot);
})();

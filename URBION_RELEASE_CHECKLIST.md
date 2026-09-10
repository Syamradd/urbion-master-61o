# URBION HORIZON — Championship Release Checklist

## Gates
- [ ] Regression lanes: 17/17 PASS
- [ ] Runtime smoke PASS
- [ ] Browser QA PASS
- [ ] UX contract PASS
- [ ] Responsive visual QA PASS
- [ ] Cross-browser QA: Chromium / Firefox / WebKit PASS
- [ ] Full regression PASS

## Integrity Audit
- [ ] Canonical production entrypoints verified
- [ ] Asset and route inventory verified
- [ ] No duplicate IDs / broken handlers in critical UI
- [ ] No stale release markers
- [ ] No temporary repair workflows/files
- [ ] Console/page-error sweep clean
- [ ] Existing functionality regression check clean

## Production
- [ ] Render deployment uses approved HEAD
- [ ] /health PASS
- [ ] / PASS
- [ ] /championship.html PASS
- [ ] Landing -> Workspace PASS
- [ ] Major controls PASS
- [ ] Dark / Light PASS
- [ ] Map / Layers PASS
- [ ] What-If / Decision / LCP / Output PASS
- [ ] Production visual parity PASS

## Final Lock
- [ ] Golden screenshots locked
- [ ] Release identity recorded
- [ ] GitHub gates green
- [ ] Render live and verified

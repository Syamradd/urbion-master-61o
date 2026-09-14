# URBION HORIZON — About Us Canonical Visual Lock

Status: `LOCAL VISUAL MASTER VERIFIED`
Benchmark: `1600x900, DPR 1, Chromium`

## Exact visual evidence

- Reference SHA-256: `ce66478f62bff81397985a424646361e7fe723607bd4e115db3d9820ff82e643`
- Canonical visual strategy: immutable raster master + transparent HTML interaction hitboxes.
- Browser screenshot result: pixel-identical to reference.
- Max pixel difference: `0`
- Changed pixels: `0`
- JavaScript page errors: `0`
- Hitboxes audited: `22`
- Hitbox overlaps: `0`

## Canonical asset reconciliation

- `about_master.png` is present in the audited release tree.
- Repository blob SHA: `8e372fdf984f58d7afcda4b1bac7d03c3663d805`
- The binary is preserved from the existing canonical-workspace asset; it was not recreated or redrawn.
- `urbion_horizon_about.html` references `/about_master.png` as the immutable visual master.
- The production wrapper exposes the canonical About page at `/about`; `/about.html` is retained only as a compatibility alias that redirects to `/about`.

## Functional evidence

Verified locally in Chromium:

- Mission modal
- Vision modal
- Journey modal
- Syamir profile modal
- Alea profile modal
- Fahmi profile modal
- Education / UiTM modal
- Theme toggle / ARIA state
- Modal close controls
- Transparent navigation hitboxes

## Release gate

Do not replace the raster master with reconstructed CSS artwork. The visual benchmark is considered passed only when a browser screenshot at the fixed 1600x900/DPR1 benchmark has zero changed pixels against the locked reference.

The visual master is now present in the release tree. Final production status still remains locked until the overall release SHA, CI, Render configuration, and live smoke are proven together.

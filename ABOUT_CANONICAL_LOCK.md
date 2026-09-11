# URBION HORIZON — About Us Canonical Visual Lock

Status: LOCAL VISUAL MASTER VERIFIED
Benchmark: 1600x900, DPR 1, Chromium

## Exact visual evidence

- Reference SHA-256: `ce66478f62bff81397985a424646361e7fe723607bd4e115db3d9820ff82e643`
- Canonical visual strategy: immutable raster master + transparent HTML interaction hitboxes.
- Browser screenshot result: pixel-identical to reference.
- Max pixel difference: `0`
- Changed pixels: `0`
- JavaScript page errors: `0`
- Hitboxes audited: `22`
- Hitbox overlaps: `0`

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

The latest local candidate is intentionally not marked as deployed here because the exact binary raster master still needs to be transferred into the repository/deployment artifact without alteration.

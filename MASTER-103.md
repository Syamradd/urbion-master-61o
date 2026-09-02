# MASTER-103 — Development Intensity

Adds a deterministic planning-analysis layer that converts supplied lot area and plot ratio into **indicative GFA**.

Example: 5,000 m² × 4.5 = 22,500 m² indicative GFA.

## Guardrails
- Missing or invalid area/plot ratio returns `EVIDENCE REQUIRED`.
- Intensity bands are descriptive (`LOW`, `MODERATE`, `HIGH`), not statutory thresholds.
- GFA is explicitly indicative and must not be presented as development approval or a verified planning control.

## Next
Bind the intensity layer to the GIS workspace so lot size and development intensity are visible together, then connect verified land-use/zoning evidence where available.

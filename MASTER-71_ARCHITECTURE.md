# URBION HORIZON — MASTER-71 Architecture Lock

MASTER-71 is the engineering-hardening checkpoint after the MASTER-70 championship freeze.

## Decision pipeline

`SITE INPUT → SPATIAL/TOD → TYPOLOGY → POLICY RETRIEVAL → APPLICABILITY → COMPLIANCE → SUITABILITY → RECOMMENDATION → EVIDENCE → TRACE`

## Product layers

1. **Spatial intelligence** — coordinates, TOD distance and spatial band.
2. **Planning intelligence** — typology-aware RT MBMB 2035 rule retrieval for covered MBMB cases.
3. **Compliance engine** — explicit COMPLY / NON-COMPLIANCE / REVIEW / NOT APPLICABLE outcomes.
4. **Suitability layer** — transparent screening indicators; never presented as statutory approval.
5. **Evidence intelligence** — source state is preserved and unsafe states cannot become verified evidence.
6. **Decision trace** — every assessment exposes the reasoning stages that led to the outcome.
7. **Demo intelligence** — deterministic scenarios allow judges to reproduce the same outcomes.

## External-source boundary

PBT GIS / MelGIS, i-Plan, JUPEM, MyGEMS and MyEQMS remain explicitly represented according to their verified connector/evidence state. URBION must not manufacture live parcel, cadastral, geology, environmental or zoning evidence.

## Judge objective

The strongest demonstration is not a perfect-looking answer. It is an explainable answer that clearly separates **verified rule evidence**, **screening analytics**, and **evidence gaps requiring planner/authority verification**.

## Release criterion

Any future MASTER must preserve the deterministic demo contract and evidence-safety policy before new intelligence is added.

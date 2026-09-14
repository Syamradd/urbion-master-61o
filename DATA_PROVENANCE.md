# URBION HORIZON — Data & Source Provenance

## Current official PLANMalaysia references traced for the planning workspace

| Source | Current evidence | Use in URBION |
|---|---|---|
| PLANMalaysia, **Manual Sistem Maklumat Geografi (GIS) Rancangan Pemajuan Versi 3.0** (2025) | Official MyPLAN publication and manual; Chapter 3 covers Guna Tanah classification and colour codes | Canonical GT1 → GT2 → GT3 taxonomy |
| PLANMalaysia official portal announcement, **Manual Sistem Maklumat Geografi (GIS) Rancangan Pemajuan Versi 3** | Published 9 Apr 2025; describes standardisation of geospatial data, metadata, land-use codes and planning database structure | Source provenance / release trace |
| PLANMalaysia, **Panduan Perancangan dan Pengurusan Kawasan Sensitif Alam Sekitar (PPP KSAS)** | States that planning-data layers should follow the latest GIS Rancangan Pemajuan manual; references KSAS, topography, risk and related layer groups | Layer/category organisation and environmental-risk provenance |

## Taxonomy guardrails

- Commercial GT1 term: **Komersial**.
- Legacy **Perdagangan** must not appear in the visible canonical selectors.
- Cascading hierarchy is **Guna Tanah 1 → Guna Tanah 2 → Guna Tanah 3 / Activity**.

## Runtime source boundary

URBION uses live service context and returned evidence where available. It does not present live-source context as automatic statutory approval or final authority determination.

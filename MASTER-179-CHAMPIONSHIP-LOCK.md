# MASTER-179 — Championship Lock

MASTER-178 is CI-verified. This lock freezes the judge-facing release path:

**Site Assessment → Map Studio → Evidence → What-If → Decision Center → Planner Review → KM/OSC**

Hard boundaries remain: invalid spatial placeholders are rejected; evidence provenance is explicit; remote values are escaped; What-If exposes baseline/scenario delta; KM/OSC is workflow support only and never statutory approval.

A future release must pass the full GitHub Actions regression gate before being considered GREEN.

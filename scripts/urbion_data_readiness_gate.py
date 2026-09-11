#!/usr/bin/env python3
"""Static readiness gate for URBION's planning data, AI and evidence stack."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRITICAL = {
    "workspace": [
        "landing_server.py", "workspace_v5.html", "urbion_workspace_final.js",
        "urbion_workspace_bridge.js", "urbion_workspace_runtime.js",
    ],
    "ai": [
        "urbion_agent_api.py", "urbion_agent_orchestrator.py", "urbion_copilot.py",
        "urbion_copilot_api.py", "urbion_llm_provider.py",
    ],
    "retrieval": [
        "urbion_retrieval.py", "urbion_knowledge_orchestrator.py", "urbion_knowledge_api.py",
        "urbion_evidence.py", "urbion_evidence_ledger.py", "urbion_evidence_quality.py",
    ],
    "planning": [
        "urbion_rules.py", "urbion_applicability.py", "urbion_compliance.py",
        "urbion_guideline_intelligence.py", "urbion_planning_sources.py", "urbion_iplan.py",
        "urbion_landuse_zoning.py", "urbion_kebenaran_merancang.py",
    ],
    "spatial": [
        "urbion_spatial.py", "urbion_spatial_intelligence.py", "urbion_spatial_context.py",
        "urbion_gis_binding.py", "urbion_gis_lot.py", "urbion_cadastral_context.py",
        "urbion_network_intelligence.py", "urbion_live_stations.py",
    ],
    "sources": [
        "urbion_data_sources.py", "urbion_multi_source.py", "urbion_public_sources.py",
        "urbion_myeqms_adapter.py", "urbion_development_impact.py",
        "urbion_environment_intelligence.py", "urbion_lcp_intelligence.py",
    ],
}


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def main() -> None:
    for group, names in CRITICAL.items():
        missing = [n for n in names if not (ROOT / n).is_file()]
        if missing:
            fail(f"{group} modules missing: {', '.join(missing)}")
        ok(f"{group} module set present ({len(names)})")

    texts = {name: (ROOT / name).read_text(encoding="utf-8") for names in CRITICAL.values() for name in names}

    llm = texts["urbion_llm_provider.py"]
    for token in ("GEMINI_API_KEY", "deterministic_source", "Never say a proposal is approved"):
        if token not in llm:
            fail(f"LLM safety contract missing: {token}")
    ok("bounded optional LLM narrative contract present")

    rag = texts["urbion_knowledge_orchestrator.py"] + texts["urbion_retrieval.py"]
    for token in ("urbion_retrieve_rules", "source_register", "evidence_boundary", "traceability"):
        if token.lower() not in rag.lower():
            fail(f"knowledge/RAG grounding token missing: {token}")
    ok("traceable deterministic retrieval/RAG foundation present")

    rules = texts["urbion_rules.py"]
    required_rule_ids = (
        "RT-MBMB-2035-COM-01", "RT-MBMB-2035-COM-02", "RT-MBMB-2035-COM-03",
        "RT-MBMB-2035-COM-04", "RT-MBMB-2035-TOD-01", "RT-MBMB-2035-TOD-02",
    )
    missing_rules = [rid for rid in required_rule_ids if rid not in rules]
    if missing_rules:
        fail("core RT MBMB rule IDs missing: " + ", ".join(missing_rules))
    ok("core RT MBMB deterministic rule set present")

    compliance = texts["urbion_compliance.py"]
    for token in ("urbion_evaluate_compliance", "urbion_calculate_overall_status", "REQUIRES REVIEW", "source_document", "source_section"):
        if token not in compliance:
            fail(f"compliance trace contract missing: {token}")
    ok("compliance + provenance trace contract present")

    guideline = texts["urbion_guideline_intelligence.py"]
    for token in ("GUIDELINES", "CANDIDATE_REVIEW", "statutory_verification", "PLANMalaysia"):
        if token not in guideline:
            fail(f"guideline intelligence contract missing: {token}")
    ok("GP/guideline applicability boundary present")

    agent = texts["urbion_agent_api.py"]
    for route in ("/agents/run", "/copilot/run", "/copilot/explain", "/intelligence/decision-os", "/planner/handoff"):
        if route not in agent:
            fail(f"AI orchestration route missing: {route}")
    ok("AI orchestration API routes present")

    workspace = texts["workspace_v5.html"] + texts["urbion_workspace_final.js"] + texts["urbion_workspace_runtime.js"]
    for token in ("/workstation/analysis", "/what-if", "/decision-center", "/map/layers", "landuse1", "landuse2", "landuse3", "#runtimeHelp"):
        if token not in workspace:
            fail(f"workspace integration token missing: {token}")
    ok("workspace-to-engine integration contracts present")

    all_source = "\n".join(texts.values())
    if re.search(r"AIza[0-9A-Za-z_-]{20,}", all_source):
        fail("possible hard-coded Google API key detected")
    ok("no obvious hard-coded API key pattern detected")

    print("URBION DATA READINESS GATE: PASS")
    print("External data freshness, adopted-plan currency and authority-specific verification remain runtime/source-specific checks.")


if __name__ == "__main__":
    main()

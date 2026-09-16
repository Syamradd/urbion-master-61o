"""Unified bounded planner copilot orchestration for URBION HORIZON.

The copilot composes existing deterministic planning services into one
traceable packet. It does not call an LLM, grant statutory approval, or
upgrade source context into verified evidence.
"""
import server
from urbion_knowledge_orchestrator import build_knowledge_pack
from urbion_spatial_intelligence import build_spatial_intelligence
from urbion_impact_intelligence import build_impact_intelligence
from urbion_decision_center import build_decision_center
from urbion_agent_orchestrator import run_agents
from urbion_what_if import execute_what_if
from urbion_scenario_ranking import rank_scenarios
from urbion_evidence_ledger import build_evidence_ledger
from urbion_evidence_quality import build_evidence_quality
from server import AssessmentRequest
from urbion_network_intelligence import network_distance_m
from urbion_canonical_evidence import build_canonical_evidence_packet


def _lcp_data_readiness(*, assessment: dict, canonical_packet: dict, spatial: dict, knowledge: dict, impact: dict, evidence_ledger: dict) -> dict:
    """Build a deterministic, non-statutory LCP-oriented data acquisition plan."""
    proposal = assessment.get("proposal") or {}
    site = assessment.get("site") or {}
    evidence = canonical_packet.get("evidence") or {}
    site_analysis = assessment.get("site_analysis") or {}
    rules = assessment.get("retrieved_rules") or []
    review_gaps = list(canonical_packet.get("review_gaps", []) or [])
    ledger_items = evidence_ledger.get("items") or evidence_ledger.get("evidence") or []

    def present(label: str, value, source: str, verification: str = "REVIEW_REQUIRED", note: str = "") -> dict:
        has_value = value not in (None, "", [], {})
        return {
            "id": label.lower().replace(" ", "_"),
            "label": label,
            "status": "AVAILABLE" if has_value else "MISSING",
            "value": value if has_value else None,
            "source_target": source,
            "verification": verification,
            "note": note or ("Evidence is present in the canonical packet." if has_value else "Not available from the current canonical packet; obtain or verify before use."),
        }

    spatial_value = spatial.get("metrics") or evidence.get("spatial") or site_analysis
    environment_value = evidence.get("environment") or {}
    station_value = evidence.get("stations") or {}
    impact_value = impact or evidence.get("development_impact") or {}
    access_value = spatial.get("network_access") or spatial.get("road_distance_m") or (site_analysis.get("road_distance_m") if isinstance(site_analysis, dict) else None)
    zoning_value = knowledge.get("policy_graph") or knowledge.get("guidelines") or assessment.get("policy_coverage")
    cadastral_value = canonical_packet.get("cadastral_identity") or {}
    source_registry = evidence.get("source_registry") or []

    fields = [
        present("Site / project identity", {k: site.get(k) for k in ("project_name", "state", "district", "pbt", "lot_no", "latitude", "longitude") if site.get(k) not in (None, "")}, "Project input + authoritative cadastral/i-Plan verification", "VERIFICATION_REQUIRED", "Confirm parcel identity and project reference against the authoritative parcel source."),
        present("Existing land use", spatial_value, "PLANMalaysia i-Plan / local planning source", "SOURCE_REVIEW_REQUIRED", "Use the thematic current-land-use source and preserve its legend/source context."),
        present("Zoning / planning designation", zoning_value, "Applicable local plan / PLANMalaysia planning source", "SOURCE_REVIEW_REQUIRED", "Confirm the current statutory planning designation and applicability."),
        present("Development proposal parameters", {k: proposal.get(k) for k in ("development_type", "units", "site_area_ha", "commercial_gfa_m2", "population", "jobs", "daily_trips", "ratio") if proposal.get(k) not in (None, "")}, "User/project input + calculation model", "USER_REVIEW_REQUIRED", "Enter missing proposal quantities explicitly; calculated values must retain their CALCULATED state."),
        present("Site suitability / spatial screening", site_analysis, "URBION deterministic spatial assessment", "CALCULATED", "Screening evidence is not statutory approval and should be retained as decision-support context."),
        present("Cadastral / parcel evidence", cadastral_value, "JUPEM / PTD / authoritative parcel source", "VERIFICATION_REQUIRED", "Cadastral identity is deliberately kept separate from statutory verification."),
        present("Road access / mobility context", access_value, "Authoritative road/network source + site verification", "VERIFICATION_REQUIRED", "Verify access, hierarchy and any required traffic/access study inputs."),
        present("Flood / environmental constraints", environment_value, "JPS / JAS / PLANMalaysia environmental datasets", "SOURCE_REVIEW_REQUIRED", "Use live/source-context observations only within their stated evidence boundary."),
        present("Nearest live monitoring stations", station_value, "JPS Public Infobanjir / JAS MyEQMS / configured APIMS source", "SOURCE_CONTEXT", "Live station observations support context; they do not by themselves establish statutory compliance."),
        present("Development impact screening", impact_value, "URBION impact model + authoritative technical inputs", "CALCULATED", "Validate all missing assumptions and replace screening assumptions with project evidence where required."),
        present("Planning rules / controls", rules, "Applicable local plan, guideline and authority source", "SOURCE_REVIEW_REQUIRED", "Each rule should retain a source locator/page/clause/table before being relied upon."),
        present("Agency / technical coordination evidence", assessment.get("agency_comments") or assessment.get("technical_reviews") or {}, "Relevant technical agencies / OSC coordination", "VERIFICATION_REQUIRED", "Collect current agency requirements and retain correspondence/comment references."),
        present("Evidence register / traceability", {"item_count": len(ledger_items), "source_count": len(source_registry), "review_gap_count": len(review_gaps)}, "URBION canonical evidence ledger", "CALCULATED", "Use the evidence ledger to trace each substantive planning statement back to a source or calculation."),
    ]
    available = [x for x in fields if x["status"] == "AVAILABLE"]
    missing = [x for x in fields if x["status"] == "MISSING"]
    actions = [{"field": x["label"], "action": f"Obtain or verify {x['label'].lower()}.", "source_target": x["source_target"], "verification": x["verification"]} for x in missing]
    for gap in review_gaps[:8]:
        actions.append({"field": "Review gap", "action": str(gap), "source_target": "See canonical evidence trace", "verification": "REVIEW_REQUIRED"})
    return {
        "status": "READY" if not missing else "PARTIAL",
        "scope": "LCP_ORIENTED_DATA_READINESS",
        "disclaimer": "This checklist supports LCP preparation and evidence collection; it is not a legal declaration of all statutory LCP requirements.",
        "available_fields": available,
        "missing_fields": missing,
        "acquisition_actions": actions[:20],
        "available_count": len(available),
        "missing_count": len(missing),
        "review_gap_count": len(review_gaps),
    }


def _enrich_canonical_packet(packet: dict, *, spatial: dict, knowledge: dict, impact: dict, scenarios: dict, decision: dict, evidence_ledger: dict, evidence_quality: dict) -> dict:
    """Attach deterministic downstream intelligence to the one canonical packet."""
    packet = dict(packet or {})
    evidence = dict(packet.get("evidence") or {})
    evidence.update({
        "spatial": spatial or {},
        "development_impact": impact or {},
        "policy_graph": knowledge.get("policy_graph") if isinstance(knowledge, dict) else {},
    })
    packet["evidence"] = evidence
    packet["knowledge"] = knowledge or {}
    packet["what_if"] = scenarios or {}
    packet["decision_center"] = decision or {}
    packet["evidence_ledger"] = evidence_ledger or {}
    packet["evidence_quality"] = evidence_quality or {}
    packet["review_gaps"] = list(dict.fromkeys(list(packet.get("review_gaps", []) or []) + list((impact or {}).get("review_gaps", []) or []) + list((scenarios or {}).get("review_gaps", []) or []) + list((decision or {}).get("review_gaps", []) or [])))
    packet["trace"] = "SITE → SPATIAL → POLICY → ENVIRONMENT/IMPACT → WHAT-IF → DECISION → REVIEW"
    packet["convergence"] = {"status": "CANONICAL", "downstream_modules": ["SPATIAL", "KNOWLEDGE", "IMPACT", "WHAT_IF", "DECISION", "EVIDENCE_LEDGER", "EVIDENCE_QUALITY"]}
    packet["statutory_verification"] = "NOT_CLAIMED"
    return packet


def build_copilot_packet(inputs: dict, variants=None, radii=(400, 800), constraints=None,
                         environmental_context=None, canonical_evidence_packet=None):
    raw = dict(inputs or {})
    assessment = server.assess_core(AssessmentRequest(**raw))
    site = assessment["site"]
    canonical_packet = canonical_evidence_packet if isinstance(canonical_evidence_packet, dict) else build_canonical_evidence_packet(
        assessment=assessment,
        spatial=assessment.get("site_analysis"),
        environment=assessment.get("evidence_intelligence"),
        policy_graph={"policy_coverage": assessment.get("policy_coverage")},
    )
    spatial = build_spatial_intelligence(site["latitude"], site["longitude"], raw.get("tod_lat"), raw.get("tod_lon"), tuple(radii or (400, 800)), constraints, environmental_context)
    if environmental_context:
        spatial["environment"] = environmental_context
        spatial["evidence_model"]["environmental_overlay"] = "SOURCE_CONTEXT ONLY"
    network_target = raw.get("network_target_lat"), raw.get("network_target_lon")
    if all(value is not None for value in network_target):
        spatial["network_access"] = network_distance_m(site["latitude"], site["longitude"], float(network_target[0]), float(network_target[1]))
        spatial["evidence_model"]["network_access"] = spatial["network_access"].get("evidence_state", "UNVERIFIED")
    knowledge = build_knowledge_pack(assessment.get("development_type") or raw.get("development_type") or "", site.get("pbt") or raw.get("pbt") or "MBMB", spatial)
    impact = build_impact_intelligence(spatial=spatial, assessment=assessment, environmental_context=environmental_context)
    variant_list = variants or []
    if not isinstance(variant_list, list) or len(variant_list) > 12:
        raise ValueError("variants must be a list with at most 12 items")
    if variant_list:
        scenario_intelligence = execute_what_if(raw, variant_list, lambda scenario_inputs: server.assess_core(AssessmentRequest(**scenario_inputs)))
        scenario_intelligence = rank_scenarios(scenario_intelligence)
        scenario_intelligence["status"] = "COMPLETE"
        scenario_intelligence["count"] = len(scenario_intelligence.get("scenarios", []))
    else:
        scenario_intelligence = {
            "title": "What-If Scenario Comparison", "version": "PHASE-D.2", "baseline": assessment,
            "baseline_status": assessment.get("final_status", "REQUIRES REVIEW"),
            "baseline_score": (assessment.get("site_analysis", {}) or {}).get("score", 0),
            "scenarios": [], "ranked_scenarios": [], "best_candidate": None, "count": 0,
            "status": "SKIPPED", "decision_pathway": ["Supply scenario variants to run a comparative What-If analysis."],
            "disclaimer": "Scenario comparison is decision support only; it does not replace statutory assessment or authority review.",
        }
    decision = build_decision_center(assessment=assessment, scenario_comparison=scenario_intelligence)
    agent_packet = run_agents(assessment=assessment, spatial=spatial, knowledge=knowledge, scenarios=scenario_intelligence if scenario_intelligence["count"] else None, decision=decision)
    ranked = scenario_intelligence.get("ranked_scenarios", [])
    preferred = ranked[0] if ranked else None
    evidence_ledger = build_evidence_ledger(assessment=assessment, spatial=spatial, knowledge=knowledge, impact=impact, scenarios=scenario_intelligence, decision=decision)
    evidence_quality = build_evidence_quality(evidence_ledger)
    canonical_packet = _enrich_canonical_packet(canonical_packet, spatial=spatial, knowledge=knowledge, impact=impact, scenarios=scenario_intelligence, decision=decision, evidence_ledger=evidence_ledger, evidence_quality=evidence_quality)
    lcp_data_readiness = _lcp_data_readiness(assessment=assessment, canonical_packet=canonical_packet, spatial=spatial, knowledge=knowledge, impact=impact, evidence_ledger=evidence_ledger)
    next_actions = [
        "Review retrieved policy evidence and source traceability.",
        "Validate spatial and environmental context against authoritative sources.",
        "Review impact gaps before relying on any planning recommendation.",
    ]
    if lcp_data_readiness["missing_count"]:
        next_actions.insert(0, f"Collect or verify {lcp_data_readiness['missing_count']} LCP-oriented data area(s) listed in lcp_data_readiness before finalising the LCP evidence base.")
    if preferred:
        next_actions.insert(0, f"Review ranked scenario {preferred} and verify its evidence before advancing.")
    else:
        next_actions.append("Use What-If scenarios before preparing an LCP handoff.")
    explanation = {
        "source": "CANONICAL_EVIDENCE_PACKET",
        "status": canonical_packet.get("assessment", {}).get("final_status"),
        "review_gaps": list(canonical_packet.get("review_gaps", [])),
        "statutory_verification": canonical_packet.get("statutory_verification", "NOT_CLAIMED"),
        "instruction": "Explain only what is present in the canonical evidence packet; do not invent rules, approvals, scores, or verified status.",
        "lcp_data_readiness": lcp_data_readiness,
    }
    return {
        "mode": "BOUNDED_PLANNER_COPILOT", "assessment": assessment, "spatial": spatial, "knowledge": knowledge,
        "impact": impact, "scenario_intelligence": scenario_intelligence, "preferred_scenario": preferred,
        "agents": agent_packet, "decision": decision, "evidence_ledger": evidence_ledger,
        "evidence_quality": evidence_quality, "lcp_data_readiness": lcp_data_readiness, "canonical_evidence_packet": canonical_packet,
        "explanation": explanation,
        "next_actions": next_actions[:7], "decision_authority": "NONE", "statutory_verification": "NOT_CLAIMED",
        "generation_boundary": "CANONICAL_PACKET_ONLY; DETERMINISTIC_CONTEXT_ONLY; FUTURE_GENERATION_MUST_PRESERVE_TRACEABILITY",
    }

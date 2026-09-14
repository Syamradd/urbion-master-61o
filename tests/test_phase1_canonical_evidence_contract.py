from urbion_canonical_evidence import EVIDENCE_STATES, PACKET_VERSION, build_canonical_evidence_packet


def test_packet_preserves_core_assessment_and_states():
    packet = build_canonical_evidence_packet(
        assessment={
            "project": "URBION",
            "site": {"state": "Melaka", "district": "Melaka Tengah", "pbt": "Majlis Bandaraya Melaka Bersejarah", "lot_no": "11213"},
            "final_status": "COMPLY",
            "classification": "TOD 400m",
            "decision_confidence": {"score": 90, "band": "HIGH"},
            "recommendation": {"headline": "PROCEED WITH PLANNER REVIEW"},
            "policy_coverage": {"coverage": "FULL_RULE_ENGINE"},
            "retrieved_rules": [{"rule_id": "RT-MBMB-2035-TOD-01"}],
            "evidence_state": {"site_coordinates": "USER_PROVIDED", "tod_distance": "CALCULATED"},
            "decision_trace": "SITE → TOD → POLICY → COMPLIANCE → DECISION",
            "source_registry": [{"source": "PLANMalaysia / Rancangan Tempatan", "status": "REFERENCE_REGISTERED"}],
        },
        spatial={"review_gaps": ["terrain"]},
        environment={"review_gaps": ["environment:water_quality"]},
    )
    assert packet["version"] == PACKET_VERSION == "PHASE1.2"
    assert packet["assessment"]["final_status"] == "COMPLY"
    assert packet["identity"]["lot_no"] == "11213"
    assert packet["evidence_states"]["tod_distance"] == "CALCULATED"
    assert packet["review_gaps"] == [
        "terrain",
        "environment:water_quality",
        "RT-MBMB-2035-TOD-01: exact page/clause/table locator and current applicability require review (planning source).",
    ]
    assert packet["statutory_verification"] == "NOT_CLAIMED"


def test_invalid_evidence_state_is_downgraded_to_unverified():
    packet = build_canonical_evidence_packet(
        assessment={"evidence_state": {"site_coordinates": "MAGIC_VERIFIED"}}
    )
    assert packet["identity"]["identity_evidence"] == "UNVERIFIED"


def test_evidence_states_are_closed_vocabulary():
    assert EVIDENCE_STATES == ("USER_PROVIDED", "CALCULATED", "SOURCE_CONTEXT", "VERIFIED", "UNVERIFIED")

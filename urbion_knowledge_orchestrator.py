"""Bounded knowledge/RAG foundation for URBION HORIZON.

This module deliberately separates retrieval from verification and generation.
It creates a deterministic knowledge pack from the existing rule and evidence
layers so future LLM/RAG adapters can consume traceable context safely.
"""
from urbion_retrieval import urbion_retrieve_rules


def build_knowledge_pack(development_type, authority="MBMB", spatial_context=None):
    spatial_context = spatial_context or {}
    rules = urbion_retrieve_rules(
        development_type=development_type,
        authority=authority,
        spatial_context=spatial_context,
    )
    sources = []
    for rule in rules:
        source = {
            "source_document": rule.get("source_document"),
            "source_section": rule.get("source_section"),
            "evidence_classification": rule.get("evidence_classification"),
            "traceability": rule.get("traceability"),
        }
        if source not in sources:
            sources.append(source)
    return {
        "mode": "DETERMINISTIC_RETRIEVAL",
        "development_type": development_type or "",
        "authority": authority or "MBMB",
        "candidate_rules": rules,
        "source_register": sources,
        "retrieval_count": len(rules),
        "evidence_boundary": "RETRIEVAL_IS_NOT_STATUTORY_VERIFICATION",
        "generation_ready": True,
        "generation_policy": "Any future generated answer must preserve source traceability and must not upgrade SOURCE_CONTEXT into VERIFIED evidence.",
    }

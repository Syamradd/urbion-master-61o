# ============================================================
# 🏙️ URBION COMPLIANCE ENGINE
# ============================================================


def _parse_ratio(value):
    """Convert ratio strings such as 1:6.0 into the denominator."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if ":" in text:
        try:
            return float(text.split(":")[-1])
        except ValueError:
            return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_numeric(value):
    """Convert common numeric proposal values into float."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    for word in ("storeys", "storey", "m", "metres", "meter", "meters", "ha"):
        text = text.replace(word, "")
    try:
        return float(text.strip())
    except ValueError:
        return None


def _reference_trace(item):
    """Expose rule provenance without inventing a page/clause not stored in the rule DB."""
    document = item.get("source_document")
    section = item.get("source_section")
    page = item.get("source_page")
    clause = item.get("source_clause")
    return {
        "document": document,
        "section": section,
        "page": page,
        "clause": clause,
        "page_status": "AVAILABLE" if page is not None else "NOT_ESTABLISHED",
        "clause_status": "AVAILABLE" if clause else "NOT_ESTABLISHED",
        "reference": " / ".join(str(x) for x in (document, section) if x),
    }


def urbion_evaluate_compliance(applicability_results, proposal):
    """Evaluate compliance after applicability has been determined."""
    results = []

    for item in applicability_results:
        rule_id = item.get("rule_id", "")
        parameter = item.get("parameter", "")
        requirement = item.get("requirement", "")
        applicability = item.get("applicability", "")
        proposed = proposal.get(parameter)

        if applicability == "NOT APPLICABLE":
            status = "NOT APPLICABLE"
            reason = "The planning rule does not apply to the proposed development typology."
        elif applicability in ("REQUIRES SPATIAL VERIFICATION", "REQUIRES TYPOLOGY VERIFICATION", "REQUIRES REVIEW"):
            status = "REQUIRES REVIEW"
            reason = item.get("reason", "Applicability remains unverified.")
        elif applicability == "APPLICABLE":
            if rule_id == "RT-MBMB-2035-COM-02":
                proposed_value = _parse_numeric(proposed)
                required_value = 3.0
                if proposed_value is None:
                    status = "REQUIRES REVIEW"
                    reason = "A valid numeric perimeter planting value could not be established."
                elif proposed_value >= required_value:
                    status = "COMPLY"
                    reason = f"Proposed {proposed_value:.1f} m meets the minimum requirement of {required_value:.1f} m."
                else:
                    status = "CONDITIONAL NON-COMPLIANCE"
                    reason = f"Proposed {proposed_value:.1f} m is below the minimum requirement of {required_value:.1f} m."
            elif rule_id == "RT-MBMB-2035-COM-01":
                proposed_value = _parse_ratio(proposed)
                required_value = 6.0
                if proposed_value is None:
                    status = "REQUIRES REVIEW"
                    reason = "A valid plot ratio could not be established."
                elif proposed_value <= required_value:
                    status = "COMPLY"
                    reason = f"Proposed plot ratio 1:{proposed_value:g} is within the maximum requirement of 1:{required_value:g}."
                else:
                    status = "NON-COMPLIANCE"
                    reason = f"Proposed plot ratio 1:{proposed_value:g} exceeds the maximum requirement of 1:{required_value:g}."
            elif rule_id == "RT-MBMB-2035-COM-03":
                proposed_value = _parse_numeric(proposed)
                required_value = 1.5
                if proposed_value is None:
                    status = "REQUIRES REVIEW"
                    reason = "A valid numeric walkway value could not be established."
                elif proposed_value >= required_value:
                    status = "COMPLY"
                    reason = f"Proposed {proposed_value:.1f} m meets the minimum requirement of {required_value:.1f} m."
                else:
                    status = "NON-COMPLIANCE"
                    reason = f"Proposed {proposed_value:.1f} m is below the minimum requirement of {required_value:.1f} m."
            elif rule_id == "RT-MBMB-2035-COM-04":
                proposed_value = _parse_numeric(proposed)
                required_value = 4
                if proposed_value is None:
                    status = "REQUIRES REVIEW"
                    reason = "A valid building height could not be established."
                elif proposed_value <= required_value:
                    status = "COMPLY"
                    reason = f"Proposed {proposed_value:g} storeys is within the maximum requirement of {required_value:g} storeys."
                else:
                    status = "NON-COMPLIANCE"
                    reason = f"Proposed {proposed_value:g} storeys exceeds the maximum requirement of {required_value:g} storeys."
            elif rule_id in ("RT-MBMB-2035-TOD-01", "RT-MBMB-2035-TOD-02"):
                proposed_value = _parse_ratio(proposed)
                required_value = 4.5 if rule_id == "RT-MBMB-2035-TOD-01" else 4.0
                if proposed_value is None:
                    status = "REQUIRES REVIEW"
                    reason = "A valid plot ratio could not be established."
                elif proposed_value <= required_value:
                    status = "COMPLY"
                    reason = f"Proposed plot ratio 1:{proposed_value:g} is within the applicable maximum of 1:{required_value:g}."
                else:
                    status = "NON-COMPLIANCE"
                    reason = f"Proposed plot ratio 1:{proposed_value:g} exceeds the applicable maximum of 1:{required_value:g}."
            else:
                status = "REQUIRES REVIEW"
                reason = "No deterministic compliance comparison has been established for this rule."
        else:
            status = "REQUIRES REVIEW"
            reason = "Applicability status is not recognised by the Compliance Engine."

        reference_trace = _reference_trace(item)
        results.append({
            "rule_id": rule_id,
            "parameter": parameter,
            "proposed": proposed,
            "requirement": requirement,
            "applicability": applicability,
            "status": status,
            "reason": reason,
            "why": reason,
            "source_document": item.get("source_document"),
            "source_section": item.get("source_section"),
            "source_page": item.get("source_page"),
            "source_clause": item.get("source_clause"),
            "reference_trace": reference_trace,
            "evidence_text": item.get("evidence_text"),
            "evidence_classification": item.get("evidence_classification"),
            "traceability": item.get("traceability"),
        })

    return results

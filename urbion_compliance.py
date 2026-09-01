
# ============================================================
# 🏙️ URBION COMPLIANCE ENGINE
# ============================================================

def _parse_ratio(value):
    """
    Convert ratio strings such as:

        1:6.0
        1:4.5

    into their numeric denominator.
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if ":" in text:

        try:

            return float(
                text.split(":")[-1]
            )

        except ValueError:

            return None

    try:

        return float(text)

    except ValueError:

        return None


def _parse_numeric(value):
    """
    Convert common numeric proposal values
    into float.
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):

        return float(value)

    text = str(value).strip()

    # Remove common units / words
    replacements = [
        "storeys",
        "storey",
        "m",
        "metres",
        "meter",
        "meters",
        "ha",
    ]

    for word in replacements:

        text = text.replace(
            word,
            ""
        )

    try:

        return float(
            text.strip()
        )

    except ValueError:

        return None


def urbion_evaluate_compliance(
    applicability_results,
    proposal
):
    """
    Evaluate compliance after applicability
    has been determined.

    IMPORTANT:

    Rules requiring spatial or typology verification
    are NOT automatically treated as non-compliant.

    They remain REQUIRES REVIEW.
    """

    results = []


    # ========================================================
    # EVALUATE EACH RULE
    # ========================================================

    for item in applicability_results:

        rule_id = item.get(
            "rule_id",
            ""
        )

        parameter = item.get(
            "parameter",
            ""
        )

        requirement = item.get(
            "requirement",
            ""
        )

        applicability = item.get(
            "applicability",
            ""
        )

        # ----------------------------------------------------
        # PROPOSED VALUE
        # ----------------------------------------------------

        proposed = proposal.get(
            parameter
        )


        # ====================================================
        # APPLICABILITY GATE
        # ====================================================

        if applicability == (
            "NOT APPLICABLE"
        ):

            status = (
                "NOT APPLICABLE"
            )

            reason = (
                "The planning rule does not apply "
                "to the proposed development typology."
            )


        elif applicability in (
            "REQUIRES SPATIAL VERIFICATION",
            "REQUIRES TYPOLOGY VERIFICATION",
            "REQUIRES REVIEW"
        ):

            status = (
                "REQUIRES REVIEW"
            )

            reason = (
                item.get(
                    "reason",
                    "Applicability remains unverified."
                )
            )


        # ====================================================
        # APPLICABLE RULES
        # ====================================================

        elif applicability == "APPLICABLE":

            # ------------------------------------------------
            # PERIMETER PLANTING
            # ------------------------------------------------

            if rule_id == (
                "RT-MBMB-2035-COM-02"
            ):

                proposed_value = (
                    _parse_numeric(
                        proposed
                    )
                )

                required_value = 3.0

                if proposed_value is None:

                    status = (
                        "REQUIRES REVIEW"
                    )

                    reason = (
                        "A valid numeric perimeter "
                        "planting value could not be established."
                    )

                elif proposed_value >= required_value:

                    status = "COMPLY"

                    reason = (
                        f"Proposed {proposed_value:.1f} m "
                        f"meets the minimum requirement "
                        f"of {required_value:.1f} m."
                    )

                else:

                    status = (
                        "CONDITIONAL NON-COMPLIANCE"
                    )

                    reason = (
                        f"Proposed {proposed_value:.1f} m "
                        f"is below the minimum requirement "
                        f"of {required_value:.1f} m."
                    )


            # ------------------------------------------------
            # COM-01 — PLOT RATIO
            # ------------------------------------------------

            elif rule_id == (
                "RT-MBMB-2035-COM-01"
            ):

                proposed_value = (
                    _parse_ratio(
                        proposed
                    )
                )

                required_value = 6.0

                if proposed_value is None:

                    status = (
                        "REQUIRES REVIEW"
                    )

                    reason = (
                        "A valid plot ratio could not "
                        "be established."
                    )

                elif proposed_value <= required_value:

                    status = "COMPLY"

                    reason = (
                        f"Proposed plot ratio "
                        f"1:{proposed_value:g} "
                        f"is within the maximum "
                        f"requirement of 1:{required_value:g}."
                    )

                else:

                    status = (
                        "NON-COMPLIANCE"
                    )

                    reason = (
                        f"Proposed plot ratio "
                        f"1:{proposed_value:g} "
                        f"exceeds the maximum "
                        f"requirement of 1:{required_value:g}."
                    )


            # ------------------------------------------------
            # COM-03 — WALKWAY
            # ------------------------------------------------

            elif rule_id == (
                "RT-MBMB-2035-COM-03"
            ):

                proposed_value = (
                    _parse_numeric(
                        proposed
                    )
                )

                required_value = 1.5

                if proposed_value is None:

                    status = (
                        "REQUIRES REVIEW"
                    )

                    reason = (
                        "A valid numeric walkway "
                        "value could not be established."
                    )

                elif proposed_value >= required_value:

                    status = "COMPLY"

                    reason = (
                        f"Proposed {proposed_value:.1f} m "
                        f"meets the minimum requirement "
                        f"of {required_value:.1f} m."
                    )

                else:

                    status = (
                        "NON-COMPLIANCE"
                    )

                    reason = (
                        f"Proposed {proposed_value:.1f} m "
                        f"is below the minimum requirement "
                        f"of {required_value:.1f} m."
                    )


            # ------------------------------------------------
            # COM-04 — BUILDING HEIGHT
            # ------------------------------------------------

            elif rule_id == (
                "RT-MBMB-2035-COM-04"
            ):

                proposed_value = (
                    _parse_numeric(
                        proposed
                    )
                )

                required_value = 4

                if proposed_value is None:

                    status = (
                        "REQUIRES REVIEW"
                    )

                    reason = (
                        "A valid building height "
                        "could not be established."
                    )

                elif proposed_value <= required_value:

                    status = "COMPLY"

                    reason = (
                        f"Proposed {proposed_value:g} "
                        f"storeys is within the maximum "
                        f"requirement of {required_value:g} storeys."
                    )

                else:

                    status = (
                        "NON-COMPLIANCE"
                    )

                    reason = (
                        f"Proposed {proposed_value:g} "
                        f"storeys exceeds the maximum "
                        f"requirement of {required_value:g} storeys."
                    )


            # ------------------------------------------------
            # TOD RULES
            # ------------------------------------------------

            elif rule_id in (
                "RT-MBMB-2035-TOD-01",
                "RT-MBMB-2035-TOD-02"
            ):

                proposed_value = (
                    _parse_ratio(
                        proposed
                    )
                )

                if rule_id == (
                    "RT-MBMB-2035-TOD-01"
                ):

                    required_value = 4.5

                else:

                    required_value = 4.0


                if proposed_value is None:

                    status = (
                        "REQUIRES REVIEW"
                    )

                    reason = (
                        "A valid plot ratio could not "
                        "be established."
                    )

                elif proposed_value <= required_value:

                    status = "COMPLY"

                    reason = (
                        f"Proposed plot ratio "
                        f"1:{proposed_value:g} "
                        f"is within the applicable "
                        f"maximum of 1:{required_value:g}."
                    )

                else:

                    status = (
                        "NON-COMPLIANCE"
                    )

                    reason = (
                        f"Proposed plot ratio "
                        f"1:{proposed_value:g} "
                        f"exceeds the applicable "
                        f"maximum of 1:{required_value:g}."
                    )


            # ------------------------------------------------
            # FALLBACK
            # ------------------------------------------------

            else:

                status = (
                    "REQUIRES REVIEW"
                )

                reason = (
                    "No deterministic compliance "
                    "comparison has been established "
                    "for this rule."
                )


        # ====================================================
        # UNKNOWN APPLICABILITY
        # ====================================================

        else:

            status = (
                "REQUIRES REVIEW"
            )

            reason = (
                "Applicability status is not recognised "
                "by the Compliance Engine."
            )


        # ====================================================
        # STORE RESULT
        # ====================================================

        results.append({

            "rule_id":
                rule_id,

            "parameter":
                parameter,

            "proposed":
                proposed,

            "requirement":
                requirement,

            "applicability":
                applicability,

            "status":
                status,

            "reason":
                reason,

            "source_document":
                item.get(
                    "source_document"
                ),

            "source_section":
                item.get(
                    "source_section"
                ),

            "evidence_text":
                item.get(
                    "evidence_text"
                ),

            "evidence_classification":
                item.get(
                    "evidence_classification"
                ),

            "traceability":
                item.get(
                    "traceability"
                )
        })


    return results


# ============================================================
# OVERALL STATUS
# ============================================================

def urbion_calculate_overall_status(
    compliance_results
):
    """
    Calculate an overall assessment status.

    NOT APPLICABLE rules are excluded.

    Any unresolved verification state such as
    REQUIRES REVIEW or REQUIRES TYPOLOGY VERIFICATION
    prevents a full COMPLY result.

    Priority:
    1. NON-COMPLIANCE
    2. CONDITIONAL NON-COMPLIANCE
    3. REQUIRES REVIEW / VERIFICATION
    4. COMPLY
    """

    relevant_results = [
        item
        for item in compliance_results
        if item.get("applicability")
        != "NOT APPLICABLE"
    ]

    statuses = [
        item.get(
            "status",
            ""
        )
        for item in relevant_results
    ]

    # --------------------------------------------------------
    # HARD FAILURE
    # --------------------------------------------------------

    if "NON-COMPLIANCE" in statuses:

        return (
            "🔴 NON-COMPLIANCE"
        )

    # --------------------------------------------------------
    # CONDITIONAL FAILURE
    # --------------------------------------------------------

    if (
        "CONDITIONAL NON-COMPLIANCE"
        in statuses
    ):

        return (
            "🟠 CONDITIONAL RISK"
        )

    # --------------------------------------------------------
    # UNRESOLVED / VERIFICATION REQUIRED
    # --------------------------------------------------------

    review_statuses = {
        "REQUIRES REVIEW",
        "REQUIRES TYPOLOGY VERIFICATION",
        "REQUIRES SPATIAL VERIFICATION",
    }

    if any(
        status in review_statuses
        for status in statuses
    ):

        return (
            "🟡 REQUIRES REVIEW"
        )

    # --------------------------------------------------------
    # FULL COMPLIANCE
    # --------------------------------------------------------

    if relevant_results and all(
        status == "COMPLY"
        for status in statuses
    ):

        return (
            "🟢 COMPLY"
        )

    return (
        "🟡 REQUIRES REVIEW"
    )

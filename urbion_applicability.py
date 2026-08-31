
# ============================================================
# 🏙️ URBION APPLICABILITY ENGINE
# ============================================================

def urbion_check_applicability(
    proposal,
    retrieved_rules
):
    """
    Determine whether each retrieved planning rule is:

    1. APPLICABLE
    2. NOT APPLICABLE
    3. REQUIRES SPATIAL VERIFICATION
    4. REQUIRES TYPOLOGY VERIFICATION

    IMPORTANT:
    This engine does not invent spatial facts.

    If spatial evidence is not verified, the rule remains
    subject to spatial verification.
    """

    results = []

    development_type = (
        proposal.get(
            "development_type",
            ""
        )
        or ""
    ).strip()

    spatial_context = (
        proposal.get(
            "spatial_context",
            {}
        )
        or {}
    )

    tod_verified = bool(
        spatial_context.get(
            "tod_verified",
            False
        )
    )

    tod_distance_m = spatial_context.get(
        "tod_distance_m"
    )

    tod_400_verified = bool(
        tod_verified
        and tod_distance_m is not None
        and float(tod_distance_m) <= 400
    )

    tod_800_verified = bool(
        tod_verified
        and tod_distance_m is not None
        and float(tod_distance_m) <= 800
    )

    shop_frontage_verified = bool(
        spatial_context.get(
            "shop_frontage_verified",
            False
        )
    )

    precinct_verified = bool(
        spatial_context.get(
            "precinct_verified",
            False
        )
    )


    # ========================================================
    # EVALUATE EACH RETRIEVED RULE
    # ========================================================

    for rule in retrieved_rules:

        rule_id = rule.get(
            "rule_id",
            ""
        )

        rule_applicability = rule.get(
            "applicability",
            ""
        )

        status = "REQUIRES REVIEW"

        reason = (
            "Applicability could not be established "
            "from the available evidence."
        )


        # ====================================================
        # COM-01 — PRECINCT-DEPENDENT PLOT RATIO
        # ====================================================

        if rule_id == (
            "RT-MBMB-2035-COM-01"
        ):

            if precinct_verified:

                status = "APPLICABLE"

                reason = (
                    "The proposal's parcel-to-precinct "
                    "relationship has been spatially verified."
                )

            else:

                status = (
                    "REQUIRES SPATIAL VERIFICATION"
                )

                reason = (
                    "Plot ratio is precinct-dependent. "
                    "The proposal is commercial and "
                    "free-standing, but the exact "
                    "parcel-to-precinct relationship "
                    "has not been independently verified."
                )


        # ====================================================
        # COM-02 — PERIMETER PLANTING
        # ====================================================

        elif rule_id == (
            "RT-MBMB-2035-COM-02"
        ):

            if (
                "free-standing"
                in development_type.lower()
            ):

                status = "APPLICABLE"

                reason = (
                    "The rule explicitly refers to "
                    "free-standing buildings and matches "
                    "the proposed development type."
                )

            else:

                status = "NOT APPLICABLE"

                reason = (
                    "The proposal is not identified as "
                    "a free-standing building."
                )


        # ====================================================
        # COM-03 — LANDSCAPED WALKWAY
        # ====================================================

        elif rule_id == (
            "RT-MBMB-2035-COM-03"
        ):

            if shop_frontage_verified:

                status = "APPLICABLE"

                reason = (
                    "The proposal has been verified as "
                    "meeting the shop-frontage typology "
                    "required by the rule."
                )

            elif (
                "shop"
                in development_type.lower()
                or
                "shop-office"
                in development_type.lower()
            ):

                status = (
                    "REQUIRES TYPOLOGY VERIFICATION"
                )

                reason = (
                    "The proposal appears related to "
                    "shop / shop-office development, "
                    "but shop-frontage applicability "
                    "has not been independently verified."
                )

            else:

                status = (
                    "REQUIRES TYPOLOGY VERIFICATION"
                )

                reason = (
                    "The rule refers specifically to "
                    "shop frontages. A free-standing "
                    "commercial building cannot automatically "
                    "be treated as a shop frontage."
                )


        # ====================================================
        # COM-04 — SHOP-OFFICE HEIGHT
        # ====================================================

        elif rule_id == (
            "RT-MBMB-2035-COM-04"
        ):

            if (
                "shop-office"
                in development_type.lower()
            ):

                status = (
                    "REQUIRES TYPOLOGY VERIFICATION"
                )

                reason = (
                    "The proposal is identified as "
                    "shop-office, but the applicable "
                    "commercial control requires "
                    "typology confirmation."
                )

            else:

                status = "NOT APPLICABLE"

                reason = (
                    "The proposal is not shop-office. "
                    "The rule does not automatically apply "
                    "to free-standing commercial development."
                )


        # ====================================================
        # TOD-01 / TOD-02
        # ====================================================

        elif rule_id in (
            "RT-MBMB-2035-TOD-01",
            "RT-MBMB-2035-TOD-02"
        ):

            # ====================================================
            # TOD RULE DEVELOPMENT-TYPE GATE
            # ====================================================

            development_lower = (
                development_type.lower()
            )

            is_tod_development = (
                "tod" in development_lower
                or "mixed-use" in development_lower
                or "mixed use" in development_lower
                or "mixed" in development_lower
            )

            # ====================================================
            # NON-TOD DEVELOPMENT
            # ====================================================

            if not is_tod_development:

                status = "NOT APPLICABLE"

                reason = (
                    "This TOD-specific planning rule is not "
                    "applicable to the selected development type."
                )

            else:

                # =================================================
                # NORMALISE VERIFIED TOD DISTANCE
                # =================================================

                tod_distance = spatial_context.get(
                    "tod_distance_m",
                    None
                )

                try:

                    tod_distance = (
                        float(tod_distance)
                        if tod_distance is not None
                        else None
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    tod_distance = None

                # =================================================
                # TOD-01 — 400 M RADIUS / PLOT RATIO 1:4.5
                # =================================================

                if rule_id == (
                    "RT-MBMB-2035-TOD-01"
                ):

                    if (
                        tod_distance is not None
                        and tod_400_verified
                        and tod_distance <= 400
                    ):

                        status = "APPLICABLE"

                        reason = (
                            "The verified TOD distance is within "
                            "the designated 400 m radius. "
                            "TOD-01 plot ratio requirement of "
                            "1:4.5 is applicable."
                        )

                    elif (
                        tod_distance is not None
                        and tod_distance > 400
                    ):

                        status = "NOT APPLICABLE"

                        reason = (
                            "The verified TOD distance is outside "
                            "the designated 400 m radius. "
                            "The 800 m TOD rule is assessed separately."
                        )

                    elif tod_400_verified:

                        status = "APPLICABLE"

                        reason = (
                            "The 400 m TOD relationship has been "
                            "explicitly spatially verified."
                        )

                    else:

                        status = (
                            "REQUIRES SPATIAL VERIFICATION"
                        )

                        reason = (
                            "TOD-01 requires verified spatial "
                            "relationship to the Terminal Sg. Udang "
                            "TOD 400 m radius."
                        )

                # =================================================
                # TOD-02 — 800 M RADIUS / PLOT RATIO 1:4.0
                # =================================================

                else:

                    if (
                        tod_distance is not None
                        and tod_800_verified
                        and 400 < tod_distance <= 800
                    ):

                        status = "APPLICABLE"

                        reason = (
                            "The verified TOD distance is within "
                            "the 401–800 m range. TOD-02 plot ratio "
                            "requirement of 1:4.0 is applicable."
                        )

                    elif (
                        tod_distance is not None
                        and tod_distance <= 400
                    ):

                        status = "NOT APPLICABLE"

                        reason = (
                            "The verified TOD distance falls within "
                            "the more specific 400 m TOD radius. "
                            "TOD-01 is the applicable TOD plot ratio rule."
                        )

                    elif (
                        tod_distance is not None
                        and tod_distance > 800
                    ):

                        status = "NOT APPLICABLE"

                        reason = (
                            "The verified TOD distance is outside "
                            "the designated 800 m TOD radius."
                        )

                    elif tod_800_verified:

                        status = "APPLICABLE"

                        reason = (
                            "The 800 m TOD relationship has been "
                            "explicitly spatially verified."
                        )

                    else:

                        status = (
                            "REQUIRES SPATIAL VERIFICATION"
                        )

                        reason = (
                            "TOD-02 requires verified spatial "
                            "relationship to the Terminal Sg. Udang "
                            "TOD 800 m radius."
                        )


        # ====================================================
        # FALLBACK
        # ====================================================

        else:

            status = "REQUIRES REVIEW"

            reason = (
                "No deterministic applicability condition "
                "has been established for this rule."
            )


        # ====================================================
        # STORE RESULT
        # ====================================================

        results.append({

            "rule_id":
                rule_id,

            "parameter":
                rule.get(
                    "parameter"
                ),

            "requirement":
                rule.get(
                    "requirement"
                ),

            "proposed":
                proposal.get(
                    rule.get(
                        "parameter",
                        ""
                    )
                ),

            "applicability":
                status,

            "reason":
                reason,

            "spatial_condition":
                rule.get(
                    "spatial_condition"
                ),

            "source_document":
                rule.get(
                    "source_document"
                ),

            "source_section":
                rule.get(
                    "source_section"
                ),

            "evidence_text":
                rule.get(
                    "evidence_text"
                ),

            "evidence_classification":
                rule.get(
                    "evidence_classification"
                ),

            "traceability":
                rule.get(
                    "traceability"
                )
        })


    return results

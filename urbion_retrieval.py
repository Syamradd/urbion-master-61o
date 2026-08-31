
# ============================================================
# 🏙️ URBION RULE RETRIEVAL ENGINE
# ============================================================

from urbion_rules import URBION_RULES


def urbion_retrieve_rules(
    development_type,
    authority="MBMB",
    spatial_context=None
):
    """
    Retrieve candidate planning rules.

    Retrieval considers:
    1. Planning authority
    2. Development typology
    3. Commercial applicability
    4. Spatial / TOD conditions

    IMPORTANT:
    Retrieval does NOT make a final applicability decision.

    The retrieved rules are candidate rules that will later
    be evaluated by the Applicability Engine.
    """

    candidates = []

    development_type = (
        development_type or ""
    ).strip()

    authority = (
        authority or "MBMB"
    ).strip()

    spatial_context = (
        spatial_context or {}
    )

    # --------------------------------------------------------
    # AUTHORITY FILTER
    # --------------------------------------------------------

    # Current database is RT MBMB.
    # If another authority is selected, no MBMB rule should
    # automatically be treated as authoritative.

    if authority != "MBMB":

        return candidates


    # --------------------------------------------------------
    # DEVELOPMENT TYPE NORMALISATION
    # --------------------------------------------------------

    development_lower = (
        development_type.lower()
    )


    # --------------------------------------------------------
    # RETRIEVE CANDIDATE RULES
    # --------------------------------------------------------

    for rule in URBION_RULES:

        rule_type = (
            rule.get(
                "development_type",
                ""
            ).lower()
        )

        applicability = (
            rule.get(
                "applicability",
                ""
            )
        )

        development_match = False


        # ====================================================
        # 1. EXACT / TYPOLOGY MATCH
        # ====================================================

        if (
            development_lower
            in rule_type
        ):

            development_match = True


        # ====================================================
        # 2. FREE-STANDING COMMERCIAL
        # ====================================================

        elif (
            "free-standing"
            in development_lower
            and
            (
                "commercial"
                in rule_type
                or
                "building"
                in rule_type
            )
        ):

            development_match = True


        # ====================================================
        # 3. SHOP-OFFICE
        # ====================================================

        elif (
            "shop-office"
            in development_lower
            and
            (
                "shop-office"
                in rule_type
                or
                "shop frontage"
                in rule_type
            )
        ):

            development_match = True


        # ====================================================
        # 4. MIXED DEVELOPMENT / TOD
        # ====================================================

        elif (
            (
                "mixed"
                in development_lower
            )
            and
            (
                "tod"
                in rule_type
            )
        ):

            development_match = True


        # ====================================================
        # 5. TOD SPATIAL CANDIDATES
        # ====================================================

        elif (
            applicability
            == "TOD_SPATIAL_DEPENDENT"
        ):

            # TOD rules remain candidates because the
            # retrieval layer should not independently decide
            # whether the parcel is actually inside the radius.

            development_match = True


        # ====================================================
        # 6. COMMERCIAL RULES
        # ====================================================

        elif (
            "commercial"
            in development_lower
            and
            rule.get(
                "land_use",
                ""
            ).lower()
            == "commercial"
        ):

            development_match = True


        # ----------------------------------------------------
        # ADD CANDIDATE
        # ----------------------------------------------------

        if development_match:

            candidates.append({

                "rule_id":
                    rule["rule_id"],

                "parameter":
                    rule["parameter"],

                "requirement":
                    rule["requirement"],

                "value":
                    rule.get(
                        "value"
                    ),

                "unit":
                    rule.get(
                        "unit"
                    ),

                "development_type":
                    rule["development_type"],

                "land_use":
                    rule.get(
                        "land_use"
                    ),

                "spatial_condition":
                    rule["spatial_condition"],

                "applicability":
                    rule["applicability"],

                "source_document":
                    rule["source_document"],

                "source_section":
                    rule["source_section"],

                "evidence_text":
                    rule["evidence_text"],

                "evidence_classification":
                    rule["evidence_classification"],

                "traceability":
                    rule["traceability"],

                "notes":
                    rule.get(
                        "notes",
                        ""
                    )
            })


    return candidates

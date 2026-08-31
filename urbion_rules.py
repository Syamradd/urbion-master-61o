
# ============================================================
# 🏙️ URBION RULE DATABASE
# RT MBMB 2035 — Development Control Rules
# ============================================================

URBION_RULES = [

    # --------------------------------------------------------
    # COM-01 — FREE-STANDING COMMERCIAL PLOT RATIO
    # --------------------------------------------------------

    {
        "rule_id": "RT-MBMB-2035-COM-01",

        "parameter": "Plot Ratio",

        "development_type":
            "Free-Standing Commercial",

        "land_use":
            "Class B Commercial",

        "requirement":
            "Free Standing 1:6.0",

        "value": 6.0,

        "unit":
            "ratio",

        "spatial_condition":
            "Specific precinct / planning block",

        "applicability":
            "SPATIAL_DEPENDENT",

        "source_document":
            "RT MBMB 2035 Jilid I",

        "source_section":
            "Jadual Kelas Penggunaan Tanah / Commercial Land Use Tables",

        "evidence_text":
            "Free Standing 1:6.0",

        "evidence_classification":
            "RULE_ESTABLISHED",

        "traceability":
            "PARTIALLY_TRACEABLE",

        "notes":
            (
                "Value is precinct-dependent and must not be "
                "treated as a universal city-wide commercial standard."
            )
    },


    # --------------------------------------------------------
    # COM-02 — PERIMETER PLANTING
    # --------------------------------------------------------

    {
        "rule_id": "RT-MBMB-2035-COM-02",

        "parameter":
            "Perimeter Planting",

        "development_type":
            "Free-Standing Building",

        "land_use":
            "Commercial",

        "requirement":
            "Minimum 3.0 m around lot boundary",

        "value":
            3.0,

        "unit":
            "metres",

        "spatial_condition":
            "Free-standing building requirement",

        "applicability":
            "DEVELOPMENT_TYPE_MATCH",

        "source_document":
            "RT MBMB 2035 Jilid I",

        "source_section":
            "Column IV / Syarat-Syarat Umum",

        "evidence_text":
            (
                "Free standing building perlu menyediakan "
                "3.0 meter perimeter planting di sekeliling "
                "sempadan lot."
            ),

        "evidence_classification":
            "RULE_ESTABLISHED",

        "traceability":
            "PARTIALLY_TRACEABLE",

        "notes":
            (
                "Specific precinct overrides must still be "
                "checked before issuing a final statutory determination."
            )
    },


    # --------------------------------------------------------
    # COM-03 — LANDSCAPED PEDESTRIAN WALKWAY
    # --------------------------------------------------------

    {
        "rule_id": "RT-MBMB-2035-COM-03",

        "parameter":
            "Landscaped Pedestrian Walkway",

        "development_type":
            "Commercial Shop Frontage",

        "land_use":
            "Commercial",

        "requirement":
            "1.5 m minimum",

        "value":
            1.5,

        "unit":
            "metres",

        "spatial_condition":
            "Front of shops up to corner lots",

        "applicability":
            "TYPOLOGY_DEPENDENT",

        "source_document":
            "RT MBMB 2035 Jilid I",

        "source_section":
            "Column IV / Syarat-Syarat Umum",

        "evidence_text":
            (
                "Penyediaan 1.5 meter laluan siar kaki "
                "berlandskap perlu disediakan di hadapan "
                "kedai hingga lot kedai penjuru."
            ),

        "evidence_classification":
            "RULE_ESTABLISHED",

        "traceability":
            "PARTIALLY_TRACEABLE",

        "notes":
            (
                "Must not automatically be applied to every "
                "free-standing commercial development."
            )
    },


    # --------------------------------------------------------
    # COM-04 — BUILDING HEIGHT
    # --------------------------------------------------------

    {
        "rule_id": "RT-MBMB-2035-COM-04",

        "parameter":
            "Building Height",

        "development_type":
            "Commercial Shop-Office",

        "land_use":
            "Class B Commercial",

        "requirement":
            "Maximum 4 storeys",

        "value":
            4,

        "unit":
            "storeys",

        "spatial_condition":
            "Specific commercial shop-office controls",

        "applicability":
            "TYPOLOGY_DEPENDENT",

        "source_document":
            "RT MBMB 2035 Jilid I",

        "source_section":
            "Commercial Land Use Tables",

        "evidence_text":
            "Kedai Pejabat Ketinggian 4 tingkat",

        "evidence_classification":
            "RULE_ESTABLISHED",

        "traceability":
            "PARTIALLY_TRACEABLE",

        "notes":
            (
                "Does not automatically apply to free-standing "
                "commercial buildings."
            )
    },


    # --------------------------------------------------------
    # TOD-01 — 400m RADIUS
    # --------------------------------------------------------

    {
        "rule_id": "RT-MBMB-2035-TOD-01",

        "parameter":
            "Plot Ratio",

        "development_type":
            "TOD Development / Mixed Use",

        "land_use":
            "TOD",

        "requirement":
            "1:4.5",

        "value":
            4.5,

        "unit":
            "ratio",

        "spatial_condition":
            "Terminal Sg. Udang TOD — 400 m radius",

        "applicability":
            "TOD_SPATIAL_DEPENDENT",

        "source_document":
            "RT MBMB 2035 Jilid I",

        "source_section":
            "TOD Development Controls",

        "evidence_text":
            (
                "Terminal Sg. Udang TOD 400 meter radius "
                "sahaja dibenarkan ... plot ratio 1:4.5."
            ),

        "evidence_classification":
            "RULE_ESTABLISHED",

        "traceability":
            "PARTIALLY_TRACEABLE",

        "notes":
            (
                "Only applicable if the site is within "
                "the designated TOD radius."
            )
    },


    # --------------------------------------------------------
    # TOD-02 — 800m RADIUS
    # --------------------------------------------------------

    {
        "rule_id": "RT-MBMB-2035-TOD-02",

        "parameter":
            "Plot Ratio",

        "development_type":
            "TOD Development / Mixed Use",

        "land_use":
            "TOD",

        "requirement":
            "1:4.0",

        "value":
            4.0,

        "unit":
            "ratio",

        "spatial_condition":
            "Terminal Sg. Udang TOD — 800 m radius",

        "applicability":
            "TOD_SPATIAL_DEPENDENT",

        "source_document":
            "RT MBMB 2035 Jilid I",

        "source_section":
            "TOD Development Controls",

        "evidence_text":
            (
                "Terminal Sg. Udang TOD 800 meter radius "
                "sahaja dibenarkan ... plot ratio 1:4.0."
            ),

        "evidence_classification":
            "RULE_ESTABLISHED",

        "traceability":
            "PARTIALLY_TRACEABLE",

        "notes":
            (
                "Only applicable if the site is within "
                "the designated TOD radius."
            )
    }
]


# ============================================================
# HELPER
# ============================================================

def get_urbion_rules():
    """
    Return the complete URBION rule database.
    """
    return URBION_RULES

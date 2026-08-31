
# ============================================================
# 🏙️ URBION v1.2
# DEVELOPMENT CONTROL DECISION-SUPPORT SYSTEM
# ============================================================

import streamlit as st
from pathlib import Path
from datetime import datetime
import json

from urbion_spatial import (
    urbion_create_spatial_context,
    urbion_get_spatial_status,
    urbion_spatial_verification_summary,
    calculate_distance_m,
    classify_tod_distance
)


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="URBION",
    page_icon="🏙️",
    layout="wide"
)

URBION_DATA_PATH = "/content/urbion_assessments.json"


# ============================================================
# PERSISTENCE
# ============================================================

def urbion_load_assessments():

    path = Path(
        URBION_DATA_PATH
    )

    if not path.exists():
        return []

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception as error:

        st.warning(
            f"Unable to load assessment history: {error}"
        )

        return []


def urbion_persist_assessments(
    assessments
):

    with open(
        URBION_DATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            assessments,
            file,
            ensure_ascii=False,
            indent=2,
            default=str
        )


def urbion_save_assessment(
    assessment
):

    assessments = (
        urbion_load_assessments()
    )

    assessments.append(
        assessment
    )

    urbion_persist_assessments(
        assessments
    )

    return assessments


# ============================================================
# RULE DATABASE
# ============================================================

URBION_RULE_DATABASE = [

    {
        "rule_id": "RT-MBMB-2035-COM-01",
        "parameter": "Plot Ratio",
        "requirement": "Free Standing 1:6.0",
        "development_type": "Free-Standing Commercial",
        "spatial_condition":
            "Specific precinct land use schedules",
        "applicability":
            "CONDITIONAL — PRECINCT DEPENDENT",
        "value": 6.0,
        "source_document":
            "RT MBMB 2035 Jilid I",
        "source_section":
            "Jadual Kelas Penggunaan Tanah / Commercial Land Use Tables",
        "evidence_text":
            "Free Standing 1:6.0",
        "evidence_classification":
            "RULE_ESTABLISHED",
        "traceability":
            "PARTIALLY_TRACEABLE"
    },

    {
        "rule_id": "RT-MBMB-2035-COM-02",
        "parameter": "Perimeter Planting",
        "requirement":
            "Minimum 3.0 m around lot boundary",
        "development_type":
            "Free-Standing Commercial",
        "spatial_condition":
            "Free-standing building",
        "applicability":
            "APPLICABLE",
        "value": 3.0,
        "source_document":
            "RT MBMB 2035 Jilid I",
        "source_section":
            "Column IV / Syarat-Syarat Umum",
        "evidence_text":
            "Free standing building perlu menyediakan 3.0 meter perimeter planting di sekeliling sempadan lot.",
        "evidence_classification":
            "RULE_ESTABLISHED",
        "traceability":
            "PARTIALLY_TRACEABLE"
    },

    {
        "rule_id":
            "RT-MBMB-2035-COM-03",
        "parameter":
            "Landscaped Pedestrian Walkway",
        "requirement":
            "1.5 m landscaped pedestrian walkway",
        "development_type":
            "Shop Frontage / Shop-Office",
        "spatial_condition":
            "Front of shops up to corner lots",
        "applicability":
            "TYPOLOGY DEPENDENT",
        "value": 1.5,
        "source_document":
            "RT MBMB 2035 Jilid I",
        "source_section":
            "Column IV / Syarat-Syarat Umum",
        "evidence_text":
            "Penyediaan 1.5 meter laluan siar kaki berlandskap perlu disediakan di hadapan kedai hingga lot kedai penjuru.",
        "evidence_classification":
            "RULE_ESTABLISHED",
        "traceability":
            "PARTIALLY_TRACEABLE"
    },

    {
        "rule_id":
            "RT-MBMB-2035-COM-04",
        "parameter":
            "Building Height",
        "requirement":
            "Maximum 4 storeys",
        "development_type":
            "Shop-Office",
        "spatial_condition":
            "Specific commercial shop-office controls",
        "applicability":
            "TYPOLOGY DEPENDENT",
        "value": 4,
        "source_document":
            "RT MBMB 2035 Jilid I",
        "source_section":
            "Commercial Land Use Tables",
        "evidence_text":
            "Kedai Pejabat Ketinggian 4 tingkat",
        "evidence_classification":
            "RULE_ESTABLISHED",
        "traceability":
            "PARTIALLY_TRACEABLE"
    },

    {
        "rule_id":
            "RT-MBMB-2035-TOD-01",
        "parameter":
            "Plot Ratio",
        "requirement":
            "1:4.5",
        "development_type":
            "TOD / Mixed-use Development",
        "spatial_condition":
            "Terminal Sg. Udang TOD — 400 m radius",
        "applicability":
            "TOD CONDITIONAL",
        "value": 4.5,
        "source_document":
            "RT MBMB 2035 Jilid I",
        "source_section":
            "TOD Development Controls",
        "evidence_text":
            "Terminal Sg. Udang TOD 400 meter radius sahaja dibenarkan ... plot ratio 1:4.5.",
        "evidence_classification":
            "RULE_ESTABLISHED",
        "traceability":
            "PARTIALLY_TRACEABLE"
    },

    {
        "rule_id":
            "RT-MBMB-2035-TOD-02",
        "parameter":
            "Plot Ratio",
        "requirement":
            "1:4.0",
        "development_type":
            "TOD / Mixed-use Development",
        "spatial_condition":
            "Terminal Sg. Udang TOD — 800 m radius",
        "applicability":
            "TOD CONDITIONAL",
        "value": 4.0,
        "source_document":
            "RT MBMB 2035 Jilid I",
        "source_section":
            "TOD Development Controls",
        "evidence_text":
            "Terminal Sg. Udang TOD 800 meter radius sahaja dibenarkan ... plot ratio 1:4.0.",
        "evidence_classification":
            "RULE_ESTABLISHED",
        "traceability":
            "PARTIALLY_TRACEABLE"
    }
]


# ============================================================
# RULE RETRIEVAL
# ============================================================

def urbion_retrieve_rules(
    development_type,
    authority,
    spatial_context=None
):

    if authority != "MBMB":
        return []

    proposal = development_type.lower()

    candidates = []

    for rule in URBION_RULE_DATABASE:

        rule_type = (
            rule["development_type"]
            .lower()
        )

        if (
            "free-standing commercial"
            in proposal
        ):

            if (
                "free-standing commercial"
                in rule_type
                or "shop" in rule_type
                or "tod" in rule_type
            ):

                candidates.append(rule)

        elif "shop-office" in proposal:

            if (
                "shop-office" in rule_type
                or "free-standing" in rule_type
            ):

                candidates.append(rule)

        else:

            if (
                "tod" in rule_type
                or "commercial" in rule_type
            ):

                candidates.append(rule)

    return candidates


# ============================================================
# APPLICABILITY
# ============================================================

def urbion_check_applicability(
    rule,
    development_type,
    spatial_context,
    spatial_verification
):

    rule_id = rule["rule_id"]

    proposal = (
        development_type.lower()
    )

    if rule_id == "RT-MBMB-2035-COM-01":

        if "free-standing commercial" in proposal:

            if spatial_verification.get(
                "precinct_verified",
                False
            ):

                return (
                    "APPLICABLE",
                    "Precinct relationship has been verified."
                )

            return (
                "REQUIRES SPATIAL VERIFICATION",
                "Plot ratio is precinct-dependent and parcel-to-precinct relationship remains unverified."
            )

        return (
            "NOT APPLICABLE",
            "Development type does not match."
        )

    if rule_id == "RT-MBMB-2035-COM-02":

        if "free-standing commercial" in proposal:

            return (
                "APPLICABLE",
                "Rule explicitly refers to free-standing buildings."
            )

        return (
            "NOT APPLICABLE",
            "Rule is specific to free-standing buildings."
        )

    if rule_id == "RT-MBMB-2035-COM-03":

        if spatial_verification.get(
            "shop_frontage_verified",
            False
        ):

            return (
                "APPLICABLE",
                "Shop frontage has been verified."
            )

        return (
            "REQUIRES TYPOLOGY VERIFICATION",
            "The rule specifically refers to shop frontage."
        )

    if rule_id == "RT-MBMB-2035-COM-04":

        if "shop-office" in proposal:

            return (
                "REQUIRES REVIEW",
                "Shop-office typology requires applicable precinct verification."
            )

        return (
            "NOT APPLICABLE",
            "Proposal is not shop-office development."
        )

    if rule_id == "RT-MBMB-2035-TOD-01":

        if spatial_verification.get(
            "tod_400_verified",
            False
        ):

            return (
                "APPLICABLE",
                "TOD 400m relationship has been verified."
            )

        return (
            "REQUIRES SPATIAL VERIFICATION",
            "TOD 400m applicability requires verified spatial evidence."
        )

    if rule_id == "RT-MBMB-2035-TOD-02":

        if spatial_verification.get(
            "tod_800_verified",
            False
        ):

            return (
                "APPLICABLE",
                "TOD 800m relationship has been verified."
            )

        return (
            "REQUIRES SPATIAL VERIFICATION",
            "TOD 800m applicability requires verified spatial evidence."
        )

    return (
        "REQUIRES REVIEW",
        "No validated applicability logic exists."
    )


# ============================================================
# COMPLIANCE
# ============================================================

def urbion_evaluate_compliance(
    parameter,
    proposed_value,
    rule,
    applicability
):

    if applicability != "APPLICABLE":

        return (
            "REQUIRES REVIEW",
            f"Rule applicability is '{applicability}'. Definitive compliance cannot be issued."
        )

    try:

        if parameter == "Plot Ratio":

            proposed = float(
                str(proposed_value)
                .replace("1:", "")
                .strip()
            )

            required = float(
                rule["value"]
            )

            if proposed <= required:

                return (
                    "COMPLY",
                    f"Proposed plot ratio 1:{proposed:g} is within the maximum 1:{required:g}."
                )

            return (
                "NON-COMPLIANCE",
                f"Proposed plot ratio 1:{proposed:g} exceeds the maximum 1:{required:g}."
            )


        if parameter == "Perimeter Planting":

            proposed = float(
                proposed_value
            )

            required = float(
                rule["value"]
            )

            if proposed >= required:

                return (
                    "COMPLY",
                    f"Proposed {proposed:.1f} m meets the minimum {required:.1f} m."
                )

            return (
                "CONDITIONAL NON-COMPLIANCE",
                f"Proposed {proposed:.1f} m is below the minimum {required:.1f} m."
            )


        if parameter == "Landscaped Pedestrian Walkway":

            proposed = float(
                proposed_value
            )

            required = float(
                rule["value"]
            )

            if proposed >= required:

                return (
                    "COMPLY",
                    f"Proposed {proposed:.1f} m meets the minimum {required:.1f} m."
                )

            return (
                "NON-COMPLIANCE",
                f"Proposed {proposed:.1f} m is below the minimum {required:.1f} m."
            )


        if parameter == "Building Height":

            proposed = float(
                str(proposed_value)
                .lower()
                .replace("storeys", "")
                .replace("storey", "")
                .strip()
            )

            required = float(
                rule["value"]
            )

            if proposed <= required:

                return (
                    "COMPLY",
                    f"Proposed {proposed:g} storeys is within the maximum {required:g} storeys."
                )

            return (
                "NON-COMPLIANCE",
                f"Proposed {proposed:g} storeys exceeds the maximum {required:g} storeys."
            )

    except Exception:

        return (
            "REQUIRES REVIEW",
            "Unable to interpret the proposed value numerically."
        )

    return (
        "REQUIRES REVIEW",
        "No validated comparison logic exists."
    )


# ============================================================
# OVERALL STATUS
# ============================================================

def urbion_calculate_overall_status(
    results
):

    statuses = [
        item.get("status")
        for item in results
    ]

    if "NON-COMPLIANCE" in statuses:
        return "🔴 NON-COMPLIANCE"

    if "CONDITIONAL NON-COMPLIANCE" in statuses:
        return "🟠 CONDITIONAL RISK"

    if "REQUIRES REVIEW" in statuses:
        return "🟡 REQUIRES REVIEW"

    if statuses and all(
        status == "COMPLY"
        for status in statuses
    ):

        return "🟢 COMPLY"

    return "🟡 REQUIRES REVIEW"


# ============================================================
# SESSION INITIALIZATION
# ============================================================

if "assessment_history" not in st.session_state:

    st.session_state.assessment_history = (
        urbion_load_assessments()
    )


# ============================================================
# NAVIGATION
#
# IMPORTANT:
# current_page is NOT used as a widget key.
# This prevents the Streamlit state error encountered earlier.
# ============================================================

if "current_page" not in st.session_state:

    st.session_state.current_page = (
        "🏠 Dashboard"
    )


NAVIGATION = [
    "🏠 Dashboard",
    "➕ New Assessment",
    "📋 Assessments",
    "📚 Policy Library",
    "📍 Spatial Intelligence",
    "📊 Analytics"
]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🏙️ URBION"
    )

    st.caption(
        "Urban Planning Decision-Support System"
    )

    st.write("")

    selected_page = st.radio(
        "Navigation",
        NAVIGATION,
        index=NAVIGATION.index(
            st.session_state.current_page
        )
    )

    if selected_page != st.session_state.current_page:

        st.session_state.current_page = (
            selected_page
        )

        st.rerun()

    st.markdown("---")

    st.caption(
        "URBION v1.2"
    )

    st.caption(
        "Evidence-aware planning assessment"
    )


page = st.session_state.current_page


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title(
        "🏙️ URBION Dashboard"
    )

    st.caption(
        "Development control assessment and planning decision support."
    )

    # Always read latest persistent data.
    assessment_history = (
        urbion_load_assessments()
    )

    st.session_state.assessment_history = (
        assessment_history
    )

    total = len(
        assessment_history
    )

    comply = sum(
        1
        for item in assessment_history
        if item.get("Status") == "🟢 COMPLY"
    )

    review = sum(
        1
        for item in assessment_history
        if item.get("Status") == "🟡 REQUIRES REVIEW"
    )

    risk = sum(
        1
        for item in assessment_history
        if (
            "NON-COMPLIANCE"
            in item.get("Status", "")
            or
            "RISK"
            in item.get("Status", "")
        )
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Assessments",
            total
        )

    with c2:
        st.metric(
            "Comply",
            comply
        )

    with c3:
        st.metric(
            "Requires Review",
            review
        )

    with c4:
        st.metric(
            "Potential Risk",
            risk
        )

    st.write("")

    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    st.subheader(
        "Quick Actions"
    )

    q1, q2 = st.columns(2)

    with q1:

        if st.button(
            "➕ NEW ASSESSMENT",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.current_page = (
                "➕ New Assessment"
            )

            st.rerun()

    with q2:

        if st.button(
            "📋 VIEW ASSESSMENTS",
            use_container_width=True
        ):

            st.session_state.current_page = (
                "📋 Assessments"
            )

            st.rerun()

    st.write("")

    # ========================================================
    # RECENT ASSESSMENTS
    # ========================================================

    st.subheader(
        "Recent Assessments"
    )

    if not assessment_history:

        st.info(
            "No assessments have been recorded yet."
        )

    else:

        recent = (
            assessment_history[-5:][::-1]
        )

        for item in recent:

            status = item.get(
                "Status",
                "🟡 REQUIRES REVIEW"
            )

            st.markdown(
                f"""
                **Lot {item.get('Lot', '—')}**
                {item.get('Development Type', '—')}
                `{status}` · {item.get('Created', '—')}
                """
            )

            st.markdown("---")


# ============================================================
# NEW ASSESSMENT
# ============================================================

elif page == "➕ New Assessment":

    st.title(
        "➕ New Assessment"
    )

    st.caption(
        "Preliminary development control assessment."
    )

    st.subheader(
        "Site / Proposal Information"
    )

    c1, c2 = st.columns(2)

    with c1:

        lot_number = st.text_input(
            "Lot Number",
            value="11213"
        )

        location = st.text_input(
            "Planning Context",
            value="Presint 2.2 / ZP2"
        )

        negeri_options = {
            "Melaka": {
                "Majlis Bandaraya Melaka Bersejarah":
                    {
                        "engine_code": "MBMB",
                        "references": [
                            "Rancangan Tempatan Majlis Bandaraya Melaka Bersejarah 2035"
                        ]
                    },
                "Majlis Perbandaran Alor Gajah":
                    {
                        "engine_code": None,
                        "references": [
                            "Rujukan perancangan belum disambungkan"
                        ]
                    },
                "Majlis Perbandaran Jasin":
                    {
                        "engine_code": None,
                        "references": [
                            "Rujukan perancangan belum disambungkan"
                        ]
                    }
            },
            "Selangor": {
                "Majlis Bandaraya Shah Alam":
                    {
                        "engine_code": None,
                        "references": [
                            "Rujukan perancangan belum disambungkan"
                        ]
                    },
                "Majlis Bandaraya Petaling Jaya":
                    {
                        "engine_code": None,
                        "references": [
                            "Rujukan perancangan belum disambungkan"
                        ]
                    },
                "Majlis Bandaraya Subang Jaya":
                    {
                        "engine_code": None,
                        "references": [
                            "Rujukan perancangan belum disambungkan"
                        ]
                    }
            },
            "Pulau Pinang": {
                "Majlis Bandaraya Pulau Pinang":
                    {
                        "engine_code": None,
                        "references": [
                            "Rujukan perancangan belum disambungkan"
                        ]
                    },
                "Majlis Bandaraya Seberang Perai":
                    {
                        "engine_code": None,
                        "references": [
                            "Rujukan perancangan belum disambungkan"
                        ]
                    }
            }
        }

        state = st.selectbox(
            "Negeri",
            list(negeri_options.keys()),
            index=0
        )

        pbt_options = negeri_options[state]

        pbt = st.selectbox(
            "Pihak Berkuasa Tempatan",
            list(pbt_options.keys()),
            index=0
        )

        pbt_config = pbt_options[pbt]

        reference_options = pbt_config[
            "references"
        ]

        planning_reference = st.selectbox(
            "Rujukan Perancangan",
            reference_options,
            index=0
        )

        authority = pbt_config[
            "engine_code"
        ]

        if authority is None:

            st.warning(
                "⚠️ PBT ini tersedia dalam rangka kerja "
                "URBION tetapi enjin penilaian belum "
                "disambungkan untuk bidang kuasa ini."
            )

        else:

            st.caption(
                f"Enjin URBION aktif: {pbt}"
            )

        site_area = st.number_input(
            "Site Area (hectares)",
            min_value=0.0,
            value=1.145,
            step=0.001
        )

    with c2:

        development_type = st.selectbox(
            "Development Type",
            [
                "Free-Standing Commercial",
                "Shop-Office",
                "TOD / Mixed-use Development"
            ]
        )

        plot_ratio = st.text_input(
            "Plot Ratio",
            value="1:4.5"
        )

        building_height = st.text_input(
            "Building Height",
            value="5 storeys"
        )

        perimeter = st.number_input(
            "Perimeter Planting (m)",
            min_value=0.0,
            value=2.0,
            step=0.1
        )

        walkway = st.number_input(
            "Landscaped Pedestrian Walkway (m)",
            min_value=0.0,
            value=1.5,
            step=0.1
        )

    st.write("")

    # ========================================================

    # ========================================================
    # SPATIAL & GIS VERIFICATION
    # ========================================================

    st.subheader(
        "🗺️ Spatial & GIS Verification"
    )

    st.caption(
        "Pengesahan spatial hendaklah disokong oleh bukti "
        "lokasi, sempadan, jarak atau data spatial yang "
        "boleh disemak."
    )

    # --------------------------------------------------------
    # GIS EVIDENCE SOURCE
    # --------------------------------------------------------

    st.subheader(
        "📡 Sumber Bukti Spatial"
    )

    evidence_source = st.selectbox(
        "Sumber Bukti",
        [
            "GIS Melaka",
            "myGEMS",
            "Jabatan Ukur dan Pemetaan Malaysia (JUPEM)",
            "Google Maps / Imejan Satelit",
            "Data / Pelan Pemohon",
            "Lain-lain"
        ],
        key="spatial_evidence_source"
    )

    evidence_reference = st.text_input(
        "Rujukan / Catatan Bukti Spatial",
        placeholder=(
            "Contoh: Peta GIS, nombor lot, koordinat, "
            "pelan ukur atau rujukan data"
        ),
        key="spatial_evidence_reference"
    )

    # --------------------------------------------------------
    # LOCATION VERIFICATION
    # --------------------------------------------------------

    st.subheader(
        "📍 Pengesahan Lokasi"
    )

    spatial_location = st.text_input(
        "Precinct / Kawasan",
        value=location,
        key="spatial_location"
    )

    precinct_verified = st.checkbox(
        "Precinct telah disahkan berdasarkan bukti spatial",
        value=False
    )

    # --------------------------------------------------------
    # GIS COORDINATES
    # --------------------------------------------------------

    st.subheader(
        "🛰️ Koordinat Spatial"
    )

    coord_col1, coord_col2 = st.columns(2)

    with coord_col1:

        site_lat = st.number_input(
            "Site Latitude",
            value=2.3000,
            format="%.6f",
            key="site_latitude"
        )

        tod_lat = st.number_input(
            "TOD Latitude",
            value=2.3020,
            format="%.6f",
            key="tod_latitude"
        )

    with coord_col2:

        site_lon = st.number_input(
            "Site Longitude",
            value=102.2000,
            format="%.6f",
            key="site_longitude"
        )

        tod_lon = st.number_input(
            "TOD Longitude",
            value=102.2000,
            format="%.6f",
            key="tod_longitude"
        )

    # --------------------------------------------------------
    # AUTOMATIC TOD DISTANCE
    # --------------------------------------------------------

    tod_distance = calculate_distance_m(
        site_lat,
        site_lon,
        tod_lat,
        tod_lon
    )

    tod_classification = classify_tod_distance(
        tod_distance
    )

    if tod_classification == "TOD 400m":

        tod_400_verified = True
        tod_800_verified = True

    elif tod_classification == "TOD 800m":

        tod_400_verified = False
        tod_800_verified = True

    else:

        tod_400_verified = False
        tod_800_verified = False

    tod_verified = (
        tod_400_verified
        or tod_800_verified
    )

    st.metric(
        "Calculated TOD Distance",
        f"{tod_distance:.1f} m"
    )

    st.info(
        f"🎯 TOD Classification: "
        f"**{tod_classification}**"
    )

    # --------------------------------------------------------
    # SHOP FRONTAGE
    # --------------------------------------------------------

    st.subheader(
        "🏢 Pengesahan Shop Frontage"
    )

    shop_frontage_verified = st.checkbox(
        "Shop frontage telah disahkan",
        value=False
    )

    # --------------------------------------------------------
    # SPATIAL ENGINE CONTEXT
    # --------------------------------------------------------

    spatial_context = (
        urbion_create_spatial_context(
            precinct=spatial_location,
            precinct_verified=precinct_verified,
            tod_verified=tod_verified,
            tod_400_verified=tod_400_verified,
            tod_800_verified=tod_800_verified,
            shop_frontage_verified=shop_frontage_verified,
            tod_distance_m=(
                tod_distance
                if tod_distance > 0
                else None
            )
        )
    )

    spatial_summary = (
        urbion_spatial_verification_summary(
            spatial_context
        )
    )

    st.info(
        f"Spatial state: "
        f"{spatial_summary['verification_state']} "
        f"— {spatial_summary['verified_count']}/"
        f"{spatial_summary['total_checks']} checks verified."
    )

    # --------------------------------------------------------
    # EVIDENCE SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "🔎 Ringkasan Bukti"
    )

    evidence_col1, evidence_col2 = st.columns(2)

    with evidence_col1:

        st.write(
            f"**Sumber:** {evidence_source}"
        )

    with evidence_col2:

        st.write(
            f"**Rujukan:** "
            f"{evidence_reference or 'Belum dinyatakan'}"
        )

    st.write(
        f"**Kawasan:** {spatial_location}"
    )

    st.caption(
        "Status pengesahan spatial tidak dianggap sah "
        "semata-mata berdasarkan pemilihan sumber; "
        "bukti spatial perlu tersedia untuk semakan."
    )


    # RUN ASSESSMENT
    # ========================================================

    if st.button(
        "🔍 RUN URBION ASSESSMENT",
        type="primary",
        use_container_width=True
    ):

        proposal = {
            "development_type": development_type,
            "authority": authority,
            "planning_reference": planning_reference,
            "Plot Ratio": plot_ratio,
            "Building Height": building_height,
            "Perimeter Planting": perimeter,
            "Landscaped Pedestrian Walkway": walkway,
            "spatial_context": spatial_context
        }

        retrieved_rules = (
            urbion_retrieve_rules(
                development_type=development_type,
                authority=authority,
                spatial_context=spatial_context
            )
        )

        # ========================================================

        # MASTER-59B CANONICAL ENGINE PIPELINE

        # ========================================================

        #

        # IMPORTANT:

        # The legacy UI previously executed applicability and

        # compliance one-rule-at-a-time using an obsolete

        # interface.

        #

        # The recovered engine uses:

        #

        #   proposal + retrieved_rules

        #          ↓

        #   applicability_results

        #          ↓

        #   compliance_results

        #          ↓

        #   overall_status

        #

        # We explicitly import the recovered module functions

        # here so the legacy function definitions embedded in

        # this app cannot shadow the canonical engine.

        # ========================================================



        from urbion_applicability import (

            urbion_check_applicability as _master59_check_applicability

        )



        from urbion_compliance import (

            urbion_evaluate_compliance as _master59_evaluate_compliance,

            urbion_calculate_overall_status as _master59_calculate_overall_status

        )



        # ========================================================

        # CANONICAL APPLICABILITY

        # ========================================================



        applicability_results = (

            _master59_check_applicability(

                proposal,

                retrieved_rules

            )

        )



        # ========================================================

        # CANONICAL COMPLIANCE

        # ========================================================



        compliance_results = (

            _master59_evaluate_compliance(

                applicability_results,

                proposal

            )

        )



        # ========================================================

        # CANONICAL OVERALL STATUS

        # ========================================================



        overall_status = (

            _master59_calculate_overall_status(

                compliance_results

            )

        )



        # ========================================================

        # UI RESULT NORMALISATION

        # ========================================================

        #

        # The rest of the existing UI expects assessment_results.

        # We preserve that contract while using the recovered

        # canonical engine above.

        # ========================================================



        assessment_results = []



        for result in compliance_results:



            assessment_results.append(

                {

                    "rule_id":

                        result.get("rule_id"),



                    "parameter":

                        result.get("parameter"),



                    "proposed":

                        result.get(

                            "proposed",

                            proposal.get(

                                result.get("parameter"),

                                "N/A"

                            )

                        ),



                    "requirement":

                        result.get("requirement"),



                    "applicability":

                        result.get("applicability"),



                    "status":

                        result.get("status"),



                    "reason":

                        result.get("reason"),



                    "source_document":

                        result.get(

                            "source_document"

                        ),



                    "source_section":

                        result.get(

                            "source_section"

                        ),



                    "evidence_text":

                        result.get(

                            "evidence_text"

                        ),



                    "evidence_classification":

                        result.get(

                            "evidence_classification"

                        ),



                    "traceability":

                        result.get(

                            "traceability"

                        ),



                    "spatial_condition":

                        result.get(

                            "spatial_condition"

                        )

                }

            )
        assessment_record = {

            "Lot":
                lot_number,

            "Location":
                location,

            "Authority":
                authority,

            "Site Area":
                site_area,

            "Development Type":
                development_type,

            "Plot Ratio":
                plot_ratio,

            "Building Height":
                building_height,

            "Perimeter Planting":
                perimeter,

            "Landscaped Walkway":
                walkway,

            "Status":
                overall_status,

            "Spatial Context":
                spatial_context,

            "Retrieved Rules":
                retrieved_rules,

            "Compliance Results":
                assessment_results,

            "Created":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
        }

        st.session_state.assessment_history = (
            urbion_save_assessment(
                assessment_record
            )
        )

        st.success(
            "✅ URBION assessment completed and saved."
        )

        if "🔴" in overall_status:

            st.error(
                f"Overall Status: {overall_status}"
            )

        elif "🟠" in overall_status:

            st.warning(
                f"Overall Status: {overall_status}"
            )

        elif "🟡" in overall_status:

            st.warning(
                f"Overall Status: {overall_status}"
            )

        else:

            st.success(
                f"Overall Status: {overall_status}"
            )

        st.subheader(
            "⚖️ Compliance Matrix"
        )

        for item in assessment_results:

            status = item["status"]

            if status == "COMPLY":
                icon = "🟢"

            elif status == "NON-COMPLIANCE":
                icon = "🔴"

            elif status == "CONDITIONAL NON-COMPLIANCE":
                icon = "🟠"

            elif status == "NOT APPLICABLE":
                icon = "⚪"

            else:
                icon = "🟡"

            with st.expander(
                f"{icon} "
                f"{item['parameter']} — "
                f"{item['status']}"
            ):

                c1, c2 = st.columns(2)

                with c1:

                    st.write(
                        f"**Proposed:** "
                        f"{item['proposed']}"
                    )

                with c2:

                    st.write(
                        f"**Requirement:** "
                        f"{item['requirement']}"
                    )

                st.write(
                    f"**Applicability:** "
                    f"{item['applicability']}"
                )

                st.info(
                    item["reason"]
                )

                st.markdown(
                    "### 📚 Evidence & Traceability"
                )

                st.write(
                    f"**Rule ID:** "
                    f"{item['rule_id']}"
                )

                st.write(
                    f"**Source:** "
                    f"{item['source_document']}"
                )

                st.write(
                    f"**Section:** "
                    f"{item['source_section']}"
                )

                st.write(
                    f"**Spatial Condition:** "
                    f"{item['spatial_condition']}"
                )

                st.code(
                    item["evidence_text"]
                )

                st.write(
                    f"**Evidence Classification:** "
                    f"{item['evidence_classification']}"
                )

                st.write(
                    f"**Traceability:** "
                    f"{item['traceability']}"
                )


# ============================================================
# ASSESSMENT HISTORY
# ============================================================

elif page == "📋 Assessments":

    st.title(
        "📋 Assessment History"
    )

    assessments = (
        urbion_load_assessments()
    )

    st.session_state.assessment_history = (
        assessments
    )

    if not assessments:

        st.info(
            "No assessments have been recorded yet."
        )

    else:

        st.write(
            f"**{len(assessments)} saved assessment(s)**"
        )

        for index, item in enumerate(
            reversed(assessments),
            start=1
        ):

            status = item.get(
                "Status",
                "🟡 REQUIRES REVIEW"
            )

            with st.expander(
                f"{status} — "
                f"Lot {item.get('Lot', '—')} — "
                f"{item.get('Created', '—')}"
            ):

                c1, c2 = st.columns(2)

                with c1:

                    st.write(
                        f"**Location:** "
                        f"{item.get('Location', '—')}"
                    )

                    st.write(
                        f"**Development:** "
                        f"{item.get('Development Type', '—')}"
                    )

                    st.write(
                        f"**Authority:** "
                        f"{item.get('Authority', '—')}"
                    )

                with c2:

                    st.write(
                        f"**Plot Ratio:** "
                        f"{item.get('Plot Ratio', '—')}"
                    )

                    st.write(
                        f"**Building Height:** "
                        f"{item.get('Building Height', '—')}"
                    )

                    st.write(
                        f"**Created:** "
                        f"{item.get('Created', '—')}"
                    )

                st.markdown(
                    "### 🗺️ Spatial Context"
                )

                st.json(
                    item.get(
                        "Spatial Context",
                        {}
                    )
                )

                results = item.get(
                    "Compliance Results",
                    []
                )

                if results:

                    st.markdown(
                        "### ⚖️ Compliance Results"
                    )

                    for result in results:

                        st.write(
                            f"**{result.get('parameter', '—')}** "
                            f"— "
                            f"{result.get('status', '—')}"
                        )

                        st.caption(
                            result.get(
                                "reason",
                                ""
                            )
                        )

                        with st.expander(
                            "Evidence & Traceability"
                        ):

                            st.write(
                                f"Rule ID: "
                                f"{result.get('rule_id', '—')}"
                            )

                            st.write(
                                f"Source: "
                                f"{result.get('source_document', '—')}"
                            )

                            st.write(
                                f"Section: "
                                f"{result.get('source_section', '—')}"
                            )

                            st.write(
                                f"Evidence: "
                                f"{result.get('evidence_text', '—')}"
                            )

                            st.write(
                                f"Traceability: "
                                f"{result.get('traceability', '—')}"
                            )


# ============================================================
# POLICY LIBRARY
# ============================================================

elif page == "📚 Policy Library":

    st.title(
        "📚 Policy Library"
    )

    st.caption(
        "URBION rule database currently loaded."
    )

    for rule in URBION_RULE_DATABASE:

        with st.expander(
            f"{rule['rule_id']} — "
            f"{rule['parameter']}"
        ):

            st.write(
                f"**Requirement:** "
                f"{rule['requirement']}"
            )

            st.write(
                f"**Development Type:** "
                f"{rule['development_type']}"
            )

            st.write(
                f"**Spatial Condition:** "
                f"{rule['spatial_condition']}"
            )

            st.write(
                f"**Source:** "
                f"{rule['source_document']}"
            )

            st.code(
                rule["evidence_text"]
            )


# ============================================================
# SPATIAL INTELLIGENCE
# ============================================================

elif page == "📍 Spatial Intelligence":

    st.title(
        "📍 Spatial Intelligence"
    )

    st.caption(
        "Evidence-aware spatial verification."
    )

    c1, c2 = st.columns(2)

    with c1:

        spatial_lot = st.text_input(
            "Lot Number",
            value="11213",
            key="spatial_lot"
        )

    with c2:

        spatial_location = st.text_input(
            "Claimed Precinct / Location",
            value="Presint 2.2 / ZP2",
            key="spatial_location"
        )

    st.write("")

    st.subheader(
        "Spatial Verification"
    )

    p1, p2 = st.columns(2)

    with p1:

        p_verified = st.checkbox(
            "Precinct Verified",
            key="spatial_precinct_verified"
        )

        tod400 = st.checkbox(
            "TOD 400m Verified",
            key="spatial_tod400"
        )

    with p2:

        tod800 = st.checkbox(
            "TOD 800m Verified",
            key="spatial_tod800"
        )

        frontage = st.checkbox(
            "Shop Frontage Verified",
            key="spatial_frontage"
        )

    distance = st.number_input(
        "TOD Distance (m)",
        min_value=0.0,
        value=0.0,
        key="spatial_distance"
    )

    context = (
        urbion_create_spatial_context(
            precinct=spatial_location,
            precinct_verified=p_verified,
            tod_verified=(
                tod400
                or tod800
            ),
            shop_frontage_verified=frontage,
            tod_distance_m=(
                distance
                if distance > 0
                else None
            )
        )
    )

    statuses = (
        urbion_get_spatial_status(
            context
        )
    )

    summary = (
        urbion_spatial_verification_summary(
            context
        )
    )

    st.write("")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "Precinct",
            statuses["Precinct"]
        )

    with b:
        st.metric(
            "TOD 400m",
            statuses["TOD 400m"]
        )

    with c:
        st.metric(
            "TOD 800m",
            statuses["TOD 800m"]
        )

    with d:
        st.metric(
            "Shop Frontage",
            statuses["Shop Frontage"]
        )

    st.write("")

    st.info(
        f"Verification State: "
        f"{summary['verification_state']} "
        f"({summary['verified_count']}/"
        f"{summary['total_checks']})"
    )

    st.subheader(
        "Spatial Evidence Status"
    )

    st.warning(
        "URBION does not independently verify parcel "
        "location, TOD radius or frontage status without "
        "supporting spatial evidence."
    )

    st.subheader(
        "Planned Verification Inputs"
    )

    st.markdown(
        """
        - Parcel / cadastral boundary
        - Planning precinct boundary
        - TOD station location
        - 400 m TOD radius
        - 800 m TOD radius
        - Development frontage / typology
        """
    )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.title(
        "📊 Analytics"
    )

    assessments = (
        urbion_load_assessments()
    )

    st.metric(
        "Total Assessments",
        len(assessments)
    )

    if assessments:

        status_counts = {}

        for item in assessments:

            status = item.get(
                "Status",
                "UNKNOWN"
            )

            status_counts[status] = (
                status_counts.get(
                    status,
                    0
                ) + 1
            )

        st.subheader(
            "Assessment Status Distribution"
        )

        for status, count in (
            status_counts.items()
        ):

            st.write(
                f"**{status}:** {count}"
            )

    else:

        st.info(
            "No assessment data available."
        )


# ============================================================
# END
# ============================================================

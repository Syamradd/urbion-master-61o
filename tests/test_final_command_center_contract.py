from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_final_command_centre_is_wired():
    server = (ROOT / 'championship_server.py').read_text(encoding='utf-8')
    assert 'urbion_championship_final_command_center.js' in server
    assert 'urbion_championship_final_command_center_hotfix.js' in server
    assert 'urbion_championship_final_command_center_policy.js' in server
    assert 'urbion_championship_final_runtime_enforcer.js' in server
    assert 'def _exact_asset_handler(asset_name: str):' in server
    assert 'for _asset in sorted(ALLOWED_ASSETS):' in server
    assert 'app.state.frontend_release="MASTER-331"' in server


def test_final_command_centre_covers_required_case_flow_and_support_surfaces():
    ui = (ROOT / 'urbion_championship_final_command_center.js').read_text(encoding='utf-8')
    policy_ui = (ROOT / 'urbion_championship_final_command_center_policy.js').read_text(encoding='utf-8')
    enforcer = (ROOT / 'urbion_championship_final_runtime_enforcer.js').read_text(encoding='utf-8')
    required = [
        'Site / Project Full Name', 'Latitude / Longitude', 'State',
        'Pihak Berkuasa Tempatan (PBT)', 'District / Daerah', 'Lot / UPI Reference',
        'Project Reference', 'Land Use Type', 'Development Category', 'Activity',
        'Development / Proposal', 'Intensity / Plot Ratio', 'TOD Latitude / Longitude',
        'LIVE GIS / SPATIAL EVIDENCE', 'RESOLVE LOT', 'EVIDENCE', 'WHAT-IF',
        'DECISION', 'OUTPUT', 'OSC 3.0 Plus', 'ABOUT US', 'DATA SOURCES',
        'SYSTEM STATUS', 'Print', 'Export Case', 'RESET CASE',
        'JUPEM MyLot', 'JMG MyGEMS', 'JPS · Public Infobanjir', 'MyEQMS / EQMP Monitoring',
        'i-Plan · Current Land Use', 'i-Plan · Zoning', 'i-Plan · Committed Land Use',
        'i-Plan · KSAS', 'i-Plan · CFS', 'i-Plan · Ecological Network',
        'i-Plan · Heritage', 'i-Plan · Topography', 'i-Plan · Flood',
        'i-Plan · Disaster Risk', 'i-Plan · RFN', 'i-Plan · Affordable Housing',
        'MyGEMS · Major Faults', 'MyGEMS · Mines & Quarries', 'MyGEMS · Groundwater',
        'MyGEMS · Geoheritage / Geopark', 'MyGEMS · Lithology', 'MyGEMS · Seismic',
        'MyGEMS · Mineral Resources', 'CASE → GIS → EVIDENCE',
        'LIVE_QUERY', 'NO_FEATURE', 'QUERY_ERROR', 'EVIDENCE_GAP',
        'prefers-reduced-motion:reduce', 'urbion_logo_dark.svg'
    ]
    missing = [item for item in required if item not in ui]
    assert not missing, f'missing final command-centre scope: {missing}'
    assert 'FINAL COMMAND CENTRE DID NOT MOUNT' in enforcer
    assert 'urbion_championship_final_command_center.js?runtime=' in enforcer
    assert 'urbion_championship_ux_v5_integrity.js?runtime=' in enforcer
    policy_required = [
        'Policy & Guideline Intelligence', 'Garis Panduan Perancangan',
        'Town and Country Planning Act 1976 (Act 172)', 'National Land Code 1965 (Act 828)',
        'National Physical Plan (RFN)', 'State Structure Plan (RSN)',
        'Local Plan / RTD / adopted local controls', 'OSC 3.0 Plus development-control workflow',
        '/lcp/intelligence', 'guideline_intelligence', 'policy_graph', 'recommendations',
        'statutory approval'
    ]
    missing_policy = [item for item in policy_required if item not in policy_ui]
    assert not missing_policy, f'missing policy/guideline scope: {missing_policy}'

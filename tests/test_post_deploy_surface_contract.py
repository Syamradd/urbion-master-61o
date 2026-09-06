from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_post_deploy_surface_contract():
    server=(ROOT/'championship_server.py').read_text(encoding='utf-8')
    manifest=(ROOT/'DEPLOYMENT_MANIFEST.json').read_text(encoding='utf-8')
    visual=(ROOT/'urbion_championship_visual_overhaul.js').read_text(encoding='utf-8')
    cleanup=(ROOT/'urbion_championship_visual_cleanup.js').read_text(encoding='utf-8')
    assert 'app.state.frontend_release="MASTER-330"' in server
    assert 'urbion_championship_visual_cleanup.js' in server
    assert 'urbion_championship_visual_overhaul.js' in server
    assert 'urbion_logo_dark.svg' in server and 'urbion_logo_light.svg' in server
    assert '"deployment_ready": true' in manifest
    assert 'MAP EVIDENCE' in visual
    assert 'EVIDENCE BOUNDARY' in visual
    assert 'GEOSERVER_WMS' in visual
    assert 'ARCGIS_MAP' in visual
    for mode in ('SATELLITE · ESRI','HYBRID · ESRI','TOPO · ESRI','LIGHT · CARTO','DARK · CARTO','TERRAIN · OTM'):
        assert mode in cleanup

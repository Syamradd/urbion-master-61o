"""Deterministic showcase inputs for the URBION judging workflow."""

DEMO_SCENARIOS = [
    {"id":"TOD-COMPLY","name":"TOD Mixed-Use Candidate","tag":"COMPLY + HIGH POTENTIAL","inputs":{"site_lat":2.3,"site_lon":102.2,"tod_lat":2.302,"tod_lon":102.2,"plot_ratio":4.5,"precinct":"Terminal Sg. Udang","development_type":"TOD Development / Mixed Use","development_class":"Mixed Use","state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":"DEMO-TOD-01"}},
    {"id":"SHOP-COMPLY","name":"Shop Frontage — Verified","tag":"COMPLY","inputs":{"site_lat":2.3,"site_lon":102.2,"tod_lat":2.302,"tod_lon":102.2,"plot_ratio":4.5,"precinct":"Terminal Sg. Udang","development_type":"Commercial Shop Frontage","development_class":"Commercial","state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":"DEMO-COM-01","landscaped_pedestrian_walkway":1.5,"shop_frontage_verified":True}},
    {"id":"SHOP-FAIL","name":"Shop Frontage — Missing Walkway","tag":"NON-COMPLIANCE","inputs":{"site_lat":2.3,"site_lon":102.2,"tod_lat":2.302,"tod_lon":102.2,"plot_ratio":4.5,"precinct":"Terminal Sg. Udang","development_type":"Commercial Shop Frontage","development_class":"Commercial","state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":"DEMO-COM-02","landscaped_pedestrian_walkway":0.5,"shop_frontage_verified":True}},
    {"id":"OFFICE-REVIEW","name":"Shop-Office — Verification Gap","tag":"REQUIRES REVIEW","inputs":{"site_lat":2.3,"site_lon":102.2,"tod_lat":2.302,"tod_lon":102.2,"plot_ratio":4.5,"precinct":"Terminal Sg. Udang","development_type":"Commercial Shop-Office","development_class":"Commercial","state":"Melaka","district":"Melaka Tengah","pbt":"Majlis Bandaraya Melaka Bersejarah","lot_no":"DEMO-COM-03","building_height":4,"shop_office_verified":False}},
    {"id":"NON-MBMB","name":"Cross-PBT Evidence Guard","tag":"EVIDENCE REQUIRED","inputs":{"site_lat":3.07,"site_lon":101.52,"tod_lat":3.071,"tod_lon":101.52,"plot_ratio":3,"precinct":"Demo Precinct","development_type":"Urban Mixed Use","development_class":"Mixed Use","state":"Selangor","district":"Klang","pbt":"Majlis Bandaraya DiRaja Klang","lot_no":"DEMO-PBT-01"}},
]


def demo_scenarios():
    """Return a fresh deterministic catalog so callers cannot mutate the source list."""
    return [dict(item, inputs=dict(item["inputs"])) for item in DEMO_SCENARIOS]


def get_demo_scenario(scenario_id: str):
    """Resolve a scenario by stable id; return None when unknown."""
    return next((item for item in demo_scenarios() if item["id"] == scenario_id), None)

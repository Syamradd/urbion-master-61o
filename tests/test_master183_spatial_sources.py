from urbion_data_sources import map_layer_catalog, source_catalog


def test_master183_source_domains_are_present():
    sources = source_catalog()
    ids = {s['id'] for s in sources}
    assert {'iplan', 'jupem-mylot', 'jmg-mygems', 'jps-public-infobanjir', 'doe-myeqms'} <= ids


def test_master183_priority_visual_layers_are_advertised():
    layers = map_layer_catalog('Melaka')
    ids = {x['id'] for x in layers}
    assert {
        'iplan-current', 'iplan-zoning', 'iplan-committed',
        'iplan-topography', 'iplan-flood', 'iplan-disaster-risk', 'iplan-ksas',
        'iplan-cfs', 'iplan-ecology', 'iplan-heritage',
        'mygems-faults', 'mygems-quarries', 'mygems-groundwater',
        'mygems-lithology', 'mygems-seismic', 'mygems-mineral'
    } <= ids


def test_master183_portal_sources_remain_source_registry_context_only():
    sources = {s['id']: s for s in source_catalog()}
    assert sources['jps-public-infobanjir']['category'] == 'HYDROLOGY'
    assert sources['doe-myeqms']['category'] == 'ENVIRONMENT'
    assert sources['jupem-mylot']['category'] == 'CADASTRAL'
    layers = map_layer_catalog('Melaka')
    ids = {x['id'] for x in layers}
    assert not {'jps-infobanjir', 'myeqms', 'mylot'} & ids


def test_master183_query_only_layers_are_not_advertised():
    layers = map_layer_catalog('Melaka')
    ids = {x['id'] for x in layers}
    assert 'iplan-contour' not in ids
    assert not any(x.get('type') == 'ARCGIS_QUERY' for x in layers)


def test_master183_layers_keep_source_context_boundary():
    layers = map_layer_catalog('Melaka')
    for layer in layers:
        if layer.get('source') in {'iplan', 'jmg-mygems'}:
            assert layer.get('evidence') == 'SOURCE_CONTEXT'

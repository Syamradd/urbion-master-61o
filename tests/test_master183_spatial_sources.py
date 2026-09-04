from urbion_data_sources import map_layer_catalog, source_catalog


def test_master183_source_domains_are_present():
    sources = source_catalog()
    ids = {s['id'] for s in sources}
    assert {'iplan', 'jupem-mylot', 'jmg-mygems', 'jps-public-infobanjir', 'doe-myeqms'} <= ids


def test_master183_priority_layers_are_advertised():
    layers = map_layer_catalog('Melaka')
    ids = {x['id'] for x in layers}
    assert {
        'iplan-current', 'iplan-zoning', 'iplan-committed',
        'iplan-topography', 'iplan-flood', 'iplan-disaster-risk', 'iplan-ksas',
        'iplan-cfs', 'iplan-ecology', 'iplan-heritage', 'jps-infobanjir',
        'mygems-faults', 'mygems-quarries', 'mygems-groundwater',
        'mygems-lithology', 'mygems-seismic', 'mygems-mineral', 'myeqms', 'mylot'
    } <= ids


def test_master183_query_only_layers_are_not_advertised():
    layers = map_layer_catalog('Melaka')
    ids = {x['id'] for x in layers}
    assert 'iplan-contour' not in ids
    assert not any(x.get('type') == 'ARCGIS_QUERY' for x in layers)


def test_master183_layers_keep_source_context_boundary():
    layers = map_layer_catalog('Melaka')
    for layer in layers:
        if layer.get('source') in {'iplan', 'jmg-mygems', 'jps-public-infobanjir', 'doe-myeqms', 'jupem-mylot'}:
            assert layer.get('evidence') == 'SOURCE_CONTEXT'

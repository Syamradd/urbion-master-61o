import urbion_copilot


PAYLOAD = {
    "site_lat": 2.285,
    "site_lon": 102.196,
    "tod_lat": 2.286,
    "tod_lon": 102.197,
    "plot_ratio": 4.5,
    "precinct": "Terminal Sg. Udang",
    "development_type": "TOD Development / Mixed Use",
    "development_class": "Mixed Use",
    "state": "Melaka",
    "district": "Melaka Tengah",
    "pbt": "Majlis Bandaraya Melaka Bersejarah",
    "lot_no": "11213",
}


def test_network_context_is_optional_and_traceable(monkeypatch):
    monkeypatch.setattr(
        urbion_copilot,
        "network_distance_m",
        lambda *args: {"status": "LIVE_QUERY", "distance_m": 900.0, "evidence_state": "SOURCE_CONTEXT"},
    )
    payload = dict(PAYLOAD, network_target_lat=2.286, network_target_lon=102.197)
    packet = urbion_copilot.build_copilot_packet(payload)
    assert packet["spatial"]["network_access"]["distance_m"] == 900.0
    assert packet["spatial"]["network_access"]["evidence_state"] == "SOURCE_CONTEXT"
    assert packet["spatial"]["evidence_model"]["network_access"] == "SOURCE_CONTEXT"
    assert packet["statutory_verification"] == "NOT_CLAIMED"


def test_network_context_is_not_called_without_explicit_targets(monkeypatch):
    called = {"value": False}
    def fail_if_called(*args):
        called["value"] = True
        raise AssertionError("network routing should be opt-in")
    monkeypatch.setattr(urbion_copilot, "network_distance_m", fail_if_called)
    urbion_copilot.build_copilot_packet(PAYLOAD)
    assert called["value"] is False

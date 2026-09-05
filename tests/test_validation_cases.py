from urbion_validation import get_validation_case, validation_cases


def test_validation_case_catalog_is_three_case_report_contract():
    cases = validation_cases()
    assert [case["id"] for case in cases] == ["TC-01", "TC-02", "TC-03"]
    assert [case["focus"] for case in cases] == [
        "GIS & Spatial Validation",
        "Rule Retrieval & Compliance",
        "End-to-End Assessment",
    ]
    assert all(case["scenario_id"] for case in cases)


def test_end_to_end_case_has_two_what_if_variants():
    case = get_validation_case("TC-03")
    assert case is not None
    assert [item["id"] for item in case["variants"]] == ["LOWER-DENSITY", "HIGHER-DENSITY"]
    assert case["variants"][0]["overrides"]["plot_ratio"] == 3.0
    assert case["variants"][1]["overrides"]["plot_ratio"] == 6.0


def test_unknown_validation_case_is_not_resolved():
    assert get_validation_case("TC-99") is None

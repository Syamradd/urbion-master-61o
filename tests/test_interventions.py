from urbion_interventions import intervention_catalog, build_intervention_variants


def test_intervention_catalog_is_deterministic():
    a=intervention_catalog(); b=intervention_catalog()
    assert [x["id"] for x in a]==[x["id"] for x in b]
    assert len(a)>=4


def test_selected_interventions_are_isolated():
    variants=build_intervention_variants({}, ["FIX-WALKWAY","VERIFY-SHOP"])
    assert [x["id"] for x in variants]==["FIX-WALKWAY","VERIFY-SHOP"]
    variants[0]["overrides"]["landscaped_pedestrian_walkway"]=99
    assert intervention_catalog()[0]["overrides"]["landscaped_pedestrian_walkway"]==1.5

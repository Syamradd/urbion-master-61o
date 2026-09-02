"""Deterministic planning intervention presets for URBION Phase D."""
from __future__ import annotations
from typing import Any

INTERVENTIONS = [
    {"id":"FIX-WALKWAY","name":"Improve pedestrian walkway","description":"Raise landscaped pedestrian walkway to 1.5 m.","overrides":{"landscaped_pedestrian_walkway":1.5}},
    {"id":"VERIFY-SHOP","name":"Verify shop frontage","description":"Mark shop-frontage evidence as verified.","overrides":{"shop_frontage_verified":True}},
    {"id":"VERIFY-OFFICE","name":"Verify shop-office","description":"Mark shop-office evidence as verified.","overrides":{"shop_office_verified":True}},
    {"id":"LOWER-HEIGHT","name":"Reduce building height","description":"Set building height to 4 storeys for screening.","overrides":{"building_height":4}},
]

def intervention_catalog() -> list[dict[str, Any]]:
    return [{**x, "overrides":dict(x["overrides"])} for x in INTERVENTIONS]

def build_intervention_variants(base_inputs: dict[str, Any], ids: list[str] | None = None) -> list[dict[str, Any]]:
    wanted = set(ids or [x["id"] for x in INTERVENTIONS])
    variants=[]
    for item in intervention_catalog():
        if item["id"] in wanted:
            variants.append({"id":item["id"],"name":item["name"],"overrides":item["overrides"]})
    return variants

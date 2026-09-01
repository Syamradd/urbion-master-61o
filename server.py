from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import math
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

sys.path.insert(
    0,
    str(BASE_DIR)
)


from urbion_spatial import (
    urbion_create_spatial_context
)

from urbion_retrieval import (
    urbion_retrieve_rules
)

from urbion_applicability import (
    urbion_check_applicability
)

from urbion_compliance import (
    urbion_evaluate_compliance
)


app = FastAPI(
    title="URBION API",
    version="MASTER-61O"
)

# ============================================================
# URBION PUBLIC API — CORS
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



class AssessmentRequest(BaseModel):

    site_lat: float = Field(
        ...,
        ge=-90,
        le=90
    )

    site_lon: float = Field(
        ...,
        ge=-180,
        le=180
    )

    tod_lat: float = Field(
        ...,
        ge=-90,
        le=90
    )

    tod_lon: float = Field(
        ...,
        ge=-180,
        le=180
    )

    plot_ratio: float = Field(
        ...,
        gt=0
    )

    precinct: str = (
        "Terminal Sg. Udang"
    )


def distance_m(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371000

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dp = math.radians(
        lat2 - lat1
    )

    dl = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(dp / 2) ** 2
        +
        math.cos(p1)
        *
        math.cos(p2)
        *
        math.sin(dl / 2) ** 2
    )

    c = (
        2 *
        math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )
    )

    return R * c


def classify(
    distance
):

    if distance <= 400:

        return "TOD 400m"

    if distance <= 800:

        return "TOD 800m"

    return "OUTSIDE TOD 800m"


@app.get("/")
def root():

    return {
        "project": "URBION",
        "version": "MASTER-61O",
        "status": "ONLINE"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "engine": "URBION MASTER-61O"
    }


@app.post("/assess")
def assess(
    request: AssessmentRequest
):

    distance = distance_m(
        request.site_lat,
        request.site_lon,
        request.tod_lat,
        request.tod_lon
    )

    classification = classify(
        distance
    )

    tod_400 = (
        distance <= 400
    )

    tod_800 = (
        distance <= 800
    )


    spatial_context = (
        urbion_create_spatial_context(

            precinct=request.precinct,

            precinct_verified=True,

            tod_verified=(
                tod_400 or tod_800
            ),

            tod_400_verified=tod_400,

            tod_800_verified=tod_800,

            shop_frontage_verified=False,

            tod_distance_m=distance
        )
    )


    proposal = {

        "development_type":
            "TOD / Mixed-use Development",

        "authority":
            "MBMB",

        "planning_reference":
            "RT-MBMB-2035",

        "Plot Ratio":
            request.plot_ratio,

        "Building Height":
            None,

        "Perimeter Planting":
            None,

        "Landscaped Pedestrian Walkway":
            None,

        "spatial_context":
            spatial_context
    }


    retrieved_rules = (
        urbion_retrieve_rules(

            development_type=
                proposal[
                    "development_type"
                ],

            authority=
                proposal[
                    "authority"
                ],

            spatial_context=
                spatial_context
        )
    )


    applicability_results = (
        urbion_check_applicability(

            proposal,

            retrieved_rules
        )
    )


    compliance_results = (
        urbion_evaluate_compliance(

            applicability_results,

            proposal
        )
    )


    applicable = [

        item

        for item in compliance_results

        if item.get(
            "applicability"
        ) == "APPLICABLE"

    ]


    if applicable:

        primary = applicable[0]

        final_rule = primary.get(
            "rule_id"
        )

        final_status = primary.get(
            "status",
            "REQUIRES REVIEW"
        )

    elif classification == (
        "OUTSIDE TOD 800m"
    ):

        final_rule = None

        final_status = (
            "NOT APPLICABLE"
        )

    else:

        final_rule = None

        final_status = (
            "REQUIRES REVIEW"
        )


    return {

        "project":
            "URBION",

        "version":
            "MASTER-61O",

        "site": {

            "latitude":
                request.site_lat,

            "longitude":
                request.site_lon
        },

        "tod": {

            "latitude":
                request.tod_lat,

            "longitude":
                request.tod_lon
        },

        "precinct":
            request.precinct,

        "tod_distance_m":
            distance,

        "classification":
            classification,

        "retrieved_rules":
            retrieved_rules,

        "applicability_results":
            applicability_results,

        "compliance_results":
            compliance_results,

        "final_rule":
            final_rule,

        "final_status":
            final_status,

        "gis_provenance":
            "URBION GIS decision pipeline"
    }
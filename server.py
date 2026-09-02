from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import math
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from urbion_spatial import urbion_create_spatial_context
from urbion_retrieval import urbion_retrieve_rules
from urbion_applicability import urbion_check_applicability
from urbion_compliance import urbion_evaluate_compliance, urbion_calculate_overall_status
from urbion_site_intelligence import (
    STATE_PBT,
    DEVELOPMENT_CLASSES,
    build_site_analysis,
    policy_coverage,
    source_registry_snapshot,
)

app = FastAPI(title="URBION API", version="MASTER-62")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AssessmentRequest(BaseModel):
    site_lat: float = Field(..., ge=-90, le=90)
    site_lon: float = Field(..., ge=-180, le=180)
    tod_lat: float = Field(..., ge=-90, le=90)
    tod_lon: float = Field(..., ge=-180, le=180)
    plot_ratio: float = Field(default=4.5, gt=0)
    precinct: str = "Terminal Sg. Udang"
    development_type: str = "TOD Development / Mixed Use"
    development_class: str = "Mixed Use"
    state: str = "Melaka"
    district: str = "Melaka Tengah"
    pbt: str = "Majlis Bandaraya Melaka Bersejarah"
    lot_no: str = ""
    building_height: float | None = Field(default=None, ge=0)
    perimeter_planting: float | None = Field(default=None, ge=0)
    landscaped_pedestrian_walkway: float | None = Field(default=None, ge=0)
    shop_frontage_verified: bool = False
    shop_office_verified: bool = False

def distance_m(lat1, lon1, lat2, lon2):
    R = 6371000
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def classify(distance):
    if distance <= 400:
        return "TOD 400m"
    if distance <= 800:
        return "TOD 800m"
    return "OUTSIDE TOD 800m"

def normalise_class(development_type: str, development_class: str) -> str:
    if development_class in DEVELOPMENT_CLASSES:
        return development_class
    value = development_type.lower()
    if "residential" in value or "housing" in value:
        return "Residential"
    if "industrial" in value:
        return "Industrial"
    if "institution" in value or "education" in value or "health" in value:
        return "Institutional"
    if "recreation" in value or "tourism" in value:
        return "Recreation"
    if "infrastructure" in value or "utility" in value:
        return "Infrastructure"
    if "mixed" in value or "tod" in value:
        return "Mixed Use"
    return "Commercial"

@app.get("/")
def root():
    return {"project": "URBION", "version": "MASTER-62", "status": "ONLINE"}

@app.get("/health")
def health():
    return {"status": "healthy", "engine": "URBION MASTER-62"}

@app.get("/metadata")
def metadata():
    return {
        "project": "URBION HORIZON",
        "version": "MASTER-62",
        "states": sorted(STATE_PBT.keys()),
        "pbt": STATE_PBT,
        "development_classes": DEVELOPMENT_CLASSES,
        "source_registry": source_registry_snapshot(),
        "policy_coverage": "RT MBMB 2035 rule engine active for supported typologies; other PBTs are spatial-demo coverage only.",
    }

@app.post("/assess")
def assess(request: AssessmentRequest):
    distance = distance_m(request.site_lat, request.site_lon, request.tod_lat, request.tod_lon)
    classification = classify(distance)
    tod_400 = distance <= 400
    tod_800 = distance <= 800
    development_class = normalise_class(request.development_type, request.development_class)
    coverage = policy_coverage(request.pbt)

    # The frozen MASTER-61O decision engine remains the statutory-rule layer.
    # MASTER-62 adds site intelligence around it without inventing new rules.
    spatial_context = urbion_create_spatial_context(
        precinct=request.precinct,
        precinct_verified=True,
        tod_verified=(tod_400 or tod_800),
        tod_400_verified=tod_400,
        tod_800_verified=tod_800,
        shop_frontage_verified=request.shop_frontage_verified,
        shop_office_verified=request.shop_office_verified,
        tod_distance_m=distance,
    )

    proposal = {
        "development_type": request.development_type,
        "authority": "MBMB" if request.pbt == "Majlis Bandaraya Melaka Bersejarah" else request.pbt,
        "planning_reference": "RT MBMB 2035" if request.pbt == "Majlis Bandaraya Melaka Bersejarah" else "Local planning policy not loaded",
        "Plot Ratio": request.plot_ratio,
        "Building Height": request.building_height,
        "Perimeter Planting": request.perimeter_planting,
        "Landscaped Pedestrian Walkway": request.landscaped_pedestrian_walkway,
        "shop_frontage_verified": request.shop_frontage_verified,
        "shop_office_verified": request.shop_office_verified,
        "spatial_context": spatial_context,
    }

    retrieved_rules = []
    applicability_results = []
    compliance_results = []
    final_rule = None
    final_status = "REQUIRES REVIEW"

    if request.pbt == "Majlis Bandaraya Melaka Bersejarah":
        retrieved_rules = urbion_retrieve_rules(
            development_type=proposal["development_type"],
            authority=proposal["authority"],
            spatial_context=spatial_context,
        )
        applicability_results = urbion_check_applicability(proposal, retrieved_rules)
        compliance_results = urbion_evaluate_compliance(applicability_results, proposal)
        applicable = [item for item in compliance_results if item.get("applicability") == "APPLICABLE"]

        if applicable:
            final_rule = applicable[0].get("rule_id")
            overall = urbion_calculate_overall_status(compliance_results)
            if "NON-COMPLIANCE" in overall:
                final_status = "NON-COMPLIANCE"
            elif "CONDITIONAL RISK" in overall:
                final_status = "CONDITIONAL RISK"
            elif "COMPLY" in overall:
                final_status = "COMPLY"
            else:
                final_status = "REQUIRES REVIEW"
        elif classification == "OUTSIDE TOD 800m" and ("tod" in request.development_type.lower() or "mixed" in request.development_type.lower()):
            final_status = "NOT APPLICABLE"
    else:
        final_status = "REQUIRES REVIEW"
        compliance_results = [{
            "rule_id": None,
            "applicability": "NOT_LOADED",
            "status": "REQUIRES REVIEW",
            "reason": "URBION has site intelligence for this PBT, but its local statutory rule set is not loaded into the verified decision engine.",
        }]

    site_analysis = build_site_analysis(
        state=request.state,
        district=request.district,
        pbt=request.pbt,
        lot_no=request.lot_no,
        latitude=request.site_lat,
        longitude=request.site_lon,
        tod_distance_m=distance,
        development_class=development_class,
        development_type=request.development_type,
        policy_status=final_status,
        final_status=final_status,
    )

    return {
        "project": "URBION",
        "version": "MASTER-62",
        "site": {
            "latitude": request.site_lat,
            "longitude": request.site_lon,
            "state": request.state,
            "district": request.district,
            "pbt": request.pbt,
            "lot_no": request.lot_no or "Not specified",
        },
        "tod": {"latitude": request.tod_lat, "longitude": request.tod_lon},
        "precinct": request.precinct,
        "development_class": development_class,
        "development_type": request.development_type,
        "proposal": proposal,
        "tod_distance_m": distance,
        "classification": classification,
        "policy_coverage": coverage,
        "retrieved_rules": retrieved_rules,
        "applicability_results": applicability_results,
        "compliance_results": compliance_results,
        "final_rule": final_rule,
        "final_status": final_status,
        "site_analysis": site_analysis,
        "source_registry": source_registry_snapshot(),
        "gis_provenance": "URBION GIS decision pipeline + source registry; external portal live-query status is explicitly disclosed.",
    }

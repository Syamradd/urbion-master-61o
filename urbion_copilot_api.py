"""Production API for the unified bounded planner copilot."""
from fastapi import APIRouter, Body, HTTPException
from server import app
from urbion_copilot import build_copilot_packet

router = APIRouter(tags=["copilot"])

@router.post("/copilot/run")
def run_copilot(payload: dict = Body(default_factory=dict)):
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        raise HTTPException(status_code=422, detail={"code": "SITE_INPUT_REQUIRED"})
    try:
        return build_copilot_packet(
            inputs,
            variants=payload.get("variants"),
            radii=payload.get("radii") or (400, 800),
            constraints=payload.get("constraints"),
        )
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code": "COPILOT_INPUT_ERROR", "message": str(exc)}) from exc

app.include_router(router)

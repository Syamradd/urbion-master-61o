"""Production API surfaces for URBION's bounded planning-agent synthesis and copilot."""
import json

from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from server import app
from urbion_copilot import build_copilot_packet
from urbion_validation import validation_cases, run_validation_case
from urbion_planner_handoff import build_planner_handoff_from_copilot
from urbion_judge_demo import build_judge_demo
from urbion_llm_provider import generate_planner_explanation
from urbion_decision_os import build_decision_os
from urbion_championship_optional_assessment_api import assess_optional
from urbion_error_contract import canonical_error
import urbion_frontend_asset_guard

router = APIRouter(tags=["planning-agents"])


def _canonical_http_error(*, code: str, message: str, route: str, stage: str, source: str | None = None, retryable: bool = False, details=None, status_code: int = 422):
    return JSONResponse(
        status_code=status_code,
        content=canonical_error(
            code=code,
            message=message,
            route=route,
            stage=stage,
            source=source,
            evidence_state="UNVERIFIED",
            review_required=True,
            retryable=retryable,
            canonical_packet_available=False,
            details=details,
        ),
    )


@app.middleware("http")
async def _optional_tod_compat(request: Request, call_next):
    """Own only the optional-TOD assessment adapter; public `/what-if` stays canonical."""
    if request.method != "POST" or request.url.path != "/assess":
        return await call_next(request)

    body = await request.body()
    try:
        payload = json.loads(body.decode("utf-8")) if body else {}
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return _canonical_http_error(code="INVALID_JSON", message=str(exc), route=request.url.path, stage="REQUEST_PARSE", source="URBION_REQUEST_GATE", status_code=400)

    if not isinstance(payload, dict):
        return await call_next(request)

    tod_keys = ("tod_lat", "tod_lon")
    missing_tod = all(payload.get(key) in (None, "") for key in tod_keys)
    partial_tod = (payload.get("tod_lat") in (None, "")) != (payload.get("tod_lon") in (None, ""))
    if not (missing_tod or partial_tod):
        return await call_next(request)

    try:
        return JSONResponse(content=assess_optional(payload))
    except HTTPException as exc:
        return _canonical_http_error(code="OPTIONAL_TOD_INPUT_ERROR", message=str(exc.detail), route=request.url.path, stage="OPTIONAL_TOD", source="URBION_OPTIONAL_TOD", details=exc.detail, status_code=exc.status_code)
    except Exception as exc:
        return _canonical_http_error(code="OPTIONAL_TOD_INPUT_ERROR", message=str(exc), route=request.url.path, stage="OPTIONAL_TOD", source="URBION_OPTIONAL_TOD")


def _run(payload: dict):
    raw = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(raw, dict):
        raise ValueError("ASSESSMENT_INPUT_REQUIRED")
    return build_copilot_packet(
        raw,
        variants=payload.get("variants"),
        radii=payload.get("radii") or (400, 800),
        constraints=payload.get("constraints"),
    )


@router.post("/agents/run")
def run_agent_workflow(payload: dict = Body(default_factory=dict)):
    try:
        result = _run(payload)
        if isinstance(result, dict):
            result = dict(result)
            result["mode"] = "BOUNDED_PLANNER_AGENT_WORKFLOW"
            result["generation_boundary"] = "CANONICAL_PACKET_ONLY; AGENT_OUTPUTS_MUST_NOT_CREATE_A_SECOND_DECISION_STATE"
        return result
    except HTTPException as exc:
        detail = exc.detail if isinstance(exc.detail, dict) else {"detail": exc.detail}
        return _canonical_http_error(code=str(detail.get("code") or "AGENT_INPUT_ERROR"), message=str(detail.get("message") or detail.get("detail") or "Agent workflow input is invalid."), route="/agents/run", stage="AGENTS", source="URBION_AGENT_WORKFLOW", details=detail)
    except Exception as exc:
        return _canonical_http_error(code="AGENT_WORKFLOW_ERROR", message=str(exc), route="/agents/run", stage="AGENTS", source="URBION_AGENT_WORKFLOW")


@router.post("/copilot/run")
def run_copilot_workflow(payload: dict = Body(default_factory=dict)):
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        return _canonical_http_error(code="SITE_INPUT_REQUIRED", message="Valid site coordinates are required.", route="/copilot/run", stage="COPILOT", source="URBION_COPILOT")
    try:
        return build_copilot_packet(inputs, variants=payload.get("variants"), radii=payload.get("radii") or (400,800), constraints=payload.get("constraints"))
    except Exception as exc:
        return _canonical_http_error(code="COPILOT_INPUT_ERROR", message=str(exc), route="/copilot/run", stage="COPILOT", source="URBION_COPILOT")


@router.post("/copilot/explain")
def explain_copilot_workflow(payload: dict = Body(default_factory=dict)):
    """Add optional LLM narrative without changing deterministic planning outputs."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        return _canonical_http_error(code="SITE_INPUT_REQUIRED", message="Valid site coordinates are required.", route="/copilot/explain", stage="COPILOT_EXPLAIN", source="URBION_COPILOT")
    try:
        packet = build_copilot_packet(inputs, variants=payload.get("variants"), radii=payload.get("radii") or (400, 800), constraints=payload.get("constraints"))
        explanation = generate_planner_explanation(packet)
        return {"mode":"BOUNDED_PLANNER_COPILOT_LLM","explanation":explanation,"evidence_ledger":packet.get("evidence_ledger") or {},"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED","deterministic_packet":packet,"generation_boundary":"LLM_NARRATIVE_ONLY; DETERMINISTIC_PACKET_REMAINS_SOURCE_OF_TRUTH"}
    except Exception as exc:
        return _canonical_http_error(code="COPILOT_EXPLANATION_ERROR", message=str(exc), route="/copilot/explain", stage="COPILOT_EXPLAIN", source="URBION_COPILOT")


@router.post("/intelligence/decision-os")
def decision_os_workflow(payload: dict = Body(default_factory=dict)):
    """Run the unified deterministic copilot, then apply an evidence-gated planner-review gate."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        return _canonical_http_error(code="SITE_INPUT_REQUIRED", message="Valid site coordinates are required.", route="/intelligence/decision-os", stage="DECISION_OS", source="URBION_DECISION_OS")
    try:
        packet = build_copilot_packet(inputs, variants=payload.get("variants"), radii=payload.get("radii") or (400, 800), constraints=payload.get("constraints"))
        result = build_decision_os(packet)
        return {"mode":"URBION_DECISION_OS","decision_os":result,"deterministic_packet":packet,"decision_authority":"NONE","statutory_verification":"NOT_CLAIMED"}
    except Exception as exc:
        return _canonical_http_error(code="DECISION_OS_ERROR", message=str(exc), route="/intelligence/decision-os", stage="DECISION_OS", source="URBION_DECISION_OS")


@router.post("/planner/handoff")
def run_planner_handoff(payload: dict = Body(default_factory=dict)):
    """Run the production copilot and convert its evidence into a planner handoff."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        return _canonical_http_error(code="SITE_INPUT_REQUIRED", message="Valid site coordinates are required.", route="/planner/handoff", stage="PLANNER_HANDOFF", source="URBION_PLANNER_HANDOFF")
    try:
        return build_planner_handoff_from_copilot(inputs,copilot_fn=lambda raw: build_copilot_packet(raw,variants=payload.get("variants"),radii=payload.get("radii") or (400,800),constraints=payload.get("constraints")))
    except Exception as exc:
        return _canonical_http_error(code="PLANNER_HANDOFF_ERROR", message=str(exc), route="/planner/handoff", stage="PLANNER_HANDOFF", source="URBION_PLANNER_HANDOFF")


@router.post("/judge/demo")
def run_judge_demo(payload: dict = Body(default_factory=dict)):
    """Run one production copilot path and return a judge-ready evidence snapshot."""
    inputs = payload.get("assessment") or payload.get("assessment_inputs") or payload
    if not isinstance(inputs, dict) or inputs.get("site_lat") is None or inputs.get("site_lon") is None:
        return _canonical_http_error(code="SITE_INPUT_REQUIRED", message="Valid site coordinates are required.", route="/judge/demo", stage="JUDGE_DEMO", source="URBION_JUDGE_DEMO")
    try: return build_judge_demo(inputs, build_copilot_packet)
    except Exception as exc: return _canonical_http_error(code="JUDGE_DEMO_ERROR", message=str(exc), route="/judge/demo", stage="JUDGE_DEMO", source="URBION_JUDGE_DEMO")


@router.get("/validation/cases")
def list_validation_cases():
    return {"project":"URBION HORIZON","cases":validation_cases()}


@router.post("/validation/run/{case_id}")
def execute_validation_case(case_id: str):
    try: result = run_validation_case(case_id, assess_fn=lambda inputs: __import__('server').assess_core(__import__('server').AssessmentRequest(**inputs)), copilot_fn=build_copilot_packet)
    except Exception as exc: return _canonical_http_error(code="VALIDATION_CASE_ERROR", message=str(exc), route=f"/validation/run/{case_id}", stage="VALIDATION", source="URBION_VALIDATION")
    if result is None: return _canonical_http_error(code="VALIDATION_CASE_NOT_FOUND", message=f"Validation case '{case_id}' was not found.", route=f"/validation/run/{case_id}", stage="VALIDATION", source="URBION_VALIDATION", status_code=404)
    return result

app.include_router(router)

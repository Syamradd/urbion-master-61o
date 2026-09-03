"""Deployment gateway that adds optional advisory integrations without changing core rules."""
from fastapi import Body
from server import AssessmentRequest, app, assess_core
from urbion_gemini_redteam import gemini_configured, review_with_gemini


@app.get("/gemini/status")
def gemini_status():
    return {
        "provider": "Google Gemini",
        "role": "RED_TEAM_ADVISORY",
        "configured": gemini_configured(),
        "decision_authority": "NONE",
    }


@app.post("/gemini/red-team")
def gemini_red_team(packet: dict = Body(...)):
    return review_with_gemini(packet)


@app.post("/gemini/red-team-assessment")
def gemini_red_team_assessment(r: AssessmentRequest):
    """Run Gemini against the deterministic URBION assessment as an advisory review."""
    assessment = assess_core(r)
    packet = {
        "assessment": assessment,
        "guardrails": {
            "decision_authority": "NONE",
            "statutory_verification": "NOT_CLAIMED",
            "purpose": "independent red-team review only",
        },
    }
    return review_with_gemini(packet)

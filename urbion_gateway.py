"""Deployment gateway that adds optional advisory integrations without changing core rules."""
from fastapi import Body
from server import app
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

"""Optional Gemini narrative layer for URBION HORIZON.

The deterministic planning packet remains the source of truth. This module only
turns already-computed evidence into planner-facing prose when GEMINI_API_KEY is
configured. It never changes scores, rankings, approvals, or statutory status.
"""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"
MAX_PROMPT_CHARS = 24000
MAX_OUTPUT_CHARS = 4000


def _fallback(packet: dict) -> str:
    assessment = packet.get("assessment") or {}
    decision = packet.get("decision") or {}
    ledger = packet.get("evidence_ledger") or {}
    status = assessment.get("final_status") or decision.get("status") or "REQUIRES REVIEW"
    score = (assessment.get("site_analysis") or {}).get("score")
    review = ledger.get("review_required_items", 0)
    score_text = f" with a deterministic score of {score}" if isinstance(score, (int, float)) else ""
    return (f"URBION HORIZON screens this proposal as {status}{score_text}. "
            f"The evidence ledger contains {ledger.get('total_items', 0)} item(s), "
            f"including {review} requiring review. Validate source currency, geometry, "
            "planning rules and agency requirements before relying on the result.")


def _prompt(packet: dict) -> str:
    compact = {"assessment":packet.get("assessment"),"spatial":packet.get("spatial"),"knowledge":packet.get("knowledge"),"impact":packet.get("impact"),"scenario_intelligence":packet.get("scenario_intelligence"),"decision":packet.get("decision"),"evidence_ledger":packet.get("evidence_ledger"),"next_actions":packet.get("next_actions")}
    payload = json.dumps(compact, ensure_ascii=False, default=str)
    if len(payload) > MAX_PROMPT_CHARS:
        payload = payload[:MAX_PROMPT_CHARS] + "\n[CONTEXT_TRUNCATED_BY_URBION]"
    return ("You are the narrative layer of URBION HORIZON, a planning decision-support system. "
            "Summarize ONLY the supplied deterministic packet. Do not invent facts, policies, "
            "measurements, sources, approvals, or confidence. Distinguish CALCULATED, SOURCE_CONTEXT, "
            "USER_PROVIDED and VERIFIED evidence. Never say a proposal is approved or compliant. "
            "Return concise planner-facing prose with: finding, evidence caveat, and next action.\n\n"
            + payload)


def generate_planner_explanation(packet: dict, timeout: float = 12.0) -> dict:
    """Generate traceable prose without allowing the LLM to alter deterministic results."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return {"provider":"NONE","model":None,"status":"DISABLED_NO_API_KEY","text":_fallback(packet),"deterministic_source":True}
    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    url = f"{API_ROOT}/{model}:generateContent?key={key}"
    payload = {"contents":[{"parts":[{"text":_prompt(packet)}]}],"generationConfig":{"temperature":0.1,"maxOutputTokens":500}}
    request = Request(url,data=json.dumps(payload).encode("utf-8"),headers={"Content-Type":"application/json"},method="POST")
    try:
        with urlopen(request, timeout=timeout) as response: body = json.loads(response.read().decode("utf-8"))
        text = (((body.get("candidates") or [{}])[0].get("content") or {}).get("parts") or [{}])[0].get("text")
        if not isinstance(text, str) or not text.strip(): raise ValueError("Gemini returned no text")
        text = text.strip()
        if len(text) > MAX_OUTPUT_CHARS:
            text = text[:MAX_OUTPUT_CHARS].rstrip() + "…"
        return {"provider":"GEMINI","model":model,"status":"GENERATED","text":text,"deterministic_source":False}
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as exc:
        return {"provider":"GEMINI","model":model,"status":"FALLBACK","text":_fallback(packet),"deterministic_source":True,"error_type":type(exc).__name__}

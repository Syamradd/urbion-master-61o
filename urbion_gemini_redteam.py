"""Optional Gemini red-team adapter for URBION.

Gemini is advisory only. It cannot create statutory rules, compliance results,
approvals, or override the deterministic URBION decision engine.
Configure GEMINI_API_KEY only in the server environment; never commit it.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

SYSTEM_INSTRUCTION = (
    "You are URBION HORIZON's independent red-team reviewer. "
    "Review planning decision-support outputs for reasoning gaps, evidence overclaim, "
    "missing verification, scenario inconsistency, and unsafe statutory language. "
    "Do not invent Malaysian local-plan rules, PBT controls, cadastral facts, approvals, "
    "or source evidence. Treat SOURCE_CONTEXT and CALCULATED as different from VERIFIED. "
    "You are advisory only and must never approve development or override URBION's "
    "deterministic decision engine. Return concise JSON with verdict, risks, evidence_gaps, "
    "recommended_corrections, and statutory_boundary."
)


def gemini_configured() -> bool:
    return bool(os.getenv("GEMINI_API_KEY", "").strip())


def _clean_packet(packet: dict[str, Any]) -> dict[str, Any]:
    blocked = {"api_key", "gemini_api_key", "authorization", "password", "secret", "token"}

    def clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items() if k.lower() not in blocked}
        if isinstance(value, list):
            return [clean(v) for v in value]
        return value

    return clean(packet)


def build_redteam_prompt(packet: dict[str, Any]) -> str:
    return SYSTEM_INSTRUCTION + "\n\nURBION DECISION PACKET:\n" + json.dumps(
        _clean_packet(packet), ensure_ascii=False, separators=(",", ":")
    ) + "\n\nReturn JSON only."


def review_with_gemini(packet: dict[str, Any], timeout_seconds: float = 20.0) -> dict[str, Any]:
    """Run an advisory Gemini review; failures never block URBION's core decision."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL
    if not key:
        return {
            "status": "NOT_CONFIGURED",
            "provider": "Google Gemini",
            "role": "RED_TEAM_ADVISORY",
            "decision_authority": "NONE",
            "message": "GEMINI_API_KEY is not configured; deterministic URBION decision flow remains active.",
        }

    url = f"{API_BASE}/{model}:generateContent?key={key}"
    body = {
        "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "contents": [{"parts": [{"text": build_redteam_prompt(packet)}]}],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
        try:
            review = json.loads(text)
        except json.JSONDecodeError:
            review = {"raw_review": text}
        return {
            "status": "LIVE",
            "provider": "Google Gemini",
            "model": model,
            "role": "RED_TEAM_ADVISORY",
            "decision_authority": "NONE",
            "review": review,
        }
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as exc:
        return {
            "status": "UNAVAILABLE",
            "provider": "Google Gemini",
            "model": model,
            "role": "RED_TEAM_ADVISORY",
            "decision_authority": "NONE",
            "message": "Gemini red-team review is unavailable; deterministic URBION decision flow remains active.",
            "error_type": type(exc).__name__,
        }

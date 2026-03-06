"""
AI Strategic Advisor — backend proxy for Anthropic API calls.
Keeps the API key server-side.
"""
from __future__ import annotations

import json
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/advisor", tags=["Advisor"])


class AdvisorRequest(BaseModel):
    synopsis: str
    budget: float


class Recommendation(BaseModel):
    jurisdiction: str
    rate: str
    estimated_credit: str
    reason: str
    best_for: str


class AdvisorResponse(BaseModel):
    recommendations: list[Recommendation]


@router.post("/recommend", response_model=AdvisorResponse)
async def advisor_recommend(req: AdvisorRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY is not configured on the server.",
        )

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        prompt = (
            "You are a film tax incentive advisor. "
            "Given this project synopsis and budget, recommend the top 3 US states or "
            "international jurisdictions and explain why. "
            "Be specific about incentive rates and qualifying criteria.\n\n"
            f"Synopsis: {req.synopsis}\n"
            f"Budget: ${int(req.budget):,}\n\n"
            "Respond in JSON only (no markdown): "
            '{"recommendations": [{"jurisdiction": "string", "rate": "string", '
            '"estimated_credit": "string", "reason": "string", "best_for": "string"}]}'
        )

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        text = message.content[0].text
        clean = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)
        return data

    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail=f"Invalid JSON from AI: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

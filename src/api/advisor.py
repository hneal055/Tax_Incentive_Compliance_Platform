"""
AI Advisor API — Anthropic-powered chat proxy with streaming and event summarization.
"""
import json
import logging
import os
from typing import AsyncGenerator, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.utils.database import prisma

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/advisor", tags=["AI Advisor"])

SYSTEM_PROMPT = """You are PilotForge AI Advisor, an expert in film and television production tax incentives. You help producers, production companies, and accountants maximize tax incentives across global jurisdictions.

Your expertise includes:
- Film tax credits and incentive programs across US states (Georgia, New York, California, Louisiana, Illinois, Michigan, New Jersey, Virginia, Colorado, Hawaii, Oregon, Montana, Mississippi, New Mexico, etc.)
- International programs (UK AVEC, Canadian provincial credits (BC, Ontario, Quebec), Australian offsets, Irish relief, French and Spanish tax rebates, New Zealand grants, etc.)
- Qualifying expense rules, minimum spend thresholds, and credit caps
- Federal incentives (Section 181, etc.) and stacking strategies
- Application documentation requirements and submission timelines
- Budget optimization strategies for maximum incentive yield

Always provide specific, actionable information. Include credit rates, thresholds, and program names when relevant. Format responses with markdown for readability. Note that tax laws change — recommend consulting a production accountant for final compliance decisions."""

SUMMARIZATION_SYSTEM = (
    "You are a regulatory intelligence analyst specializing in film and television "
    "production tax incentives. Summarize the following regulatory update in 2-3 concise "
    "sentences. Focus on: what changed, which jurisdictions are affected, and the impact "
    "on productions. Be factual and specific."
)


# ── Pydantic models ───────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str   # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    production_id: Optional[str] = None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_client():
    """Return an AsyncAnthropic client, raising 503 if key not configured."""
    import anthropic  # lazy import — only needed when route is hit
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Advisor is not configured — ANTHROPIC_API_KEY not set",
        )
    return anthropic.AsyncAnthropic(api_key=api_key)


async def _build_system_prompt(production_id: Optional[str]) -> str:
    """Extend base system prompt with production context if a production is selected."""
    if not production_id:
        return SYSTEM_PROMPT

    try:
        prod = await prisma.production.find_unique(
            where={"id": production_id},
            include={"jurisdiction": True},
        )
        if prod:
            ctx = (
                f"\n\nCurrent production context:\n"
                f"- Title: {prod.title}\n"
                f"- Type: {prod.productionType}\n"
                f"- Company: {prod.productionCompany}\n"
                f"- Total Budget: ${prod.budgetTotal:,.0f}\n"
            )
            if prod.budgetQualifying:
                ctx += f"- Qualifying Budget: ${prod.budgetQualifying:,.0f}\n"
            ctx += f"- Status: {prod.status}\n"
            if hasattr(prod, "jurisdiction") and prod.jurisdiction:
                ctx += (
                    f"- Primary Jurisdiction: {prod.jurisdiction.name} "
                    f"({prod.jurisdiction.code})\n"
                )
            ctx += "\nFactor this production context into your responses when relevant."
            return SYSTEM_PROMPT + ctx
    except Exception as e:
        logger.warning(f"Could not load production context for {production_id}: {e}")

    return SYSTEM_PROMPT


async def _stream_chunks(messages: list[dict], system: str) -> AsyncGenerator[str, None]:
    """Yield SSE-formatted text chunks from Anthropic streaming API."""
    client = _get_client()
    try:
        async with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {json.dumps({'delta': text})}\n\n"
        yield "data: [DONE]\n\n"
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Anthropic streaming error: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/chat", summary="Streaming AI advisor chat")
async def chat(req: ChatRequest):
    """
    Proxy chat messages to Anthropic with optional production context.
    Returns a server-sent events (SSE) stream of delta chunks.
    Each chunk: `data: {"delta": "..."}\\n\\n`
    Stream end: `data: [DONE]\\n\\n`
    """
    system = await _build_system_prompt(req.production_id)
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    return StreamingResponse(
        _stream_chunks(messages, system),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post(
    "/summarize-event/{event_id}",
    summary="AI-summarize a monitoring event and persist the result",
)
async def summarize_event(event_id: str):
    """
    Fetch a MonitoringEvent, send its content to Claude Haiku for a structured
    2-3 sentence summary, and store the result in `MonitoringEvent.summary`.
    Returns the updated event record.
    """
    event = await prisma.monitoringevent.find_unique(where={"id": event_id})
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    client = _get_client()

    content_parts = [f"Title: {event.title}"]
    if event.summary:
        content_parts.append(f"Content: {event.summary}")
    if event.url:
        content_parts.append(f"Source URL: {event.url}")

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=SUMMARIZATION_SYSTEM,
            messages=[{"role": "user", "content": "\n".join(content_parts)}],
        )
        summary_text = response.content[0].text

        updated = await prisma.monitoringevent.update(
            where={"id": event_id},
            data={"summary": summary_text},
        )
        logger.info(f"Summarized monitoring event {event_id}")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Event summarization failed for {event_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Summarization failed: {str(e)}",
        )

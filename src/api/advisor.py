"""
AI Advisor API — Anthropic-powered chat proxy with streaming and event summarization.
Falls back to scripted keyword-matched responses when no API key is configured,
preserving the full SSE streaming experience for demos.
"""
import asyncio
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


# ── Scripted demo responses (used when ANTHROPIC_API_KEY is not set) ──────────

_SCRIPTED: list[tuple[list[str], str]] = [
    (["georgia", "expens", "qualif"], (
        "**Georgia Qualifying Expenses**\n\n"
        "Georgia's Entertainment Industry Investment Act covers:\n\n"
        "**Eligible:** Below-the-line labor, equipment rentals, location fees, catering, "
        "post-production, and set construction.\n\n"
        "**Excluded:** Story rights, music rights, above-the-line compensation (unless resident).\n\n"
        "Minimum **$500k** qualified spend required. Georgia residents earn an additional "
        "**10% uplift** on their wages. The base credit is **20%**, rising to **30%** with "
        "the Georgia promotional logo included in end credits."
    )),
    (["california", " ca ", "ca film"], (
        "**California Film Tax Credit 3.0**\n\n"
        "California offers a **25% credit** on qualified expenditures.\n\n"
        "**Requirements:**\n"
        "- Minimum $1M qualified spend\n"
        "- 75% of principal photography must occur in California\n"
        "- Competitive allocation — projects are scored and ranked\n\n"
        "**Eligible:** Below-the-line labor, equipment, locations, post-production.\n\n"
        "**Max credit:** $25M per project. Apply through the California Film Commission."
    )),
    (["new york", " ny ", "new york film"], (
        "**New York Film Tax Credit**\n\n"
        "New York provides a **25–35% credit** on qualified below-the-line costs.\n\n"
        "**Base rate:** 25% statewide\n"
        "**Upstate bonus:** Additional 10% for productions outside NYC\n\n"
        "**Requirements:**\n"
        "- Minimum $1M qualified spend\n"
        "- 75% of shooting days in New York\n"
        "- Non-competitive — credits issued as earned\n\n"
        "**Max credit:** $7M per project. Applications accepted year-round."
    )),
    (["new mexico"], (
        "**New Mexico Film Production Tax Credit**\n\n"
        "New Mexico is one of the most competitive incentive programs in the US:\n\n"
        "**Base credit:** 25% on all direct production expenditures\n"
        "**Rural bonus:** +5% for productions outside Bernalillo County\n"
        "**TV bonus:** +10% for series spending over $30M in NM\n\n"
        "**No minimum spend** — accessible to indie and large-budget productions alike. "
        "Credits are refundable, meaning the state will cut you a check even with no tax liability."
    )),
    (["louisiana", " la "], (
        "**Louisiana Entertainment Tax Credit**\n\n"
        "Louisiana offers a **25% base rebate** plus a **15% resident payroll** uplift.\n\n"
        "**Requirements:** Minimum $300k qualified spend.\n\n"
        "Credits are **transferable** and can be sold at 85–90 cents on the dollar for "
        "immediate cash — ideal for productions that can't use the credit directly.\n\n"
        "Applications are handled by the Louisiana Office of Entertainment Industry Development."
    )),
    (["uk", "united kingdom", "avec", "bfi"], (
        "**UK Film Tax Relief (AVEC)**\n\n"
        "The UK offers **25% on qualifying UK production expenditure** (QUPE).\n\n"
        "**Requirements:**\n"
        "- Pass the BFI Cultural Test (minimum 18/35 points)\n"
        "- At least 10% of core expenditure must be UK spend\n"
        "- No minimum spend threshold\n\n"
        "High-End TV (HETV) productions with budgets over £1M/episode also qualify. "
        "The credit is payable through HMRC and can be claimed during production."
    )),
    (["canada", "british columbia", " bc ", "ontario", "quebec", " qc "], (
        "**Canadian Provincial Film Incentives**\n\n"
        "Canada's three largest provinces offer some of the world's strongest credits:\n\n"
        "**British Columbia:** 28% basic production services tax credit + 6% distant location bonus\n"
        "**Ontario:** 21.5% OFTTC + 18% OPSTC for foreign productions — stackable\n"
        "**Quebec:** 20% QPSP on all eligible Quebec spend; 32% on Quebec resident labor\n\n"
        "All provinces offer additional bonuses for visual effects, animation, and regional shoots."
    )),
    (["australia", " au "], (
        "**Australian Screen Production Incentive**\n\n"
        "Australia offers two complementary programs:\n\n"
        "**Producer Offset:** 40% for Australian feature films; 20% for TV/SVOD\n"
        "**Location Offset:** 16.5% for large-budget foreign productions (min AUD $15M)\n"
        "**PDV Offset:** 30% for post, digital & VFX work (min AUD $500k)\n\n"
        "Offsets are refundable tax rebates administered by Screen Australia. "
        "The Location Offset can be stacked with state-level incentives."
    )),
    (["highest", "best", "compare", "which jurisd", "top state", "most competitive"], (
        "**Top Film Incentive Jurisdictions — 2025**\n\n"
        "| Jurisdiction | Rate | Min Spend | Notes |\n"
        "|---|---|---|---|\n"
        "| New Mexico | 25–40% | None | Fully refundable |\n"
        "| Georgia | 20–30% | $500K | Logo bonus available |\n"
        "| Louisiana | 25% + 15% | $300K | Transferable credits |\n"
        "| New York | 25–35% | $1M | Upstate bonus |\n"
        "| California | 25% | $1M | Competitive allocation |\n"
        "| UK | 25% | None | AVEC — cultural test |\n"
        "| Ireland | 32% | None | Section 481 |\n"
        "| New Zealand | 40% | NZD 500K | NZSPG |\n\n"
        "The best jurisdiction depends on your budget, shooting locations, and crew residency. "
        "PilotForge's calculator can run a side-by-side comparison for your specific production."
    )),
    (["stack", "federal", "section 181", "181 "], (
        "**Stacking Federal + State Incentives**\n\n"
        "**Section 181 (Federal):** Allows 100% first-year deduction for productions up to $15M "
        "($20M in qualifying low-income communities). No application required — taken on your federal return.\n\n"
        "**How stacking works:**\n"
        "1. Section 181 reduces your federal taxable income\n"
        "2. State tax credit directly offsets your state tax liability\n"
        "3. Both are claimed independently — they don't reduce each other\n\n"
        "**Example:** A $5M production in Georgia could claim 181 federally AND the 30% Georgia "
        "credit — effectively double-dipping on a legitimate, IRS-sanctioned basis."
    )),
    (["document", "application", "require", "checklist", "submit"], (
        "**Standard Application Requirements**\n\n"
        "**Pre-production (file before shooting):**\n"
        "- Production company registration in the state\n"
        "- Estimated budget with expense category breakdown\n"
        "- Shooting schedule with location-days by county\n"
        "- Proof of financing (bank letter or equity commitment)\n\n"
        "**Post-production (file after final delivery):**\n"
        "- Final cost report certified by a CPA\n"
        "- Payroll records with residency verification for each crew member\n"
        "- Vendor invoices for all qualified expenditures\n"
        "- SAG/AFTRA contracts (if applicable)\n\n"
        "Most states allow electronic filing. Allow 60–120 days for credit certification."
    )),
    (["ireland", " ie ", "section 481"], (
        "**Ireland Section 481 Film Tax Credit**\n\n"
        "Ireland offers a **32% credit** on eligible Irish expenditure — one of the highest rates in Europe.\n\n"
        "**Requirements:**\n"
        "- No minimum spend threshold\n"
        "- Production must have cultural or creative merit\n"
        "- At least some Irish-resident crew required\n\n"
        "The credit applies to features, animation, TV series, and documentaries. "
        "Ireland also offers additional regional incentives through regional uplift schemes."
    )),
    (["minimum spend", "threshold", "minimum budget"], (
        "**Minimum Spend Requirements by Jurisdiction**\n\n"
        "| Jurisdiction | Minimum Spend |\n"
        "|---|---|\n"
        "| New Mexico | None |\n"
        "| Ireland | None |\n"
        "| UK | 10% UK spend (no $ floor) |\n"
        "| Louisiana | $300K |\n"
        "| Georgia | $500K |\n"
        "| New York | $1M |\n"
        "| California | $1M |\n"
        "| Australia | AUD $15M (Location Offset) |\n\n"
        "Lower-budget productions should prioritize states with no minimums (NM, Ireland) "
        "or low thresholds (Louisiana $300K, Georgia $500K)."
    )),
]

_DEFAULT_RESPONSE = (
    "**PilotForge AI Advisor**\n\n"
    "I'm your expert guide to film and television tax incentives across 30+ jurisdictions.\n\n"
    "I can help you with:\n\n"
    "- **Jurisdiction comparisons** — credit rates, caps, and eligibility across US states and international programs\n"
    "- **Qualifying expenses** — exactly what counts toward your incentive base in each state\n"
    "- **Application requirements** — documentation, timelines, and pre-certification steps\n"
    "- **Incentive stacking** — combining Section 181 with state credits for maximum yield\n"
    "- **Budget optimization** — structuring your spend to maximize the credit\n\n"
    "Try asking about Georgia, New Mexico, California, New York, Louisiana, or the UK — "
    "or ask me to compare jurisdictions for your specific budget."
)


def _scripted_response(question: str) -> str:
    """Return the best keyword-matched canned response for a question."""
    q = question.lower()
    for keywords, response in _SCRIPTED:
        if any(kw in q for kw in keywords):
            return response
    return _DEFAULT_RESPONSE


async def _stream_scripted(text: str) -> AsyncGenerator[str, None]:
    """Stream a scripted response word-by-word to simulate AI typing."""
    words = text.split(" ")
    chunk = ""
    for i, word in enumerate(words):
        chunk += ("" if i == 0 else " ") + word
        # Flush every 3 words for smooth streaming feel
        if (i + 1) % 3 == 0 or i == len(words) - 1:
            yield f"data: {json.dumps({'delta': chunk})}\n\n"
            chunk = ""
            await asyncio.sleep(0.03)
    yield "data: [DONE]\n\n"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_client():
    """Return an AsyncAnthropic client, or None if not available (no key or package missing)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic  # lazy import — optional dependency
        return anthropic.AsyncAnthropic(api_key=api_key)
    except ImportError:
        logger.warning("anthropic package not installed — using scripted demo responses")
        return None


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
    """Yield SSE-formatted text chunks. Uses Anthropic when configured, scripted fallback otherwise."""
    client = _get_client()
    if client is None:
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        logger.info("ANTHROPIC_API_KEY not set — using scripted demo response")
        async for chunk in _stream_scripted(_scripted_response(last_user)):
            yield chunk
        return
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
    if client is None:
        summary_text = f"Regulatory update: {event.title}. Review the source for full details on jurisdictional impact and compliance requirements."
        updated = await prisma.monitoringevent.update(where={"id": event_id}, data={"summary": summary_text})
        return updated

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

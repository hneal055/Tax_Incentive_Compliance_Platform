from fastapi import APIRouter, HTTPException, status
from src.utils.database import prisma
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/admin", tags=["Legacy Rules Engine"])

@router.get("/health")
async def legacy_health():
    count = await prisma.jurisdiction.count()
    return {"status": "ok", "api_version": "v1", "engine": "Scene Reader Studio Rules Engine", "platform": "PilotForge", "jurisdictions_loaded": count}

@router.get("/jurisdictions")
async def list_jurisdictions():
    jurisdictions = await prisma.jurisdiction.find_many(where={"active": True}, order={"name": "asc"})
    return {"total": len(jurisdictions), "jurisdictions": [{"id": j.id, "code": j.code, "name": j.name, "country": j.country, "type": j.type, "description": j.description, "website": j.website, "active": j.active} for j in jurisdictions]}

@router.get("/jurisdictions/{jid}")
async def get_jurisdiction(jid: str):
    j = await prisma.jurisdiction.find_first(where={"OR": [{"id": jid}, {"code": jid.upper()}]})
    if not j:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Jurisdiction not found")
    return {"id": j.id, "code": j.code, "name": j.name, "country": j.country, "type": j.type, "description": j.description, "website": j.website, "active": j.active}

@router.get("/jurisdictions/{jid}/programs")
async def get_programs(jid: str):
    j = await prisma.jurisdiction.find_first(where={"OR": [{"id": jid}, {"code": jid.upper()}]})
    if not j:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Jurisdiction not found")
    rules = await prisma.incentiverule.find_many(where={"jurisdictionId": j.id, "active": True}, order={"percentage": "desc"})
    return {"jurisdiction_id": j.id, "jurisdiction_name": j.name, "jurisdiction_code": j.code, "total": len(rules), "programs": [{"id": r.id, "name": r.ruleName, "code": r.ruleCode, "incentive_type": r.incentiveType, "percentage": r.percentage, "min_spend": r.minSpend, "max_credit": r.maxCredit, "eligible_expenses": r.eligibleExpenses, "excluded_expenses": r.excludedExpenses, "requirements": r.requirements, "effective_date": r.effectiveDate, "active": r.active} for r in rules]}

@router.get("/programs/{pid}/rules")
async def get_program_rules(pid: str):
    r = await prisma.incentiverule.find_unique(where={"id": pid})
    if not r:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Program not found")
    j = await prisma.jurisdiction.find_unique(where={"id": r.jurisdictionId})
    return {"program": {"id": r.id, "name": r.ruleName, "code": r.ruleCode, "incentive_type": r.incentiveType, "active": r.active}, "jurisdiction": {"id": j.id if j else None, "name": j.name if j else None, "code": j.code if j else None, "country": j.country if j else None, "website": j.website if j else None}, "credit_structure": {"base_rate": r.percentage, "max_credit": r.maxCredit, "min_spend": r.minSpend}, "qualified_expenses": {"eligible": r.eligibleExpenses, "excluded": r.excludedExpenses}, "requirements": r.requirements, "effective_date": r.effectiveDate, "expiration_date": r.expirationDate}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.program import Program
from app.models.jurisdiction import Jurisdiction
from app.schemas.program import ProgramResponse, ProgramRulesResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/programs/{program_id}/rules", response_model=ProgramRulesResponse)
async def get_program_rules(program_id: str, db: Session = Depends(get_db)):
    """
    Get the complete rule JSON for a specific program.
    Used for admin viewing and debugging.
    """
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    return {
        "program_id": program.id,
        "program_name": program.name,
        "jurisdiction_id": program.jurisdiction_id,
        "rules": program.rules,
        "last_updated": program.updated_at,
    }


@router.get("/jurisdictions/{jurisdiction_id}/programs")
async def list_programs_with_rules(jurisdiction_id: str, db: Session = Depends(get_db)):
    """
    List all programs for a jurisdiction with their rules.
    """
    programs = (
        db.query(Program).filter(Program.jurisdiction_id == jurisdiction_id).all()
    )

    return {
        "jurisdiction_id": jurisdiction_id,
        "programs": [
            {
                "id": p.id,
                "name": p.name,
                "active": p.active,
                "rules_preview": (
                    p.rules.get("base_credit_rate", "N/A") if p.rules else None
                ),
                "last_updated": p.updated_at,
            }
            for p in programs
        ],
    }


@router.get("/all-programs")
async def get_all_programs(db: Session = Depends(get_db), include_rules: bool = False):
    """
    Get all programs, optionally with full rules.
    """
    programs = db.query(Program).all()

    result = []
    for p in programs:
        program_data = {
            "id": p.id,
            "name": p.name,
            "jurisdiction_id": p.jurisdiction_id,
            "active": p.active,
        }
        if include_rules:
            program_data["rules"] = p.rules
        result.append(program_data)

    return {"programs": result}


from fastapi import APIRouter
from app.api.v1.endpoints import (
    productions,
    budgets,
    jurisdictions,
    eligibility,
    applications,
    documents,
    admin,
)

router = APIRouter()
router.include_router(productions.router, prefix="/productions", tags=["productions"])
router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
router.include_router(
    jurisdictions.router, prefix="/jurisdictions", tags=["jurisdictions"]
)
router.include_router(eligibility.router, prefix="/eligibility", tags=["eligibility"])
router.include_router(
    applications.router, prefix="/applications", tags=["applications"]
)
router.include_router(documents.router, prefix="/documents", tags=["documents"])
router.include_router(admin.router, prefix="/admin", tags=["admin"])

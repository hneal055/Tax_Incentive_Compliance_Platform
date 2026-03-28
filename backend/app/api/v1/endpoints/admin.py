"""Admin endpoints for viewing jurisdiction rules."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.db.session import get_db
from app.models.jurisdiction import Jurisdiction
from app.models.program import Program

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/jurisdictions")
async def get_jurisdictions(db: Session = Depends(get_db)):
    """List all jurisdictions."""
    jurisdictions = db.query(Jurisdiction).all()
    return {
        "jurisdictions": [
            {
                "id": str(j.id),
                "name": j.name,
                "type": j.type
            }
            for j in jurisdictions
        ]
    }


@router.get("/jurisdictions/{jurisdiction_id}/programs")
async def get_jurisdiction_programs(jurisdiction_id: str, db: Session = Depends(get_db)):
    """Get all programs for a jurisdiction."""
    programs = db.query(Program).filter(Program.jurisdiction_id == jurisdiction_id).all()
    return {
        "programs": [
            {
                "id": str(p.id),
                "name": p.name,
                "active": p.active,
                "has_rules": p.rules is not None
            }
            for p in programs
        ]
    }


@router.get("/programs/{program_id}/rules")
async def get_program_rules(program_id: str, db: Session = Depends(get_db)):
    """Get the complete rules JSON for a program."""
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Parse rules if stored as JSON string
    rules = {}
    if program.rules:
        try:
            rules = json.loads(program.rules) if isinstance(program.rules, str) else program.rules
        except:
            rules = {"error": "Could not parse rules"}
    
    return {
        "program_id": str(program.id),
        "program_name": program.name,
        "jurisdiction_id": str(program.jurisdiction_id),
        "rules": rules,
        "active": program.active
    }

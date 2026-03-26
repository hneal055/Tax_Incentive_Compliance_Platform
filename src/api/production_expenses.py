"""
Production-scoped expense endpoints — nested under /productions/{id}/expenses.
Matches the URL pattern expected by the frontend API client.
"""
import logging
from typing import Optional
from datetime import date

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.utils.database import prisma

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Expenses"])

EXPENSE_CATEGORIES = [
    "labor", "equipment", "locations", "post_production",
    "travel", "catering", "legal", "insurance", "visual_effects", "other",
]


# ── Pydantic models ───────────────────────────────────────────────────────────

class ExpenseCreate(BaseModel):
    category:      str
    description:   str
    amount:        float
    expenseDate:   str           # ISO date string YYYY-MM-DD
    isQualifying:  bool = True
    vendorName:    Optional[str] = None
    subcategory:   Optional[str] = None
    qualifyingNote: Optional[str] = None


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/productions/{production_id}/expenses",
            summary="List expenses for a production")
async def list_expenses(production_id: str):
    prod = await prisma.production.find_unique(where={"id": production_id})
    if not prod:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Production not found")

    expenses = await prisma.expense.find_many(
        where={"productionId": production_id},
        order={"expenseDate": "desc"},
    )
    total_amount      = sum(e.amount for e in expenses)
    qualifying_amount = sum(e.amount for e in expenses if e.isQualifying)
    return {
        "total":            len(expenses),
        "totalAmount":      total_amount,
        "qualifyingAmount": qualifying_amount,
        "nonQualifyingAmount": total_amount - qualifying_amount,
        "expenses":         expenses,
    }


@router.post("/productions/{production_id}/expenses",
             status_code=status.HTTP_201_CREATED,
             summary="Add an expense to a production")
async def create_expense(production_id: str, data: ExpenseCreate):
    prod = await prisma.production.find_unique(where={"id": production_id})
    if not prod:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Production not found")

    if data.amount <= 0:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Amount must be positive")

    try:
        expense_date = date.fromisoformat(data.expenseDate)
    except ValueError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid expenseDate — use YYYY-MM-DD")

    create_data: dict = {
        "productionId": production_id,
        "category":     data.category,
        "description":  data.description,
        "amount":       data.amount,
        "expenseDate":  expense_date.isoformat() + "T00:00:00Z",
        "isQualifying": data.isQualifying,
    }
    if data.vendorName:     create_data["vendorName"]    = data.vendorName
    if data.subcategory:    create_data["subcategory"]   = data.subcategory
    if data.qualifyingNote: create_data["qualifyingNote"] = data.qualifyingNote

    expense = await prisma.expense.create(data=create_data)
    logger.info(f"Expense created: {expense.id} for production {production_id}")
    return expense


@router.delete("/productions/{production_id}/expenses/{expense_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete an expense")
async def delete_expense(production_id: str, expense_id: str):
    expense = await prisma.expense.find_unique(where={"id": expense_id})
    if not expense or expense.productionId != production_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Expense not found")
    await prisma.expense.delete(where={"id": expense_id})
    return None

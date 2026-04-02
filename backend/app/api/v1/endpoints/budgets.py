from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.budget_line_item import BudgetLineItem

router = APIRouter()

@router.get("/{budget_id}/line_items")
def get_budget_line_items(budget_id: str, db: Session = Depends(get_db)):
    items = db.query(BudgetLineItem).filter(BudgetLineItem.budget_id == budget_id).all()
    return [
        {
            "id": item.id,
            "description": item.description,
            "amount": item.amount,
            "category": item.category,
            "is_eligible": item.is_eligible
        }
        for item in items
    ]

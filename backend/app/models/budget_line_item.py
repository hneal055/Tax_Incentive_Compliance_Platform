from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


class BudgetLineItem(Base):
    __tablename__ = "budget_line_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    budget_id = Column(
        String(36), ForeignKey("budgets.id", ondelete="CASCADE"), nullable=False
    )
    account_code = Column(String(50), nullable=True)
    description = Column(String(500), nullable=False)
    category = Column(String(100), nullable=True)
    amount = Column(Float, nullable=False)
    is_eligible = Column(Boolean, default=True)
    extra_data = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_budget_line_items_budget_id", "budget_id"),)

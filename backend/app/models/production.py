from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.sql import func
from app.db.session import Base
import uuid

class Production(Base):
    __tablename__ = "productions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    status = Column(Enum("planning", "pre_production", "production", "post", "completed", "archived", name="production_status"), default="planning")
    budget_id = Column(String(36), ForeignKey("budgets.id"), nullable=True)
    owner_id = Column(String(36), nullable=True)
    filming_locations = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

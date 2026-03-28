from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.sql import func
from app.db.session import Base
import uuid
import os

# For SQLite, use JSON instead of JSONB, and String for UUID
if os.getenv("DATABASE_URL", "").startswith("postgresql"):
    from sqlalchemy.dialects.postgresql import UUID as UUIDType, JSONB as JSONType
else:
    from sqlalchemy import String as UUIDType, JSON as JSONType

class Program(Base):
    __tablename__ = "programs"

    if os.getenv("DATABASE_URL", "").startswith("postgresql"):
        id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        jurisdiction_id = Column(PGUUID(as_uuid=True), ForeignKey("jurisdictions.id"), nullable=False)
        rules = Column(JSONB, nullable=True)
    else:
        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        jurisdiction_id = Column(String(36), ForeignKey("jurisdictions.id"), nullable=False)
        rules = Column(JSONType, nullable=True)
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

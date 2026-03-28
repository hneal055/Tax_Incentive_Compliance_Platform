from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
from app.db.session import Base
import uuid
import os

# Use appropriate UUID type based on database
if os.getenv("DATABASE_URL", "").startswith("postgresql"):
    from sqlalchemy.dialects.postgresql import UUID as UUIDType
else:
    from sqlalchemy import String as UUIDType
    # For SQLite, we'll store UUID as string
    def generate_uuid():
        return str(uuid.uuid4())

class Jurisdiction(Base):
    __tablename__ = "jurisdictions"

    if os.getenv("DATABASE_URL", "").startswith("postgresql"):
        id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    else:
        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    name = Column(String(100), nullable=False)
    type = Column(Enum("state", "country", "province", name="jurisdiction_type"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

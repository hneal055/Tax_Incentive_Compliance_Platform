"""Model for storing Largo project submissions and their incentive results."""
import os
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL.startswith("postgresql"):
    from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
    _id_col   = lambda: Column(PGUUID(as_uuid=False), primary_key=True)
    _json_col = lambda: Column(JSONB)
else:
    _id_col   = lambda: Column(String(36), primary_key=True)
    _json_col = lambda: Column(Text)

from app.db.session import Base


class LargoProject(Base):
    __tablename__ = "largo_projects"

    id                       = _id_col()
    project_name             = Column(String(200), nullable=False)
    largo_data               = _json_col()          # raw incoming request JSON
    incentive_recommendations = _json_col()          # computed response JSON
    created_at               = Column(DateTime, default=datetime.utcnow)

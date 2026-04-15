from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uuid
from datetime import datetime
import os

# Database setup
DATABASE_URL = "sqlite:///./tax_incentive.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define BudgetLineItem model (matching your existing table)
class BudgetLineItem(Base):
    __tablename__ = "budget_line_items"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    budget_id = Column(String(36), nullable=False)
    description = Column(String(500), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=True)
    is_eligible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "SceneIQ Budget API", "demo": "/static/budget_demo.html"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/budgets/{budget_id}/line_items")
def get_line_items(budget_id: str, db: Session = Depends(lambda: SessionLocal())):
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

# Optional: serve static files (like your demo HTML pages)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print(f"Serving static files from {static_dir}")


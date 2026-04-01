from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Determine database path based on environment
if os.getenv("RAILWAY_ENVIRONMENT"):
    # On Railway: use persistent volume mounted at /data
    DB_PATH = "/data/tax_incentive.db"
    os.makedirs("/data", exist_ok=True)
else:
    # Local development
    DB_PATH = "tax_incentive.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

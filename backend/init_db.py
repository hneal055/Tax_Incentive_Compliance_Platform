"""Initialize the database and create tables."""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine, Base
from app.models import Jurisdiction, Program

def init_db():
    """Create all tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("   Created tables: jurisdictions, programs")
    
    # List all tables created
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"   Tables: {', '.join(tables)}")

if __name__ == "__main__":
    init_db()

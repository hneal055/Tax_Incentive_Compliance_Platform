#!/usr/bin/env python3
"""Add Georgia jurisdiction to the database."""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction
import uuid

def add_georgia():
    db = SessionLocal()
    
    try:
        # Check if Georgia already exists
        existing = db.query(Jurisdiction).filter(
            Jurisdiction.name == "Georgia"
        ).first()
        
        if existing:
            print(f"⚠️  Georgia already exists!")
            print(f"   ID: {existing.id}")
            print(f"   Name: {existing.name}")
            print(f"   Type: {existing.type}")
        else:
            # Create new jurisdiction - store UUID as string for SQLite
            jurisdiction_id = str(uuid.uuid4())
            georgia = Jurisdiction(
                id=jurisdiction_id,
                name="Georgia",
                type="state"
            )
            db.add(georgia)
            db.commit()
            print(f"✅ Created Georgia jurisdiction!")
            print(f"   ID: {georgia.id}")
            print(f"   Name: {georgia.name}")
            print(f"   Type: {georgia.type}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_georgia()

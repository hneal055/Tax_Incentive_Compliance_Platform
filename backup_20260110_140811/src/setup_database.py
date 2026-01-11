# setup_database.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    # First, connect to default postgres database
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="your_password"  # Change this
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE tax_compliance;")
    print("✓ Database 'tax_compliance' created")
    
    # Create user
    cursor.execute("CREATE USER tax_user WITH PASSWORD 'tax_password123';")
    print("✓ User 'tax_user' created")
    
    # Grant privileges
    cursor.execute("GRANT ALL PRIVILEGES ON DATABASE tax_compliance TO tax_user;")
    print("✓ Privileges granted")
    
    cursor.close()
    conn.close()
    
    # Now connect to new database to create tables
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="tax_compliance",
        user="postgres",
        password="your_password"
    )
    cursor = conn.cursor()
    
    # Create jurisdictions table
    cursor.execute("""
    CREATE TABLE jurisdictions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(200) NOT NULL,
        code VARCHAR(20) UNIQUE NOT NULL,
        country VARCHAR(100) NOT NULL,
        state_province VARCHAR(100),
        incentive_rate DECIMAL(5,2) NOT NULL CHECK (incentive_rate >= 0 AND incentive_rate <= 100),
        incentive_type VARCHAR(50) NOT NULL,
        max_cap_amount DECIMAL(15,2),
        minimum_spend DECIMAL(15,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Create projects table
    cursor.execute("""
    CREATE TABLE projects (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(200) NOT NULL,
        production_company VARCHAR(200) NOT NULL,
        project_type VARCHAR(50) NOT NULL,
        total_budget DECIMAL(15,2) NOT NULL,
        qualified_spend DECIMAL(15,2) NOT NULL,
        estimated_incentive DECIMAL(15,2),
        status VARCHAR(50) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✓ Tables created successfully")
    print("\nConnection details:")
    print("Host: localhost")
    print("Port: 5432")
    print("Database: tax_compliance")
    print("Username: tax_user")
    print("Password: tax_password123")

if __name__ == "__main__":
    try:
        setup_database()
    except Exception as e:
        print(f"Error: {e}")
        
# create-db.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connection details
conn = psycopg2.connect(
    user="postgres",
    password="103855",
    host="127.0.0.1",
    port="5432",
    database="postgres"  # Connect to default postgres database
)

# Set autocommit mode
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Create cursor
cursor = conn.cursor()

# Create database
try:
    cursor.execute("CREATE DATABASE tax_incentives;")
    print("✓ Database 'tax_incentives' created successfully!")
except Exception as e:
    if "already exists" in str(e):
        print("✓ Database 'tax_incentives' already exists!")
    else:
        print(f"✗ Error: {e}")

# Close connection
cursor.close()
conn.close()
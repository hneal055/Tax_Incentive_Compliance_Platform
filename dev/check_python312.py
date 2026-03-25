import sys
import subprocess

print("🔍 Python 3.12 Environment Verification")
print("=" * 50)

# Check Python version
python_version = sys.version_info
print(f"Python Version: {sys.version}")
if python_version.major == 3 and python_version.minor == 12:
    print("✅ Python 3.12 confirmed")
else:
    print(f"❌ Wrong Python version: {python_version.major}.{python_version.minor}")
    print("   Expected: Python 3.12")
    sys.exit(1)

# Check key packages
required_packages = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "uvicorn"),
    ("psycopg2", "psycopg2"),
    ("reportlab", "reportlab"),
    ("openpyxl", "openpyxl"),
    ("sqlalchemy", "SQLAlchemy"),
]

print("\n📦 Checking installed packages:")
all_ok = True
for import_name, display_name in required_packages:
    try:
        __import__(import_name)
        print(f"✅ {display_name}")
    except ImportError:
        print(f"❌ {display_name} - missing")
        all_ok = False

# Check virtual environment
print(f"\n🏠 Virtual Environment: {sys.prefix}")
if "venv" in sys.prefix or ".venv" in sys.prefix:
    print("✅ Running in virtual environment")
else:
    print("⚠️  Not running in virtual environment")

print("\n" + "=" * 50)
if all_ok:
    print("🎉 Python 3.12 environment is ready!")
    print("\nNext steps:")
    print("1. Run: .\start.ps1")
    print("2. Visit: http://localhost:8000/docs")
else:
    print("❌ Some packages are missing")
    print("Run: pip install fastapi uvicorn psycopg2-binary reportlab openpyxl")
    sys.exit(1)

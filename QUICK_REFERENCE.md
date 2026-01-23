# 🚀 Tax Incentive Compliance Platform - Quick Reference

## Daily Startup (ONE COMMAND!)
```powershell
.\start.ps1
```
That's it! The script will:
- ✅ Find Python 3.12 automatically
- ✅ Create/fix virtual environment if needed
- ✅ Start Docker & PostgreSQL
- ✅ Install dependencies
- ✅ Launch the server

## First Time Setup
1. Install Python 3.12 from https://www.python.org/downloads/
   - ✅ **CHECK "Add Python to PATH"** during installation
2. Install Docker Desktop from https://www.docker.com/products/docker-desktop/
3. Clone this repository
4. Run `.\start.ps1` - it handles everything else!

## Important URLs
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Database GUI:** http://localhost:5555 (run: npx prisma studio)

## File Locations
- **Project:** `C:\Users\<YourUsername>\Tax_Incentive_Compliance_Platform`
- **Virtual Env:** `.venv` (auto-created by start.ps1)
- **Database:** Docker container `tax-incentive-db`
- **Config:** `.env` file (auto-created from .env.example)

## Common Commands
```powershell
# View all jurisdictions
curl http://localhost:8000/api/v1/jurisdictions/

# Check PostgreSQL
docker exec tax-incentive-db pg_isready -U postgres

# Restart everything
docker-compose restart
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

## Manual Startup (if needed)
```powershell
# 1. Start Docker Desktop (GUI)
# 2. Run these commands:
cd C:\Users\<YourUsername>\Tax_Incentive_Compliance_Platform
docker-compose up -d
.\.venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --reload
```

## Emergency Fixes
```powershell
# PostgreSQL won't start
docker-compose down
docker-compose up -d

# Dependencies missing
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Prisma errors
.\.venv\Scripts\python.exe -m prisma generate

# Complete reset (nuclear option)
docker-compose down -v
Remove-Item -Recurse -Force .venv
.\start.ps1
```

## GitHub
```powershell
git add .
git commit -m "Your message"
git push origin main
```

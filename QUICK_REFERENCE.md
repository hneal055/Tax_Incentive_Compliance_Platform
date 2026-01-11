# 🚀 PilotForge - Quick Reference

## Daily Startup (ONE COMMAND!)
```powershell
.\start.ps1
```

## Manual Startup
```powershell
# 1. Start Docker Desktop (GUI)
# 2. Run these commands:
cd C:\Projects\PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
docker-compose up -d
.\venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --reload
```

## Important URLs
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Database GUI:** http://localhost:5555 (run: npx prisma studio)

## Common Commands
```powershell
# View all jurisdictions
curl http://localhost:8000/api/v1/jurisdictions/

# Check PostgreSQL
docker exec tax-incentive-db pg_isready -U postgres

# Restart everything
docker-compose restart
python -m uvicorn src.main:app --reload
```

## Emergency Fixes
```powershell
# PostgreSQL won't start
docker-compose down
docker-compose up -d

# Dependencies missing
pip install -r requirements.txt

# Prisma errors
python -m prisma generate
```

## File Locations
- **Project:** `C:\Projects\PilotForge`
- **Virtual Env:** `.\venv`
- **Database:** Docker container `tax-incentive-db`
- **Config:** `.env` file

## GitHub
```powershell
git add .
git commit -m "Your message"
git push origin main
```

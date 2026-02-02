# Backend (FastAPI)
cd C:\Projects\Tax_Incentive_Compliance_Platform
$env:PYTHONPATH = (Get-Location).Path
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Frontend (Vite - in a new terminal)
cd C:\Projects\Tax_Incentive_Compliance_Platform
npm run frontend:dev  # This runs on port 3000

# Dashboard (if needed - in another terminal)
cd C:\Projects\Tax_Incentive_Compliance_Platform\dashboard-app
$env:HOST = "127.0.0.1"; npm start  # Port 3001 with IPv4
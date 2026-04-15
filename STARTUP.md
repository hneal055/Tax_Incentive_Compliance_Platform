# SceneIQ — Daily Startup Guide

## Quick Start (Normal Day)

Open **PowerShell** in `c:\Projects\Tax_Incentive_Compliance_Platform` and run:

```powershell
cd C:\Projects\Tax_Incentive_Compliance_Platform
docker compose up -d
```

That's it. All four services start in dependency order. Wait ~15 seconds, then open:

```
http://localhost
```

Login: `admin@pilotforge.com` / `pilotforge2024`

---

## Service Map

| Container | Role | URL |
|---|---|---|
| `pilotforge-db` | PostgreSQL 16 | `localhost:5435` (external) |
| `pilotforge-api` | FastAPI backend | `http://localhost:8001/api/0.1.0/` |
| `pilotforge-ui` | React frontend (Vite) | `http://localhost:3000` (direct, no proxy) |
| `pilotforge-nginx` | Reverse proxy | **`http://localhost`** ← use this |

> Always use `http://localhost` (port 80). The direct frontend port (`localhost:3000`) bypasses the API proxy — API calls will fail there.

---

## Status Check

```powershell
docker compose ps
```

Expected output — all four services should show `healthy` or `Up`:

```
NAME              STATUS
pilotforge-db     Up (healthy)
pilotforge-api    Up (healthy)
pilotforge-ui     Up (healthy)
pilotforge-nginx  Up
```

Detailed view with ports:

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## Stopping Services

```powershell
# Stop all services (preserves data)
docker compose stop

# Stop and remove containers (preserves DB volume)
docker compose down

# Full teardown including DB volume — WARNING: destroys all data
docker compose down -v
```

---

## Individual Service Commands

```powershell
# Restart backend or nginx (picks up config/env changes)
docker compose restart backend
docker compose restart nginx

# NOTE: restarting frontend alone does NOT apply source code changes.
# For frontend source changes, see "After Code Changes → Frontend" below.

# View live logs
docker compose logs -f backend
docker compose logs -f frontend

# View last 50 lines
docker compose logs --tail 50 backend
```

---

## After Code Changes

### Backend (`src/` changes)
The `./src` directory is volume-mounted — FastAPI picks up changes automatically via hot reload. No restart needed for most edits.

For changes to files **outside** `src/` (e.g., `maximizer.py`, `scripts/`):

```powershell
# Copy a file into the container
docker cp scripts/my_script.py pilotforge-api:/app/scripts/my_script.py

# Then run it
docker exec pilotforge-api python scripts/my_script.py
```

### Frontend (`frontend/src/` changes)
The frontend runs from a **pre-built image** — source changes require a full rebuild:

```powershell
docker compose build frontend
docker compose up -d --no-deps frontend
docker compose restart nginx
```

Then hard-refresh the browser (`Ctrl+Shift+R`) to clear the cached bundle.

### `docker-compose.yml` changes
Changes to environment variables, volumes, or ports require a full recreate:

```powershell
docker compose up -d --no-deps backend
```

---

## AI Advisor

The AI Advisor is powered by **Claude Sonnet** (Anthropic) via the `/advisor/chat` streaming endpoint.

### AI Advisor Requirements

- `ANTHROPIC_API_KEY` must be present in `.env` — Docker Compose passes it to the backend container automatically.
- Verify the key is live inside the container:

```powershell
docker exec pilotforge-api python -c "import os; print('Key present:', bool(os.getenv('ANTHROPIC_API_KEY')))"
```

### AI Advisor Features

- **Real Claude API** — open-ended questions (e.g. "how many counties in NY have incentives?") are answered by the live model, not keyword-matched scripted responses.
- **Production Questions panel** — select a production in the left sidebar and a blue *Production Questions* section appears with up to 4 questions tailored to that production's title, budget, and status.
- **Suggested Questions** — 10 static prompts covering GA, CA, NY, LA, TX, NM, SA, and UK incentives.
- **Scripted fallback** — if the API key is unavailable, keyword-matched responses cover the most common jurisdictions (GA, CA, NY, NM, LA, TX, SA, UK, Ireland, Canada, Australia).

### AI Advisor Troubleshooting

- **"30+ jurisdictions" or generic response** → API key not reaching the container. Check `.env` and `docker-compose.yml` environment block.
- **Scripted response instead of live AI** → Run the key-check command above. If `False`, recreate the backend: `docker compose up -d --no-deps backend`.

---

## FAQ

A full user-facing FAQ is available at [`FAQ.md`](FAQ.md) in the project root. It covers:

- Platform overview and intended audience
- Incentive type glossary — credit, rebate, grant, transferable, refundable, stacking
- Jurisdiction-specific Q&A: Georgia, California, New York, Louisiana, New Mexico, Texas, San Antonio, UK
- Feature walkthroughs: Dashboard, Calculator, Maximizer, Jurisdictions, Rule Review, AI Advisor
- Data currency, source verification, and compliance disclaimers

---

## Running Seed Scripts

```powershell
# Copy script to container, then execute
docker cp scripts/seed_jurisdictions.py pilotforge-api:/app/scripts/seed_jurisdictions.py
docker exec -e DATABASE_URL=postgresql://postgres:postgres@postgres:5432/tax_incentive_db pilotforge-api python scripts/seed_jurisdictions.py
```

**Fresh database recovery order:**

```powershell
# 1. Apply schema
docker exec pilotforge-api python -m prisma migrate deploy

# 2. Seed in order (each depends on the previous)
docker cp scripts/seed_jurisdictions.py       pilotforge-api:/app/scripts/seed_jurisdictions.py
docker cp scripts/seed_incentive_rules.py     pilotforge-api:/app/scripts/seed_incentive_rules.py
docker cp scripts/seed_more_jurisdictions.py  pilotforge-api:/app/scripts/seed_more_jurisdictions.py
docker cp scripts/seed_more_rules.py          pilotforge-api:/app/scripts/seed_more_rules.py

docker exec pilotforge-api python scripts/seed_jurisdictions.py
docker exec pilotforge-api python scripts/seed_incentive_rules.py
docker exec pilotforge-api python scripts/seed_more_jurisdictions.py
docker exec pilotforge-api python scripts/seed_more_rules.py
```

---

## Running the Monitor

```powershell
# Run monitor for a specific jurisdiction (use --code, not --jurisdiction)
docker exec pilotforge-api python monitor.py --code TX-SANANTONIO
docker exec pilotforge-api python monitor.py --code CA-SANDIEGO
docker exec pilotforge-api python monitor.py --code NM
```

---

## Database Access

### Connect via psql

```powershell
# Inside the container
docker exec -it pilotforge-db psql -U postgres -d tax_incentive_db

# Or from host (port 5435)
psql -h localhost -p 5435 -U postgres -d tax_incentive_db
```

### Run a quick query

```powershell
docker exec pilotforge-db psql -U postgres -d tax_incentive_db -c "SELECT code, name FROM jurisdictions ORDER BY code;"
```

---

## API Quick Tests

```powershell
# Health check
curl http://localhost:8001/api/0.1.0/health

# Login and capture token
$body = '{"email":"admin@pilotforge.com","password":"pilotforge2024"}'
$resp = Invoke-RestMethod -Uri http://localhost:8001/api/0.1.0/auth/login -Method Post -ContentType "application/json" -Body $body
$token = $resp.access_token

# List jurisdictions
Invoke-RestMethod -Uri http://localhost:8001/api/0.1.0/jurisdictions -Headers @{Authorization="Bearer $token"}

# Run Maximizer
$payload = '{"jurisdiction_codes":["TX","TX-SANANTONIO"],"project_type":"film","qualified_spend":5000000}'
Invoke-RestMethod -Uri http://localhost:8001/api/0.1.0/maximize -Method Post -ContentType "application/json" -Headers @{Authorization="Bearer $token"} -Body $payload
```

---

## Environment Variables

Key values in `.env` (read automatically by Docker Compose):

| Variable | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API key — enables real AI responses in AI Advisor |
| `DATABASE_URL` | Set in `docker-compose.yml` — not needed in `.env` for local dev |

> The `.env` file is in `.gitignore`. Never commit it.

---

## Troubleshooting

### Backend won't start / crash-looping

```powershell
docker logs pilotforge-api --tail 30
```

Common causes:
- `ModuleNotFoundError: No module named 'maximizer'` → `maximizer.py` not volume-mounted. Check `docker-compose.yml` volumes include `./maximizer.py:/app/maximizer.py`
- DB connection refused → postgres container not healthy yet; wait and retry
- `ANTHROPIC_API_KEY` not found → check `.env` has the key and `docker-compose.yml` passes `ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}`

### Frontend changes not showing

The frontend runs from a **pre-built image** — `restart` alone is not enough. A full rebuild is required:

```powershell
docker compose build frontend
docker compose up -d --no-deps frontend
docker compose restart nginx
```

Then hard-refresh the browser (`Ctrl+Shift+R`) to clear the cached JS bundle.

### API calls fail from `localhost:3000`

Use `http://localhost` (port 80 via nginx). The direct frontend port has no API proxy.

### Port already in use

```powershell
# Find what's using port 80
netstat -ano | findstr ":80 "

# Or use PowerShell
Get-NetTCPConnection -LocalPort 80 -State Listen | Select-Object -Property LocalAddress,LocalPort,OwningProcess
```

### Full reset (keeps DB data)

```powershell
docker compose down
docker compose up -d
```

### Nuclear reset (destroys all data)

```powershell
docker compose down -v
docker compose up -d
# Re-run all seed scripts after
```

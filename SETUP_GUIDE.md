# SceneIQ — Setup & Launch Guide

**Tax Incentive Compliance Platform for Film & TV Production**

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Docker Desktop** | [docs.docker.com/desktop](https://docs.docker.com/desktop/) — must be running before launch |
| **Windows 10/11** | PowerShell 5.1+ included by default |
| **Internet access** | Required on first launch to pull images (~2.2 GB total, one-time only) |

No Python, Node.js, or database installation required. Everything runs inside Docker.

---

## First-Time Setup

### Step 1 — Get the project

**Option A: Clone from GitHub**
```powershell
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform
```

**Option B: Download ZIP**
- Go to [github.com/hneal055/Tax_Incentive_Compliance_Platform](https://github.com/hneal055/Tax_Incentive_Compliance_Platform)
- Click **Code → Download ZIP** — extract to a folder of your choice

### Step 2 — Start Docker Desktop
Open Docker Desktop from the Start menu and wait for the whale icon in the system tray to stop animating (usually 30–60 seconds).

### Step 3 — Run the startup script
Open **PowerShell** in the project folder and run:

```powershell
.\start.ps1
```

**First launch** downloads ~2.2 GB of Docker images. This happens once — subsequent launches are fast (under 30 seconds).

The script will:
1. Verify Docker Desktop is running
2. Pull images from Docker Hub if not already present
3. Remove any conflicting containers
4. Start all 4 services (database, backend API, frontend, nginx)
5. Wait for the backend to be healthy
6. Open the dashboard automatically in your browser

---

## Accessing the Platform

| URL | Purpose |
|---|---|
| **http://localhost:3000** | Main dashboard (use this) |
| http://localhost | Same dashboard via nginx proxy |
| http://localhost:8001/docs | Live API documentation (Swagger UI) |

### Login credentials

| Field | Value |
|---|---|
| Email | `admin@pilotforge.com` |
| Password | `pilotforge2024` |

---

## What You'll See

The dashboard loads with three demo productions pre-seeded:

| Production | Type | Budget | Jurisdiction | Status |
|---|---|---|---|---|
| The Silent Horizon | Feature Film | $15M | Georgia | In Production |
| Echoes of Midnight | TV Series | $8M | New York | Pre-Production |
| Neon Pulse | Feature Film | $4.5M | California | Planning |

### Platform Features

**Dashboard**
- Budget volume, estimated tax credits, active projects, and alerts at a glance
- Budget vs. Actual Spend bar chart across all productions

**Productions**
- Create, view, and delete productions
- Each production linked to a jurisdiction

**Incentive Calculator**
- Select any production + jurisdiction
- Real-time calculation: qualified expenses × credit rate = estimated incentive
- Download report button

**Jurisdictions**
- 23 jurisdictions across USA, Canada, and international markets
- Search and filter by country or incentive type
- Incentive rules per jurisdiction (35 rules total)

**AI Advisor**
- Chat interface for tax incentive questions
- Production context selector — responses factor in your specific project
- Pre-built suggested questions for common scenarios

---

## Stopping the Platform

```powershell
docker compose down
```

Your data persists in the Docker volume (`pilotforge_postgres_data`) and will be there next time you run `.\start.ps1`.

---

## Restarting After a Break

Just run the startup script again — it handles everything:

```powershell
.\start.ps1
```

---

## Troubleshooting

### "Docker Desktop is not running"
Open Docker Desktop from the Start menu and wait for it to finish starting before running `start.ps1`.

### Browser opens but shows a blank page or login fails
Wait 10–15 seconds and refresh (`Ctrl+R`). The backend may still be completing its startup seeding. If the problem persists:
```powershell
docker compose restart backend
```

### Port already in use (3000, 80, or 8001)
Another application is using that port. Either stop that application, or run:
```powershell
docker compose down
.\start.ps1
```

### 500 error on login
An orphaned container from a previous session is interfering. The `start.ps1` script cleans these automatically. If you launched Docker manually instead of using the script, run:
```powershell
docker compose down
.\start.ps1
```

### Images won't pull ("unauthorized")
You need to log in to Docker Hub:
```powershell
docker login --username hneal1038
```
Use a Personal Access Token (not your password) from [hub.docker.com/settings/personal-access-tokens](https://hub.docker.com/settings/personal-access-tokens) with **Read** access.

### Dashboard shows $0 / empty chart
The demo productions weren't seeded. This can happen if the database was just created. Restart the backend to re-run the seed:
```powershell
docker compose restart backend
```
Wait 15 seconds, then refresh.

---

## For Developers

### Making backend code changes
The `src/` directory is live-mounted into the container. Edit files in `src/` and restart the backend to pick up changes:
```powershell
docker compose restart backend
```

### Making frontend code changes
The frontend is built into the Docker image — it requires a rebuild after changes:
```powershell
docker compose build frontend
docker compose up -d frontend
```

### Rebuilding everything from source
```powershell
docker compose build
docker compose up -d
```

### Pushing updated images to Docker Hub
```powershell
docker compose build
docker tag pilotforge-backend:latest hneal1038/pilotforge-backend:latest
docker tag pilotforge-frontend:latest hneal1038/pilotforge-frontend:latest
docker push hneal1038/pilotforge-backend:latest
docker push hneal1038/pilotforge-frontend:latest
```

### Database — fresh reset
```powershell
docker compose down -v        # removes the volume (all data deleted)
.\start.ps1                   # recreates and re-seeds from scratch
```

---

## Architecture

```
Browser
  └── http://localhost:3000
        └── pilotforge-ui  (React 19 + Vite + Tailwind CSS)
              └── http://localhost:80 (nginx reverse proxy)
                    ├── /           → pilotforge-ui:3000
                    └── /api/       → pilotforge-api:8000
                          └── pilotforge-db (PostgreSQL 16)
```

| Container | Image | Port |
|---|---|---|
| pilotforge-ui | hneal1038/pilotforge-frontend:latest | 3000 |
| pilotforge-api | hneal1038/pilotforge-backend:latest | 8001 (direct) |
| pilotforge-db | postgres:16-alpine | 5435 |
| pilotforge-nginx | nginx:alpine | 80 |

**Tech stack:** React 19 · TypeScript · Tailwind CSS v4 · FastAPI · Prisma ORM · PostgreSQL 16 · Docker

---

## Repository

- **GitHub:** [github.com/hneal055/Tax_Incentive_Compliance_Platform](https://github.com/hneal055/Tax_Incentive_Compliance_Platform)
- **Docker Hub:** [hub.docker.com/u/hneal1038](https://hub.docker.com/u/hneal1038)
- **Working branch:** `feature/test-ci`
- **Stable branch:** `main`

---

*SceneIQ — Tax Incentive Intelligence for Film & TV*

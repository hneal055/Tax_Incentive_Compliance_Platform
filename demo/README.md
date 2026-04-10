# PilotForge — Tax Incentive Intelligence Platform
## Demo Setup Guide

---

### Requirements

| | |
|---|---|
| **Software** | Docker Desktop (free) — [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) |
| **OS** | Windows 10/11, macOS 12+, or Linux |
| **Disk space** | ~2 GB (downloaded once on first launch) |
| **Internet** | Required for first launch only |

---

### Step-by-Step Setup

**Step 1 — Install Docker Desktop**

Download and install Docker Desktop from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
After installing, open it and wait for the whale icon in your taskbar to stop animating (fully started).

**Step 2 — Extract the zip file**

Extract `PilotForge-Demo.zip` to any folder on your computer (Desktop, Documents, etc.).
Keep all files together in the same folder — do not move individual files out.

**Step 3 — Launch the platform**

- **Windows:** Right-click `start.ps1` → **Run with PowerShell**
- **Mac/Linux:** Open Terminal in the extracted folder and run `docker compose up -d`

On first launch, Docker downloads the application images (~2 GB). This takes 3–10 minutes depending on your connection. Subsequent launches are instant.

**Step 4 — Open the dashboard**

The browser opens automatically. If it does not, navigate to:

```
http://localhost:3000
```

**Step 5 — Sign in**

| Field | Value |
|---|---|
| Email | `admin@pilotforge.com` |
| Password | `pilotforge2024` |

---

### Stopping the Demo

- **Windows:** Right-click `stop.ps1` → Run with PowerShell
- **Mac/Linux:** Run `docker compose down` in the folder

Your data (productions, calculations) is saved between sessions.

To reset to a clean slate:
```bash
docker compose down -v
```

---

### What's Included

| Module | Description |
|---|---|
| **Executive Dashboard** | Credit pipeline summary, budget volume, active project count |
| **Productions** | Create and manage film & TV productions |
| **Incentive Calculator** | Real-time credit estimates across all jurisdictions |
| **Jurisdiction Intelligence** | 23+ jurisdictions — USA, Canada, UK, EU, Australia, New Zealand |
| **AI Advisor** | Natural language Q&A for jurisdiction strategy and comparisons |
| **MMB Connector** | Cast & crew data import from production management systems |
| **Regulatory Feed** | Live monitoring of incentive program updates |

---

### Troubleshooting

**"Docker is not running"**
Open Docker Desktop from the Start Menu (Windows) or Applications (Mac). Wait ~30 seconds for it to fully start, then run `start.ps1` again.

**Dashboard shows a blank or loading page**
The backend takes up to 30 seconds to initialize on first launch. Wait, then refresh the browser.

**"Port 3000 is already in use"**
Another application on your computer is using port 3000. Either stop that application, or contact your PilotForge representative for an alternate configuration.

**PowerShell security warning on Windows**
If Windows blocks `start.ps1`, open PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Then try `start.ps1` again.

---

*PilotForge · Tax Incentive Intelligence for Film & TV Production*
*For support contact: [your email here]*

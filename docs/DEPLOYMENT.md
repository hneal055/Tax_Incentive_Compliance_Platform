# 🚀 Deployment Guide - Tax-Incentive Compliance Platform

> Step-by-step guide to deploy your platform to production

---

## 📋 Table of Contents

1. [Deployment Options](#deployment-options)
2. [Render.com Deployment](#rendercom-deployment-recommended)
3. [Railway.app Deployment](#railwayapp-deployment)
4. [Fly.io Deployment](#flyio-deployment)
5. [AWS Deployment](#aws-deployment)
6. [Environment Variables](#environment-variables)
7. [Database Setup](#database-setup)
8. [Post-Deployment](#post-deployment)
9. [Monitoring](#monitoring)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Deployment Options

| Platform | Difficulty | Cost | Best For |
|----------|------------|------|----------|
| **Render.com** | ⭐ Easy | Free tier | **Recommended** |
| Railway.app | ⭐⭐ Easy | Free $5/month | Quick deploy |
| Fly.io | ⭐⭐ Medium | Free tier | Docker users |
| AWS | ⭐⭐⭐ Hard | Pay-as-you-go | Enterprise |
| DigitalOcean | ⭐⭐ Medium | $4+/month | Full control |

---

## 🌟 Render.com Deployment (RECOMMENDED)

### **Why Render?**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Built-in PostgreSQL
- ✅ HTTPS included
- ✅ Easy environment variables
- ✅ No credit card required

### **Step-by-Step Guide**

#### **1. Prepare Your Repository**

Create these files in your project root:

**`render.yaml`**
```yaml
services:
  - type: web
    name: tax-incentive-platform
    env: python
    plan: free
    buildCommand: cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt && python -m prisma generate
    startCommand: python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: DATABASE_URL
        fromDatabase:
          name: tax-incentive-db
          property: connectionString
      - key: VITE_API_URL
        value: https://pilotforge.onrender.com

databases:
  - name: tax-incentive-db
    plan: free
    databaseName: tax_incentive_db
    user: tax_incentive_user
```

**`requirements.txt`** (ensure you have this)
```txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
prisma==0.15.0
pydantic==2.10.6
python-dotenv==1.0.1
reportlab==4.4.7
openpyxl==3.1.5
pillow==12.1.0
httpx==0.26.0
```

#### **2. Push to GitHub**

```bash
# Initialize git if not done
git init
git add .
git commit -m "Prepare for Render deployment"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/Tax_Incentive_Compliance_Platform.git
git branch -M main
git push -u origin main
```

#### **3. Deploy on Render**

1. **Sign up** at [render.com](https://render.com)
2. **Click "New +"** → **"Blueprint"**
3. **Connect your GitHub repo**
4. **Render will detect `render.yaml`** and create:
   - Web service (API)
   - PostgreSQL database
5. **Click "Apply"**
6. **Wait 5-10 minutes** for initial deploy

#### **4. Set Up Database**

After deployment completes:

```bash
# Connect to your Render shell
# (Use the "Shell" button in Render dashboard)

# Run migrations
python -m prisma migrate deploy

# Load initial data
python src/setup_database.py
```

#### **5. Access Your API**

Your API will be live at:
```
https://tax-incentive-platform.onrender.com
```

Access Swagger UI:
```
https://tax-incentive-platform.onrender.com/docs
```

---

## 🚂 Railway.app Deployment

### **Step-by-Step Guide**

#### **1. Install Railway CLI**

```bash
npm install -g @railway/cli
railway login
```

#### **2. Initialize Railway Project**

```bash
railway init
railway add --name tax-incentive-db postgresql
```

#### **3. Set Environment Variables**

```bash
railway variables set PYTHON_VERSION=3.12.0
```

#### **4. Deploy**

```bash
railway up
```

#### **5. Run Migrations**

```bash
railway run python -m prisma migrate deploy
railway run python src/setup_database.py
```

**Your API:** `https://your-app.railway.app`

---

## ✈️ Fly.io Deployment

### **Step-by-Step Guide**

#### **1. Install Fly CLI**

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

#### **2. Create `Dockerfile`**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Generate Prisma client
RUN python -m prisma generate

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **3. Create `fly.toml`**

```toml
app = "tax-incentive-platform"

[build]
  dockerfile = "Dockerfile"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[env]
  PORT = "8000"
```

#### **4. Launch App**

```bash
fly auth login
fly launch
fly postgres create --name tax-incentive-db
fly postgres attach tax-incentive-db
fly deploy
```

#### **5. Run Migrations**

```bash
fly ssh console
python -m prisma migrate deploy
python src/setup_database.py
exit
```

**Your API:** `https://tax-incentive-platform.fly.dev`

---

## ☁️ AWS Deployment

### **Architecture**

- **EC2**: Application server
- **RDS**: PostgreSQL database
- **Elastic Load Balancer**: Traffic distribution
- **CloudWatch**: Monitoring

### **Quick Guide**

#### **1. Create RDS PostgreSQL Database**

```bash
# AWS Console → RDS → Create Database
# Engine: PostgreSQL 16
# Template: Free tier
# Instance: db.t3.micro
```

#### **2. Launch EC2 Instance**

```bash
# Ubuntu Server 22.04 LTS
# Instance type: t2.micro (free tier)
# Security group: Allow 8000, 22, 443
```

#### **3. Connect and Deploy**

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3.12 python3-pip postgresql-client git

# Clone repo
git clone your-repo-url
cd Tax_Incentive_Compliance_Platform

# Set up virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:pass@rds-endpoint:5432/db"

# Run migrations
python -m prisma generate
python -m prisma migrate deploy
python src/setup_database.py

# Start application
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

#### **4. Use Systemd for Auto-Restart**

Create `/etc/systemd/system/tax-incentive.service`:

```ini
[Unit]
Description=Tax Incentive Platform
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Tax_Incentive_Compliance_Platform
Environment="DATABASE_URL=postgresql://..."
ExecStart=/home/ubuntu/Tax_Incentive_Compliance_Platform/venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable tax-incentive
sudo systemctl start tax-incentive
```

---

## 🔐 Environment Variables

### **Backend Variables**

#### **Required:**

```bash
# Backend
DATABASE_URL=postgresql://user:password@host:5432/database
PORT=8000
PYTHON_VERSION=3.12.0

# Frontend
VITE_API_URL=https://your-app.onrender.com
```

#### **Optional:**

```bash
# Logging
LOG_LEVEL=INFO

# CORS (if frontend on different domain)
CORS_ORIGINS=https://your-frontend.com

# Email (if implemented)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Frontend Debug Mode
VITE_DEBUG=false
```

### **Frontend Environment Variables**

The frontend uses Vite environment variables (prefixed with `VITE_`):

**Development:**
```bash
VITE_API_URL=http://localhost:8000
VITE_DEBUG=true
```

**Production:**
```bash
VITE_API_URL=https://pilotforge.onrender.com
VITE_DEBUG=false
```

**Setting Frontend Variables:**
- Create `.env` file in `frontend/` directory
- Variables must start with `VITE_` prefix
- Access in code: `import.meta.env.VITE_API_URL`
### **Frontend Variables**

#### **Required:**

```bash
# API endpoint (must be prefixed with VITE_)
VITE_API_URL=https://your-api.onrender.com/api/v1
```

**Development (.env.development):**
```bash
VITE_API_URL=http://localhost:8000/api/v1
```

**Production (.env.production):**
```bash
VITE_API_URL=https://pilotforge-api.onrender.com/api/v1
```

**Important:**
- All Vite env vars **must** start with `VITE_` prefix
- Frontend env vars are **public** (visible in browser)
- Never store secrets in frontend environment variables

### **Setting Variables**

**Render.com:**
```
Dashboard → Environment → Add Environment Variable
```

**Railway:**
```bash
railway variables set DATABASE_URL="postgresql://..."
```

**Fly.io:**
```bash
fly secrets set DATABASE_URL="postgresql://..."
```

**Heroku:**
```bash
heroku config:set DATABASE_URL="postgresql://..."
```

---

## 🎨 Frontend Build Process

### **Building the Frontend**

The React frontend must be built before deployment. The build process:

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Build Production Bundle**
```bash
npm run build
```

**Build Output:**
- Location: `frontend/dist/`
- JavaScript: 283KB (92KB gzipped)
- CSS: 3.6KB
- Static assets and HTML

3. **Preview Build Locally**
```bash
npm run preview
# Access at http://localhost:4173
```

### **Build Output Location**

```
frontend/dist/
├── assets/
│   ├── index-[hash].js      # Bundled JavaScript
│   ├── index-[hash].css     # Compiled CSS
│   └── [other-assets]
└── index.html               # Entry point
```

### **Static File Serving Configuration**

The FastAPI backend serves the frontend from `frontend/dist/`:

```python
# In main.py
from fastapi.staticfiles import StaticFiles

# API routes first
app.include_router(api_router, prefix="/api/v1")

# Serve frontend (catch-all for non-API routes)
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
```

**Route Handling:**
- `/api/v1/*` → FastAPI backend
- `/*` → Frontend static files

### **Deployment Build Steps**

#### **Full Stack Deployment**

```bash
# 1. Build frontend
cd frontend
npm install
npm run build
cd ..

# 2. Install backend dependencies
pip install -r requirements.txt

# 3. Generate Prisma client
python -m prisma generate

# 4. Run migrations (if needed)
python -m prisma migrate deploy

# 5. Start server (serves both API and frontend)
python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

#### **Render.com Build Command**

The build command in `render.yaml` handles everything:

```yaml
buildCommand: cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt && python -m prisma generate
```

**This command executes the following steps:**
1. Navigates to frontend directory (`cd frontend`)
2. Installs npm dependencies (`npm install`)
3. Builds production bundle (`npm run build`)
4. Returns to root directory (`cd ..`)
5. Installs Python dependencies (`pip install -r requirements.txt`)
6. Generates Prisma client (`python -m prisma generate`)

**Alternative: Using a Build Script**

For better maintainability, you can create a `build.sh` script:

```bash
#!/bin/bash
# build.sh
set -e  # Exit on error

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Generating Prisma client..."
python -m prisma generate

echo "Build complete!"
```

Then update `render.yaml`:
```yaml
buildCommand: chmod +x build.sh && ./build.sh
```

### **Verifying Frontend Build**

After deployment, verify the frontend is accessible:

```bash
# Check frontend loads
curl https://your-app.onrender.com/

# Check API still works
curl https://your-app.onrender.com/api/v1/
```

**Expected:**
- `/` returns React app HTML
- `/api/v1/` returns API JSON response
## 🎨 Frontend Deployment

### **Frontend Build Process**

The React frontend must be built before deployment. There are two deployment strategies:

#### **Strategy 1: Static Files from FastAPI (Single Server)**

Serve the frontend build from the FastAPI backend:

**1. Build Frontend:**
```bash
cd frontend
npm install
npm run build
```

**2. Configure FastAPI to Serve Static Files:**

Update `src/main.py`:
```python
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pathlib import Path

app = FastAPI()

# Serve frontend static files
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
```

**3. Update Build Command in `render.yaml`:**
```yaml
services:
  - type: web
    name: tax-incentive-platform
    env: python
    plan: free
    buildCommand: |
      pip install -r requirements.txt && 
      python -m prisma generate &&
      cd frontend && 
      npm install && 
      npm run build && 
      cd ..
    startCommand: python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: DATABASE_URL
        fromDatabase:
          name: tax-incentive-db
          property: connectionString
```

**Benefits:**
- Single deployment
- Simpler architecture
- One domain for API and UI

---

#### **Strategy 2: Separate Frontend Deployment (Recommended for Production)**

Deploy frontend separately on Vercel, Netlify, or Render Static Site.

**Option A: Vercel Deployment**

**1. Install Vercel CLI:**
```bash
npm install -g vercel
```

**2. Deploy Frontend:**
```bash
cd frontend
vercel
```

**3. Configure Environment Variable:**

In Vercel dashboard, set:
```
VITE_API_URL=https://your-backend.onrender.com/api/v1
```

**4. Vercel Configuration (`vercel.json`):**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**Benefits:**
- CDN-powered edge delivery
- Automatic HTTPS
- Git-based deployments
- Preview deployments for PRs

---

**Option B: Netlify Deployment**

**1. Create `netlify.toml`:**
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**2. Deploy via Netlify CLI:**
```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod
```

**3. Set Environment Variables:**

In Netlify dashboard:
```
VITE_API_URL=https://your-backend.onrender.com/api/v1
```

**Benefits:**
- Free tier with 100GB bandwidth
- Automatic deployments from GitHub
- Form handling and serverless functions

---

**Option C: Render Static Site**

**1. Create `render-frontend.yaml`:**
```yaml
services:
  - type: web
    name: pilotforge-frontend
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    envVars:
      - key: VITE_API_URL
        value: https://your-backend.onrender.com/api/v1
```

**2. Deploy:**
- Push to GitHub
- Connect repository in Render
- Render will detect the config and deploy

**Benefits:**
- Free tier available
- Same platform as backend
- Automatic SSL

---

### **Frontend Environment Variables**

The frontend requires the following environment variable:

```bash
# .env.production (in frontend directory)
VITE_API_URL=https://your-api-domain.com/api/v1
```

**Important Notes:**
- ⚠️ All Vite env vars must be prefixed with `VITE_`
- ⚠️ Frontend env vars are exposed to the browser (no secrets!)
- ⚠️ Update CORS settings in backend to allow frontend domain

### **Update Backend CORS Settings**

Update `src/main.py` to allow your frontend domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",           # Local development
        "https://your-frontend.vercel.app", # Production frontend
        "https://pilotforge.com"           # Custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### **Complete Deployment Checklist**

**Backend:**
- [ ] Deploy FastAPI to Render/Railway/Fly.io
- [ ] Set `DATABASE_URL` environment variable
- [ ] Run database migrations
- [ ] Configure CORS for frontend domain
- [ ] Verify API at `/docs` endpoint

**Frontend:**
- [ ] Build frontend with `npm run build`
- [ ] Set `VITE_API_URL` to production API
- [ ] Deploy to Vercel/Netlify/Render
- [ ] Verify routing works (SPA redirects)
- [ ] Test API connectivity from deployed frontend

**DNS (Optional):**
- [ ] Point custom domain to frontend
- [ ] Point API subdomain to backend (e.g., api.pilotforge.com)
- [ ] Configure SSL certificates

---

## 🗄️ Database Setup

### **Render Postgres**

Automatically provisioned. Connection string in environment.

### **External PostgreSQL**

```bash
# Create database
createdb tax_incentive_db

# Run migrations
DATABASE_URL="postgresql://..." python -m prisma migrate deploy

# Load data
python src/setup_database.py
```

### **Backup Strategy**

```bash
# Automated backups (Render)
# Included in free tier - daily backups

# Manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20260110.sql
```

---

## ✅ Post-Deployment

### **1. Verify Frontend is Running**

```bash
# Check frontend loads
curl https://your-app.onrender.com/

# Or visit in browser
https://pilotforge.onrender.com
```

**Expected Response:**
- HTML page with React app
- No 404 errors
- Page loads successfully

### **2. Verify API is Running**

```bash
curl https://your-app.onrender.com/api/v1/
```

**Expected Response:**
```json
{
  "message": "Tax-Incentive Compliance Platform API",
  "version": "v1"
}
```

### **3. Test Frontend Features**

Visit the deployed application and verify:

- ✅ Dashboard loads with production count
- ✅ Jurisdictions page displays all jurisdictions
- ✅ Productions page allows creating new productions
- ✅ Calculator page works for tax calculations
- ✅ Navigation between pages works
- ✅ API calls succeed (check browser Network tab)

### **4. Test Backend Endpoints**

```bash
# Test jurisdictions
curl https://your-app.onrender.com/api/v1/jurisdictions/

# Test calculator
curl -X POST https://your-app.onrender.com/api/v1/calculate/options
```

### **5. Access Swagger UI**

```
https://your-app.onrender.com/docs
```

### **6. Update README**

Add your live URL:
```markdown
## 🌐 Live Demo

**Frontend UI**: https://pilotforge.onrender.com
**API Docs**: https://pilotforge.onrender.com/docs
```

---

## 📊 Monitoring

### **Render.com**

Built-in monitoring:
- CPU usage
- Memory usage
- Request logs
- Error logs

Access: `Dashboard → Metrics`

### **Custom Monitoring**

Add to `src/main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

### **Health Checks**

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }
```

---

## 🐛 Troubleshooting

### **Issue: Build Fails**

**Error:** `Module not found`

**Solution:**
```bash
# Ensure all dependencies in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### **Issue: Database Connection Fails**

**Error:** `Connection refused`

**Solution:**
```bash
# Check DATABASE_URL format
postgresql://user:password@host:port/database

# Verify database is running
pg_isready -h your-db-host
```

### **Issue: Prisma Generate Fails**

**Error:** `Prisma client not generated`

**Solution:**
```bash
# Add to buildCommand in render.yaml
buildCommand: pip install -r requirements.txt && python -m prisma generate
```

### **Issue: Port Already in Use**

**Error:** `Address already in use`

**Solution:**
```python
# Use environment variable for port
import os
port = int(os.getenv("PORT", 8000))
```

### **Issue: Slow Cold Starts (Render Free Tier)**

**Note:** Free tier spins down after 15 minutes of inactivity

**Solutions:**
1. Upgrade to paid tier ($7/month)
2. Use uptime monitoring to ping every 14 minutes
3. Accept 30-second delay on first request

---

## 🚨 Security Checklist

- [ ] Environment variables set (no hardcoded secrets)
- [ ] HTTPS enabled (automatic on Render/Railway/Fly)
- [ ] Database credentials secure
- [ ] CORS configured properly
- [ ] Rate limiting enabled (if needed)
- [ ] Regular security updates
- [ ] Backup strategy in place

---

## 📈 Scaling

### **Render.com**

```
Free tier: 512MB RAM, shared CPU
Starter: $7/month, 512MB RAM
Standard: $25/month, 2GB RAM
Pro: $85/month, 4GB RAM
```

### **Performance Optimization**

```python
# Add database connection pooling
# In src/utils/database.py

from prisma import Prisma

prisma = Prisma(
    datasource={
        "url": os.getenv("DATABASE_URL"),
        "pool": {
            "max": 10,
            "timeout": 5000
        }
    }
)
```

---

## 🎉 Success!

Your Tax-Incentive Compliance Platform is now live and accessible worldwide!

**Share your URL:**
```
https://your-app.onrender.com/docs
```

**Next Steps:**
1. Share with potential users
2. Gather feedback
3. Monitor performance
4. Add features
5. Build frontend

---

## 📞 Support

**Deployment Issues:**
- Render: [render.com/docs](https://render.com/docs)
- Railway: [docs.railway.app](https://docs.railway.app)
- Fly.io: [fly.io/docs](https://fly.io/docs)

**Platform Issues:**
- Check logs in platform dashboard
- Review [Troubleshooting](#troubleshooting)
- Open GitHub issue

---

**Deployed successfully?** Update your README with the live URL! 🚀

# 📚 UI Documentation Index

Welcome to the PilotForge frontend documentation! This guide helps you navigate all UI-related documentation.

## 🚀 Getting Started (Pick One)

### Quick Start (Experienced Developers)
**[frontend/QUICK_START.md](./frontend/QUICK_START.md)** - One-page reference  
→ For developers who want to start coding immediately

### Complete Setup Guide (First Time Users)
**[UI_SETUP.md](./UI_SETUP.md)** - Comprehensive 11K guide  
→ For reviewers, testers, and new developers  
→ Includes troubleshooting, prerequisites, and step-by-step instructions

### Development Workflow
**[frontend/DEVELOPMENT.md](./frontend/DEVELOPMENT.md)** - Tips and best practices  
→ For active development and code reviews

## 📖 Documentation Structure

```
Documentation/
├── UI_SETUP.md                    # Main UI setup guide (START HERE)
├── README.md                      # Project overview with quick start
├── frontend/
│   ├── QUICK_START.md            # One-page quick reference
│   ├── DEVELOPMENT.md            # Development tips & workflow
│   └── FRONTEND_README.md        # Technology stack details
└── docs/
    ├── USER_MANUAL.md            # End-user guide for the application
    └── DEPLOYMENT.md             # Production deployment
```

## 🎯 By Use Case

### "I want to review/test the UI"
1. Read: [UI_SETUP.md](./UI_SETUP.md)
2. Run: `./start-fullstack.sh` (or `.ps1` on Windows)
3. Visit: http://localhost:3000

### "I want to develop the UI"
1. Quick start: [frontend/QUICK_START.md](./frontend/QUICK_START.md)
2. Development tips: [frontend/DEVELOPMENT.md](./frontend/DEVELOPMENT.md)
3. Run: `cd frontend && ./start-ui.sh`

### "I just want the basics"
1. Clone the repo
2. Run: `./start-fullstack.sh` (starts both backend and frontend)
3. Open: http://localhost:3000

### "I'm having issues"
→ See [UI_SETUP.md - Troubleshooting section](./UI_SETUP.md#troubleshooting)

## 🛠️ Startup Scripts

All scripts are in the repository root and `frontend/` directory:

| Script | Purpose | Platform |
|--------|---------|----------|
| `start-fullstack.sh` | Start backend + frontend | Linux/Mac |
| `start-fullstack.ps1` | Start backend + frontend | Windows |
| `frontend/start-ui.sh` | Start frontend only | Linux/Mac |
| `frontend/start-ui.ps1` | Start frontend only | Windows |

## 🔗 Key URLs

When running locally:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📦 Technology Stack

- **React 19** with TypeScript
- **Vite 7** for lightning-fast builds
- **TailwindCSS 4** for styling
- **Zustand** for state management
- **React Router v7** for navigation
- **Axios** for API calls

See [frontend/FRONTEND_README.md](./frontend/FRONTEND_README.md) for details.

## 🎬 Quick Command Reference

```bash
# Full stack startup (recommended)
./start-fullstack.sh              # Linux/Mac
.\start-fullstack.ps1             # Windows

# Frontend only
cd frontend
npm install                        # Install dependencies
npm run dev                        # Start dev server (http://localhost:3000)
npm run build                      # Build for production
npm run preview                    # Preview production build
npm run lint                       # Check code quality
npm run type-check                 # Check TypeScript types

# Backend only
python -m uvicorn src.main:app --reload
```

## ❓ Common Questions

**Q: What are the prerequisites?**  
A: Node.js 20+, npm 10+, Python 3.11+, PostgreSQL 16 (for backend)

**Q: Do I need the backend running?**  
A: Yes, the frontend needs the API at http://localhost:8000

**Q: How do I fix "port already in use"?**  
A: Use a different port: `npm run dev -- --port 3001`

**Q: Where are the logs?**  
A: Browser console (F12) for frontend, terminal for backend

**Q: How do I contribute?**  
A: See [frontend/DEVELOPMENT.md](./frontend/DEVELOPMENT.md) for workflow

## 🏗️ Project Structure

```
Tax_Incentive_Compliance_Platform/
├── frontend/                      # Frontend application
│   ├── src/
│   │   ├── components/           # UI components
│   │   ├── pages/                # Page components
│   │   ├── store/                # State management
│   │   ├── App.tsx               # Root component
│   │   └── main.tsx              # Entry point
│   ├── package.json              # Dependencies
│   ├── vite.config.ts            # Vite configuration
│   ├── .env.example              # Environment template
│   └── start-ui.sh/.ps1          # Startup scripts
├── src/                          # Backend source
├── docs/                         # Additional documentation
├── start-fullstack.sh/.ps1       # Full stack startup
└── UI_SETUP.md                   # Main setup guide
```

## 🎓 Learning Resources

- **Vite**: https://vite.dev/
- **React**: https://react.dev/
- **TypeScript**: https://www.typescriptlang.org/
- **TailwindCSS**: https://tailwindcss.com/
- **Zustand**: https://docs.pmnd.rs/zustand/

## 📝 Documentation Maintenance

This documentation was created as part of the UI startup process implementation.

**Last Updated**: January 2026  
**Maintainer**: PilotForge Team

---

**Need help?** Start with [UI_SETUP.md](./UI_SETUP.md) for comprehensive guidance.

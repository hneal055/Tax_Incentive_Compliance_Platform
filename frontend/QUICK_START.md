# 🚀 Quick Start - Frontend

## One Command Start

**Linux/Mac:**
```bash
./start-ui.sh
```

**Windows:**
```powershell
.\start-ui.ps1
```

**Manual:**
```bash
npm install
npm run dev
```

## URLs

- **UI**: http://localhost:3000
- **Backend**: http://localhost:8000 (must be running)
- **API Docs**: http://localhost:8000/docs

## Common Commands

```bash
npm install          # Install dependencies
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Check code quality
```

## Troubleshooting

**Port 3000 in use?**
```bash
npm run dev -- --port 3001
```

**Backend not running?**
```bash
# Terminal 1: Start backend from project root
python -m uvicorn src.main:app --reload

# Terminal 2: Start frontend
cd frontend && npm run dev
```

**Dependencies issue?**
```bash
rm -rf node_modules
npm install
```

## Need More Help?

See [../UI_SETUP.md](../UI_SETUP.md) for complete setup guide and troubleshooting.

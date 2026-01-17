# PilotForge

> **Tax Incentive Intelligence for Film & TV Productions**

Jurisdictional rule engine for managing tax incentives for the film & television industry.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 🎯 Features

- 🌍 **32 Global Jurisdictions** - Compare incentives across USA, Canada, UK, and more
- 💰 **Tax Incentive Calculator** - Instant credit estimates with compliance checks
- 🎬 **Production Management** - Track productions, budgets, and locations
- 📊 **Dashboard UI** - Modern React interface for easy navigation
- 📄 **PDF & Excel Reports** - Professional documentation for stakeholders
- 🔒 **Type-Safe** - Full TypeScript coverage for reliability

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 20+** and **npm 10+**
- **PostgreSQL 16**

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
python -m prisma generate

# Run migrations
python -m prisma migrate deploy

# Start development server
python -m uvicorn src.main:app --reload
```

Visit: **http://localhost:8000/docs** (Swagger UI)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit: **http://localhost:3000**

---

## 🛠️ Technology Stack

### Backend
- **Python 3.12** - Modern Python with FastAPI
- **FastAPI** - High-performance async web framework
- **PostgreSQL 16** - Robust relational database
- **Prisma ORM** - Type-safe database client
- **Pytest** - Comprehensive testing suite

### Frontend
- **React 19** - Latest React with concurrent features
- **TypeScript 5.9** - Type safety and better DX
- **Vite 7** - Lightning-fast build tool and HMR
- **TailwindCSS 4** - Utility-first CSS framework
- **Zustand** - Lightweight state management (<1KB)
- **React Router v7** - Client-side routing
- **Axios** - Promise-based HTTP client

---

## 📚 Documentation

- **[Frontend Setup Guide](./docs/FRONTEND_SETUP.md)** - Complete frontend development guide
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - Deploy to production (Render, Vercel, AWS)
- **[User Manual](./docs/USER_MANUAL.md)** - API reference and UI guide
- **[API Examples](./docs/API_EXAMPLES.md)** - Code examples in Python, JavaScript, TypeScript
- **[Roadmap](./docs/ROADMAP.md)** - Development phases and future plans
- **[Full Documentation](./docs/README.md)** - Architecture overview

---

## 💡 Example Usage

### Calculate Tax Incentive (API)

```python
import httpx

response = httpx.post('http://localhost:8000/api/v1/calculate/simple', json={
    'budget': 5000000,
    'jurisdictionId': 'california-id',
    'ruleId': 'ca-film-credit-2025'
})

result = response.json()
print(f"Estimated Credit: ${result['estimatedCredit']:,}")
# Output: Estimated Credit: $1,000,000
```

### Using Frontend (React/TypeScript)

```typescript
import { calculatorService } from './api'

const result = await calculatorService.calculate(
  productionId,
  jurisdictionId
)

console.log(`Estimated Credit: $${result.estimatedCredit.toLocaleString()}`)
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculator_logic.py

# Run with coverage
pytest --cov=src
```

**Test Coverage:** 31/31 tests passing ✅

---

## 📦 Project Structure

```
Tax_Incentive_Compliance_Platform/
├── src/                    # Backend source code
│   ├── main.py            # FastAPI application
│   ├── routes.py          # API endpoints
│   └── ...
├── frontend/              # React frontend
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # UI components
│   │   ├── pages/        # Route pages
│   │   ├── store/        # Zustand store
│   │   └── types/        # TypeScript types
│   └── package.json
├── docs/                  # Documentation
├── tests/                 # Backend tests
├── rules/                 # Jurisdiction rule files
└── requirements.txt       # Python dependencies
```

---

## 🌐 Deployment

Deploy the backend to **Render.com**, **Railway**, **Fly.io**, or **AWS**.

Deploy the frontend to **Vercel**, **Netlify**, or **Render Static Site**.

See **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** for detailed instructions.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License

Copyright (c) 2025-2026 Howard Neal - PilotForge

See [LICENSE](./docs/LICENSE) for details.

---

## 📞 Support

- **Documentation Issues**: Open a GitHub issue
- **Questions**: Check [docs/USER_MANUAL.md](./docs/USER_MANUAL.md)
- **Bug Reports**: Include reproduction steps and error messages

---

**Built with ❤️ for the film & TV industry**

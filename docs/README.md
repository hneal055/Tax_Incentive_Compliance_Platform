# 🎬 PilotForge

> **Tax Incentive Intelligence for Film & TV Productions**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF.svg)](https://vite.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-4-38B2AC.svg)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/Tests-31%2F31%20Passing-success.svg)](./tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 🎯 What is PilotForge?

PilotForge is a comprehensive tax incentive calculation and compliance platform 
for the global film and television industry. We help productions maximize their 
tax savings by comparing 32 jurisdictions and 33 incentive programs worldwide.

### 💰 Real-World Impact

**Example:** A $5M feature film uses PilotForge to discover Louisiana offers 
$1.75M in stackable credits (35%) vs California's $1M (20%).

**Result: $750,000 in additional savings** 🎉

---

## 🏗️ Architecture

### Backend Technology

- **Framework**: Python 3.12+ with FastAPI
- **Database**: PostgreSQL 16 with Prisma ORM
- **Testing**: Pytest with 31 passing tests
- **APIs**: RESTful API with OpenAPI/Swagger documentation
- **Features**: 
  - Multi-jurisdictional tax incentive rules engine
  - Production expense tracking
  - Automated incentive calculations
  - Compliance verification
  - PDF & Excel report generation

### Frontend Architecture

Modern, production-ready React UI built with cutting-edge technologies:

**Core Stack:**
- **React 19** + TypeScript for type-safe component development
- **Vite 7** for lightning-fast builds and Hot Module Replacement
- **TailwindCSS 4** for utility-first styling and responsive design
- **Zustand** for lightweight state management (<1KB)
- **React Router v7** for client-side routing
- **Axios** for typed API communication

**Project Structure:**
```
frontend/src/
├── api/           # Typed Axios client & service methods
│   ├── client.ts  # Base API configuration
│   └── index.ts   # Service functions (productions, jurisdictions, calculator)
├── components/    # Reusable UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   ├── Spinner.tsx
│   ├── Navbar.tsx
│   └── Layout.tsx
├── pages/         # Route-based page components
│   ├── Dashboard.tsx      # Metrics overview & quick actions
│   ├── Productions.tsx    # Production CRUD interface
│   ├── Jurisdictions.tsx  # Jurisdiction browsing
│   └── Calculator.tsx     # Tax incentive calculator
├── store/         # Zustand state management
│   └── index.ts   # Global state (productions, jurisdictions, loading)
└── types/         # TypeScript interfaces
    └── index.ts   # API contract types
```

**Pages & Features:**
- **Dashboard**: Production metrics, jurisdiction counts, quick action buttons
- **Productions**: Create, view, and manage productions with form validation
- **Jurisdictions**: Browse 32 jurisdictions with filtering by type/country
- **Calculator**: Select production & jurisdiction, view tax credit estimates

---

## 📚 Documentation

- **[FRONTEND_SETUP.md](./FRONTEND_SETUP.md)** - Complete frontend setup guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment instructions
- **[USER_MANUAL.md](./USER_MANUAL.md)** - API and UI usage guide
- **[API_EXAMPLES.md](./API_EXAMPLES.md)** - Code examples and integration patterns
- **[ROADMAP.md](./ROADMAP.md)** - Development phases and future plans

---

## 🚀 Quick Start

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

Visit: http://localhost:8000/docs

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit: http://localhost:3000

---

## 🔗 Key Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Frontend Dev Server**: http://localhost:3000
- **Repository**: https://github.com/hneal055/Tax_Incentive_Compliance_Platform

---

## 📄 License

MIT License

Copyright (c) 2025-2026 Howard Neal - PilotForge

# 🎬 PilotForge

> **Tax Incentive Intelligence for Film & TV Productions**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue.svg)](https://www.typescriptlang.org/)
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

## 🏗️ Backend Architecture

PilotForge is built on a modern, rule-engine-first architecture:

### **Core Components**
- **FastAPI Backend**: High-performance REST API with automatic OpenAPI documentation
- **PostgreSQL Database**: Robust data persistence with Prisma ORM
- **Rule Engine**: Jurisdiction-specific tax incentive calculations
- **Report Generation**: PDF and Excel export capabilities

### **Key Features**
- 32+ jurisdictions with 33+ incentive programs
- Multi-jurisdiction comparison
- Compliance verification
- Stackable credit calculations
- Scenario modeling
- Audit trail and reporting

---

## 🎨 Frontend Architecture

PilotForge features a modern React frontend built with cutting-edge technologies:

### **Technology Stack**

#### **Core Framework**
- **React 19**: Latest React version with improved rendering and performance
- **TypeScript 5.9**: Type-safe development with full IntelliSense support
- **Vite 7**: Lightning-fast build tool with Hot Module Replacement (HMR)

#### **Styling & UI**
- **TailwindCSS 4**: Utility-first CSS framework for rapid UI development
- **Responsive Design**: Mobile-first approach with PilotForge branding
- **Component Library**: Reusable Button, Card, Input, Spinner, Navbar, and Layout components

#### **State Management & Routing**
- **Zustand**: Lightweight state management for productions and jurisdictions
- **React Router v7**: Client-side routing with declarative navigation
- **Axios**: Typed HTTP client for API communication

### **Frontend Structure**

```
frontend/src/
├── api/              # Typed Axios client and service methods
│   ├── client.ts     # Base axios configuration
│   └── index.ts      # API service endpoints
├── components/       # Reusable UI components
│   ├── Button.tsx    # Customizable button component
│   ├── Card.tsx      # Content card wrapper
│   ├── Input.tsx     # Form input component
│   ├── Spinner.tsx   # Loading indicator
│   ├── Navbar.tsx    # Navigation header
│   └── Layout.tsx    # Page layout wrapper
├── pages/            # Application pages
│   ├── Dashboard.tsx     # Overview with metrics and quick actions
│   ├── Productions.tsx   # Production management
│   ├── Jurisdictions.tsx # Jurisdiction browser
│   └── Calculator.tsx    # Tax incentive calculator
├── store/            # Zustand state management
│   └── index.ts      # Global state stores
└── types/            # TypeScript interfaces and types
```

### **Component Library Overview**

#### **Button Component**
Flexible button with variants (primary, secondary, danger) and sizes (small, medium, large).

#### **Card Component**
Reusable content wrapper with consistent styling and optional title/description.

#### **Input Component**
Form input with built-in label, error handling, and validation states.

#### **Spinner Component**
Loading indicator with size variants for different contexts.

#### **Navbar Component**
Responsive navigation header with PilotForge branding and route links.

#### **Layout Component**
Page wrapper providing consistent structure across all views.

### **Pages & Features**

#### **Dashboard**
- Production count and jurisdiction overview
- Quick actions for creating productions and viewing jurisdictions
- Grid display of available jurisdictions with filtering

#### **Productions Management**
- List all productions with status indicators
- Create new productions with detailed forms
- View and edit existing production details
- Delete productions with confirmation

#### **Jurisdictions Browser**
- Browse all 32+ jurisdictions
- Filter by type (State, Country, Province)
- View jurisdiction details and available incentive programs
- Search and sort capabilities

#### **Tax Incentive Calculator**
- Select production and jurisdiction
- Calculate tax incentives in real-time
- View detailed breakdown of credits
- Compare multiple jurisdictions

### **API Integration**

The frontend uses a fully typed Axios client with service methods:

```typescript
import { api } from '../api';

// Fetch all productions
const productions = await api.productions.list();

// Create new production
const newProduction = await api.productions.create({
  title: "The Great Film",
  budget: 5000000,
  status: "ACTIVE"
});

// Calculate tax incentive
const result = await api.calculations.calculate(
  productionId,
  jurisdictionId
);
```

### **State Management**

Zustand stores provide centralized state for:
- **Productions Store**: Managing production data across components
- **Jurisdictions Store**: Caching jurisdiction list for quick access
- **UI State**: Loading states, modals, and notifications

### **Build & Performance**

- **Production Bundle**: 283KB JavaScript (92KB gzipped), 3.6KB CSS
- **Vite Optimization**: Code splitting, tree shaking, and minification
- **Fast Refresh**: Instant feedback during development
- **TypeScript Checking**: Compile-time error detection

---

## 📚 Documentation

### **Getting Started**
- [Frontend Setup Guide](./FRONTEND_SETUP.md) - Complete frontend installation and development guide
- [User Manual](./USER_MANUAL.md) - API and UI usage documentation
- [API Examples](./API_EXAMPLES.md) - Code samples including frontend examples

### **Development**
- [Roadmap](./ROADMAP.md) - Project phases and future features
- [Deployment Guide](./DEPLOYMENT.md) - Production deployment instructions
- [Rule Format](./RULE_FORMAT.md) - Jurisdiction rule schema

### **Reference**
- [North Star](./NORTH_STAR.md) - Project vision and principles
- [Brand Guidelines](./BRAND.md) - Design and branding standards

---

## 🚀 Quick Start

### **Backend**
```bash
# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
python -m prisma generate

# Run migrations
python -m prisma migrate deploy

# Start server
python -m uvicorn src.main:app --reload
```

Visit: http://localhost:8000/docs

### **Frontend**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit: http://localhost:3000

---

## 🌐 Live Demo

**Production URL**: https://pilotforge.onrender.com

Access the full-stack application with the React UI and FastAPI backend.

---

## 📄 License

MIT License

Copyright (c) 2025-2026 Howard Neal - PilotForge

See [LICENSE](./LICENSE) for full details.

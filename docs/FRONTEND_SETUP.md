# 🎨 Frontend Setup Guide - PilotForge

> Comprehensive guide to setting up and developing the React frontend
# 🎨 Frontend Setup Guide

> Complete guide to developing with the PilotForge React frontend

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Development Server](#development-server)
5. [Environment Variables](#environment-variables)
6. [Project Structure](#project-structure)
7. [Available Scripts](#available-scripts)
8. [Tech Stack Details](#tech-stack-details)
9. [Development Workflow](#development-workflow)
10. [Build and Deployment](#build-and-deployment)
11. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

The PilotForge frontend is a modern React 19 application built with TypeScript, Vite, and TailwindCSS. It provides a fast, responsive UI for managing film productions and calculating tax incentives.

### **Quick Start**
1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Tech Stack](#tech-stack)
4. [Available Scripts](#available-scripts)
5. [Development Workflow](#development-workflow)
6. [State Management](#state-management)
7. [API Integration](#api-integration)
8. [Styling](#styling)
9. [Routing](#routing)
10. [Building for Production](#building-for-production)
11. [Environment Variables](#environment-variables)
12. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

- **Node.js**: 20+ (check with `node --version`)
- **npm**: 10+ (check with `npm --version`)
- **Backend API**: Running on http://localhost:8000

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### **Required**
- **Node.js**: Version 18.0.0 or higher
  - Download from [nodejs.org](https://nodejs.org/)
  - Verify: `node --version`
- **npm**: Version 9.0.0 or higher (comes with Node.js)
  - Verify: `npm --version`

### **Optional but Recommended**
- **pnpm**: Fast, disk space efficient package manager
  - Install: `npm install -g pnpm`
  - Use: `pnpm install` instead of `npm install`
- **yarn**: Alternative package manager
  - Install: `npm install -g yarn`
  - Use: `yarn` instead of `npm install`

### **Backend Requirement**
The frontend requires the PilotForge backend API to be running:
- Backend should be running on `http://localhost:8000`
- See main README.md for backend setup instructions

### **Verify Installation**

```bash
# Check Node.js version
node --version
# Expected: v18.0.0 or higher

# Check npm version
npm --version
# Expected: 9.0.0 or higher
```

---

## 💿 Installation

### **Step 1: Clone Repository** (if not already done)

```bash
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform
```

### **Step 2: Navigate to Frontend Directory**

```bash
cd frontend
```

### **Step 3: Install Dependencies**

```bash
# Using npm (default)
npm install

# OR using pnpm (faster)
pnpm install

# OR using yarn
yarn install
```

**Installation Time**: ~2-3 minutes for initial install

### **Step 4: Verify Installation**

```bash
# Check that node_modules was created
ls -la node_modules

# Verify key packages
npm list react react-dom vite
```

---

## 🔧 Development Server

### **Start Development Server**

```bash
npm run dev
```

**Output:**
```
  VITE v7.2.4  ready in 823 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### **Access the Application**

- **Local**: http://localhost:3000
- **Network**: http://your-ip:3000 (use `npm run dev -- --host`)

### **Development Features**

- **Hot Module Replacement (HMR)**: Changes appear instantly without refresh
- **Fast Refresh**: React components update while preserving state
- **TypeScript Checking**: Real-time type errors in terminal and IDE
- **ESLint Integration**: Code quality warnings during development

### **Stop Development Server**

Press `Ctrl + C` in the terminal

---

## 🔐 Environment Variables

### **Configuration File**

Create a `.env` file in the `frontend/` directory:

```bash
# Copy the example file
cp .env.example .env
```

### **Environment Variables**

```env
# API Base URL
VITE_API_URL=http://localhost:8000

# Optional: Enable debug mode
VITE_DEBUG=false

# Optional: API timeout (milliseconds)
VITE_API_TIMEOUT=30000
```

### **Environment-Specific Configuration**

#### **Development**
```env
VITE_API_URL=http://localhost:8000
VITE_DEBUG=true
```

#### **Production**
```env
VITE_API_URL=https://pilotforge.onrender.com
VITE_DEBUG=false
```

#### **Staging**
```env
VITE_API_URL=https://staging.pilotforge.onrender.com
VITE_DEBUG=true
```

### **Accessing Environment Variables**

In TypeScript/JavaScript code:

```typescript
const apiUrl = import.meta.env.VITE_API_URL;
const isDebug = import.meta.env.VITE_DEBUG === 'true';
```

**Important**: All environment variables must start with `VITE_` to be accessible in the frontend.

---

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
│   └── vite.svg           # Favicon
├── src/
│   ├── api/               # API client and services
│   │   ├── client.ts      # Axios instance configuration
│   │   └── index.ts       # API service methods
│   ├── components/        # Reusable UI components
│   │   ├── Button.tsx     # Button component (primary, secondary, danger)
│   │   ├── Card.tsx       # Card wrapper component
│   │   ├── Input.tsx      # Form input component
│   │   ├── Spinner.tsx    # Loading spinner
│   │   ├── Navbar.tsx     # Navigation header
│   │   └── Layout.tsx     # Page layout wrapper
│   ├── pages/             # Application pages/routes
│   │   ├── Dashboard.tsx      # Main dashboard
│   │   ├── Productions.tsx    # Production management
│   │   ├── Jurisdictions.tsx  # Jurisdiction browser
│   │   └── Calculator.tsx     # Tax incentive calculator
│   ├── store/             # State management
│   │   └── index.ts       # Zustand stores
│   ├── types/             # TypeScript type definitions
│   │   └── index.ts       # Shared types and interfaces
│   ├── App.tsx            # Main App component with routing
│   ├── App.css            # Global styles
│   ├── main.tsx           # Application entry point
│   └── index.css          # TailwindCSS imports
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── eslint.config.js       # ESLint configuration
├── index.html             # HTML entry point
├── package.json           # Dependencies and scripts
├── postcss.config.js      # PostCSS configuration
├── tailwind.config.js     # TailwindCSS configuration
├── tsconfig.json          # TypeScript configuration
├── tsconfig.app.json      # TypeScript app-specific config
├── tsconfig.node.json     # TypeScript Node config
└── vite.config.ts         # Vite build configuration
```

### **Key Directories**

#### **`src/api/`**
Centralized API communication layer with typed methods for:
- Productions CRUD operations
- Jurisdictions retrieval
- Incentive rules queries
- Tax calculations
- Expense management

#### **`src/components/`**
Reusable UI building blocks:
- **Button**: Customizable with variants (primary, secondary, danger) and sizes
- **Card**: Content wrapper with consistent styling
- **Input**: Form input with label and error handling
- **Spinner**: Loading indicators with size variants
- **Navbar**: Top navigation with PilotForge branding
- **Layout**: Page wrapper providing consistent structure

#### **`src/pages/`**
Top-level route components:
- **Dashboard**: Overview with metrics and quick actions
- **Productions**: List, create, edit, delete productions
- **Jurisdictions**: Browse and filter jurisdictions
- **Calculator**: Calculate tax incentives

#### **`src/store/`**
Zustand state management:
- Productions store
- Jurisdictions store
- UI state (modals, loading, notifications)

#### **`src/types/`**
TypeScript interfaces for:
- Production
- Jurisdiction
- IncentiveRule
- Expense
- CalculationResult
- API responses
```

### Running Development Server

```bash
# Start dev server with hot reload
npm run dev
```

The frontend will be available at **http://localhost:3000**

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/                    # API client and services
│   │   ├── client.ts           # Axios instance with base configuration
│   │   └── index.ts            # Service methods (productions, jurisdictions, calculator)
│   │
│   ├── components/             # Reusable UI components
│   │   ├── Button.tsx          # Primary/secondary button variants
│   │   ├── Card.tsx            # Container component with shadow
│   │   ├── Input.tsx           # Text/number/date input fields
│   │   ├── Spinner.tsx         # Loading spinner
│   │   ├── Navbar.tsx          # Top navigation with active states
│   │   └── Layout.tsx          # Page wrapper with Navbar
│   │
│   ├── pages/                  # Route-based page components
│   │   ├── Dashboard.tsx       # Home page with metrics & quick actions
│   │   ├── Productions.tsx     # Production CRUD interface
│   │   ├── Jurisdictions.tsx   # Jurisdiction browsing grid
│   │   └── Calculator.tsx      # Tax incentive calculator
│   │
│   ├── store/                  # Zustand state management
│   │   └── index.ts            # Global stores (productions, jurisdictions, loading)
│   │
│   ├── types/                  # TypeScript type definitions
│   │   └── index.ts            # API contract interfaces (Production, Jurisdiction, etc.)
│   │
│   ├── App.tsx                 # Root component with routing
│   ├── main.tsx                # Entry point
│   ├── App.css                 # Global styles
│   └── index.css               # Tailwind imports
│
├── public/                     # Static assets
│   └── vite.svg
│
├── index.html                  # HTML entry point
├── package.json                # Dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite build configuration
├── tailwind.config.js          # Tailwind CSS configuration
└── eslint.config.js            # ESLint rules

```

---

## 🛠️ Tech Stack

### Core Technologies

| Technology | Version | Purpose | Why We Chose It |
|------------|---------|---------|-----------------|
| **React** | 19.2.0 | UI framework | Latest features, improved performance, server components ready |
| **TypeScript** | 5.9.3 | Type safety | Catch errors early, better IDE support, self-documenting code |
| **Vite** | 7.2.4 | Build tool | Lightning-fast HMR, optimized production builds, ES modules |
| **TailwindCSS** | 4.1.18 | Styling | Utility-first, responsive design, small bundle size |
| **Zustand** | 5.0.10 | State management | Minimal API (<1KB), no boilerplate, TypeScript-first |
| **React Router** | 7.12.0 | Navigation | Industry standard, type-safe routes, nested routing |
| **Axios** | 1.13.2 | HTTP client | Interceptors, typed responses, request cancellation |

### Why This Stack?

**React 19** - Cutting-edge features like automatic batching and improved concurrent rendering

**TypeScript** - Type safety ensures API contracts are respected, reducing runtime errors

**Vite** - 10x faster than Webpack for development, instant server start

**TailwindCSS 4** - Latest version with improved performance and CSS-first configuration

**Zustand** - Simpler than Redux, more powerful than Context API, perfect for medium-sized apps

**React Router v7** - Seamless client-side navigation with type-safe routes

**Axios** - Better error handling and interceptors compared to fetch

---

## 📜 Available Scripts

### **Development**

```bash
# Start development server (localhost:3000)
npm run dev

# Start with network access
npm run dev -- --host

# Start on different port
npm run dev -- --port 5173
```

### **Build**

```bash
# Build for production
npm run build

# Output: frontend/dist/
```

Build process:
1. TypeScript compilation (`tsc -b`)
2. Vite bundling and optimization
3. Asset minification and compression
4. CSS purging (removes unused TailwindCSS)

**Build Output:**
- JavaScript: 283KB (92KB gzipped)
- CSS: 3.6KB
- Static assets in `dist/` directory

### **Preview**
### Development

```bash
# Start development server (http://localhost:3000)
npm run dev
```
- Enables Hot Module Replacement (HMR)
- TypeScript type checking in watch mode
- Opens browser automatically

### Production Build

```bash
# Build optimized production bundle
npm run build
```
- Compiles TypeScript to JavaScript
- Minifies and tree-shakes code
- Outputs to `dist/` directory
- Generates source maps

### Preview Production Build

```bash
# Preview production build locally
npm run preview

# Access at http://localhost:4173
```

### **Linting**

```bash
# Run ESLint
npm run lint

# Auto-fix issues
npm run lint -- --fix
```

### **Type Checking**

```bash
# TypeScript type checking only (no build)
npx tsc --noEmit
```

### **Clean**

```bash
# Remove node_modules
rm -rf node_modules

# Remove build output
rm -rf dist

# Fresh install
npm install
```

---

## 🛠️ Tech Stack Details

### **React 19**

Latest version of React with improved features:
- **Concurrent Rendering**: Better performance for complex UIs
- **Automatic Batching**: Reduced re-renders
- **Transitions API**: Smooth UI updates
- **Server Components** (future): Ready for SSR migration

**Key Benefits:**
- Faster rendering
- Better user experience
- Modern hooks and patterns
- Strong TypeScript support

### **Vite 7**

Next-generation build tool:
- **Lightning Fast HMR**: Changes reflect instantly
- **ESM-based**: Native ES modules for development
- **Optimized Builds**: Rollup-powered production bundles
- **Plugin Ecosystem**: Rich plugin support

**Configuration** (`vite.config.ts`):
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

### **TailwindCSS 4**

Utility-first CSS framework:
- **Utility Classes**: Rapid UI development
- **JIT Compiler**: Only builds classes you use
- **Responsive Design**: Mobile-first breakpoints
- **Dark Mode Support**: Ready to implement
- **Custom Theming**: PilotForge brand colors

**Configuration** (`tailwind.config.js`):
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pilotforge: {
          primary: '#1e40af',
          secondary: '#3b82f6',
        }
      }
    }
  }
}
```

### **Zustand**

Lightweight state management:
- **Simple API**: Easy to learn and use
- **No Boilerplate**: Minimal setup required
- **TypeScript Support**: Full type safety
- **DevTools**: Integration with Redux DevTools
- **Small Bundle**: Only 1KB gzipped

**Store Example**:
```typescript
import { create } from 'zustand'

interface ProductionStore {
  productions: Production[]
  loading: boolean
  fetchProductions: () => Promise<void>
}

export const useProductionStore = create<ProductionStore>((set) => ({
  productions: [],
  loading: false,
  fetchProductions: async () => {
    set({ loading: true })
    const data = await api.productions.list()
    set({ productions: data, loading: false })
  }
}))
```

### **React Router v7**

Client-side routing:
- **Declarative Routing**: Component-based routes
- **Code Splitting**: Lazy load route components
- **Nested Routes**: Complex routing patterns
- **Navigation Guards**: Protected routes
- **URL Parameters**: Dynamic route matching

**Router Setup**:
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/productions" element={<Productions />} />
        <Route path="/jurisdictions" element={<Jurisdictions />} />
        <Route path="/calculator" element={<Calculator />} />
      </Routes>
    </BrowserRouter>
  )
}
```

### **Axios**

HTTP client for API calls:
- **Interceptors**: Global request/response handling
- **TypeScript Support**: Typed requests and responses
- **Error Handling**: Centralized error management
- **Cancellation**: Abort requests
- **Automatic JSON**: Handles JSON serialization

---

## 🎯 Development Workflow

### **Component Development Guidelines**

#### **File Naming**
- Components: `PascalCase.tsx` (e.g., `Button.tsx`)
- Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
- Types: `PascalCase.ts` (e.g., `Production.ts`)

#### **Component Structure**
```typescript
// 1. Imports
import React from 'react'
import { api } from '../api'
import type { Production } from '../types'

// 2. Type definitions
interface ProductionCardProps {
  production: Production
  onEdit?: (id: string) => void
}

// 3. Component
export function ProductionCard({ production, onEdit }: ProductionCardProps) {
  // Hooks
  const [loading, setLoading] = React.useState(false)
  
  // Event handlers
  const handleEdit = () => {
    onEdit?.(production.id)
  }
  
  // Render
  return (
    <div className="border rounded-lg p-4">
      <h3>{production.title}</h3>
      <button onClick={handleEdit}>Edit</button>
    </div>
  )
}
```

### **State Management Best Practices**

#### **When to Use Zustand**
- Global state (productions list, user preferences)
- Shared across multiple components
- Persisted state (localStorage sync)

#### **When to Use Local State**
- UI state (modals, tooltips, forms)
- Component-specific data
- Temporary state

#### **Store Organization**
```typescript
// Separate concerns into focused stores
import { create } from 'zustand'

// Production store
export const useProductionStore = create(...)

// Jurisdiction store
export const useJurisdictionStore = create(...)

// UI store
export const useUIStore = create(...)
```

### **API Service Usage**

#### **Fetching Data**
```typescript
import { api } from '../api'

// In component
const fetchProductions = async () => {
  try {
    const productions = await api.productions.list()
    setProductions(productions)
  } catch (error) {
    console.error('Failed to fetch productions:', error)
  }
}
```

#### **Creating Resources**
```typescript
const createProduction = async (data: Partial<Production>) => {
  try {
    const newProduction = await api.productions.create(data)
    // Update local state
    setProductions([...productions, newProduction])
  } catch (error) {
    console.error('Failed to create production:', error)
  }
}
```

#### **Error Handling**
```typescript
try {
  const result = await api.productions.get(id)
} catch (error) {
  if (axios.isAxiosError(error)) {
    if (error.response?.status === 404) {
      console.error('Production not found')
    } else if (error.response?.status === 500) {
      console.error('Server error')
    }
  }
}
```

### **TypeScript Typing Conventions**

#### **Props Interfaces**
```typescript
// Always define props interface
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
}

export function Button({ label, onClick, variant = 'primary', disabled }: ButtonProps) {
  // ...
}
```

#### **API Response Types**
```typescript
// Define response types
interface ProductionListResponse {
  total: number
  productions: Production[]
}

// Use in API service
const listProductions = async (): Promise<Production[]> => {
  const response = await apiClient.get<Production[]>('/productions')
  return response.data
}
```

### **Styling with TailwindCSS**

#### **Utility-First Approach**
```typescript
// Good: Use Tailwind utilities
<button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Click Me
</button>

// Avoid: Custom CSS when Tailwind can do it
<button className="custom-button">
  Click Me
</button>
```

#### **Responsive Design**
```typescript
// Mobile-first responsive classes
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Content */}
</div>
```

#### **Reusable Classes**
```typescript
// Define in component for consistency
const cardClasses = "bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"

<div className={cardClasses}>
  {/* Card content */}
</div>
```

---

## 🚀 Build and Deployment

### **Production Build Process**

#### **Step 1: Build Frontend**

```bash
cd frontend
npm run build
```

**Build Output:**
```
dist/
├── assets/
│   ├── index-[hash].js      # Main JavaScript bundle (283KB → 92KB gzipped)
│   ├── index-[hash].css     # Styles (3.6KB)
│   └── [other-assets]
└── index.html               # Entry HTML file
```

#### **Step 2: Verify Build**

```bash
# Preview locally
npm run preview

# Check bundle size
ls -lh dist/assets/
```

### **Static File Serving via FastAPI**

The FastAPI backend serves the frontend static files:

**Backend Configuration** (`main.py`):
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# API routes
app.include_router(api_router, prefix="/api/v1")

# Serve frontend static files
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
```

**File Structure:**
```
/
├── api/              # FastAPI backend
│   └── v1/          # API endpoints
├── frontend/
│   └── dist/        # Built frontend files
└── [static files served for non-API routes]
```

### **Environment Configuration**

#### **Development**
```env
VITE_API_URL=http://localhost:8000
```

#### **Production**
```env
VITE_API_URL=https://pilotforge.onrender.com
```

Build with environment:
```bash
# Production build
VITE_API_URL=https://pilotforge.onrender.com npm run build
```

### **CORS Setup**

Backend CORS configuration for frontend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",           # Development
        "https://pilotforge.onrender.com"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Deployment to Render.com**

Update `render.yaml` to include frontend build:

```yaml
services:
  - type: web
    name: pilotforge
    env: python
    buildCommand: |
      cd frontend && npm install && npm run build && cd ..
      pip install -r requirements.txt
      python -m prisma generate
    startCommand: python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

**Deployment Steps:**
1. Push code to GitHub
2. Render automatically detects changes
3. Runs build command (installs frontend deps, builds, then backend)
4. Starts server serving both API and frontend
```
- Serves the `dist/` folder
- Useful for testing production build before deployment

### Linting

```bash
# Run ESLint on all source files
npm run lint
```
- Checks for code quality issues
- Enforces React best practices
- Catches common mistakes

### Type Checking

```bash
# Run TypeScript compiler in check mode
npx tsc --noEmit
```
- Validates all TypeScript types
- No build output, just error checking

---

## 💻 Development Workflow

### Hot Module Replacement (HMR)

Changes to React components are reflected **instantly** without full page reload:

```typescript
// Edit any .tsx file
export default function MyComponent() {
  return <div>Updated content!</div>  // Changes appear immediately
}
```

### TypeScript Integration

All components are type-safe:

```typescript
interface Production {
  id: string;
  title: string;
  budget: number;
  startDate: string;
}

// TypeScript ensures correct usage
const production: Production = {
  id: '123',
  title: 'My Film',
  budget: 5000000,
  startDate: '2026-06-01'
}
```

### Component Development

**1. Create a new component:**

```typescript
// src/components/MyComponent.tsx
export default function MyComponent({ title }: { title: string }) {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold">{title}</h2>
    </div>
  )
}
```

**2. Use it in a page:**

```typescript
// src/pages/MyPage.tsx
import MyComponent from '../components/MyComponent'

export default function MyPage() {
  return <MyComponent title="Hello World" />
}
```

---

## 🗂️ State Management

PilotForge uses **Zustand** for global state management.

### Store Structure

```typescript
// src/store/index.ts
import { create } from 'zustand'

interface AppStore {
  // Productions
  productions: Production[]
  setProductions: (productions: Production[]) => void
  addProduction: (production: Production) => void
  
  // Jurisdictions
  jurisdictions: Jurisdiction[]
  setJurisdictions: (jurisdictions: Jurisdiction[]) => void
  
  // Loading states
  isLoading: boolean
  setLoading: (loading: boolean) => void
}

const useStore = create<AppStore>((set) => ({
  productions: [],
  setProductions: (productions) => set({ productions }),
  addProduction: (production) => set((state) => ({
    productions: [...state.productions, production]
  })),
  
  jurisdictions: [],
  setJurisdictions: (jurisdictions) => set({ jurisdictions }),
  
  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading })
}))
```

### Using the Store

```typescript
// In a component
import useStore from '../store'

export default function ProductionList() {
  const productions = useStore((state) => state.productions)
  const setProductions = useStore((state) => state.setProductions)
  
  useEffect(() => {
    fetchProductions().then(setProductions)
  }, [])
  
  return (
    <div>
      {productions.map(p => <div key={p.id}>{p.title}</div>)}
    </div>
  )
}
```

### Why Zustand?

- **Simple API**: No providers, no context, no boilerplate
- **Small bundle**: <1KB gzipped
- **TypeScript-first**: Full type inference
- **Performant**: Only re-renders components that use changed state

---

## 🔌 API Integration

### Axios Client Configuration

```typescript
// src/api/client.ts
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default apiClient
```

### Service Methods

```typescript
// src/api/index.ts
import apiClient from './client'
import type { Production, Jurisdiction } from '../types'

export const productionService = {
  // Get all productions
  getAll: async (): Promise<Production[]> => {
    const response = await apiClient.get('/productions')
    return response.data
  },
  
  // Get single production
  getById: async (id: string): Promise<Production> => {
    const response = await apiClient.get(`/productions/${id}`)
    return response.data
  },
  
  // Create production
  create: async (data: Omit<Production, 'id'>): Promise<Production> => {
    const response = await apiClient.post('/productions', data)
    return response.data
  },
  
  // Update production
  update: async (id: string, data: Partial<Production>): Promise<Production> => {
    const response = await apiClient.put(`/productions/${id}`, data)
    return response.data
  },
  
  // Delete production
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/productions/${id}`)
  }
}

export const jurisdictionService = {
  getAll: async (): Promise<Jurisdiction[]> => {
    const response = await apiClient.get('/jurisdictions')
    return response.data
  }
}

export const calculatorService = {
  calculate: async (productionId: string, jurisdictionId: string) => {
    const response = await apiClient.post('/calculate/simple', {
      productionId,
      jurisdictionId
    })
    return response.data
  }
}
```

### Using Services in Components

```typescript
import { productionService } from '../api'
import useStore from '../store'

export default function Productions() {
  const setProductions = useStore((state) => state.setProductions)
  const setLoading = useStore((state) => state.setLoading)
  
  useEffect(() => {
    const loadProductions = async () => {
      try {
        setLoading(true)
        const data = await productionService.getAll()
        setProductions(data)
      } catch (error) {
        console.error('Failed to load productions:', error)
      } finally {
        setLoading(false)
      }
    }
    
    loadProductions()
  }, [])
  
  // ... render logic
}
```

---

## 🎨 Styling

### TailwindCSS Utility Classes

```typescript
export default function Button({ children, variant = 'primary' }) {
  const baseClasses = 'px-4 py-2 rounded font-medium transition'
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300'
  }
  
  return (
    <button className={`${baseClasses} ${variantClasses[variant]}`}>
      {children}
    </button>
  )
}
```

### Responsive Design

```typescript
<div className="
  p-4           /* padding on mobile */
  md:p-6        /* medium padding on tablets */
  lg:p-8        /* large padding on desktop */
  
  grid
  grid-cols-1   /* 1 column on mobile */
  md:grid-cols-2 /* 2 columns on tablets */
  lg:grid-cols-3 /* 3 columns on desktop */
  
  gap-4         /* 1rem gap between items */
">
  {/* Grid items */}
</div>
```

### Custom Styles

When Tailwind isn't enough, use App.css:

```css
/* src/App.css */
.custom-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

## 🧭 Routing

### Route Configuration

```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/productions" element={<Productions />} />
        <Route path="/jurisdictions" element={<Jurisdictions />} />
        <Route path="/calculator" element={<Calculator />} />
      </Routes>
    </BrowserRouter>
  )
}
```

### Navigation

```typescript
import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  
  return (
    <nav>
      {/* Declarative navigation */}
      <Link to="/">Dashboard</Link>
      <Link to="/productions">Productions</Link>
      
      {/* Programmatic navigation */}
      <button onClick={() => navigate('/calculator')}>
        Go to Calculator
      </button>
    </nav>
  )
}
```

### Active Route Highlighting

```typescript
import { NavLink } from 'react-router-dom'

<NavLink 
  to="/productions"
  className={({ isActive }) => 
    isActive ? 'text-blue-600 font-bold' : 'text-gray-600'
  }
>
  Productions
</NavLink>
```

---

## 📦 Building for Production

### Build Process

```bash
npm run build
```

**What happens:**
1. TypeScript compiles to JavaScript
2. Code is minified and tree-shaken
3. CSS is optimized and purged
4. Assets are hashed for caching
5. Source maps are generated
6. Output goes to `dist/` directory

### Build Output

```
dist/
├── assets/
│   ├── index-[hash].js      # Main JavaScript bundle
│   ├── index-[hash].css     # Compiled CSS
│   └── *.svg                # Static assets
└── index.html               # Entry HTML file
```

### Production Optimizations

**Code Splitting:**
```typescript
// Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Productions = lazy(() => import('./pages/Productions'))

<Suspense fallback={<Spinner />}>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/productions" element={<Productions />} />
  </Routes>
</Suspense>
```

**Tree Shaking:**
Vite automatically removes unused code

**CSS Purging:**
TailwindCSS removes unused utility classes

### Testing Production Build Locally

```bash
npm run preview
```

Visit: http://localhost:4173

---

## 🔐 Environment Variables

### Configuration

Create `.env` file in `frontend/` directory:

```bash
# API endpoint
VITE_API_URL=http://localhost:8000/api/v1
```

### Usage in Code

```typescript
// Access environment variables
const apiUrl = import.meta.env.VITE_API_URL

// All Vite env vars must be prefixed with VITE_
console.log(import.meta.env.VITE_API_URL)
```

### Environment-Specific Configs

```bash
# .env.development (used by npm run dev)
VITE_API_URL=http://localhost:8000/api/v1

# .env.production (used by npm run build)
VITE_API_URL=https://api.pilotforge.com/api/v1
```

### Important Notes

⚠️ **Only `VITE_` prefixed variables are exposed to the client**

⚠️ **Never store secrets in frontend env vars** (they're visible in the browser)

---

## 🐛 Troubleshooting

### **Issue: npm install fails**

**Error:** `ERESOLVE unable to resolve dependency tree`

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Try with legacy peer deps
npm install --legacy-peer-deps

# Or use --force
npm install --force
```

### **Issue: Port 3000 already in use**

**Error:** `Port 3000 is already in use`

**Solution:**
```bash
# Use different port
npm run dev -- --port 5173

# Or kill process on port 3000
# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID [PID] /F
```

### **Issue: API calls fail with CORS error**

**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution:**
1. Verify backend is running on http://localhost:8000
2. Check backend CORS configuration includes http://localhost:3000
3. Verify VITE_API_URL in `.env` is correct

### **Issue: Environment variables not working**

**Error:** `import.meta.env.VITE_API_URL is undefined`

**Solution:**
1. Ensure variable starts with `VITE_`
2. Restart dev server after changing `.env`
3. Check `.env` file is in `frontend/` directory
4. Verify no typos in variable name

### **Issue: TypeScript errors**

**Error:** `Type 'X' is not assignable to type 'Y'`

**Solution:**
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Verify types are installed
npm install --save-dev @types/react @types/react-dom

# Clear TypeScript cache
rm -rf node_modules/.cache
```

### **Issue: Build fails**
### Issue: Port 3000 Already in Use

**Error:** `Port 3000 is already in use`

**Solution:**
```bash
# Option 1: Kill process on port 3000
npx kill-port 3000

# Option 2: Use different port
npm run dev -- --port 3001
```

---

### Issue: Module Not Found

**Error:** `Cannot find module './api'`

**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install

# Or clear npm cache
npm cache clean --force
npm install
```

---

### Issue: TypeScript Errors

**Error:** `Property 'xyz' does not exist on type 'ABC'`

**Solution:**
```typescript
// Update type definitions in src/types/index.ts
export interface Production {
  id: string
  title: string
  xyz: string  // Add missing property
}

// Or run TypeScript in watch mode to see all errors
npx tsc --watch --noEmit
```

---

### Issue: API Connection Failed

**Error:** `Network Error` or `ERR_CONNECTION_REFUSED`

**Solution:**
1. Verify backend is running: http://localhost:8000/docs
2. Check `.env` file has correct `VITE_API_URL`
3. Restart dev server after changing `.env`

```bash
# Stop dev server (Ctrl+C)
# Restart
npm run dev
```

---

### Issue: Styles Not Updating

**Error:** Tailwind classes not applying

**Solution:**
```bash
# Restart dev server
# Vite might cache CSS, try hard refresh
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Or clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

---

### Issue: Build Fails

**Error:** `Build failed with errors`

**Solution:**
```bash
# Clear dist folder
rm -rf dist

# Clear node_modules and reinstall
rm -rf node_modules
npm install

# Build again
npm run build
```

### **Issue: HMR not working**

**Problem:** Changes don't reflect in browser

**Solution:**
1. Check browser console for errors
2. Restart dev server
3. Clear browser cache (Ctrl+Shift+R)
4. Check firewall isn't blocking port 3000

### **Common Pitfalls**

#### **Forgetting to start backend**
Frontend needs backend API running. Start backend first:
```bash
# Terminal 1: Start backend
python -m uvicorn src.main:app --reload

# Terminal 2: Start frontend
cd frontend && npm run dev
```

#### **Wrong Node.js version**
Use Node.js 18.0.0+ for compatibility:
```bash
node --version  # Should be v18.0.0 or higher
```

#### **Not installing dependencies**
Always run `npm install` after pulling changes:
```bash
git pull
cd frontend
npm install
# Check for TypeScript errors
npx tsc --noEmit

# Check for ESLint errors
npm run lint

# Try clean build
rm -rf dist
npm run build
```

---

### Issue: Slow HMR

**Problem:** Hot Module Replacement is slow

**Solution:**
```bash
# Update Vite config to exclude large directories
// vite.config.ts
export default {
  server: {
    fs: {
      strict: false
    }
  }
}

# Or upgrade dependencies
npm update
```

---

## 📚 Additional Resources

### **Documentation**
- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Zustand Guide](https://github.com/pmndrs/zustand)
- [React Router](https://reactrouter.com/)

### **TypeScript**
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

### **Tools**
- [VS Code](https://code.visualstudio.com/) - Recommended IDE
- [React DevTools](https://react.dev/learn/react-developer-tools) - Browser extension
- [Redux DevTools](https://github.com/reduxjs/redux-devtools) - Works with Zustand

---

## ✅ Checklist for New Developers

- [ ] Node.js 18+ installed
- [ ] Backend running on http://localhost:8000
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` file created with correct API URL
- [ ] Development server started (`npm run dev`)
- [ ] Can access http://localhost:3000
- [ ] API calls working (check Network tab)
- [ ] No console errors in browser

---

**Need help?** Check the [troubleshooting section](#troubleshooting) or open a GitHub issue!
- **React Documentation**: https://react.dev
- **TypeScript Handbook**: https://www.typescriptlang.org/docs
- **Vite Guide**: https://vite.dev/guide
- **TailwindCSS Docs**: https://tailwindcss.com/docs
- **Zustand Guide**: https://github.com/pmndrs/zustand
- **React Router Docs**: https://reactrouter.com

---

## 🎉 You're Ready!

Start developing:

```bash
cd frontend
npm run dev
```

Visit **http://localhost:3000** and start building! 🚀

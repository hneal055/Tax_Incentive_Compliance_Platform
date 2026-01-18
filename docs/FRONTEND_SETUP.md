# 🎨 Frontend Setup Guide

> Complete guide to developing with the PilotForge React frontend

---

## 📋 Table of Contents

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

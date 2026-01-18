# 🎨 Frontend Setup Guide - PilotForge

> Comprehensive guide to setting up and developing the React frontend

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

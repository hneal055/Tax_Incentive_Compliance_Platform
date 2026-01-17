# 🎬 PilotForge UI Setup Guide

Complete guide for setting up and running the PilotForge frontend application.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Environment Configuration](#environment-configuration)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)
- [Available Scripts](#available-scripts)

---

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

- **Node.js**: Version 20.x or higher
  - Check version: `node --version`
  - Download: [https://nodejs.org/](https://nodejs.org/)
  
- **npm**: Version 10.x or higher (comes with Node.js)
  - Check version: `npm --version`

- **Backend API**: The PilotForge backend must be running
  - Default URL: `http://localhost:8000`
  - See main [README.md](./README.md) for backend setup

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: ~500MB for dependencies

---

## Quick Start

For experienced developers who want to get started immediately:

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Create environment file (optional - uses defaults if not present)
cp .env.example .env

# 4. Start development server
npm run dev
```

The UI will be available at: **http://localhost:3000**

---

## Detailed Setup

### Step 1: Clone the Repository

If you haven't already cloned the repository:

```bash
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform
```

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Dependencies

Install all required npm packages:

```bash
npm install
```

**What this does:**
- Installs React 19, Vite 7, TypeScript, TailwindCSS 4, and all other dependencies
- Creates `node_modules` directory with all packages
- May take 1-3 minutes depending on your internet connection

**Expected output:**
```
added 234 packages, and audited 235 packages in 45s

67 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

### Step 4: Configure Environment (Optional)

The frontend works with default settings, but you can customize the backend API URL:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if your backend runs on a different URL
# Default: VITE_API_URL=http://localhost:8000
```

**Note:** If you don't create a `.env` file, the application will use the proxy configuration in `vite.config.ts` which points to `http://localhost:8000`.

### Step 5: Start the Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v7.2.4  ready in 823 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Step 6: Access the Application

Open your browser and navigate to:

**http://localhost:3000**

You should see the PilotForge dashboard with navigation to:
- 📊 **Dashboard**: Overview of productions and jurisdictions
- 🎬 **Productions**: Manage film/TV productions
- 🌍 **Jurisdictions**: Browse global tax incentive programs
- 🧮 **Calculator**: Calculate tax incentives

---

## Environment Configuration

### Environment Variables

The frontend uses Vite's environment variable system. All variables must be prefixed with `VITE_` to be accessible in the application.

#### Available Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` | No |

#### Example .env File

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000

# For production deployment
# VITE_API_URL=https://your-production-api.com
```

### Proxy Configuration

The Vite development server includes a proxy configuration for API requests:

- **API Proxy**: `/api/*` → `http://localhost:8000`

This means requests to `http://localhost:3000/api/v1/...` are automatically forwarded to the backend.

---

## Development Workflow

### Hot Module Replacement (HMR)

Vite provides instant hot module replacement. When you save changes to your code, the browser updates automatically without a full page reload.

**What you can edit:**
- React components (`src/components/`, `src/pages/`)
- Styles (Tailwind classes, CSS files)
- TypeScript files
- Configuration files (may require restart)

### Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Layout.tsx
│   │   ├── Navbar.tsx
│   │   └── Spinner.tsx
│   ├── pages/           # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Productions.tsx
│   │   ├── Jurisdictions.tsx
│   │   └── Calculator.tsx
│   ├── store/           # Zustand state management
│   ├── App.tsx          # Root component with routing
│   └── main.tsx         # Application entry point
├── public/              # Static assets
├── index.html           # HTML template
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies and scripts
```

### Development Best Practices

1. **Keep the backend running**: The frontend needs the API at `http://localhost:8000`
2. **Check browser console**: Look for errors in DevTools (F12)
3. **Use ESLint**: Run `npm run lint` to check for code issues
4. **TypeScript**: The project uses strict TypeScript - fix type errors before committing

---

## Available Scripts

All scripts should be run from the `frontend` directory:

### `npm run dev`
Starts the development server with hot module replacement.
- **URL**: http://localhost:3000
- **Use for**: Day-to-day development

### `npm run build`
Creates an optimized production build.
- **Output**: `dist/` directory
- **Use for**: Preparing for deployment

### `npm run preview`
Previews the production build locally.
- **URL**: http://localhost:4173
- **Use for**: Testing the production build before deployment

### `npm run lint`
Runs ESLint to check for code quality issues.
- **Use for**: Code quality checks, pre-commit validation

---

## Troubleshooting

### Common Issues and Solutions

#### ❌ "EADDRINUSE: address already in use :::3000"

**Problem**: Port 3000 is already in use by another application.

**Solution**:
```bash
# Option 1: Stop the other application using port 3000

# Option 2: Use a different port
npm run dev -- --port 3001
```

---

#### ❌ "Cannot GET /api/v1/..."

**Problem**: Backend API is not running or not accessible.

**Solution**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check backend logs for errors
3. Ensure PostgreSQL database is running (required for backend)
4. Review backend setup in main [README.md](./README.md)

---

#### ❌ "Module not found" or "Cannot find module"

**Problem**: Dependencies are not installed or corrupted.

**Solution**:
```bash
# Remove node_modules and reinstall
rm -rf node_modules
npm install

# Or on Windows
rmdir /s node_modules
npm install
```

---

#### ❌ "Network Error" or CORS errors

**Problem**: Backend is not configured to accept requests from frontend.

**Solution**:
1. Ensure backend has CORS enabled for `http://localhost:3000`
2. Check backend configuration in `src/main.py`
3. Verify `vite.config.ts` proxy settings

---

#### ❌ TypeScript errors

**Problem**: Type checking is failing.

**Solution**:
```bash
# Check TypeScript configuration
npm run build

# This will show all type errors
# Fix them before committing code
```

---

#### ❌ Slow performance or white screen

**Problem**: Browser cache issues or JavaScript errors.

**Solution**:
1. Hard refresh the page: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. Clear browser cache and cookies
3. Check browser console (F12) for JavaScript errors
4. Try a different browser

---

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look at terminal output and browser console
2. **Review documentation**: See [FRONTEND_README.md](./frontend/FRONTEND_README.md)
3. **Check backend status**: Ensure the backend API is healthy
4. **GitHub Issues**: Report bugs or ask questions on GitHub

---

## Testing the UI

### Manual Testing Checklist

After starting the UI, verify these features work:

- [ ] Dashboard loads and displays welcome message
- [ ] Navigation works (Dashboard, Productions, Jurisdictions, Calculator)
- [ ] Productions page loads (may show "No productions found" if empty)
- [ ] Jurisdictions page displays the list of jurisdictions
- [ ] Calculator page loads and accepts input
- [ ] API calls complete successfully (check Network tab in DevTools)
- [ ] No console errors (check browser console with F12)

### Browser Compatibility

The UI is tested and supported on:

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ⚠️ Internet Explorer: **Not supported**

---

## Next Steps

Once your UI is running:

1. **Explore the application**: Navigate through all pages
2. **Read the User Manual**: See [docs/USER_MANUAL.md](./docs/USER_MANUAL.md)
3. **Review API documentation**: Visit http://localhost:8000/docs
4. **Start developing**: Make changes and see them live!

---

## Production Deployment

For deploying the frontend to production:

1. **Build the production bundle**:
   ```bash
   npm run build
   ```

2. **Preview locally** (optional):
   ```bash
   npm run preview
   ```

3. **Deploy the `dist` folder** to your hosting service:
   - Vercel, Netlify, AWS S3, or any static hosting
   - Configure environment variables for production API URL
   - See [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) for details

---

## Technology Stack

The frontend is built with modern web technologies:

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7 (fast HMR and optimized builds)
- **Styling**: TailwindCSS 4 (utility-first CSS)
- **State Management**: Zustand (lightweight and simple)
- **Routing**: React Router v7 (declarative routing)
- **HTTP Client**: Axios (promise-based HTTP requests)

---

**Need more help?** Check the main [README.md](./README.md) or frontend-specific [FRONTEND_README.md](./frontend/FRONTEND_README.md).

---

**Copyright © 2025-2026 Howard Neal - PilotForge**

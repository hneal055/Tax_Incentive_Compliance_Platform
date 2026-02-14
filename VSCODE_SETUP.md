# Visual Studio Code Setup Guide

This guide will help you clone and set up the PilotForge Tax Incentive Compliance Platform in Visual Studio Code.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Visual Studio Code** (latest version)
- **Python 3.11+** 
- **Node.js 20+** and **npm 10+**
- **PostgreSQL 16**
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform
```

### 2. Open in VS Code

You have two options:

**Option A: Open the Workspace File (Recommended)**
```bash
code PilotForge.code-workspace
```

**Option B: Open the Folder**
```bash
code .
```

### 3. Install Recommended Extensions

When you first open the project, VS Code will prompt you to install recommended extensions. Click **"Install All"** to get:

- **Python** - Python language support
- **Pylance** - Fast Python language server
- **Black Formatter** - Python code formatter
- **ESLint** - JavaScript/TypeScript linter
- **Prettier** - Code formatter for web files
- **Prisma** - Database schema support
- **Tailwind CSS** - CSS IntelliSense
- **GitLens** - Enhanced Git integration
- And many more helpful tools!

### 4. Set Up the Python Environment

Open a terminal in VS Code (`` Ctrl+` `` or `Cmd+``) and run:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
python -m prisma generate
```

### 5. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials and API keys.

### 6. Set Up the Database

```bash
# Run migrations
python -m prisma migrate deploy
```

### 7. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..

cd developer-portal
npm install
cd ..
```

## Using VS Code Features

### Running the Application

#### Using Tasks (Recommended)

Press `Ctrl+Shift+B` (or `Cmd+Shift+B` on macOS) to see the build tasks menu:

- **Full Stack: Start All** - Starts both backend and frontend (default)
- **Backend: Run Server** - Starts only the FastAPI backend
- **Frontend: Dev Server** - Starts only the React frontend
- **Developer Portal: Dev Server** - Starts the documentation portal

Or use the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and type "Tasks: Run Task".

#### Using the Terminal

Open a terminal and run:

```bash
# Full stack (Windows)
.\start-fullstack.ps1

# Full stack (macOS/Linux)
./start-fullstack.sh

# Backend only
python -m uvicorn src.main:app --reload

# Frontend only
cd frontend && npm run dev -- --port 5200
```

### Debugging

Press `F5` or go to the Debug panel (`Ctrl+Shift+D` / `Cmd+Shift+D`) to start debugging.

Available debug configurations:

1. **Python: FastAPI Backend** - Debug the FastAPI server with breakpoints
2. **Python: Current File** - Debug the currently open Python file
3. **Python: Pytest Current File** - Debug tests in the current file
4. **Python: Pytest All Tests** - Debug all tests

Set breakpoints by clicking in the gutter to the left of the line numbers.

### Running Tests

#### Using VS Code Tasks

1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type "Tasks: Run Task"
3. Select:
   - **Backend: Run Tests** - Run Python tests
   - **Backend: Run Tests with Coverage** - Run with coverage report
   - **Frontend: Run Tests** - Run React tests
   - **Frontend: Run Tests (Watch)** - Run tests in watch mode

#### Using the Testing Panel

1. Click the Testing icon in the Activity Bar (flask icon)
2. VS Code will auto-discover your tests
3. Click the play button next to any test to run it
4. Click the debug icon to debug a test

#### Using the Terminal

```bash
# Backend tests
pytest
pytest -v
pytest --cov=src

# Frontend tests
cd frontend
npx vitest run
npx vitest  # Watch mode
```

### Code Formatting

Code is automatically formatted on save:

- **Python** files use Black formatter
- **TypeScript/JavaScript** files use Prettier
- **Imports** are automatically organized

You can also format manually:
- Right-click and select "Format Document"
- Or press `Shift+Alt+F` (Windows/Linux) / `Shift+Option+F` (macOS)

### Linting

Linting runs automatically as you type:

- **Python**: Flake8 (errors show as squiggly lines)
- **TypeScript/JavaScript**: ESLint

To run linters manually:

1. Command Palette → "Tasks: Run Task"
2. Select "Linting: Python (Flake8)" or "Frontend: Lint"

### IntelliSense & Code Navigation

- **Auto-completion**: Type and see suggestions (Python, TypeScript, etc.)
- **Go to Definition**: `F12` or `Ctrl+Click` on any symbol
- **Find All References**: `Shift+F12`
- **Rename Symbol**: `F2`
- **Quick Fix**: `Ctrl+.` when on an error or warning

### Database Management

#### Prisma Studio

Open the database GUI:

1. Command Palette → "Tasks: Run Task"
2. Select "Database: Studio"
3. Opens at http://localhost:5555

Or run in terminal:
```bash
python -m prisma studio
```

#### SQLTools

If you installed the recommended SQLTools extension:

1. Click the database icon in the Activity Bar
2. Add a PostgreSQL connection
3. Browse tables, run queries, and view data

## Workspace Structure

The workspace is organized into multiple folders:

- **Root** - Main project folder
- **Backend (Python)** - Python/FastAPI source code
- **Frontend (React)** - React/TypeScript application
- **Developer Portal (Next.js)** - API documentation site

Each folder has its own settings and configurations.

## Common Tasks Reference

| Task | Shortcut | Description |
|------|----------|-------------|
| Run Build Task | `Ctrl+Shift+B` | Start the full stack application |
| Start Debugging | `F5` | Start debugging the backend |
| Open Command Palette | `Ctrl+Shift+P` | Access all VS Code commands |
| Open Terminal | `` Ctrl+` `` | Open integrated terminal |
| Format Document | `Shift+Alt+F` | Format current file |
| Toggle Sidebar | `Ctrl+B` | Show/hide file explorer |
| Go to File | `Ctrl+P` | Quick file search |
| Search in Files | `Ctrl+Shift+F` | Search across all files |
| Source Control | `Ctrl+Shift+G` | Git panel |
| Run Tests | See Testing Panel | Run/debug tests |

## Troubleshooting

### Python Interpreter Not Found

1. Press `Ctrl+Shift+P` / `Cmd+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `.venv/bin/python` or `.venv/Scripts/python.exe`

### Import Errors in Python

Make sure `PYTHONPATH` is set correctly:
1. Check `.vscode/settings.json` has `python.defaultInterpreterPath` set
2. Reload the window: Command Palette → "Developer: Reload Window"

### ESLint Not Working

```bash
cd frontend
npm install
# Reload VS Code window
```

### Prisma Extension Errors

```bash
python -m prisma generate
# Reload VS Code window
```

## Useful Extensions (Optional)

In addition to recommended extensions, you might find these useful:

- **Todo Tree** - Highlight TODO comments
- **Better Comments** - Colorful comment highlighting
- **Import Cost** - Show import package sizes
- **Path Intellisense** - Autocomplete file paths
- **Material Icon Theme** - Better file icons

## Documentation

- [Main README](./README.md) - Project overview
- [Frontend Setup Guide](./docs/FRONTEND_SETUP.md) - Detailed frontend guide
- [User Manual](./docs/USER_MANUAL.md) - API and UI documentation
- [Deployment Guide](./docs/DEPLOYMENT.md) - Production deployment

## Getting Help

- Check the [Troubleshooting Guide](./TROUBLESHOOTING.md)
- Review the [Contributing Guide](./CONTRIBUTING.md)
- Open an issue on GitHub

---

**Happy coding! 🚀**

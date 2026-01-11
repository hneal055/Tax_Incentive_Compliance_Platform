# 🤖 PilotForge Automation Suite

> Complete automation toolkit for PilotForge development and deployment

---

## 🎯 Overview

The PilotForge Automation Suite provides one-command automation for:
- **Rebranding** - Update all files with PilotForge branding
- **Version Management** - Bump versions across the project
- **Documentation Generation** - Auto-generate API docs
- **Code Quality** - Testing, linting, formatting
- **CI/CD** - Automated deployment pipeline
- **Brand Consistency** - Ensure consistent branding

---

## 🚀 Quick Start

### **Master Command (Recommended)**

```bash
# Interactive menu
python automate.py

# Run specific automation
python automate.py test
python automate.py docs
python automate.py all

# List all options
python automate.py list
```

---

## 📋 Available Automations

### **1. Rebranding (`rebrand.py`)** 🎨

Automatically updates all project files with PilotForge branding.

```bash
# Run rebranding
python rebrand.py
```

**What it does:**
- ✅ Updates all Python files (API titles, descriptions)
- ✅ Updates all documentation (README, USER_MANUAL, etc.)
- ✅ Updates LICENSE file
- ✅ Updates configuration files
- ✅ Creates backup before changes
- ✅ Generates BRAND_GUIDELINES.md

**Output:**
- Backup folder (`backup_YYYYMMDD_HHMMSS/`)
- Updated project files
- Brand guidelines document

---

### **2. Version Management (`version_manager.py`)** 🔢

Manages version numbers across the entire project using semantic versioning.

```bash
# Bump patch version (1.0.0 → 1.0.1)
python version_manager.py patch

# Bump minor version (1.0.1 → 1.1.0)
python version_manager.py minor

# Bump major version (1.1.0 → 2.0.0)
python version_manager.py major
```

**What it does:**
- ✅ Updates version in `src/main.py`
- ✅ Updates version in `pyproject.toml`
- ✅ Updates version in `README.md`
- ✅ Updates `CHANGELOG.md`
- ✅ Creates git tag (optional)

**Files updated:**
- `src/main.py`
- `pyproject.toml`
- `README.md`
- `CHANGELOG.md`

---

### **3. Documentation Generation (`generate_docs.py`)** 📚

Auto-generates comprehensive API documentation from OpenAPI specification.

```bash
# Generate all documentation
python generate_docs.py
```

**Requirements:**
- ⚠️ API must be running (`python -m uvicorn src.main:app --reload`)

**What it generates:**
- ✅ `API_REFERENCE.md` - Complete API reference
- ✅ `PilotForge.postman_collection.json` - Postman collection
- ✅ `openapi.json` - OpenAPI specification

**Use cases:**
- Keep API docs up-to-date automatically
- Generate Postman collection for testing
- Export OpenAPI spec for integrations

---

### **4. Brand Consistency Checker (`check_branding.py`)** ✅

Scans project for brand consistency issues and can auto-fix them.

```bash
# Check brand consistency
python check_branding.py
```

**What it checks:**
- ✅ Correct name usage ("PilotForge" not "Pilot Forge")
- ✅ Copyright format
- ✅ API title correctness
- ✅ Tagline usage

**Features:**
- Generates detailed report
- Shows file locations and line numbers
- Can generate auto-fix script

---

### **5. Master Automation Runner (`automate.py`)** 🎯

One command to run any automation or combination of automations.

```bash
# Interactive mode
python automate.py

# Run specific automation
python automate.py rebrand
python automate.py version patch
python automate.py docs
python automate.py test
python automate.py lint
python automate.py format

# Run full quality check
python automate.py all
```

**Commands:**

| Command | Description |
|---------|-------------|
| `rebrand` | Rebrand to PilotForge |
| `version` | Bump version numbers |
| `docs` | Generate API documentation |
| `test` | Run test suite with coverage |
| `lint` | Check code quality |
| `format` | Auto-format code |
| `all` | Run tests + lint + docs |

---

## 🔄 CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

Automated GitHub Actions workflow for continuous integration and deployment.

**Triggers:**
- Push to `main` or `develop` branch
- Pull requests to `main`
- Version tags (`v*.*.*`)

**Jobs:**

### **1. Test (Always runs)**
- ✅ Sets up PostgreSQL database
- ✅ Installs dependencies
- ✅ Runs Prisma migrations
- ✅ Executes test suite with coverage
- ✅ Uploads coverage to Codecov

### **2. Lint (Always runs)**
- ✅ Checks code formatting (Black)
- ✅ Checks import sorting (isort)
- ✅ Runs Flake8 linting

### **3. Security Scan (Always runs)**
- ✅ Scans for security vulnerabilities
- ✅ Uploads results to GitHub Security

### **4. Deploy (Main branch only)**
- ✅ Deploys to Render.com
- ✅ Only runs after tests pass
- ✅ Only runs on `main` branch pushes

### **5. Release (Version tags only)**
- ✅ Creates GitHub release
- ✅ Auto-generates release notes
- ✅ Triggered by version tags

**Setup:**

1. Add GitHub Secrets:
```
Settings → Secrets → Actions → New repository secret

RENDER_SERVICE_ID: your-render-service-id
RENDER_API_KEY: your-render-api-key
```

2. Push to trigger:
```bash
git push origin main
```

---

## 📖 Usage Examples

### **Example 1: New Feature Development**

```bash
# 1. Create feature branch
git checkout -b feature/new-calculator

# 2. Make changes...
# 3. Format and lint code
python automate.py format
python automate.py lint

# 4. Run tests
python automate.py test

# 5. Commit and push
git add .
git commit -m "Add new calculator feature"
git push origin feature/new-calculator

# GitHub Actions automatically runs tests
```

---

### **Example 2: Preparing a Release**

```bash
# 1. Ensure all tests pass
python automate.py all

# 2. Update API documentation
python -m uvicorn src.main:app --reload &
python automate.py docs

# 3. Bump version
python automate.py version minor

# 4. Update CHANGELOG.md with release notes
nano CHANGELOG.md

# 5. Commit and tag
git add .
git commit -m "Bump version to 1.1.0"
git tag -a v1.1.0 -m "PilotForge v1.1.0"

# 6. Push with tags
git push origin main --tags

# GitHub Actions automatically creates release
```

---

### **Example 3: Daily Development**

```bash
# Morning: Check brand consistency
python check_branding.py

# Before commit: Run quality checks
python automate.py all

# Before pushing: Format code
python automate.py format
```

---

## 🛠️ Installation

### **Requirements**

```bash
# Core dependencies (already in requirements.txt)
pip install -r requirements.txt

# Additional tools for automation
pip install black isort flake8 mypy
```

### **Optional: Pre-commit Hooks**

Automatically run checks before committing:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

---

## 📊 Automation Workflow

```
┌─────────────────────────────────────────────────────────┐
│                  PilotForge Automation                  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Development Changes    │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  automate.py format    │ ◄── Auto-format code
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  automate.py test      │ ◄── Run tests
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  automate.py lint      │ ◄── Check quality
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  check_branding.py     │ ◄── Verify branding
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Git Commit            │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Git Push              │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  GitHub Actions CI/CD  │ ◄── Automated pipeline
              └────────────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
         ┌──────────────┐  ┌──────────────┐
         │  Test & Lint │  │    Deploy    │
         └──────────────┘  └──────────────┘
```

---

## 🎯 Best Practices

### **1. Run Before Every Commit**
```bash
python automate.py all
```

### **2. Update Docs When API Changes**
```bash
python generate_docs.py
```

### **3. Check Branding Weekly**
```bash
python check_branding.py
```

### **4. Use Semantic Versioning**
```bash
# Bug fixes → patch
python version_manager.py patch

# New features → minor
python version_manager.py minor

# Breaking changes → major
python version_manager.py major
```

---

## 🐛 Troubleshooting

### **Issue: "API not running" error**

**Solution:**
```bash
# Start API in separate terminal
python -m uvicorn src.main:app --reload

# Then run automation
python automate.py docs
```

### **Issue: "Module not found" error**

**Solution:**
```bash
# Ensure you're in virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### **Issue: "Git tag already exists"**

**Solution:**
```bash
# Delete existing tag
git tag -d v1.0.0

# Create new tag
python version_manager.py patch
```

---

## 📞 Support

- **GitHub Issues**: Report bugs or request features
- **Documentation**: See individual script files for details
- **CI/CD Logs**: Check GitHub Actions for pipeline issues

---

## 🎉 Summary

The PilotForge Automation Suite provides:
- ✅ **One-command** automation for common tasks
- ✅ **Consistent branding** across all files
- ✅ **Automated testing** and deployment
- ✅ **Version management** with semantic versioning
- ✅ **Auto-generated documentation** from OpenAPI
- ✅ **Code quality** checks and formatting
- ✅ **CI/CD pipeline** for GitHub

**Result:** Professional, maintainable, production-ready code! 🚀

---

**Last Updated:** January 10, 2026  
**Version:** 1.0.0  
**Project:** PilotForge - Tax Incentive Intelligence for Film & TV
# 📖 PilotForge - User Manual

> **Tax Incentive Intelligence for Film & TV Productions**  
> Complete guide to the PilotForge platform

**Version:** 1.1.0  
**Last Updated:** February 2, 2026  
**Product Name:** PilotForge (formerly Tax-Incentive Compliance Platform)

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Frontend Application Guide](#frontend-application-guide)
4. [API Documentation](#api-documentation)
5. [Calculator Features](#calculator-features)
6. [Reports & Exports](#reports--exports)
7. [Data Management](#data-management)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Support & Resources](#support--resources)

---

## 🎬 Introduction

### **What is PilotForge?**

PilotForge is a comprehensive tax incentive calculation and compliance platform designed specifically for the global film and television production industry. It helps producers, line producers, and production accountants:

- **Compare tax incentives** across 32+ global jurisdictions
- **Calculate potential savings** with precision and compliance
- **Track productions** and manage budgets effectively
- **Generate professional reports** for stakeholders and investors
- **Ensure compliance** with jurisdiction-specific requirements

### **Key Features**

✅ **32 Global Jurisdictions** - USA, Canada, UK, Ireland, Australia, New Zealand, and more  
✅ **33 Incentive Programs** - State credits, federal rebates, provincial programs  
✅ **Multi-Currency Support** - Automatic currency conversion  
✅ **Stackable Credits** - Calculate base + bonus incentives  
✅ **Compliance Verification** - Automated requirement checking  
✅ **Professional Reports** - PDF and Excel exports  
✅ **Modern React UI** - Intuitive, responsive interface  
✅ **RESTful API** - Full programmatic access

### **Who Should Use This Manual?**

- **Production Managers** - Planning shooting locations
- **Line Producers** - Budgeting and cost analysis
- **Accountants** - Tax credit calculations and compliance
- **Developers** - API integration and automation
- **Investors** - ROI analysis and incentive maximization

---

## 🚀 Getting Started

### **System Requirements**

**For Users (Frontend Only):**
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Internet connection
- Screen resolution: 1280x720 minimum (responsive to mobile)

**For Developers (Full Stack):**
- **Backend:** Python 3.12+
- **Frontend:** Node.js 20+, npm 10+
- **Database:** PostgreSQL 16+
- **Operating System:** Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)

### **Quick Start - Users**

**Production Deployment:**
```
https://pilotforge.onrender.com
```

**Local Development:**
```
http://localhost:3000
```

No installation required - simply navigate to the URL in your web browser.

### **Quick Start - Developers**

#### **Option 1: Full Stack (Recommended)**

**Linux/macOS:**
```bash
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform
./start-fullstack.sh
```

**Windows:**
```powershell
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform
.\start-fullstack.ps1
```

This starts:
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Frontend UI:** http://localhost:3000

#### **Option 2: Backend Only**

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
python -m prisma generate

# Run migrations
python -m prisma migrate deploy

# Start server
python -m uvicorn src.main:app --reload
```

**Access:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### **Option 3: Frontend Only**

```bash
cd frontend
npm install
npm run dev
```

**Access:** http://localhost:3000

**Note:** Requires backend to be running for full functionality.

(Continue with the rest of the document content...)
# 📖 PilotForge - User Manual

> **Tax Incentive Intelligence for Film & TV Productions**  
> Your complete guide to maximizing film tax incentives worldwide

**Version:** 1.1.0  
**Last Updated:** February 2, 2026  
**Product Name:** PilotForge

---

## 🎬 Welcome to PilotForge

PilotForge is a comprehensive tax incentive calculation and compliance platform designed specifically for the global film and television production industry.

### **What is PilotForge?**

PilotForge helps producers, line producers, and production accountants:

- 🌍 **Compare tax incentives** across 32+ global jurisdictions
- 💰 **Calculate potential savings** with precision and compliance
- 🎬 **Track productions** and manage budgets effectively
- 📊 **Generate professional reports** for stakeholders and investors
- ✅ **Ensure compliance** with jurisdiction-specific requirements

### **Key Features**

✅ **32 Global Jurisdictions** - USA, Canada, UK, Ireland, Australia, New Zealand, and more  
✅ **33 Incentive Programs** - State credits, federal rebates, provincial programs  
✅ **Multi-Currency Support** - Automatic currency conversion  
✅ **Stackable Credits** - Calculate base + bonus incentives  
✅ **Compliance Verification** - Automated requirement checking  
✅ **Professional Reports** - PDF and Excel exports  
✅ **Modern React UI** - Intuitive, responsive interface  
✅ **RESTful API** - Full programmatic access

---

## 📚 Documentation Structure

This user manual is organized into focused guides for easy navigation:

### **Getting Started**

- 🚀 **[Quick Start Guide](#quick-start)** - Get up and running in 5 minutes
- 💻 **[Installation Guide](#installation)** - Detailed setup instructions
- 🎯 **[Your First Calculation](#tutorial)** - Step-by-step tutorial

### **User Guides**

- 🎨 **[Frontend Guide](./FRONTEND_GUIDE.md)** - Complete UI walkthrough
  - Dashboard
  - Productions Management
  - Jurisdictions Browser
  - Tax Calculator
  - Navigation & Features

- 🧮 **[Calculator Guide](./CALCULATOR_GUIDE.md)** - Tax incentive calculations
  - Simple Calculator
  - Multi-Jurisdiction Comparison
  - Compliance Verification
  - Stackable Credits
  - Scenario Modeling

- 📄 **[Reports Guide](./REPORTS_GUIDE.md)** - Generate professional documents
  - PDF Reports
  - Excel Workbooks
  - Customization Options

### **Developer Guides**

- 📡 **[API Guide](./API_GUIDE.md)** - Complete API reference
  - Authentication
  - Endpoints
  - Request/Response Formats
  - Error Handling
  - Best Practices

- 🗄️ **[Data Management Guide](./DATA_MANAGEMENT_GUIDE.md)** - CRUD operations
  - Jurisdictions API
  - Incentive Rules API
  - Productions API

### **Reference**

- 🔧 **[Troubleshooting Guide](./TROUBLESHOOTING_GUIDE.md)** - Common issues & solutions
- ❓ **[FAQ](./FAQ.md)** - Frequently asked questions
- 📖 **[Glossary](./GLOSSARY.md)** - Industry terminology
- 🔐 **[Security Guide](./SECURITY_GUIDE.md)** - Best practices

---

## 🚀 Quick Start

### **For Users (No Installation)**

**Production:**
```
https://pilotforge.onrender.com
```

**Local Development:**
```
http://localhost:3000
```

Just open in your web browser and start using!

### **For Developers (Full Stack)**

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

**Access:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 💻 Installation

### **System Requirements**

**For Users:**
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Internet connection

**For Developers:**
- **Backend:** Python 3.12+
- **Frontend:** Node.js 20+, npm 10+
- **Database:** PostgreSQL 16+

### **Backend Setup**

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python -m prisma generate
python -m prisma migrate deploy

# Start server
python -m uvicorn src.main:app --reload
```

### **Frontend Setup**

```bash
cd frontend
npm install
npm run dev
```

### **Environment Variables**

Create `.env` file:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/pilotforge"
SECRET_KEY="your-secret-key"
API_VERSION="v1"
CORS_ORIGINS="http://localhost:3000"
```

---

## 🎓 Tutorial: Your First Calculation

### **Scenario**
You're producing a $5 million feature film and want to compare California, Georgia, and Louisiana.

### **Steps**

**1. Create Your Production**
1. Navigate to http://localhost:3000/productions
2. Click "Create New Production"
3. Fill in:
   - Title: "My Feature Film"
   - Type: Feature Film
   - Budget: $5,000,000
   - Start Date: June 1, 2026
4. Click "Create Production"

**2. Calculate Tax Incentives**
1. Go to Calculator page
2. Select "My Feature Film"
3. Select "California"
4. Click "Calculate Tax Incentive"
5. Result: ~$1,000,000 (20%)

**3. Compare Jurisdictions**
1. Click "Compare More"
2. Add Georgia and Louisiana
3. View comparison:
   - Louisiana: $1,750,000 (35%) ✅ BEST
   - Georgia: $1,500,000 (30%)
   - California: $1,000,000 (20%)

**4. Generate Report**
1. Click "Generate Report"
2. Choose PDF or Excel
3. Share with stakeholders

**Decision:** Film in Louisiana to save $750,000!

---

## 📋 What's New in v1.1.0

**New Features:**
- ✨ Enhanced frontend UI with improved navigation
- 🧮 Scenario modeling calculator
- ✅ Improved compliance verification with deadline tracking
- 📊 Better mobile responsiveness

**Improvements:**
- ⚡ Faster API response times
- 📱 Better mobile interface
- 🌍 Updated jurisdiction data (32 jurisdictions)
- 📄 Improved report formatting

**Bug Fixes:**
- Fixed jurisdiction filter issues
- Corrected date validation
- Resolved currency formatting

---

## 🆘 Need Help?

- 📖 **Documentation:** Browse guides above
- 💬 **Discussions:** [GitHub Discussions](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/discussions)
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/issues)
- 🔧 **Troubleshooting:** See [Troubleshooting Guide](./TROUBLESHOOTING_GUIDE.md)

---

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details

---

**Made with ❤️ for the film & TV industry**

*Maximizing tax incentives worldwide, one production at a time.*
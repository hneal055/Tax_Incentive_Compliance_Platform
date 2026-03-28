# 🧪 QUICK START - Running Tests

## 📥 Setup (One-Time)

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Verify pytest is installed
pip show pytest

# Should show: pytest 9.0.2
```

## 🚀 Run Tests

### Basic Test Run
```powershell
pytest
```

### With Coverage Report
```powershell
pytest --cov=src --cov-report=term-missing
```

### Generate HTML Coverage Report
```powershell
pytest --cov=src --cov-report=html
start htmlcov\index.html
```

## 📊 Expected Results

You should see output like:

```
====================== test session starts ======================
collected 45 items

tests\test_calculator_logic.py ...................  [ 42%]
tests\test_api_endpoints.py ....................... [ 84%]
tests\test_report_generation.py ...............     [100%]

====================== 45 passed in 5.23s =======================
```

## ✅ What Gets Tested

1. **Calculator Logic** (19 tests)
   - Percentage calculations
   - Maximum caps
   - Stackable credits
   - Edge cases

2. **API Endpoints** (17 tests)
   - Health checks
   - Calculator endpoints
   - Report generation
   - Validation

3. **Report Generation** (9 tests)
   - PDF generation
   - Excel generation
   - Formatting

## 🎯 Coverage Goals

- **Overall**: 70%+
- **Calculator**: 90%+
- **API**: 80%+
- **Reports**: 75%+

## 🐛 If Tests Fail

### Common Issues:

1. **Database Connection Error**
   ```powershell
   # Start Docker PostgreSQL
   docker-compose up -d
   ```

2. **Import Errors**
   ```powershell
   # Regenerate Prisma client
   python -m prisma generate
   ```

3. **Module Not Found**
   ```powershell
   # Ensure you're in project root
   cd C:\Projects\Tax_Incentive_Compliance_Platform
   ```

## 📈 Next Steps

After tests pass:
1. Review coverage report
2. Add more tests if needed
3. Commit to GitHub
4. Set up CI/CD (optional)

## 🎉 Success!

If all tests pass, your platform is:
- ✅ Bulletproof
- ✅ Production-ready
- ✅ Professional quality
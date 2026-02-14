# Codecov Setup Guide

## Current Status
- ✅ Codecov action configured in CI/CD pipeline (`.github/workflows/ci-cd.yml`)
- ⚠️ CODECOV_TOKEN needs to be added to GitHub Secrets for private repository
- ⚠️ Coverage upload will be skipped if token is not configured (continue-on-error: true)

## Why Codecov Token is Needed
For **private repositories**, Codecov requires an authentication token to upload coverage reports.
Public repositories can upload coverage without a token.

## How to Set Up Codecov Token

### Step 1: Get Your Codecov Token
1. Go to [codecov.io](https://codecov.io)
2. Sign in with your GitHub account
3. Add your repository if not already added
4. Go to Settings → General → Repository Upload Token
5. Copy the token (it will look like: `abc123def456...`)

### Step 2: Add Token to GitHub Secrets
1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `CODECOV_TOKEN`
5. Value: Paste the token from Codecov
6. Click **Add secret**

### Step 3: Verify Setup
Once the token is added:
1. Push a new commit or re-run the CI/CD workflow
2. The "Upload coverage to Codecov" step should succeed
3. Visit your repository on codecov.io to see coverage reports

## Current Configuration
The CI/CD workflow uploads coverage from Python tests:
- Coverage file: `coverage.xml`
- Flags: `unittests`
- Name: `pilotforge-coverage`

## Local Coverage Testing
You can generate coverage reports locally without Codecov:

```bash
# Run tests with coverage
pytest --cov=src --cov-report=xml --cov-report=html --cov-report=term-missing

# View HTML coverage report
# Open htmlcov/index.html in your browser
```

## Notes
- The codecov upload step is set to `continue-on-error: true` so it won't fail the build if the token is missing
- This means coverage will be generated and visible in CI logs, but not uploaded to Codecov
- Once the token is configured, coverage will be automatically uploaded and tracked over time

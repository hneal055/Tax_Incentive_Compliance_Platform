# GitHub Repository Setup Checklist

## Repository: Tax_Incentive_Compliance_Platform

### ✓ Completed
- [x] Repository initialized and pushed to GitHub
- [x] v1.0.0 tag created and pushed
- [x] Git workflow documentation added

### Next: Configure GitHub Settings

---

## 1. Repository Settings (Settings tab)

### General
- [ ] **Description**: "Production-ready tax incentive compliance platform with FastAPI, PostgreSQL, and Kubernetes deployment"
- [ ] **Website**: (leave blank or add docs URL)
- [ ] **Visibility**: Public or Private (adjust as needed)

### Features (Enable)
- [ ] Discussions
- [ ] Wikis (optional)
- [ ] Projects (for issue tracking)
- [ ] Disable: Packages, Environments (unless using)

### Manage Access
- [ ] Add team members with appropriate roles
  - Maintainer: Full control
  - Developer: Push to branches, merge PRs
  - Viewer: Read-only

---

## 2. Branch Protection Rules

**URL**: Settings → Branches → Add rule

### Rule for `main` branch

**Settings:**
```
Branch name pattern: main
```

**Protections to Enable:**
- [ ] **Require a pull request before merging**
  - Require approvals: 1
  - Dismiss stale pull request approvals: ✓
  - Require code review from code owners: ✓

- [ ] **Require status checks to pass before merging**
  - Require branches to be up to date: ✓
  - Add status checks (after CI/CD configured):
    - tests (pytest)
    - build (docker build)
    - security (trivy scan)

- [ ] **Require conversation resolution before merging**
  - On any PR, discussions must be resolved

- [ ] **Require signed commits**
  - Optional but recommended for security

- [ ] **Restrict who can push to matching branches**
  - Restrict push access to: Admins only

### Rule for `develop` branch (optional)

Same as above but allow direct pushes from maintainers.

---

## 3. Secrets & Variables

**URL**: Settings → Secrets and variables

### Secrets (for CI/CD, keep sensitive)
- [ ] `DOCKER_REGISTRY_TOKEN` - Docker Hub/ECR push access
- [ ] `DATABASE_URL` - Staging PostgreSQL connection
- [ ] `API_KEY` - Third-party service API keys (if needed)

### Environment Variables (can be public)
```
APP_ENV=staging
LOG_LEVEL=INFO
DATABASE_POOL_SIZE=10
```

---

## 4. Deploy Keys (optional)

**URL**: Settings → Deploy keys

Allows external services to pull code:
- [ ] Add deploy key for staging server (read-only SSH key)

---

## 5. Webhooks (optional)

**URL**: Settings → Webhooks

For custom integrations:
- [ ] Slack notifications on PR/push
- [ ] Discord notifications
- [ ] Custom deployment hooks

---

## 6. Collaborators & Teams

**URL**: Settings → Collaborators

- [ ] Invite team members
- [ ] Assign appropriate roles
- [ ] Enable 2FA requirement (recommended)

---

## 7. GitHub Actions Configuration

### Create CI/CD Workflow

**File**: `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests
        run: pytest -v --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
          APP_ENV: test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: false
          tags: pilotforge:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

**Place file at**: `.github/workflows/ci-cd.yml`

---

## 8. Code Owners (optional but recommended)

**File**: `.github/CODEOWNERS`

```
# PilotForge Code Owners

# Global owner for everything
*                           @hneal055

# API routes need review
/src/api/                   @hneal055

# Database schema needs review
/prisma/                    @hneal055

# Security-critical code
/src/utils/security.py      @hneal055
/src/utils/exceptions.py    @hneal055

# Deployment configs
/Dockerfile                 @hneal055
/docker-compose*.yml        @hneal055
/k8s-deployment.yaml        @hneal055
```

---

## 9. README on GitHub

Check that `README.md` displays correctly:
- [ ] GitHub README renders properly
- [ ] Links work (relative paths)
- [ ] Badges display (if any)
- [ ] Code blocks syntax-highlighted

---

## 10. Releases Page Setup

**URL**: Code → Releases

- [ ] Click "Create a new release"
- [ ] Tag: `v1.0.0`
- [ ] Title: `PilotForge v1.0.0 - Production Ready`
- [ ] Description:
```markdown
## What's New

- ✓ All 8 development stages complete
- ✓ 100+ tests passing
- ✓ Production-ready containerization
- ✓ Kubernetes deployment manifests
- ✓ Comprehensive documentation

## Performance Metrics

- **Throughput**: 715 requests/second
- **Latency (P95)**: 0.43ms
- **Concurrency**: 100+ concurrent users tested

## Security

- SQL injection prevention
- XSS protection
- Rate limiting (100 req/min per IP)
- Input validation
- Security headers

## Deployment

See DEPLOYMENT_GUIDE.md for production setup.

```
- [ ] Attach any artifacts (if creating releases)
- [ ] This is a pre-release (uncheck for stable)

---

## 11. GitHub Pages (optional documentation site)

**URL**: Settings → Pages

To host API docs or deployment guides:
- [ ] Source: Deploy from branch `main` → `/docs` folder
- [ ] Creates site at: `https://hneal055.github.io/Tax_Incentive_Compliance_Platform/`

---

## 12. Automated Dependency Updates

**URL**: Settings → Code security & analysis

- [ ] Enable Dependabot alerts
- [ ] Enable Dependabot security updates (auto-merge on `develop`)
- [ ] Enable Dependabot version updates

---

## 13. Issue Templates (optional)

**Files** to create in `.github/`:

### `.github/ISSUE_TEMPLATE/bug_report.md`
```markdown
---
name: Bug Report
about: Report a bug
---

## Describe the bug
...

## To Reproduce
...

## Expected behavior
...

## Environment
- OS: 
- Python: 
- Docker: 
```

### `.github/ISSUE_TEMPLATE/feature_request.md`
```markdown
---
name: Feature Request
about: Suggest a feature
---

## Description
...

## Use Case
...

## Proposed Solution
...
```

---

## 14. Pull Request Template

**File**: `.github/pull_request_template.md`

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation
- [ ] Other

## Related Issues
Fixes #(issue number)

## Testing
- [ ] Unit tests added/passed
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Tests pass locally
```

---

## Completion Checklist

### Essential
- [ ] Branch protection rules for `main`
- [ ] CI/CD workflow (`.github/workflows/ci-cd.yml`)
- [ ] Secrets configured
- [ ] README verified on GitHub

### Recommended
- [ ] Code owners file
- [ ] Issue templates
- [ ] PR template
- [ ] Release notes created

### Optional
- [ ] GitHub Pages documentation
- [ ] Dependabot configuration
- [ ] Code scanning
- [ ] Custom domain/CNAME

---

## Verification

After setup, test:

```bash
# 1. Try to push directly to main (should fail)
git push origin main -f

# 2. Create feature branch and PR (should pass checks)
git checkout -b test/verification
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "test: verify branch protection"
git push origin test/verification
# Then create PR on GitHub

# 3. Check status checks pass

# 4. Merge via GitHub UI (PR)

# 5. Delete test branch
```

---

## Next Steps

1. **Run through this checklist** using GitHub web interface
2. **Test branch protection** by attempting direct push
3. **Set up GitHub Actions** with the CI/CD workflow above
4. **Create first release** from v1.0.0 tag
5. **Configure monitoring** after staging deployment

For questions, see `GIT_WORKFLOW.md` or `DEPLOYMENT_GUIDE.md`.

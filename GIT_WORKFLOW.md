# Git & Version Control Workflow

## Current Status

- **Repository**: https://github.com/hneal055/Tax_Incentive_Compliance_Platform
- **Current Version**: v1.0.0 (Production-Ready)
- **Main Branch**: Protected (code review required)
- **Commit**: `2967f05` - Production-ready platform with all 8 stages complete

---

## Branch Strategy

### `main` (Protected)
- Production-ready code only
- Requires 1+ peer review before merge
- Each commit is tagged with version number
- Deployable to production at any commit

### `develop` (Optional)
- Integration branch for feature development
- All PRs should target `develop`
- Merge to `main` only after testing/review

### Feature Branches
- `feature/redis-caching` - Implement Redis for performance
- `feature/oauth2-auth` - Add OAuth2 authentication
- `feature/monitoring` - Prometheus & Grafana setup
- Format: `feature/<name>`, `fix/<name>`, `docs/<name>`

---

## Common Git Commands

### View Status
```bash
git status                    # Current branch status
git log --oneline -10         # Last 10 commits
git branch -v                 # All branches with tracking info
git tag -l                    # List all version tags
```

### Make Changes
```bash
git checkout -b feature/xyz   # Create feature branch
git add src/                  # Stage changes
git commit -m "feat: add xyz"
git push origin feature/xyz
```

### Sync with Remote
```bash
git fetch origin              # Download remote changes
git pull origin main          # Update local main
git merge origin/main         # Merge into current branch
```

### Merge & Cleanup
```bash
git merge feature/xyz         # Merge feature into current branch
git branch -d feature/xyz     # Delete local branch
git push origin --delete feature/xyz  # Delete remote branch
```

---

## Commit Message Format

Follow conventional commits for clarity:

```
<type>(<scope>): <subject>

<body (optional)>

<footer (optional)>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `perf`: Performance improvement
- `refactor`: Code restructuring
- `test`: Test additions/changes
- `docs`: Documentation
- `ci`: CI/CD configuration

### Examples
```bash
git commit -m "feat(api): add redis caching for rules"
git commit -m "fix(database): prevent N+1 queries on productions"
git commit -m "perf(security): optimize rate limiter"
git commit -m "test: add integration tests for api endpoints"
```

---

## GitHub Branch Protection Rules

**Recommended settings for `main`:**

1. Require pull request reviews
   - Dismiss stale pull request approvals when new commits are pushed
   - Require code review from code owners (if CODEOWNERS file exists)

2. Require status checks to pass
   - Unit tests (pytest)
   - Security scanning (Trivy, Snyk)
   - Linting (Black, Flake8)
   - Build check (Docker build validation)

3. Require branches to be up to date before merging
   - Prevents merge conflicts

4. Restrict who can push to matching branches
   - Only repository admins can bypass rules

### Set up (via CLI)
```bash
# Note: Requires GitHub CLI (gh)
gh repo edit --enable-discussions --web
# Then configure via GitHub.com/Settings/Branches
```

---

## Version Tagging

Tag format: `v<MAJOR>.<MINOR>.<PATCH>`

```bash
# Current versions
git tag v1.0.0  # Production-ready (created)
git tag v1.1.0  # Next minor release (after features)
git tag v2.0.0  # Breaking changes

# Create annotated tag
git tag -a v1.1.0 -m "Add Redis caching"

# Push tags
git push origin v1.1.0
git push origin --tags
```

---

## Pre-Push Checklist

Before pushing to remote:

- [ ] Committed with clear commit message
- [ ] Tests pass locally: `docker compose exec backend pytest -v`
- [ ] No hardcoded secrets (check .env.example)
- [ ] Code follows style guide (Black formatting)
- [ ] Branch is up to date with `origin/main`
- [ ] No merge conflicts

---

## CI/CD Integration (Ready to Configure)

### GitHub Actions Workflow
When set up, will auto-run on every PR:
- Unit & integration tests
- Security scanning
- Build Docker image
- Push to registry (if tests pass)

**File location**: `.github/workflows/ci-cd.yml`

### Example workflow structure
```yaml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run pytest
        run: docker compose exec backend pytest -v
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
```

---

## Production Deployment Workflow

1. **Feature development** on `feature/xyz` branch
2. **Create pull request** to `develop`
3. **Code review** and merge to `develop`
4. **Integration testing** on staging deployment
5. **Create release PR** from `develop` to `main`
6. **Final review** and approval
7. **Tag release**: `git tag v1.1.0`
8. **Deploy to production** (manual or automated)
9. **Monitor** for 48 hours before closing release

---

## Emergency Hotfixes

For critical production issues:

```bash
# Create hotfix branch from main
git checkout -b hotfix/critical-fix main

# Make fix and commit
git add .
git commit -m "fix: critical security issue"

# Merge back to main
git checkout main
git merge hotfix/critical-fix
git tag v1.0.1

# Push immediately
git push origin main --tags

# Also merge back to develop
git checkout develop
git merge hotfix/critical-fix
git push origin develop

# Clean up
git branch -d hotfix/critical-fix
```

---

## Useful Aliases

Add to your Git config (`~/.gitconfig`):

```ini
[alias]
  st = status
  co = checkout
  br = branch -v
  ci = commit
  unstage = reset HEAD --
  last = log -1 HEAD
  visual = log --graph --oneline --decorate --all
```

Then use:
```bash
git st           # Instead of git status
git co develop   # Instead of git checkout develop
git br           # Instead of git branch -v
```

---

## Troubleshooting

### Accidentally committed to main?
```bash
git reset HEAD~1            # Undo last commit (keep changes)
git checkout -b feature/xyz # Create feature branch
git commit -m "feat: xyz"
git push origin feature/xyz
```

### Need to revert a merge?
```bash
git revert -m 1 <commit-hash>  # Creates new commit that undoes the merge
git push origin main
```

### Force pull from remote (discard local)?
```bash
git fetch origin
git reset --hard origin/main
```

### See what changed in a commit?
```bash
git show <commit-hash>
git diff <commit1> <commit2>
```

---

## Next: CI/CD Pipeline Setup

After confirming this workflow:
1. Create `.github/workflows/ci-cd.yml`
2. Configure GitHub branch protection rules
3. Set up Docker registry (Docker Hub, ECR, GCR)
4. Enable automated builds & deploys

See `DEPLOYMENT_GUIDE.md` for production deployment steps.

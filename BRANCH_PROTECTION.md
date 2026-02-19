# GitHub Branch Protection Configuration

## Quick Setup (5 minutes)

1. Go to: https://github.com/hneal055/Tax_Incentive_Compliance_Platform/settings/branches
2. Click "Add rule"
3. Copy the settings below
4. Save

---

## Branch Protection Rule for `main`

### Pattern: `main`

### Settings

#### 1. Pull Request Requirements
- [x] **Require a pull request before merging**
  - [x] **Require approvals**: 1
  - [x] **Dismiss stale pull request approvals when new commits are pushed**
  - [x] **Require code review from code owners** (after creating .github/CODEOWNERS)

**Why**: Prevents accidental direct pushes. Every change goes through review.

#### 2. Status Checks
- [x] **Require status checks to pass before merging**
- [x] **Require branches to be up to date before merging**

**Status checks required** (these come from GitHub Actions CI/CD):
- `test` - Python tests must pass
- `security-scan` - Security vulnerabilities must be acceptable
- `build` - Docker build must succeed

**Why**: Guarantees quality gate. No untested code merges.

#### 3. Merge Settings
- [ ] **Require conversation resolution before merging** (optional)
- [x] **Require signed commits** (optional but recommended)
- [ ] **Require up to date branches** (already set above)
- [x] **Allow auto-merge** (optional, uncheck if you want manual merges only)

#### 4. Dismiss Stale Reviews
- [x] **Dismiss stale pull request approvals when new commits are pushed**

**Why**: If reviewers approved but new commits are added, approval is dismissed.

#### 5. Access Restrictions
- [x] **Restrict who can push to matching branches**
  - [ ] Allow specified actors to bypass: (leave unchecked, or add admins)

**Who can push**: Only admins and repo owners

**Why**: Even maintainers can't force-push to main.

---

## Branch Protection Rule for `develop` (Optional)

### Pattern: `develop`

Use same settings as `main` but:
- [x] Allow force pushes by: Admins
- [ ] Require status checks (optional, or same as main)
- [x] Require pull request review: 1

**Why**: Integration branch for feature work. Slightly more flexible than main.

---

## Detailed Step-by-Step

### Step 1: Access Settings
```
GitHub Repository → Settings → Branches
```

### Step 2: Add Rule
```
Click "Add rule" button
```

### Step 3: Branch Name Pattern
```
Pattern: main
```

### Step 4: Pull Request Requirements
```
✓ Require a pull request before merging
✓ Require approvals: 1
✓ Dismiss stale pull request approvals
✓ Require code review from code owners
```

### Step 5: Status Checks
```
✓ Require status checks to pass before merging
✓ Require branches to be up to date before merging

Required status checks:
- test
- security-scan
- build
```

### Step 6: Merge Settings
```
✓ Require signed commits (optional)
✓ Allow auto-merge (optional)
```

### Step 7: Dismiss Stale Reviews
```
✓ Dismiss stale pull request approvals when new commits are pushed
```

### Step 8: Save
```
Click "Create" button at bottom
```

---

## Verification

### Test Branch Protection Works

```bash
# 1. Attempt direct push (should fail)
git push origin main -f
# Output: ERROR - remote: Bypassed rule violations

# 2. Create feature branch & PR (should pass)
git checkout -b test/verify-protection
echo "test" > TEST.md
git add TEST.md
git commit -m "test: verify branch protection"
git push origin test/verify-protection
# Then create PR on GitHub.com

# 3. Check status checks run
# Go to GitHub → PR → See green checkmarks for tests, build, security

# 4. Verify merge requires approval
# Without approval: Merge button disabled (grayed out)
# Add approval: Merge button enabled

# 5. Clean up
git checkout main
git branch -d test/verify-protection
git push origin --delete test/verify-protection
```

---

## Troubleshooting

### Status Checks Not Showing?

This is normal if GitHub Actions workflow hasn't run yet. 

**Solution**:
1. Create a feature branch
2. Make a change
3. Push and create PR
4. Workflow will run automatically
5. After first successful run, checks appear as "required"

### Can't see status checks to select?

The checks don't appear until the workflow runs successfully at least once.

**Solution**:
1. Commit and push the `.github/workflows/ci-cd.yml` file
2. Create a PR
3. Let workflow run once
4. Then go back to branch protection settings
5. Status checks will now be available to select

### Force push blocked but I need to rebase?

You have two options:

**Option 1: Use GitHub "Update branch" button**
- Go to PR on GitHub
- Click "Update branch" (automatically rebases)

**Option 2: Create new PR**
- Create new branch from latest main
- Cherry-pick or reapply changes
- Create new PR

### PR showing "Waiting for status checks"?

This is normal. GitHub Actions runs automatically. It takes 2-5 minutes typically.

**What's running**:
- Unit tests (pytest)
- Security scanning (Trivy)
- Docker build
- Code quality checks

---

## Best Practices

### ✅ DO:
- Create descriptive PRs
- Request review before merging
- Wait for all checks to pass
- Keep commits clean and atomic
- Squash if too many tiny commits

### ❌ DON'T:
- Try to bypass branch protection
- Merge without approval
- Force-push to main
- Ignore failed tests
- Leave conversations unresolved

---

## Bypassing Branch Protection (Emergency Only)

**Only repository admins can do this.**

If there's a critical production issue:

1. Go to branch protection rule
2. Click "Edit"
3. Under "Restrict who can push"
4. Add yourself as admin
5. Click "Save"
6. Now you can force-push (don't make a habit!)

**After emergency fix**:
1. Revert the setting
2. Follow normal PR process for next time

---

## Additional Configuration

### Recommended: Add CODEOWNERS

After creating `.github/CODEOWNERS`, the branch protection rule will automatically enforce code owner reviews.

**File**: `.github/CODEOWNERS`
```
* @hneal055
/src/api/ @hneal055
/src/utils/security.py @hneal055
```

Then code owners are automatically requested on PRs.

---

## Monitoring Compliance

### View Protected Branches
```
Settings → Branches → Shows all rules
```

### View Pull Request Status
```
Pull Requests → Click PR → See status checks
```

### View Enforcement Stats
```
Settings → Branches → (Each rule shows violations blocked)
```

---

## Disaster Recovery

If branch protection is accidentally broken:

```bash
# Reset to recommended settings
# Go back to this doc and re-apply all checkboxes

# Contact GitHub support if really broken:
# https://support.github.com/contact
```

---

## Summary Table

| Setting | Enabled? | Reason |
|---------|----------|--------|
| Require PR | ✅ Yes | All changes reviewed |
| Require 1 approval | ✅ Yes | Peer review mandate |
| Dismiss stale approvals | ✅ Yes | Prevent old approvals |
| Require code owner review | ✅ Yes | Security/critical review |
| Require status checks | ✅ Yes | Quality gate |
| Require up-to-date | ✅ Yes | No merge conflicts |
| Require signed commits | ⏳ Optional | Security enhancement |
| Allow auto-merge | ⏳ Optional | Convenience |
| Restrict push access | ✅ Yes | No admins force-push |

---

## Questions?

See:
- `GITHUB_SETUP.md` - Overall GitHub config
- `GIT_WORKFLOW.md` - Git workflow guide
- `CONTRIBUTING.md` - Contribution guidelines

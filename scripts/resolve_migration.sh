#!/usr/bin/env bash
# =============================================================================
# resolve_migration.sh
# =============================================================================
# Resolves the failed Prisma migration 20260411000002_phase0_stacking_engine
# and re-applies all pending migrations to bring the database schema in sync.
#
# BACKGROUND
# ----------
# Migration 20260411000002_phase0_stacking_engine started on 2026-04-11 at
# 12:35:21 UTC but never completed due to a Prisma schema validation error
# (P1012 — duplicate subJurisdictions field). Prisma recorded the migration
# as "started" in the _prisma_migrations table, which causes every subsequent
# `prisma migrate deploy` to abort with P3009:
#
#   "migrate found failed migrations in the target database,
#    new migrations will not be applied"
#
# Additionally, the jurisdictions table is missing the `currency` and
# `treatyPartners` columns that the current schema expects, because the
# migration that was supposed to add them never completed.
#
# WHAT THIS SCRIPT DOES
# ---------------------
# 1. Validates that DATABASE_URL is set and the database is reachable.
# 2. Marks the failed migration as rolled-back via `prisma migrate resolve
#    --rolled-back`, clearing the P3009 blocker.
# 3. Runs `prisma migrate deploy` to apply all pending migrations with the
#    now-valid schema (requires PR #85 to be merged and deployed first).
# 4. Prints a final status report showing the current migration state.
#
# PREREQUISITES
# -------------
# • PR #85 must be merged and the updated schema deployed (fixes the P1012
#   duplicate subJurisdictions field that caused the original failure).
# • DATABASE_URL environment variable must be set and point to the target
#   PostgreSQL database (pilotforge-db).
# • Python and the Prisma CLI must be available in the current environment
#   (`python -m prisma` must work).
# • The script must be run from the repository root so that the prisma/
#   directory is on the expected path.
#
# USAGE
# -----
# Manual (one-off recovery):
#   export DATABASE_URL="postgresql://user:pass@host:5432/pilotforge"
#   bash scripts/resolve_migration.sh
#
# CI/CD (Railway deploy hook or GitHub Actions step):
#   - name: Resolve failed migration
#     run: bash scripts/resolve_migration.sh
#     env:
#       DATABASE_URL: ${{ secrets.DATABASE_URL }}
#
# DRY RUN (status check only, no changes):
#   DRY_RUN=1 bash scripts/resolve_migration.sh
#
# EXIT CODES
# ----------
#   0  All steps completed successfully.
#   1  Pre-flight check failed (missing DATABASE_URL, unreachable DB, etc.).
#   2  `prisma migrate resolve` failed.
#   3  `prisma migrate deploy` failed.
# =============================================================================

set -euo pipefail

# ── Colour helpers ────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; }
header()  { echo -e "\n${BOLD}${CYAN}=== $* ===${RESET}"; }

# ── Configuration ─────────────────────────────────────────────────────────────
FAILED_MIGRATION="20260411000002_phase0_stacking_engine"
DRY_RUN="${DRY_RUN:-0}"

# ── Banner ────────────────────────────────────────────────────────────────────
echo -e "${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         SceneIQ — Migration Resolution Script             ║"
echo "║         Target: ${FAILED_MIGRATION}  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

if [[ "${DRY_RUN}" == "1" ]]; then
    warn "DRY RUN mode — no changes will be made to the database."
fi

# =============================================================================
# STEP 1: Pre-flight checks
# =============================================================================
header "Step 1: Pre-flight checks"

# 1a. DATABASE_URL must be set
if [[ -z "${DATABASE_URL:-}" ]]; then
    error "DATABASE_URL is not set."
    error "Export it before running this script:"
    error "  export DATABASE_URL=\"postgresql://user:pass@host:5432/pilotforge\""
    exit 1
fi
success "DATABASE_URL is set."

# 1b. Mask the password in log output
SAFE_URL=$(echo "${DATABASE_URL}" | sed 's|://[^:]*:[^@]*@|://***:***@|')
info "Target database: ${SAFE_URL}"

# 1c. Confirm we are in the repository root (prisma/ must exist)
if [[ ! -d "prisma" ]]; then
    error "prisma/ directory not found."
    error "Run this script from the repository root:"
    error "  bash scripts/resolve_migration.sh"
    exit 1
fi
success "Repository root confirmed (prisma/ directory found)."

# 1d. Confirm Prisma CLI is available
if ! python -m prisma --version &>/dev/null; then
    error "Prisma CLI not found. Install it with:"
    error "  pip install prisma"
    exit 1
fi
PRISMA_VERSION=$(python -m prisma --version 2>&1 | head -1)
success "Prisma CLI available: ${PRISMA_VERSION}"

# 1e. Verify database connectivity using Prisma's own db execute
info "Testing database connectivity..."
if ! python -m prisma db execute --stdin --url "${DATABASE_URL}" \
        <<< "SELECT 1;" &>/dev/null; then
    error "Cannot connect to the database at: ${SAFE_URL}"
    error "Check that the database is running and DATABASE_URL is correct."
    exit 1
fi
success "Database connection successful."

# 1f. Check current state of the failed migration in _prisma_migrations
info "Checking migration table for failed record..."
MIGRATION_STATUS=$(python -m prisma db execute --stdin --url "${DATABASE_URL}" \
    <<< "SELECT migration_name, started_at, finished_at, rolled_back_at, logs
         FROM _prisma_migrations
         WHERE migration_name = '${FAILED_MIGRATION}';" 2>/dev/null || echo "TABLE_MISSING")

if [[ "${MIGRATION_STATUS}" == "TABLE_MISSING" ]]; then
    warn "_prisma_migrations table not found — the database may be completely fresh."
    warn "Running 'prisma migrate deploy' directly (no resolve step needed)."
    NEEDS_RESOLVE=0
else
    # Check if the migration is actually in a failed state
    FAILED_ROW=$(python -m prisma db execute --stdin --url "${DATABASE_URL}" \
        <<< "SELECT COUNT(*) FROM _prisma_migrations
             WHERE migration_name = '${FAILED_MIGRATION}'
               AND finished_at IS NULL
               AND rolled_back_at IS NULL;" 2>/dev/null || echo "0")

    if echo "${FAILED_ROW}" | grep -q "^1$\| 1$\|\"1\""; then
        warn "Found failed migration record: ${FAILED_MIGRATION}"
        warn "  started_at:      set"
        warn "  finished_at:     NULL  ← migration never completed"
        warn "  rolled_back_at:  NULL  ← not yet resolved"
        NEEDS_RESOLVE=1
    else
        info "Migration ${FAILED_MIGRATION} is not in a failed state."
        info "It may already be resolved or not yet recorded."
        NEEDS_RESOLVE=0
    fi
fi

# =============================================================================
# STEP 2: Resolve the failed migration as rolled-back
# =============================================================================
header "Step 2: Resolve failed migration as rolled-back"

if [[ "${NEEDS_RESOLVE}" == "1" ]]; then
    info "Marking '${FAILED_MIGRATION}' as rolled-back..."
    info "This tells Prisma the migration never completed and clears the P3009 blocker."

    if [[ "${DRY_RUN}" == "1" ]]; then
        warn "[DRY RUN] Would run: python -m prisma migrate resolve --rolled-back '${FAILED_MIGRATION}'"
    else
        if python -m prisma migrate resolve \
                --rolled-back "${FAILED_MIGRATION}"; then
            success "Migration marked as rolled-back successfully."
        else
            error "Failed to resolve migration '${FAILED_MIGRATION}'."
            error "Possible causes:"
            error "  • The migration name is incorrect (check _prisma_migrations table)."
            error "  • DATABASE_URL does not have sufficient privileges."
            error "  • The Prisma schema still has validation errors (ensure PR #85 is merged)."
            exit 2
        fi
    fi
else
    info "No resolve step needed — skipping."
fi

# =============================================================================
# STEP 3: Apply all pending migrations
# =============================================================================
header "Step 3: Apply pending migrations (prisma migrate deploy)"

info "Running 'prisma migrate deploy' to apply all pending migrations..."
info "This is safe to run multiple times — already-applied migrations are skipped."

if [[ "${DRY_RUN}" == "1" ]]; then
    warn "[DRY RUN] Would run: python -m prisma migrate deploy"
else
    if python -m prisma migrate deploy; then
        success "All pending migrations applied successfully."
    else
        error "'prisma migrate deploy' failed."
        error "Possible causes:"
        error "  • The Prisma schema still has validation errors — confirm PR #85 is merged"
        error "    and the updated schema.prisma is present in this deployment."
        error "  • Another failed migration exists — check 'prisma migrate status'."
        error "  • The database user lacks DDL privileges (CREATE TABLE, ALTER TABLE, etc.)."
        error "  • A migration SQL statement failed — check the output above for details."
        exit 3
    fi
fi

# =============================================================================
# STEP 4: Status report
# =============================================================================
header "Step 4: Migration status report"

info "Current migration state:"
if [[ "${DRY_RUN}" == "1" ]]; then
    warn "[DRY RUN] Would run: python -m prisma migrate status"
else
    python -m prisma migrate status || true
fi

# Verify the jurisdictions.currency column now exists (key indicator of success)
info "Verifying jurisdictions.currency column exists..."
if [[ "${DRY_RUN}" != "1" ]]; then
    CURRENCY_CHECK=$(python -m prisma db execute --stdin --url "${DATABASE_URL}" \
        <<< "SELECT COUNT(*) FROM information_schema.columns
             WHERE table_schema = 'public'
               AND table_name   = 'jurisdictions'
               AND column_name  = 'currency';" 2>/dev/null || echo "0")

    if echo "${CURRENCY_CHECK}" | grep -q "^1$\| 1$\|\"1\""; then
        success "jurisdictions.currency column is present. ✓"
    else
        warn "jurisdictions.currency column was NOT found."
        warn "The migration may not have added it yet, or it may be in a later migration."
        warn "Run 'prisma migrate status' to check for remaining pending migrations."
    fi
fi

# =============================================================================
# Done
# =============================================================================
echo ""
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${GREEN}║                  Resolution complete!                        ║${RESET}"
echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════════════════╝${RESET}"
echo ""

if [[ "${DRY_RUN}" == "1" ]]; then
    warn "This was a DRY RUN. Re-run without DRY_RUN=1 to apply changes."
else
    success "The database schema is now in sync with the application."
    info "Next steps:"
    info "  1. Restart the application service to pick up the updated Prisma client."
    info "  2. Run scripts/phase0_verify.sql against the database to confirm"
    info "     the Phase 0 tables (sub_jurisdictions, production_scenarios,"
    info "     scenario_optimization_results) are correctly structured."
    info "  3. Monitor application logs for any remaining schema-related errors."
fi

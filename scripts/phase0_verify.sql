-- =====================================================
-- Phase 0: Verification Script
-- Project: Tax Incentive Compliance Platform
-- Date: 2026-04-11
-- Run this after phase0_migration.sql to confirm the
-- schema is correctly deployed.
-- =====================================================

-- ─────────────────────────────────────────────────────
-- 1. Table existence
-- ─────────────────────────────────────────────────────
SELECT
    tablename,
    CASE WHEN tablename IS NOT NULL THEN 'EXISTS' ELSE 'MISSING' END AS status
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
      'sub_jurisdictions',
      'production_scenarios',
      'scenario_optimization_results'
  )
ORDER BY tablename;

-- Expected: 3 rows, all status = 'EXISTS'


-- ─────────────────────────────────────────────────────
-- 2. Column inventory with data types
-- ─────────────────────────────────────────────────────
SELECT
    table_name,
    column_name,
    data_type,
    column_default,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN (
      'sub_jurisdictions',
      'production_scenarios',
      'scenario_optimization_results'
  )
ORDER BY table_name, ordinal_position;


-- ─────────────────────────────────────────────────────
-- 3. Foreign key constraints
-- ─────────────────────────────────────────────────────
SELECT
    tc.table_name         AS source_table,
    kcu.column_name       AS source_column,
    ccu.table_name        AS target_table,
    ccu.column_name       AS target_column,
    tc.constraint_name
FROM information_schema.table_constraints        AS tc
JOIN information_schema.key_column_usage         AS kcu
     ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema    = kcu.table_schema
JOIN information_schema.constraint_column_usage  AS ccu
     ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema    = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_name IN (
      'sub_jurisdictions',
      'production_scenarios',
      'scenario_optimization_results'
  )
ORDER BY tc.table_name;

-- Expected FKs:
--   sub_jurisdictions.parent_jurisdiction_id → jurisdictions.id
--   production_scenarios.production_id       → productions.id
--   scenario_optimization_results.scenario_id → production_scenarios.id


-- ─────────────────────────────────────────────────────
-- 4. Indexes
-- ─────────────────────────────────────────────────────
SELECT
    indexname,
    tablename,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN (
      'sub_jurisdictions',
      'production_scenarios',
      'scenario_optimization_results'
  )
ORDER BY tablename, indexname;

-- Expected indexes:
--   idx_sub_jurisdictions_parent_jurisdiction  (sub_jurisdictions)
--   idx_sub_jurisdictions_active               (sub_jurisdictions, partial WHERE is_active)
--   idx_scenarios_production                   (production_scenarios)


-- ─────────────────────────────────────────────────────
-- 5. UNIQUE constraints
-- ─────────────────────────────────────────────────────
SELECT
    tc.table_name,
    tc.constraint_name,
    kcu.column_name
FROM information_schema.table_constraints       AS tc
JOIN information_schema.key_column_usage        AS kcu
     ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema    = kcu.table_schema
WHERE tc.constraint_type = 'UNIQUE'
  AND tc.table_name IN (
      'scenario_optimization_results'
  )
ORDER BY tc.table_name, tc.constraint_name;

-- Expected: scenario_optimization_results_unique on scenario_id


-- ─────────────────────────────────────────────────────
-- 6. CHECK constraints
-- ─────────────────────────────────────────────────────
SELECT
    conname   AS constraint_name,
    conrelid::regclass AS table_name,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE contype = 'c'
  AND conrelid::regclass::text = 'sub_jurisdictions'
ORDER BY conname;

-- Expected:
--   sub_jurisdictions_has_value        (rate_percent IS NOT NULL OR fixed_amount IS NOT NULL)
--   sub_jurisdictions_incentive_type_check (IN 'credit','rebate','fee_waiver','in_kind')
--   sub_jurisdictions_type_check       (IN 'county','city','region','special_district')


-- ─────────────────────────────────────────────────────
-- 7. JSONB column default probe
-- ─────────────────────────────────────────────────────
-- Insert a minimal row and confirm JSONB defaults work.
-- Rolls back automatically — safe to run on production.
BEGIN;

INSERT INTO sub_jurisdictions (
    name, type, parent_jurisdiction_id,
    incentive_type, rate_percent, effective_date
)
SELECT
    'Test County',
    'county',
    id,           -- borrow the first jurisdiction as parent
    'credit',
    5.00,
    CURRENT_DATE
FROM jurisdictions
LIMIT 1;

SELECT
    name,
    stacking_rules,
    pg_typeof(stacking_rules) AS stacking_rules_type,
    is_active,
    created_at
FROM sub_jurisdictions
WHERE name = 'Test County';

ROLLBACK;

-- Expected: one row, stacking_rules = '{}', type = jsonb, is_active = true


-- ─────────────────────────────────────────────────────
-- 8. updated_at trigger probe
-- ─────────────────────────────────────────────────────
DO $$
DECLARE
    v_trigger_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_trigger_count
    FROM pg_trigger
    WHERE tgname IN (
        'trg_sub_jurisdictions_updated_at',
        'trg_production_scenarios_updated_at'
    );

    IF v_trigger_count = 2 THEN
        RAISE NOTICE 'PASS: Both updated_at triggers are installed.';
    ELSE
        RAISE WARNING 'FAIL: Expected 2 updated_at triggers, found %.', v_trigger_count;
    END IF;
END$$;


-- ─────────────────────────────────────────────────────
-- 9. No-break check — existing tables unaffected
-- ─────────────────────────────────────────────────────
SELECT
    COUNT(*) AS jurisdiction_count
FROM jurisdictions;

SELECT
    COUNT(*) AS incentive_rule_count
FROM incentive_rules;

SELECT
    COUNT(*) AS production_count
FROM productions;

-- Expected: same row counts as before the migration ran.
-- A count of 0 for any table may indicate the migration
-- inadvertently dropped or truncated data.

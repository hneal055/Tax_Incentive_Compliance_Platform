-- =====================================================
-- Phase 0: Sub-Jurisdiction Layer Migration
-- Project: Tax Incentive Compliance Platform
-- Date: 2026-04-11
-- Description: Adds sub_jurisdictions, production_scenarios,
--              and scenario_optimization_results tables for
--              incentive stacking and what-if scenario analysis.
--
-- ADAPTATION NOTES (vs. original spec):
--   • This project uses TEXT UUIDs for all PKs (not SERIAL INTEGER).
--     gen_random_uuid() is used in place of SERIAL.
--   • The existing state-level table is "jurisdictions" (not "states").
--     parent_jurisdiction_id references jurisdictions(id) accordingly.
--   • productions(id) is TEXT UUID — FK types match.
--   • pgcrypto extension is required for gen_random_uuid() on PG < 14.
--     On PG 14+ use gen_random_uuid() natively (no extension needed).
-- =====================================================

BEGIN;

-- Ensure UUID generation is available (safe no-op if already installed)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- TABLE 1: sub_jurisdictions
-- Stores county, city, region, and special-district level
-- incentives that stack on top of the base state credit.
-- =====================================================
CREATE TABLE IF NOT EXISTS sub_jurisdictions (
    -- Primary key (UUID, consistent with existing schema)
    id                              TEXT            NOT NULL DEFAULT gen_random_uuid(),

    -- Identity
    name                            TEXT            NOT NULL,       -- e.g. "Los Angeles County"
    type                            TEXT            NOT NULL,       -- 'county' | 'city' | 'region' | 'special_district'

    -- Link to existing state-level jurisdiction (replaces spec's states(id) FK)
    parent_jurisdiction_id          TEXT            NOT NULL,       -- FK → jurisdictions(id)

    -- Incentive economics
    incentive_type                  TEXT            NOT NULL,       -- 'credit' | 'rebate' | 'fee_waiver' | 'in_kind'
    rate_percent                    NUMERIC(5,2),                   -- e.g. 10.00 for 10% bonus
    fixed_amount                    NUMERIC(12,2),                  -- Flat dollar amount, e.g. 50000.00
    cap_per_production              NUMERIC(12,2),                  -- Max incentive per single production
    annual_cap                      NUMERIC(12,2),                  -- Total annual program budget
    min_spend_required              NUMERIC(12,2),                  -- Minimum qualifying spend to unlock incentive

    -- Stacking rules (JSONB) — see structure note below
    -- Supported keys: cannot_stack_with[], requires[], stacking_order,
    --                 mutually_exclusive_groups[], notes
    stacking_rules                  JSONB           NOT NULL DEFAULT '{}',

    -- Eligible expense categories — e.g. ["labor", "lodging", "rentals"]
    eligible_expenditure_categories JSONB,

    -- Workforce requirements
    local_hire_percentage_required  NUMERIC(5,2),                   -- Minimum local crew % to qualify

    -- Temporal validity
    effective_date                  DATE            NOT NULL,       -- When incentive becomes available
    expiration_date                 DATE,                           -- NULL = no expiration

    -- Lifecycle / audit
    is_active                       BOOLEAN         NOT NULL DEFAULT TRUE,
    source_url                      TEXT,                           -- Official government source URL
    last_verified                   TIMESTAMPTZ,                    -- Last time data was confirmed accurate
    notes                           TEXT,                           -- Internal notes

    -- Timestamps
    created_at                      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT sub_jurisdictions_pkey PRIMARY KEY (id),

    -- type must be one of the four allowed values
    CONSTRAINT sub_jurisdictions_type_check
        CHECK (type IN ('county', 'city', 'region', 'special_district')),

    -- incentive_type must be one of the four allowed values
    CONSTRAINT sub_jurisdictions_incentive_type_check
        CHECK (incentive_type IN ('credit', 'rebate', 'fee_waiver', 'in_kind')),

    -- At least one of rate_percent or fixed_amount must be provided
    CONSTRAINT sub_jurisdictions_has_value
        CHECK (rate_percent IS NOT NULL OR fixed_amount IS NOT NULL)
);

-- FK added separately for idempotency safety
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'sub_jurisdictions_parent_jurisdiction_id_fkey'
    ) THEN
        ALTER TABLE sub_jurisdictions
            ADD CONSTRAINT sub_jurisdictions_parent_jurisdiction_id_fkey
            FOREIGN KEY (parent_jurisdiction_id)
            REFERENCES jurisdictions(id)
            ON UPDATE CASCADE ON DELETE RESTRICT;
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS idx_sub_jurisdictions_parent_jurisdiction
    ON sub_jurisdictions (parent_jurisdiction_id);

CREATE INDEX IF NOT EXISTS idx_sub_jurisdictions_active
    ON sub_jurisdictions (is_active)
    WHERE is_active = TRUE;


-- =====================================================
-- TABLE 2: production_scenarios
-- Stores "what-if" input parameters for a single production.
-- Multiple scenarios per production are supported so producers
-- can compare baseline vs. optimized configurations.
-- =====================================================
CREATE TABLE IF NOT EXISTS production_scenarios (
    id                      TEXT        NOT NULL DEFAULT gen_random_uuid(),

    -- Link to existing production
    production_id           TEXT        NOT NULL,                   -- FK → productions(id)

    -- Scenario identity
    name                    TEXT        NOT NULL,                   -- e.g. "Baseline NYC", "Optimized Albany"

    -- Budget inputs
    total_budget            NUMERIC(12,2),                          -- Full production budget
    qualified_spend         NUMERIC(12,2),                          -- Portion eligible for incentives

    -- Spend breakdown by category — e.g. {"labor": 5000000, "rentals": 2000000}
    spend_by_category       JSONB,

    -- Shooting schedule
    shooting_days           INTEGER,                                -- Total shooting days across all locations

    -- Per-jurisdiction day allocation
    -- e.g. [{"jurisdiction_id": "uuid-ny", "days": 20}, {"sub_jurisdiction_id": "uuid-nyc", "days": 10}]
    days_by_jurisdiction    JSONB,

    -- Post-production
    post_location           TEXT,                                   -- City/state where post occurs

    -- Workforce
    local_hire_percent      NUMERIC(5,2),                           -- Overall local hire %
    -- Per-jurisdiction hire breakdown — e.g. [{"jurisdiction_id": "...", "percent": 85.0}]
    hire_by_jurisdiction    JSONB,

    -- Timestamps
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT production_scenarios_pkey PRIMARY KEY (id)
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'production_scenarios_production_id_fkey'
    ) THEN
        ALTER TABLE production_scenarios
            ADD CONSTRAINT production_scenarios_production_id_fkey
            FOREIGN KEY (production_id)
            REFERENCES productions(id)
            ON UPDATE CASCADE ON DELETE CASCADE;
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS idx_scenarios_production
    ON production_scenarios (production_id);


-- =====================================================
-- TABLE 3: scenario_optimization_results
-- Caches the stacking-engine output for a given scenario.
-- One result row per scenario (UNIQUE on scenario_id).
-- Set expires_at to force recomputation when data changes.
-- =====================================================
CREATE TABLE IF NOT EXISTS scenario_optimization_results (
    id                      TEXT        NOT NULL DEFAULT gen_random_uuid(),

    -- One result per scenario
    scenario_id             TEXT        NOT NULL,                   -- FK → production_scenarios(id)

    -- Optimizer output
    -- e.g. [{"jurisdiction_id": "...", "name": "NY Base", "incentive_value": 4500000, "type": "credit"}]
    recommended_stack       JSONB       NOT NULL DEFAULT '[]',

    -- Aggregate financials
    total_incentive_value   NUMERIC(12,2),                          -- Net cash or credit equivalent
    effective_rate          NUMERIC(5,2),                           -- % of qualified_spend

    -- Cash-flow narrative — e.g. "refundable within 90 days of audit"
    cash_flow_estimate      TEXT,

    -- Non-fatal issues the optimizer detected
    -- e.g. ["Annual cap 82% exhausted — apply early", "Local hire threshold marginal"]
    warnings                JSONB,

    -- Timestamps / staleness
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at              TIMESTAMPTZ,                            -- NULL = never auto-expire

    CONSTRAINT scenario_optimization_results_pkey    PRIMARY KEY (id),
    CONSTRAINT scenario_optimization_results_unique  UNIQUE (scenario_id)
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'scenario_optimization_results_scenario_id_fkey'
    ) THEN
        ALTER TABLE scenario_optimization_results
            ADD CONSTRAINT scenario_optimization_results_scenario_id_fkey
            FOREIGN KEY (scenario_id)
            REFERENCES production_scenarios(id)
            ON UPDATE CASCADE ON DELETE CASCADE;
    END IF;
END$$;

-- =====================================================
-- updated_at trigger helper
-- Reusable function that sets updated_at = NOW() on every UPDATE.
-- =====================================================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_sub_jurisdictions_updated_at') THEN
        CREATE TRIGGER trg_sub_jurisdictions_updated_at
            BEFORE UPDATE ON sub_jurisdictions
            FOR EACH ROW EXECUTE FUNCTION set_updated_at();
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_production_scenarios_updated_at') THEN
        CREATE TRIGGER trg_production_scenarios_updated_at
            BEFORE UPDATE ON production_scenarios
            FOR EACH ROW EXECUTE FUNCTION set_updated_at();
    END IF;
END$$;

COMMIT;

-- =====================================================
-- Quick smoke-test (uncomment to run after migration)
-- =====================================================
-- SELECT * FROM sub_jurisdictions LIMIT 0;
-- SELECT * FROM production_scenarios LIMIT 0;
-- SELECT * FROM scenario_optimization_results LIMIT 0;

-- Validation query — active sub-jurisdictions for New York:
-- SELECT
--     j.name  AS state_name,
--     sj.name AS sub_name,
--     sj.type,
--     sj.rate_percent,
--     sj.stacking_rules
-- FROM jurisdictions j
-- LEFT JOIN sub_jurisdictions sj
--        ON sj.parent_jurisdiction_id = j.id
--       AND sj.is_active = TRUE
-- WHERE j.code = 'NY'
-- ORDER BY sj.type, sj.name;

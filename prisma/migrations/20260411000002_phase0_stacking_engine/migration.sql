-- Phase 0: Sub-Jurisdiction Layer — Stacking Engine Tables
-- Adds sub_jurisdictions, production_scenarios, and
-- scenario_optimization_results without touching existing tables.

-- Ensure UUID generation is available
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── sub_jurisdictions ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS "sub_jurisdictions" (
    "id"                              TEXT            NOT NULL DEFAULT gen_random_uuid(),
    "name"                            TEXT            NOT NULL,
    "type"                            TEXT            NOT NULL,
    "parentJurisdictionId"            TEXT            NOT NULL,
    "incentiveType"                   TEXT            NOT NULL,
    "ratePercent"                     DECIMAL(5,2),
    "fixedAmount"                     DECIMAL(12,2),
    "capPerProduction"                DECIMAL(12,2),
    "annualCap"                       DECIMAL(12,2),
    "minSpendRequired"                DECIMAL(12,2),
    "stackingRules"                   JSONB           NOT NULL DEFAULT '{}',
    "eligibleExpenditureCategories"   JSONB,
    "localHirePercentageRequired"     DECIMAL(5,2),
    "effectiveDate"                   DATE            NOT NULL,
    "expirationDate"                  DATE,
    "isActive"                        BOOLEAN         NOT NULL DEFAULT TRUE,
    "sourceUrl"                       TEXT,
    "lastVerified"                    TIMESTAMPTZ,
    "notes"                           TEXT,
    "createdAt"                       TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    "updatedAt"                       TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT "sub_jurisdictions_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "sub_jurisdictions_type_check"
        CHECK ("type" IN ('county','city','region','special_district')),
    CONSTRAINT "sub_jurisdictions_incentive_type_check"
        CHECK ("incentiveType" IN ('credit','rebate','fee_waiver','in_kind')),
    CONSTRAINT "sub_jurisdictions_has_value"
        CHECK ("ratePercent" IS NOT NULL OR "fixedAmount" IS NOT NULL)
);

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_name = 'sub_jurisdictions_parentJurisdictionId_fkey') THEN
    ALTER TABLE "sub_jurisdictions" ADD CONSTRAINT "sub_jurisdictions_parentJurisdictionId_fkey" FOREIGN KEY ("parentJurisdictionId") REFERENCES "jurisdictions"("id") ON UPDATE CASCADE ON DELETE RESTRICT;
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS "sub_jurisdictions_parentJurisdictionId_idx"
    ON "sub_jurisdictions" ("parentJurisdictionId");

-- ── production_scenarios ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS "production_scenarios" (
    "id"                TEXT        NOT NULL DEFAULT gen_random_uuid(),
    "productionId"      TEXT        NOT NULL,
    "name"              TEXT        NOT NULL,
    "totalBudget"       DECIMAL(12,2),
    "qualifiedSpend"    DECIMAL(12,2),
    "spendByCategory"   JSONB,
    "shootingDays"      INTEGER,
    "daysByJurisdiction" JSONB,
    "postLocation"      TEXT,
    "localHirePercent"  DECIMAL(5,2),
    "hireByJurisdiction" JSONB,
    "createdAt"         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updatedAt"         TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT "production_scenarios_pkey" PRIMARY KEY ("id")
);

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_name = 'production_scenarios_productionId_fkey') THEN
    ALTER TABLE "production_scenarios" ADD CONSTRAINT "production_scenarios_productionId_fkey" FOREIGN KEY ("productionId") REFERENCES "productions"("id") ON UPDATE CASCADE ON DELETE CASCADE;
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS "production_scenarios_productionId_idx"
    ON "production_scenarios" ("productionId");

-- ── scenario_optimization_results ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS "scenario_optimization_results" (
    "id"                    TEXT        NOT NULL DEFAULT gen_random_uuid(),
    "scenarioId"            TEXT        NOT NULL,
    "recommendedStack"      JSONB       NOT NULL DEFAULT '[]',
    "totalIncentiveValue"   DECIMAL(12,2),
    "effectiveRate"         DECIMAL(5,2),
    "cashFlowEstimate"      TEXT,
    "warnings"              JSONB,
    "createdAt"             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "expiresAt"             TIMESTAMPTZ,

    CONSTRAINT "scenario_optimization_results_pkey"   PRIMARY KEY ("id"),
    CONSTRAINT "scenario_optimization_results_unique" UNIQUE ("scenarioId")
);

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_name = 'scenario_optimization_results_scenarioId_fkey') THEN
    ALTER TABLE "scenario_optimization_results" ADD CONSTRAINT "scenario_optimization_results_scenarioId_fkey" FOREIGN KEY ("scenarioId") REFERENCES "production_scenarios"("id") ON UPDATE CASCADE ON DELETE CASCADE;
  END IF;
END $$;

-- ── updated_at trigger ────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW."updatedAt" = NOW();
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER "trg_sub_jurisdictions_updated_at"
    BEFORE UPDATE ON "sub_jurisdictions"
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE TRIGGER "trg_production_scenarios_updated_at"
    BEFORE UPDATE ON "production_scenarios"
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

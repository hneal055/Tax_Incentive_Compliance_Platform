-- Migration: Sub-Jurisdiction Layer Integration
-- Adds parent/child hierarchy, feed monitoring columns, and three new tables.

-- ── 1. Extend jurisdictions ────────────────────────────────────────────────────
ALTER TABLE "jurisdictions"
  ADD COLUMN IF NOT EXISTS "parentId"         TEXT,
  ADD COLUMN IF NOT EXISTS "feedUrl"          TEXT,
  ADD COLUMN IF NOT EXISTS "feedLastChecked"  TIMESTAMP(3),
  ADD COLUMN IF NOT EXISTS "feedLastHash"     TEXT;

ALTER TABLE "jurisdictions"
  ADD CONSTRAINT "jurisdictions_parentId_fkey"
  FOREIGN KEY ("parentId") REFERENCES "jurisdictions"("id")
  ON UPDATE CASCADE ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS "jurisdictions_parentId_idx" ON "jurisdictions"("parentId");

-- ── 2. local_rules ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS "local_rules" (
  "id"             TEXT         NOT NULL,
  "jurisdictionId" TEXT         NOT NULL,
  "name"           TEXT         NOT NULL,
  "code"           TEXT         NOT NULL,
  "category"       TEXT         NOT NULL,
  "ruleType"       TEXT         NOT NULL,
  "amount"         DOUBLE PRECISION,
  "percentage"     DOUBLE PRECISION,
  "description"    TEXT         NOT NULL,
  "requirements"   TEXT,
  "effectiveDate"  TIMESTAMP(3) NOT NULL,
  "expirationDate" TIMESTAMP(3),
  "sourceUrl"      TEXT,
  "extractedBy"    TEXT         NOT NULL DEFAULT 'manual',
  "active"         BOOLEAN      NOT NULL DEFAULT TRUE,
  "createdAt"      TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt"      TIMESTAMP(3) NOT NULL,

  CONSTRAINT "local_rules_pkey"           PRIMARY KEY ("id"),
  CONSTRAINT "local_rules_code_key"       UNIQUE ("code"),
  CONSTRAINT "local_rules_jurisdictionId_fkey"
    FOREIGN KEY ("jurisdictionId") REFERENCES "jurisdictions"("id")
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS "local_rules_jurisdictionId_idx" ON "local_rules"("jurisdictionId");

-- ── 3. inheritance_policies ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS "inheritance_policies" (
  "id"                   TEXT         NOT NULL,
  "childJurisdictionId"  TEXT         NOT NULL,
  "parentJurisdictionId" TEXT         NOT NULL,
  "policyType"           TEXT         NOT NULL,
  "ruleCategory"         TEXT,
  "priority"             INTEGER      NOT NULL DEFAULT 0,
  "notes"                TEXT,
  "createdAt"            TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt"            TIMESTAMP(3) NOT NULL,

  CONSTRAINT "inheritance_policies_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "inheritance_policies_unique"
    UNIQUE ("childJurisdictionId", "parentJurisdictionId", "ruleCategory"),
  CONSTRAINT "inheritance_policies_child_fkey"
    FOREIGN KEY ("childJurisdictionId") REFERENCES "jurisdictions"("id")
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT "inheritance_policies_parent_fkey"
    FOREIGN KEY ("parentJurisdictionId") REFERENCES "jurisdictions"("id")
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS "inheritance_policies_child_idx"  ON "inheritance_policies"("childJurisdictionId");
CREATE INDEX IF NOT EXISTS "inheritance_policies_parent_idx" ON "inheritance_policies"("parentJurisdictionId");

-- ── 4. pending_rules ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS "pending_rules" (
  "id"             TEXT             NOT NULL,
  "jurisdictionId" TEXT             NOT NULL,
  "sourceUrl"      TEXT             NOT NULL,
  "rawContent"     TEXT             NOT NULL,
  "extractedData"  JSONB            NOT NULL,
  "confidence"     DOUBLE PRECISION,
  "status"         TEXT             NOT NULL DEFAULT 'pending',
  "reviewNotes"    TEXT,
  "reviewedBy"     TEXT,
  "reviewedAt"     TIMESTAMP(3),
  "createdAt"      TIMESTAMP(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt"      TIMESTAMP(3)     NOT NULL,

  CONSTRAINT "pending_rules_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "pending_rules_jurisdictionId_fkey"
    FOREIGN KEY ("jurisdictionId") REFERENCES "jurisdictions"("id")
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS "pending_rules_jurisdictionId_idx" ON "pending_rules"("jurisdictionId");
CREATE INDEX IF NOT EXISTS "pending_rules_status_idx"         ON "pending_rules"("status");

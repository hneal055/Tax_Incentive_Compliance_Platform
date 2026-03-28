-- CreateTable
CREATE TABLE "jurisdictions" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "code" TEXT NOT NULL,
    "country" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "description" TEXT,
    "website" TEXT,
    "contactInfo" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "jurisdictions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "incentive_rules" (
    "id" TEXT NOT NULL,
    "jurisdictionId" TEXT NOT NULL,
    "ruleName" TEXT NOT NULL,
    "ruleCode" TEXT NOT NULL,
    "incentiveType" TEXT NOT NULL,
    "percentage" DOUBLE PRECISION,
    "fixedAmount" DOUBLE PRECISION,
    "minSpend" DOUBLE PRECISION,
    "maxCredit" DOUBLE PRECISION,
    "eligibleExpenses" TEXT[],
    "excludedExpenses" TEXT[],
    "effectiveDate" TIMESTAMP(3) NOT NULL,
    "expirationDate" TIMESTAMP(3),
    "requirements" JSONB NOT NULL,
    "metadata" JSONB,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "incentive_rules_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "productions" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "productionType" TEXT NOT NULL,
    "jurisdictionId" TEXT NOT NULL,
    "budgetTotal" DOUBLE PRECISION NOT NULL,
    "budgetQualifying" DOUBLE PRECISION,
    "startDate" TIMESTAMP(3) NOT NULL,
    "endDate" TIMESTAMP(3),
    "wrapDate" TIMESTAMP(3),
    "productionCompany" TEXT NOT NULL,
    "accountant" TEXT,
    "contact" JSONB,
    "status" TEXT NOT NULL,
    "metadata" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "productions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "expenses" (
    "id" TEXT NOT NULL,
    "productionId" TEXT NOT NULL,
    "category" TEXT NOT NULL,
    "subcategory" TEXT,
    "description" TEXT NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL,
    "expenseDate" TIMESTAMP(3) NOT NULL,
    "paymentDate" TIMESTAMP(3),
    "isQualifying" BOOLEAN NOT NULL DEFAULT false,
    "qualifyingNote" TEXT,
    "vendorName" TEXT,
    "vendorLocation" TEXT,
    "receiptNumber" TEXT,
    "invoiceNumber" TEXT,
    "metadata" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "expenses_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "calculations" (
    "id" TEXT NOT NULL,
    "productionId" TEXT NOT NULL,
    "incentiveRuleId" TEXT NOT NULL,
    "qualifyingExpenses" DOUBLE PRECISION NOT NULL,
    "creditAmount" DOUBLE PRECISION NOT NULL,
    "calculationDate" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "breakdown" JSONB NOT NULL,
    "notes" TEXT,
    "approved" BOOLEAN NOT NULL DEFAULT false,
    "submittedDate" TIMESTAMP(3),
    "approvedDate" TIMESTAMP(3),
    "rejectedDate" TIMESTAMP(3),
    "rejectionNote" TEXT,
    "submittedBy" TEXT,
    "approvedBy" TEXT,
    "metadata" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "calculations_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "users" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "role" TEXT NOT NULL,
    "company" TEXT,
    "password" TEXT NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "metadata" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "audit_logs" (
    "id" TEXT NOT NULL,
    "userId" TEXT,
    "entityType" TEXT NOT NULL,
    "entityId" TEXT NOT NULL,
    "action" TEXT NOT NULL,
    "changes" JSONB NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "audit_logs_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "jurisdictions_name_key" ON "jurisdictions"("name");

-- CreateIndex
CREATE UNIQUE INDEX "jurisdictions_code_key" ON "jurisdictions"("code");

-- CreateIndex
CREATE INDEX "jurisdictions_country_type_idx" ON "jurisdictions"("country", "type");

-- CreateIndex
CREATE INDEX "jurisdictions_active_idx" ON "jurisdictions"("active");

-- CreateIndex
CREATE INDEX "incentive_rules_jurisdictionId_idx" ON "incentive_rules"("jurisdictionId");

-- CreateIndex
CREATE INDEX "incentive_rules_incentiveType_idx" ON "incentive_rules"("incentiveType");

-- CreateIndex
CREATE INDEX "incentive_rules_active_idx" ON "incentive_rules"("active");

-- CreateIndex
CREATE INDEX "productions_jurisdictionId_idx" ON "productions"("jurisdictionId");

-- CreateIndex
CREATE INDEX "productions_status_idx" ON "productions"("status");

-- CreateIndex
CREATE INDEX "productions_productionType_idx" ON "productions"("productionType");

-- CreateIndex
CREATE INDEX "expenses_productionId_idx" ON "expenses"("productionId");

-- CreateIndex
CREATE INDEX "expenses_category_idx" ON "expenses"("category");

-- CreateIndex
CREATE INDEX "expenses_isQualifying_idx" ON "expenses"("isQualifying");

-- CreateIndex
CREATE INDEX "calculations_productionId_idx" ON "calculations"("productionId");

-- CreateIndex
CREATE INDEX "calculations_incentiveRuleId_idx" ON "calculations"("incentiveRuleId");

-- CreateIndex
CREATE INDEX "calculations_approved_idx" ON "calculations"("approved");

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE INDEX "users_email_idx" ON "users"("email");

-- CreateIndex
CREATE INDEX "users_role_idx" ON "users"("role");

-- CreateIndex
CREATE INDEX "audit_logs_entityType_entityId_idx" ON "audit_logs"("entityType", "entityId");

-- CreateIndex
CREATE INDEX "audit_logs_userId_idx" ON "audit_logs"("userId");

-- AddForeignKey
ALTER TABLE "incentive_rules" ADD CONSTRAINT "incentive_rules_jurisdictionId_fkey" FOREIGN KEY ("jurisdictionId") REFERENCES "jurisdictions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "productions" ADD CONSTRAINT "productions_jurisdictionId_fkey" FOREIGN KEY ("jurisdictionId") REFERENCES "jurisdictions"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "expenses" ADD CONSTRAINT "expenses_productionId_fkey" FOREIGN KEY ("productionId") REFERENCES "productions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "calculations" ADD CONSTRAINT "calculations_productionId_fkey" FOREIGN KEY ("productionId") REFERENCES "productions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "calculations" ADD CONSTRAINT "calculations_incentiveRuleId_fkey" FOREIGN KEY ("incentiveRuleId") REFERENCES "incentive_rules"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

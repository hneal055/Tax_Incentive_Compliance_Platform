/*
  Warnings:

  - You are about to drop the column `metadata` on the `expenses` table. All the data in the column will be lost.
  - You are about to drop the column `metadata` on the `incentive_rules` table. All the data in the column will be lost.
  - You are about to drop the column `contactInfo` on the `jurisdictions` table. All the data in the column will be lost.
  - You are about to drop the column `accountant` on the `productions` table. All the data in the column will be lost.
  - You are about to drop the column `wrapDate` on the `productions` table. All the data in the column will be lost.
  - You are about to drop the `audit_logs` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `calculations` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `users` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[ruleCode]` on the table `incentive_rules` will be added. If there are existing duplicate values, this will fail.

*/
-- DropForeignKey
ALTER TABLE "calculations" DROP CONSTRAINT "calculations_incentiveRuleId_fkey";

-- DropForeignKey
ALTER TABLE "calculations" DROP CONSTRAINT "calculations_productionId_fkey";

-- DropIndex
DROP INDEX "expenses_category_idx";

-- DropIndex
DROP INDEX "expenses_isQualifying_idx";

-- DropIndex
DROP INDEX "incentive_rules_active_idx";

-- DropIndex
DROP INDEX "incentive_rules_incentiveType_idx";

-- DropIndex
DROP INDEX "jurisdictions_active_idx";

-- DropIndex
DROP INDEX "jurisdictions_country_type_idx";

-- DropIndex
DROP INDEX "jurisdictions_name_key";

-- DropIndex
DROP INDEX "productions_productionType_idx";

-- AlterTable
ALTER TABLE "expenses" DROP COLUMN "metadata",
ALTER COLUMN "isQualifying" SET DEFAULT true;

-- AlterTable
ALTER TABLE "incentive_rules" DROP COLUMN "metadata",
ALTER COLUMN "requirements" DROP NOT NULL,
ALTER COLUMN "requirements" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "jurisdictions" DROP COLUMN "contactInfo";

-- AlterTable
ALTER TABLE "productions" DROP COLUMN "accountant",
DROP COLUMN "wrapDate",
ALTER COLUMN "contact" SET DATA TYPE TEXT,
ALTER COLUMN "metadata" SET DATA TYPE TEXT;

-- DropTable
DROP TABLE "audit_logs";

-- DropTable
DROP TABLE "calculations";

-- DropTable
DROP TABLE "users";

-- CreateIndex
CREATE INDEX "expenses_expenseDate_idx" ON "expenses"("expenseDate");

-- CreateIndex
CREATE UNIQUE INDEX "incentive_rules_ruleCode_key" ON "incentive_rules"("ruleCode");

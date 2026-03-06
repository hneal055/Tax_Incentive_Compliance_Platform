-- AlterTable
ALTER TABLE "productions" ADD COLUMN     "preferredRuleId" TEXT;

-- CreateTable
CREATE TABLE "monitoring_sources" (
    "id" TEXT NOT NULL,
    "jurisdictionId" TEXT NOT NULL,
    "sourceType" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "checkInterval" INTEGER NOT NULL DEFAULT 3600,
    "lastCheckedAt" TIMESTAMP(3),
    "lastHash" TEXT,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "monitoring_sources_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "monitoring_events" (
    "id" TEXT NOT NULL,
    "jurisdictionId" TEXT NOT NULL,
    "sourceId" TEXT,
    "eventType" TEXT NOT NULL,
    "severity" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "summary" TEXT NOT NULL,
    "sourceUrl" TEXT,
    "detectedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "readAt" TIMESTAMP(3),
    "metadata" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "monitoring_events_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "monitoring_sources_jurisdictionId_idx" ON "monitoring_sources"("jurisdictionId");

-- CreateIndex
CREATE INDEX "monitoring_sources_active_idx" ON "monitoring_sources"("active");

-- CreateIndex
CREATE INDEX "monitoring_events_jurisdictionId_idx" ON "monitoring_events"("jurisdictionId");

-- CreateIndex
CREATE INDEX "monitoring_events_sourceId_idx" ON "monitoring_events"("sourceId");

-- CreateIndex
CREATE INDEX "monitoring_events_eventType_idx" ON "monitoring_events"("eventType");

-- CreateIndex
CREATE INDEX "monitoring_events_severity_idx" ON "monitoring_events"("severity");

-- CreateIndex
CREATE INDEX "monitoring_events_detectedAt_idx" ON "monitoring_events"("detectedAt");

-- CreateIndex
CREATE INDEX "monitoring_events_readAt_idx" ON "monitoring_events"("readAt");

-- AddForeignKey
ALTER TABLE "monitoring_sources" ADD CONSTRAINT "monitoring_sources_jurisdictionId_fkey" FOREIGN KEY ("jurisdictionId") REFERENCES "jurisdictions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "monitoring_events" ADD CONSTRAINT "monitoring_events_jurisdictionId_fkey" FOREIGN KEY ("jurisdictionId") REFERENCES "jurisdictions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "monitoring_events" ADD CONSTRAINT "monitoring_events_sourceId_fkey" FOREIGN KEY ("sourceId") REFERENCES "monitoring_sources"("id") ON DELETE SET NULL ON UPDATE CASCADE;

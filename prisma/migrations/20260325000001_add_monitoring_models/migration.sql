-- CreateTable
CREATE TABLE "monitoring_sources" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "feedUrl" TEXT,
    "sourceType" TEXT NOT NULL DEFAULT 'rss',
    "jurisdiction" TEXT,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "lastFetched" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "monitoring_sources_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "monitoring_events" (
    "id" TEXT NOT NULL,
    "sourceId" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "summary" TEXT,
    "url" TEXT,
    "contentHash" TEXT,
    "severity" TEXT NOT NULL DEFAULT 'info',
    "isRead" BOOLEAN NOT NULL DEFAULT false,
    "publishedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "monitoring_events_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "monitoring_events_sourceId_idx" ON "monitoring_events"("sourceId");

-- CreateIndex
CREATE INDEX "monitoring_events_isRead_idx" ON "monitoring_events"("isRead");

-- CreateIndex
CREATE INDEX "monitoring_events_createdAt_idx" ON "monitoring_events"("createdAt");

-- AddForeignKey
ALTER TABLE "monitoring_events" ADD CONSTRAINT "monitoring_events_sourceId_fkey" FOREIGN KEY ("sourceId") REFERENCES "monitoring_sources"("id") ON DELETE CASCADE ON UPDATE CASCADE;

#!/usr/bin/env bash
# PilotForge Startup Script for Render

echo "🎬 Starting PilotForge..."

# Generate Prisma client
echo "🔧 Generating Prisma client..."
prisma generate || python -m prisma generate || echo "⚠️  Prisma generate skipped"

# Run database migrations
echo "📊 Running database migrations..."
prisma migrate deploy || python -m prisma migrate deploy || echo "⚠️  Migrations skipped"

# Start the application
echo "🚀 Starting uvicorn..."
exec python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
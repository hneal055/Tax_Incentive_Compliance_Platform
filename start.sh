#!/usr/bin/env bash
# PilotForge Startup Script for Render
echo "🎬 Starting PilotForge..."

# Generate Prisma client
echo "🔧 Generating Prisma client..."
python -m prisma generate || echo "⚠️  Prisma generate skipped"

# Start the application
echo "🚀 Starting uvicorn..."
exec python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}

#!/bin/sh
set -e

echo "Running Prisma migrations..."
prisma migrate deploy

echo "Starting application..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000

#!/bin/bash
# Docker Quick Test Script
# Tests that all Docker services start correctly

set -e

echo "🐳 Docker Container Build and Test Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    exit 1
fi

# Check if Docker Compose is installed
if ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Build and start services
echo "📦 Building Docker images..."
docker compose build --quiet

echo "✅ Images built successfully"
echo ""

echo "🚀 Starting services..."
docker compose up -d

echo "⏳ Waiting for services to be healthy (60 seconds)..."
sleep 60

# Check service status
echo ""
echo "📊 Service Status:"
docker compose ps

# Test backend health
echo ""
echo "🏥 Testing backend health..."
HEALTH_STATUS=$(curl -s http://localhost:8000/health | grep -o '"status":"healthy"' || echo "unhealthy")

if [ "$HEALTH_STATUS" == '"status":"healthy"' ]; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker compose logs app | tail -20
    exit 1
fi

# Test frontend
echo ""
echo "🎨 Testing frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)

if [ "$FRONTEND_STATUS" == "200" ]; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend test failed (HTTP $FRONTEND_STATUS)"
    exit 1
fi

# Test API endpoint
echo ""
echo "🔌 Testing API endpoint..."
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/jurisdictions)

if [ "$API_STATUS" == "200" ]; then
    echo "✅ API is responding"
else
    echo "❌ API test failed (HTTP $API_STATUS)"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend:    http://localhost"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/docs"
echo ""
echo "🛑 To stop services: docker compose down"
echo ""

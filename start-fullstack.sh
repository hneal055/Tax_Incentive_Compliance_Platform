#!/usr/bin/env bash
# ============================================
# PilotForge Full Stack Startup Script
# Starts both Backend and Frontend
# ============================================

set -e

echo "🎬 PilotForge Full Stack Startup"
echo "======================================"

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✓ Servers stopped"
    exit 0
}

trap cleanup EXIT INT TERM

# Check if we're in the project root
if [ ! -d "frontend" ] || [ ! -f "main.py" ]; then
    echo "❌ Error: This script must be run from the project root directory"
    exit 1
fi

echo ""
echo "📋 Pre-flight Checks"
echo "======================================"

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found"
    exit 1
fi
echo "✓ Python $(python --version | cut -d' ' -f2) detected"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found - install from https://nodejs.org/"
    exit 1
fi
echo "✓ Node.js $(node --version) detected"

# Check if virtual environment exists
if [ ! -d ".venv" ] && [ ! -d "venv" ]; then
    echo "⚠️  Warning: No Python virtual environment found"
    echo "   Create one with: python -m venv .venv"
    echo "   Then activate it and install dependencies"
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo ""
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✓ Frontend dependencies installed"
fi

echo ""
echo "======================================"
echo "🚀 Starting Servers"
echo "======================================"

# Start Backend
echo ""
echo "Starting backend on http://localhost:8000..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Start backend in background
python -m uvicorn src.main:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "✓ Backend started (PID: $BACKEND_PID)"
echo "  Logs: tail -f backend.log"

# Wait for backend to be ready
echo "  Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️  Backend is taking longer than expected to start"
        echo "   Check backend.log for errors"
    fi
    sleep 1
done

# Start Frontend
echo ""
echo "Starting frontend on http://localhost:3000..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "✓ Frontend started (PID: $FRONTEND_PID)"
echo "  Logs: tail -f frontend.log"

echo ""
echo "======================================"
echo "✅ Both Servers Running!"
echo "======================================"
echo ""
echo "📍 URLs:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "  Backend:   tail -f backend.log"
echo "  Frontend:  tail -f frontend.log"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

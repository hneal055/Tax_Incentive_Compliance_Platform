#!/usr/bin/env bash
# ============================================
# PilotForge Frontend Startup Script
# ============================================

set -e

echo "🎬 PilotForge Frontend Startup"
echo "======================================"

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: This script must be run from the frontend directory"
    echo "   Run: cd frontend && ./start-ui.sh"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "   Please install Node.js 20+ from https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo "⚠️  Warning: Node.js 20+ recommended, found version $(node --version)"
else
    echo "✓ Node.js $(node --version) detected"
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi
echo "✓ npm $(npm --version) detected"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo ""
    echo "📦 Installing dependencies..."
    npm install
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Check if .env exists, if not suggest creating it
if [ ! -f ".env" ]; then
    echo ""
    echo "ℹ️  Note: No .env file found (optional)"
    echo "   Using default configuration: API at http://localhost:8000"
    echo "   To customize, run: cp .env.example .env"
fi

echo ""
echo "======================================"
echo "🚀 Starting Development Server..."
echo "======================================"
echo ""
echo "Frontend will be available at:"
echo "  → http://localhost:3000"
echo ""
echo "Make sure the backend is running at:"
echo "  → http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev

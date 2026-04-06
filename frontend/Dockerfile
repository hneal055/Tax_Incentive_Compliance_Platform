# ============================================
# Multi-stage build for React + Vite frontend
# ============================================

# Stage 1: Builder
FROM node:20-alpine as builder

WORKDIR /app

# VITE_API_URL: empty = relative URLs via nginx proxy (local Docker)
#               set to backend URL for Railway/cloud deployments
# VITE_API_URL: set at build time via --build-arg or Railway Variables (must be a build var, not runtime)
# Defaults to empty string = relative URLs (local Docker, handled by top-level nginx proxy)
ARG VITE_API_URL=""

# Copy package files
COPY package*.json ./
COPY yarn.lock* ./

# Install dependencies with caching
RUN npm ci --prefer-offline --no-audit 2>/dev/null || npm install

# Copy source code
COPY . .

# Build Vite app — VITE_API_URL baked in at build time
RUN VITE_API_URL="${VITE_API_URL}" VITE_USE_REAL_API=true VITE_USE_REAL_AUTH=true npx vite build && \
    echo "Built with VITE_API_URL=${VITE_API_URL}"

# ============================================
# Stage 2: Runtime - Nginx
FROM nginx:alpine

# Install wget for health checks (lighter than curl)
RUN apk add --no-cache wget

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Always use the Railway-compatible config (PORT-aware, no Docker proxy)
COPY nginx.railway.conf /etc/nginx/conf.d/default.conf

# Entrypoint substitutes $PORT at startup (Railway injects PORT; local defaults to 3000)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create health check endpoint (empty file for nginx to serve)
RUN echo "OK" > /usr/share/nginx/html/health

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget -q -O - http://localhost:${PORT:-3000}/health > /dev/null || exit 1

# Start via entrypoint (handles PORT substitution)
CMD ["/entrypoint.sh"]

# ============================================
# Multi-stage build for React + Vite frontend
# ============================================

# Stage 1: Builder
FROM node:20-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock* ./

# Install dependencies with caching
RUN npm ci --prefer-offline --no-audit 2>/dev/null || npm install

# Copy source code
COPY . .

# Build Vite app (skip TypeScript checking, vite will bundle)
# Empty VITE_API_URL → relative URLs → routed through nginx (no CORS)
RUN VITE_API_URL="" VITE_USE_REAL_API=true VITE_USE_REAL_AUTH=true npx vite build

# ============================================
# Stage 2: Runtime - Nginx
FROM nginx:alpine

# Install wget for health checks (lighter than curl)
RUN apk add --no-cache wget

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Use nginx config that proxies /api/ to backend — works on direct port 3000 AND via main nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create health check endpoint (empty file for nginx to serve)
RUN echo "OK" > /usr/share/nginx/html/health

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget -q -O - http://localhost:3000/health > /dev/null || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

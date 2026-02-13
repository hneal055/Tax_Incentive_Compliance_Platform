# Developer Portal Deployment Guide

## Quick Deploy

### Local Development
```bash
cd developer-portal
npm install
npm run dev
```
Access at: http://localhost:3000

### Production Build
```bash
cd developer-portal
npm run build
npm start
```
Access at: http://localhost:3000

## Deployment Options

### 1. Vercel (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd developer-portal
vercel
```

### 2. Docker
Create `developer-portal/Dockerfile`:
```dockerfile
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:24-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t pilotforge-portal developer-portal
docker run -p 3000:3000 pilotforge-portal
```

### 3. Static Export
```bash
cd developer-portal
npm run build
# Deploy the .next directory to any static host
```

### 4. Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd developer-portal
netlify deploy --prod
```

## Environment Configuration

### Update API URLs
If your backend API is not on `localhost:8000`, update references in:
- `app/page.tsx` - Quick start examples
- `public/openapi.json` - Server URLs in OpenAPI spec

### Update Port
Edit `package.json`:
```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

## Updating OpenAPI Specification

When the backend API changes:

1. Start the backend:
   ```bash
   cd ..
   python -m uvicorn src.main:app --reload
   ```

2. Download the latest spec:
   ```bash
   curl http://localhost:8000/openapi.json > developer-portal/public/openapi.json
   ```

3. Rebuild:
   ```bash
   cd developer-portal
   npm run build
   ```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy Portal

on:
  push:
    branches: [main]
    paths:
      - 'developer-portal/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Build
        run: |
          cd developer-portal
          npm ci
          npm run build
      - name: Deploy
        run: |
          # Add your deployment command here
```

## Troubleshooting

### Build Errors
- Ensure Node.js 20+ is installed
- Clear cache: `rm -rf .next node_modules && npm install`

### Port Already in Use
```bash
# Change port in package.json or use:
npm run dev -- -p 3001
```

### OpenAPI Not Loading
- Verify `public/openapi.json` exists
- Check browser console for errors
- Ensure file is valid JSON

## Monitoring

### Health Check
Visit http://localhost:3000 to verify the portal is running.

### Logs
```bash
# Development logs
npm run dev

# Production logs
npm start
```

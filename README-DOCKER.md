# Docker Deployment Guide

This guide explains how to build and run the Tax Incentive Compliance Platform using Docker containers.

## Overview

The application consists of three Docker services:
- **PostgreSQL Database** - Data storage
- **Backend API** - FastAPI application (port 8000)
- **Frontend** - React application served via nginx (port 80)

## Prerequisites

- **Docker** version 20.10 or higher
- **Docker Compose** version 2.0 or higher

Check your installation:
```bash
docker --version
docker compose version
```

## Quick Start

### 1. Build and Run All Services

```bash
# Build and start all services
docker compose up --build

# Or run in detached mode (background)
docker compose up -d --build
```

This will:
1. Start PostgreSQL database on port 5432
2. Build and start the backend API on port 8000
3. Build and start the frontend on port 80

### 2. Access the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (postgres/postgres)

### 3. Stop Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes database data)
docker compose down -v
```

## Environment Configuration

### Using .env File

Create a `.env` file in the project root for production deployments:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/tax_incentive_db

# JWT Authentication
SECRET_KEY=your-super-secret-key-min-32-chars-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Monitoring APIs
NEWS_API_KEY=your-newsapi-key-here
OPENAI_API_KEY=your-openai-api-key-here
MONITOR_INTERVAL_HOURS=4

# Optional: Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password
NOTIFICATION_FROM_EMAIL=noreply@pilotforge.com
NOTIFICATION_TO_EMAILS=admin@example.com

# Optional: Slack Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#pilotforge-alerts
```

Docker Compose will automatically load this file.

### Generate Secure SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Individual Service Management

### Backend Only

```bash
# Build backend image
docker build -t tax-incentive-backend .

# Run backend (requires PostgreSQL)
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tax_incentive_db \
  tax-incentive-backend
```

### Frontend Only

```bash
# Build frontend image
cd frontend
docker build -t tax-incentive-frontend .

# Run frontend
docker run -p 80:80 tax-incentive-frontend
```

### Database Only

```bash
# Start PostgreSQL
docker compose up postgres -d
```

## Database Management

### Initialize Database

The database is automatically initialized when the backend starts. To manually run migrations:

```bash
# Access the backend container
docker compose exec app bash

# Inside container, run migrations
prisma migrate deploy

# Exit container
exit
```

### Database Backup

```bash
# Backup database to file
docker compose exec postgres pg_dump -U postgres tax_incentive_db > backup.sql

# Restore from backup
cat backup.sql | docker compose exec -T postgres psql -U postgres tax_incentive_db
```

### Access Database CLI

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U postgres -d tax_incentive_db
```

## Development Mode

For development with hot-reload:

### Backend Development

```bash
# Override the backend command to enable reload
docker compose run -p 8000:8000 app uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Development

For frontend development, it's recommended to run the dev server locally:

```bash
cd frontend
npm install
npm run dev
```

## Troubleshooting

### Check Service Status

```bash
# View running containers
docker compose ps

# View logs
docker compose logs

# View specific service logs
docker compose logs app
docker compose logs frontend
docker compose logs postgres

# Follow logs in real-time
docker compose logs -f app
```

### Health Checks

All services include health checks:

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost/

# Check database
docker compose exec postgres pg_isready -U postgres
```

### Common Issues

#### 1. Port Already in Use

If port 80, 8000, or 5432 is already in use, modify the port mapping in `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "3000:80"  # Change external port from 80 to 3000
```

#### 2. Permission Denied Errors

If you encounter permission errors, ensure Docker has proper permissions:

```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
# Then log out and back in
```

#### 3. Build Failures

Clear Docker cache and rebuild:

```bash
# Remove all containers and images
docker compose down --rmi all

# Rebuild without cache
docker compose build --no-cache

# Start services
docker compose up
```

#### 4. Database Connection Errors

Ensure PostgreSQL is fully started before the backend:

```bash
# Wait for postgres to be ready
docker compose up postgres
# Wait ~5 seconds, then start other services
docker compose up app frontend
```

Or use the depends_on configuration (already included in docker-compose.yml).

## Production Deployment

### Security Considerations

1. **Change default passwords** - Never use default credentials in production
2. **Set strong SECRET_KEY** - Generate a secure random key
3. **Use HTTPS** - Add a reverse proxy (nginx/Traefik) with SSL certificates
4. **Limit exposed ports** - Don't expose database port externally
5. **Regular updates** - Keep base images and dependencies updated

### Recommended Production Setup

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}  # Use strong password
    ports: []  # Don't expose externally

  app:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    restart: always

  frontend:
    restart: always

  # Add nginx reverse proxy with SSL
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx-ssl.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
```

## Resource Requirements

### Minimum

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disk**: 10 GB

### Recommended

- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disk**: 20+ GB (with room for database growth)

## Monitoring

### View Resource Usage

```bash
# Container stats
docker stats

# Specific service stats
docker stats tax-incentive-app tax-incentive-frontend tax-incentive-db
```

### Logs Management

```bash
# Limit log size in docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Cleanup

### Remove Stopped Containers

```bash
docker compose down
```

### Remove All Data (Including Volumes)

```bash
docker compose down -v
```

### Remove Images

```bash
# Remove project images
docker compose down --rmi all

# Remove all unused images
docker image prune -a
```

## Additional Commands

### Rebuild Single Service

```bash
# Rebuild backend only
docker compose build app

# Rebuild frontend only
docker compose build frontend
```

### Execute Commands in Containers

```bash
# Run shell in backend container
docker compose exec app bash

# Run shell in frontend container
docker compose exec frontend sh

# Run Python command in backend
docker compose exec app python -c "print('Hello from container')"
```

### Update Running Services

```bash
# Pull latest code and rebuild
git pull
docker compose up -d --build
```

## Support

For issues specific to Docker deployment:
1. Check logs: `docker compose logs`
2. Verify health: `curl http://localhost:8000/health`
3. Review environment variables
4. Check the main [README.md](./README.md) for application-specific help

---

**Built with Docker for easy deployment and scalability**

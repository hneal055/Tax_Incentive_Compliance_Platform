# Authentication System

This directory contains the authentication and authorization system for PilotForge.

## Overview

The authentication system supports two methods:
1. **JWT (JSON Web Tokens)** - For user-based authentication
2. **API Keys** - For programmatic/service access

## Components

### `auth.py`
Main authentication module with the following functions:

#### JWT Authentication
- `get_current_user(credentials, db)` - Validates JWT token and returns authenticated user
- `get_current_organization_from_jwt(user, db)` - Gets organization for JWT-authenticated user

#### API Key Authentication
- `hash_api_key(plain_key)` - Hashes an API key using SHA-256
- `get_organization_from_api_key(api_key, db)` - Validates API key and returns organization

#### Unified Authentication
- `get_current_organization(credentials, api_key, db)` - Tries JWT first, falls back to API key

### `config.py`
Re-exports configuration settings from `src.utils.config` for compatibility with imports from `app.core.config`.

### `auth_examples.py`
Example routes demonstrating how to use the authentication system.

## Usage

### JWT Authentication

```python
from fastapi import APIRouter, Depends
from prisma.models import User
from src.core.auth import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"user_id": user.id, "email": user.email}
```

To call this endpoint:
```bash
curl -H "Authorization: Bearer <jwt_token>" http://localhost:8000/api/v1/protected
```

### API Key Authentication

```python
from fastapi import APIRouter, Depends
from prisma.models import Organization
from src.core.auth import get_organization_from_api_key

router = APIRouter()

@router.get("/protected")
async def protected_route(org: Organization = Depends(get_organization_from_api_key)):
    return {"organization_id": org.id, "name": org.name}
```

To call this endpoint:
```bash
curl -H "X-API-Key: <api_key>" http://localhost:8000/api/v1/protected
```

### Unified Authentication (JWT or API Key)

```python
from fastapi import APIRouter, Depends
from prisma.models import Organization
from src.core.auth import get_current_organization

router = APIRouter()

@router.get("/protected")
async def protected_route(org: Organization = Depends(get_current_organization)):
    return {"organization_id": org.id, "name": org.name}
```

This endpoint accepts either JWT or API Key:
```bash
# With JWT
curl -H "Authorization: Bearer <jwt_token>" http://localhost:8000/api/v1/protected

# With API Key
curl -H "X-API-Key: <api_key>" http://localhost:8000/api/v1/protected
```

## Configuration

The authentication system uses the following configuration settings from `.env`:

```env
SECRET_KEY=your-secret-key-change-in-production-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important:** Always change the `SECRET_KEY` in production!

## Security Notes

1. **API Keys are hashed** using SHA-256 before storage in the database
2. **JWT tokens** use HS256 algorithm by default (configurable)
3. **Timezone-aware timestamps** are used throughout (Python 3.12+)
4. **API Key last used timestamp** is automatically updated on successful authentication

## Database Schema

The authentication system requires the following Prisma models:

- `User` - User accounts
- `Organization` - Organizations/tenants
- `Membership` - User-Organization relationships with roles
- `ApiKey` - API keys for programmatic access

See `prisma/schema.prisma` for the full schema definition.

## Testing

Comprehensive tests are available in `tests/test_auth.py`:

```bash
pytest tests/test_auth.py -v
```

Tests cover:
- JWT authentication (success, invalid token, missing credentials, user not found)
- API Key authentication (success, invalid key, missing key)
- Unified authentication (JWT, API key, fallback, neither)
- Organization retrieval (success, no membership)
- API key hashing

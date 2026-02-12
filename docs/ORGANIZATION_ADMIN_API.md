# 🏢 Organization Admin Endpoints

> API endpoints for managing organizations and members (Admin access required)

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Organization Management](#organization-management)
4. [Member Management](#member-management)
5. [Examples](#examples)

---

## 🔒 Overview

Organization admin endpoints allow administrators to manage their organization's settings and members. All endpoints require:

- **Authentication**: Valid JWT token
- **Authorization**: ADMIN role in the organization

---

## 🔑 Authentication

All requests must include a JWT token in the Authorization header:

```bash
Authorization: Bearer <your-jwt-token>
```

The JWT token must contain:
- Valid user ID (`sub` claim)
- User must have ADMIN role in the organization

---

## 🏢 Organization Management

### Get Organization Details

Retrieve details about your organization.

**Endpoint:** `GET /api/v1/organizations/{organization_id}`

**Example:**

```bash
curl -X GET http://localhost:8000/api/v1/organizations/test-org-id \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Response:**

```json
{
  "id": "test-org-id",
  "name": "Test Organization",
  "slug": "test-org",
  "createdAt": "2024-01-15T10:00:00Z",
  "updatedAt": "2024-01-15T10:00:00Z"
}
```

---

### Update Organization

Update organization name or slug.

**Endpoint:** `PUT /api/v1/organizations/{organization_id}`

**Request Body:**

```json
{
  "name": "Updated Organization Name",
  "slug": "updated-slug"
}
```

**Example:**

```bash
curl -X PUT http://localhost:8000/api/v1/organizations/test-org-id \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Organization Name",
    "slug": "updated-slug"
  }'
```

**Response:**

```json
{
  "id": "test-org-id",
  "name": "Updated Organization Name",
  "slug": "updated-slug",
  "createdAt": "2024-01-15T10:00:00Z",
  "updatedAt": "2024-01-20T14:30:00Z"
}
```

**Notes:**
- Both `name` and `slug` are optional
- Slug must be unique across all organizations
- Organization slug is used in URLs and must be URL-safe

---

## 👥 Member Management

### List Organization Members

Get all members of your organization.

**Endpoint:** `GET /api/v1/organizations/{organization_id}/members`

**Example:**

```bash
curl -X GET http://localhost:8000/api/v1/organizations/test-org-id/members \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Response:**

```json
[
  {
    "id": "membership-1",
    "role": "ADMIN",
    "userId": "user-1",
    "organizationId": "test-org-id",
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z",
    "user": {
      "id": "user-1",
      "email": "admin@example.com",
      "name": "Admin User"
    }
  },
  {
    "id": "membership-2",
    "role": "MEMBER",
    "userId": "user-2",
    "organizationId": "test-org-id",
    "createdAt": "2024-01-16T09:00:00Z",
    "updatedAt": "2024-01-16T09:00:00Z",
    "user": {
      "id": "user-2",
      "email": "member@example.com",
      "name": "Member User"
    }
  }
]
```

---

### Add Organization Member

Invite or add a user to your organization.

**Endpoint:** `POST /api/v1/organizations/{organization_id}/members`

**Request Body:**

```json
{
  "userId": "user-id-to-add",
  "role": "MEMBER"
}
```

**Roles:**
- `ADMIN` - Full administrative access
- `MEMBER` - Standard member access

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/organizations/test-org-id/members \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "new-user-id",
    "role": "MEMBER"
  }'
```

**Response:**

```json
{
  "id": "membership-3",
  "role": "MEMBER",
  "userId": "new-user-id",
  "organizationId": "test-org-id",
  "createdAt": "2024-01-20T15:00:00Z",
  "updatedAt": "2024-01-20T15:00:00Z",
  "user": {
    "id": "new-user-id",
    "email": "newuser@example.com",
    "name": "New User"
  }
}
```

**Error Cases:**
- `404` - User not found
- `409` - User is already a member

---

### Update Member Role

Change a member's role between ADMIN and MEMBER.

**Endpoint:** `PUT /api/v1/organizations/{organization_id}/members/{user_id}`

**Request Body:**

```json
{
  "role": "ADMIN"
}
```

**Example:**

```bash
curl -X PUT http://localhost:8000/api/v1/organizations/test-org-id/members/user-2 \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ADMIN"
  }'
```

**Response:**

```json
{
  "id": "membership-2",
  "role": "ADMIN",
  "userId": "user-2",
  "organizationId": "test-org-id",
  "createdAt": "2024-01-16T09:00:00Z",
  "updatedAt": "2024-01-20T16:00:00Z",
  "user": {
    "id": "user-2",
    "email": "member@example.com",
    "name": "Member User"
  }
}
```

**Protection:**
- Cannot demote yourself if you're the last admin

---

### Remove Organization Member

Remove a member from the organization.

**Endpoint:** `DELETE /api/v1/organizations/{organization_id}/members/{user_id}`

**Example:**

```bash
curl -X DELETE http://localhost:8000/api/v1/organizations/test-org-id/members/user-2 \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Response:** `204 No Content`

**Protection:**
- Cannot remove yourself if you're the last admin
- Organization must always have at least one admin

---

## 📖 Examples

### Complete Workflow: Managing Team Members

```python
import httpx

# Setup
BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "your-jwt-token"
ORG_ID = "your-org-id"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 1. List current members
response = httpx.get(
    f"{BASE_URL}/organizations/{ORG_ID}/members",
    headers=headers
)
members = response.json()
print(f"Current team size: {len(members)}")

# 2. Add a new team member
new_member = httpx.post(
    f"{BASE_URL}/organizations/{ORG_ID}/members",
    headers=headers,
    json={
        "userId": "new-developer-id",
        "role": "MEMBER"
    }
)
print(f"Added: {new_member.json()['user']['email']}")

# 3. Promote member to admin
promote = httpx.put(
    f"{BASE_URL}/organizations/{ORG_ID}/members/trusted-user-id",
    headers=headers,
    json={"role": "ADMIN"}
)
print(f"Promoted to ADMIN: {promote.json()['user']['email']}")

# 4. Update organization settings
update_org = httpx.put(
    f"{BASE_URL}/organizations/{ORG_ID}",
    headers=headers,
    json={"name": "Production Studio 2024"}
)
print(f"Updated org name: {update_org.json()['name']}")

# 5. Remove inactive member
httpx.delete(
    f"{BASE_URL}/organizations/{ORG_ID}/members/inactive-user-id",
    headers=headers
)
print("Removed inactive member")
```

### JavaScript/TypeScript Example

```typescript
const BASE_URL = 'http://localhost:8000/api/v1';
const TOKEN = 'your-jwt-token';
const ORG_ID = 'your-org-id';

const headers = {
  'Authorization': `Bearer ${TOKEN}`,
  'Content-Type': 'application/json'
};

// Add a new admin
async function addAdmin(userId: string) {
  const response = await fetch(
    `${BASE_URL}/organizations/${ORG_ID}/members`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify({
        userId,
        role: 'ADMIN'
      })
    }
  );
  
  if (!response.ok) {
    throw new Error(`Failed to add admin: ${response.statusText}`);
  }
  
  const member = await response.json();
  console.log(`Added admin: ${member.user.email}`);
  return member;
}

// List all members
async function listMembers() {
  const response = await fetch(
    `${BASE_URL}/organizations/${ORG_ID}/members`,
    { headers }
  );
  
  const members = await response.json();
  
  members.forEach((member: any) => {
    console.log(`${member.user.email} - ${member.role}`);
  });
  
  return members;
}

// Usage
await listMembers();
await addAdmin('new-admin-user-id');
```

---

## 🔒 Security Features

### Audit Logging

All admin actions are automatically logged:
- Organization updates (name, slug changes)
- Member additions
- Role changes
- Member removals

Audit logs include:
- Action type
- Actor (admin user who performed the action)
- Timestamp
- IP address
- User agent
- Metadata (details of the change)

### Role Protection

- Only ADMIN role can access organization admin endpoints
- Organizations must always have at least one admin
- Admins cannot:
  - Remove themselves if they're the last admin
  - Demote themselves if they're the last admin
  - Access other organizations

### Multi-tenancy

All endpoints enforce organization boundaries:
- Users can only access their own organization
- Cross-organization access is prevented
- All resources are scoped to the organization

---

## ⚠️ Error Responses

Common error codes:

- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - Not an admin or accessing another organization
- `404 Not Found` - Organization, user, or member not found
- `409 Conflict` - Slug already exists or user already a member
- `400 Bad Request` - Invalid request (e.g., removing last admin)

**Example error response:**

```json
{
  "detail": "Admin role required for this operation"
}
```

---

## 📝 Best Practices

1. **Role Management**
   - Always maintain at least 2 admins for redundancy
   - Use MEMBER role by default; promote to ADMIN only when needed
   - Review member roles periodically

2. **Organization Updates**
   - Choose URL-safe slugs (lowercase, hyphens, no spaces)
   - Update organization settings during off-peak hours
   - Document slug changes for frontend/API consumers

3. **Audit Trail**
   - Regularly review audit logs for member changes
   - Monitor for unexpected role changes
   - Keep audit logs for compliance

4. **API Integration**
   - Cache organization data (it changes infrequently)
   - Use proper error handling for 403/404 responses
   - Implement retry logic for network failures

---

## 🔗 Related Documentation

- [API Key Management](./API_KEY_VERIFICATION.md)
- [Authentication Guide](../src/core/README.md)
- [API Examples](./API_EXAMPLES.md)

---

*For support or questions, please refer to the main [README](../README.md).*

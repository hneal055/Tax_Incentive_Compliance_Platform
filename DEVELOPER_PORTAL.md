# Developer Portal Documentation

## Overview

The Developer Portal is a self-service interface for managing API keys in PilotForge. It allows developers to create, rotate, and manage API keys for programmatic access to the PilotForge API.

## Features

### 1. API Key Management

The Developer Portal provides complete lifecycle management for API keys:

- **Create**: Generate new API keys with custom permissions
- **View**: List all your organization's API keys
- **Rotate**: Generate new keys while invalidating old ones
- **Delete**: Revoke API keys permanently

### 2. Security Features

- **One-time Display**: API keys are only shown in full once, upon creation or rotation
- **Prefix Display**: Keys are identified by their first 8 characters for easy reference
- **Permission Levels**: Assign granular permissions (read, write, admin)
- **Expiration Dates**: Set optional expiration dates for temporary access
- **Secure Storage**: Keys are hashed using SHA-256 before storage

### 3. User Interface Components

#### DeveloperPortal Page (`/developer-portal`)

Main page for API key management featuring:

- **Header Section**: Title and "Create API Key" button
- **Getting Started Cards**: Quick guide showing the API key workflow
- **API Keys List**: Display of all API keys with:
  - Key name and prefix
  - Permission badges
  - Last used timestamp
  - Expiration status with warnings
  - Hover actions for rotate/delete
- **Documentation Section**: Code examples and API documentation links
- **Best Practices**: Security guidelines and recommendations

#### CreateApiKeyModal Component

Modal dialog for creating new API keys:

- **Form Fields**:
  - Name (required): Human-readable identifier
  - Permissions (checkboxes): read, write, admin
  - Expiration Date (optional): Set key expiration
- **Key Display**: Shows plaintext key once after creation
- **Copy Button**: Easy copy-to-clipboard functionality
- **Validation**: Ensures required fields are filled

#### ApiKeyCard Component

Card component for displaying individual API keys:

- **Key Information**:
  - Name and prefix display
  - Permission badges
  - Last used and created timestamps
  - Expiration status
- **Actions** (shown on hover):
  - Rotate button
  - Delete button
- **Status Indicators**:
  - Expired warning (red)
  - Expiring soon warning (yellow)

## API Integration

### API Service Layer

The frontend integrates with the backend through the `api.apiKeys` service:

```typescript
// List all API keys
const keys = await api.apiKeys.list();

// Get specific key
const key = await api.apiKeys.get(keyId);

// Create new key
const newKey = await api.apiKeys.create({
  name: "Production API Key",
  permissions: ["read", "write"],
  expiresAt: "2026-12-31T23:59:59Z"
});

// Update key metadata
const updated = await api.apiKeys.update(keyId, {
  name: "Updated Name",
  permissions: ["read"]
});

// Delete key
await api.apiKeys.delete(keyId);

// Rotate key
const rotated = await api.apiKeys.rotate(keyId);
```

### Backend Endpoints

The frontend communicates with these backend endpoints:

- `GET /api/v1/api-keys/` - List all keys
- `GET /api/v1/api-keys/{id}` - Get specific key
- `POST /api/v1/api-keys/` - Create new key
- `PATCH /api/v1/api-keys/{id}` - Update key
- `DELETE /api/v1/api-keys/{id}` - Delete key
- `POST /api/v1/api-keys/{id}/rotate` - Rotate key

## TypeScript Types

### ApiKey Interface

```typescript
interface ApiKey {
  id: string;
  name: string;
  organizationId: string;
  prefix: string;
  permissions: string[];
  lastUsedAt: string | null;
  expiresAt: string | null;
  createdAt: string;
  updatedAt: string;
}
```

### ApiKeyCreated Interface

```typescript
interface ApiKeyCreated extends ApiKey {
  plaintext_key: string;  // Only returned on creation/rotation
}
```

## Usage Guide

### Creating Your First API Key

1. Navigate to `/developer-portal` in the application
2. Click "Create API Key" button
3. Fill in the form:
   - Enter a descriptive name
   - Select appropriate permissions
   - (Optional) Set an expiration date
4. Click "Create API Key"
5. **Important**: Copy and save the displayed key immediately - you won't see it again!
6. Click "Done" when finished

### Using API Keys in Code

Add the API key to your request headers:

```bash
curl -X GET "http://localhost:8000/api/v1/productions/" \
  -H "X-API-Key: your_api_key_here"
```

### Rotating API Keys

1. Hover over the API key card
2. Click the "Rotate" button
3. Confirm the rotation (old key will be immediately invalidated)
4. Copy and save the new key
5. Update your applications with the new key

### Best Practices

1. **Never commit keys**: Don't store API keys in version control
2. **Use environment variables**: Store keys securely in your deployment environment
3. **Rotate regularly**: Rotate keys periodically and when team members leave
4. **Minimum permissions**: Use the least privileges required for each key
5. **Set expiration dates**: Use expiration dates for temporary or trial access
6. **Monitor usage**: Check "Last Used" timestamps to identify unused keys

## Permission Levels

### Read
- View-only access to endpoints
- Can retrieve data but cannot modify
- Suitable for reporting and analytics

### Write
- Read access plus modify capabilities
- Can create, update, and delete resources
- Suitable for application integrations

### Admin
- Full access including sensitive operations
- Can manage webhooks and audit logs
- Should be restricted to trusted systems

## Security Considerations

### Frontend Security

- API keys are only displayed in full once
- Keys are transmitted over HTTPS only
- No keys are stored in browser storage
- Clipboard API used for secure copying

### Backend Security

- Keys are hashed using SHA-256
- Only prefixes stored for display
- Organization-scoped access control
- Audit logging for all key operations
- Rate limiting per key

## Navigation

The Developer Portal is accessible from:
- **Sidebar**: Click "Developer Portal" menu item
- **Direct URL**: Navigate to `/developer-portal`
- **Icon**: Code icon (`</>`) in navigation

## Troubleshooting

### "Failed to load API keys"

**Cause**: Backend connection issue or authentication failure

**Solutions**:
1. Ensure backend is running at `http://localhost:8000`
2. Check authentication token is valid
3. Verify organization ID is set correctly
4. Check browser console for detailed errors

### "Failed to create API key"

**Cause**: Validation error or permission issue

**Solutions**:
1. Ensure all required fields are filled
2. Verify you have permission to create keys
3. Check that permissions are valid (read, write, admin)
4. Ensure expiration date is in the future

### API key not working in requests

**Cause**: Invalid key, expired key, or incorrect header

**Solutions**:
1. Verify you're using the correct key (check prefix)
2. Ensure key hasn't expired
3. Use header name `X-API-Key` (case-sensitive)
4. Check that key hasn't been deleted or rotated

## Future Enhancements

Planned improvements for the Developer Portal:

- [ ] Usage analytics per key
- [ ] Webhook configuration UI
- [ ] Audit log viewer
- [ ] Rate limit configuration
- [ ] Key usage graphs
- [ ] Multi-factor rotation workflow
- [ ] IP whitelisting
- [ ] Scope-based permissions (per-endpoint)

## Related Documentation

- **API Documentation**: `/docs` - Interactive API documentation
- **ReDoc**: `/redoc` - Alternative API documentation
- **API Verification**: See `API_KEY_VERIFICATION.md` for backend implementation details
- **User Manual**: See `USER_MANUAL.md` for general platform usage

## Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation in the `docs/` directory
- Review API examples at `http://localhost:8000/docs`

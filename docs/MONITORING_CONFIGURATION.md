# Monitoring Sources Configuration Guide

## Overview

This guide explains how to configure and manage monitoring sources for the PilotForge Real-Time Jurisdiction Monitoring System.

## Monitoring Source Types

The system supports three types of monitoring sources:

### 1. RSS Feeds (`rss`)
Monitor RSS/Atom feeds from film commissions, government agencies, and news sites.

**Best for:**
- Official film commission news feeds
- Legislative update feeds
- Industry news sites

**Example sources:**
- California Film Commission News Feed
- Georgia Department of Economic Development
- Production Weekly

### 2. Web Pages (`webpage`)
Monitor specific web pages for content changes using web scraping.

**Best for:**
- Incentive program pages
- Eligibility requirement pages
- Application deadline pages

**Example sources:**
- State film office incentive pages
- Tax credit calculator pages
- Application portal pages

### 3. API Endpoints (`api`)
Monitor JSON API endpoints for data changes.

**Best for:**
- Open data APIs
- Government data portals
- Custom integration endpoints

**Example sources:**
- Open government data APIs
- Legislative tracking APIs
- Custom data feeds

## Creating Monitoring Sources

### Via REST API

```bash
curl -X POST http://localhost:8000/api/v1/monitoring/sources \
  -H "Content-Type: application/json" \
  -d '{
    "jurisdictionId": "california-001",
    "sourceType": "rss",
    "url": "https://film.ca.gov/feed",
    "checkInterval": 3600,
    "active": true
  }'
```

### Via Python

```python
import httpx
import asyncio

async def create_monitoring_source():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/monitoring/sources",
            json={
                "jurisdictionId": "california-001",
                "sourceType": "webpage",
                "url": "https://film.ca.gov/tax-credit",
                "checkInterval": 7200,  # Check every 2 hours
                "active": True
            }
        )
        return response.json()

# Run
source = asyncio.run(create_monitoring_source())
print(f"Created source: {source['id']}")
```

## Configuration Parameters

### Required Fields

- **jurisdictionId** (string): ID of the jurisdiction this source monitors
  - Must reference an existing jurisdiction in the database
  - Example: `"california-001"`, `"georgia-001"`

- **sourceType** (string): Type of monitoring source
  - Must be one of: `"rss"`, `"webpage"`, `"api"`

- **url** (string): URL of the monitoring source
  - Must be a valid HTTP/HTTPS URL
  - Examples:
    - RSS: `"https://film.ca.gov/feed.xml"`
    - Webpage: `"https://film.ca.gov/incentives"`
    - API: `"https://api.example.gov/incentives"`

### Optional Fields

- **checkInterval** (integer): How often to check the source (in seconds)
  - Default: `3600` (1 hour)
  - Minimum recommended: `600` (10 minutes)
  - Maximum recommended: `86400` (24 hours)
  - Consider server load and rate limits

- **active** (boolean): Whether the source is actively monitored
  - Default: `true`
  - Set to `false` to pause monitoring without deleting

## Recommended Sources by Jurisdiction

### California

```json
{
  "sources": [
    {
      "sourceType": "rss",
      "url": "https://film.ca.gov/news/feed/",
      "checkInterval": 3600,
      "description": "California Film Commission News"
    },
    {
      "sourceType": "webpage",
      "url": "https://film.ca.gov/tax-credit/",
      "checkInterval": 7200,
      "description": "Tax Credit Program Page"
    }
  ]
}
```

### Georgia

```json
{
  "sources": [
    {
      "sourceType": "rss",
      "url": "https://www.georgia.org/newsroom/rss",
      "checkInterval": 3600,
      "description": "Georgia Economic Development News"
    },
    {
      "sourceType": "webpage",
      "url": "https://www.georgia.org/industries/film-entertainment/georgia-film-tv-production",
      "checkInterval": 7200,
      "description": "Film & TV Production Page"
    }
  ]
}
```

### New York

```json
{
  "sources": [
    {
      "sourceType": "rss",
      "url": "https://esd.ny.gov/news/rss.xml",
      "checkInterval": 3600,
      "description": "NY Economic Development News"
    },
    {
      "sourceType": "webpage",
      "url": "https://esd.ny.gov/film-tax-credit-program",
      "checkInterval": 7200,
      "description": "Film Tax Credit Program"
    }
  ]
}
```

## Check Intervals

Choose appropriate check intervals based on:

### High Frequency (10-30 minutes)
- Critical program pages during application periods
- News feeds during legislative sessions
- Emergency updates or urgent changes

### Medium Frequency (1-4 hours)
- Regular news feeds
- Standard program pages
- General announcements

### Low Frequency (12-24 hours)
- Archive pages
- Historical data
- Rarely updated resources

## Change Detection

The system uses SHA-256 content hashing for change detection:

1. **First Check**: Establishes baseline hash
2. **Subsequent Checks**: Compares current hash to stored hash
3. **Change Detected**: Creates monitoring event if hashes differ
4. **No Change**: Updates last checked timestamp only

### What Triggers Changes

**RSS Feeds:**
- New feed items
- Modified item titles or descriptions
- Changed publication dates

**Web Pages:**
- Text content changes
- Structure modifications
- New or removed sections

**API Endpoints:**
- JSON data changes
- New fields or values
- Modified responses

## Managing Sources

### List All Sources

```bash
curl http://localhost:8000/api/v1/monitoring/sources
```

### Filter by Jurisdiction

```bash
curl http://localhost:8000/api/v1/monitoring/sources?jurisdiction_id=california-001
```

### Filter by Type

```bash
curl http://localhost:8000/api/v1/monitoring/sources?source_type=rss
```

### Filter Active Sources Only

```bash
curl http://localhost:8000/api/v1/monitoring/sources?active=true
```

## Bulk Source Creation

### Python Script

```python
import httpx
import asyncio

SOURCES = [
    {
        "jurisdictionId": "california-001",
        "sourceType": "rss",
        "url": "https://film.ca.gov/feed",
        "checkInterval": 3600
    },
    {
        "jurisdictionId": "california-001",
        "sourceType": "webpage",
        "url": "https://film.ca.gov/tax-credit",
        "checkInterval": 7200
    },
    # Add more sources...
]

async def bulk_create_sources():
    async with httpx.AsyncClient() as client:
        for source_data in SOURCES:
            try:
                response = await client.post(
                    "http://localhost:8000/api/v1/monitoring/sources",
                    json=source_data
                )
                print(f"✓ Created: {source_data['url']}")
            except Exception as e:
                print(f"✗ Failed: {source_data['url']} - {e}")

asyncio.run(bulk_create_sources())
```

## Best Practices

### URL Selection

1. **Prefer RSS Feeds**: More structured and efficient than web scraping
2. **Use Official Sources**: Direct from government/agency sites
3. **Avoid Login-Required Pages**: Must be publicly accessible
4. **Check Robots.txt**: Respect crawling policies

### Check Intervals

1. **Start Conservative**: Begin with longer intervals (4-6 hours)
2. **Monitor Performance**: Adjust based on actual change frequency
3. **Consider Rate Limits**: Some sites limit request frequency
4. **Balance Timeliness vs. Load**: More frequent checks increase server load

### Maintenance

1. **Review Regularly**: Check for broken sources monthly
2. **Update URLs**: Sites redesign or move content
3. **Deactivate Unused**: Pause monitoring for inactive jurisdictions
4. **Monitor Logs**: Watch for repeated errors

## Troubleshooting

### Source Not Updating

1. Check if source is active: `active: true`
2. Verify URL is accessible
3. Check scheduler is running: `/health` endpoint
4. Review application logs for errors

### Too Many Events

1. Increase check interval
2. Review event classification
3. Consider filtering criteria
4. Adjust change detection sensitivity

### Missing Changes

1. Decrease check interval
2. Verify URL points to correct page
3. Check if content uses JavaScript rendering (may need different approach)
4. Review change detection logs

## Monitoring System Health

### Health Check

```bash
curl http://localhost:8000/health
```

Response includes monitoring status:
```json
{
  "status": "healthy",
  "database": "connected",
  "monitoring": "active",
  "version": "v1"
}
```

### Check Scheduler

The monitoring scheduler checks all active sources every 5 minutes by default.

### View Recent Events

```bash
curl http://localhost:8000/api/v1/monitoring/events?page=1&page_size=20
```

## Advanced Configuration

### Custom Headers (Future Enhancement)

For sources requiring authentication or custom headers:

```json
{
  "sourceType": "api",
  "url": "https://api.example.com/data",
  "headers": {
    "Authorization": "Bearer token",
    "User-Agent": "PilotForge/1.0"
  }
}
```

### Webhook Notifications (Future Enhancement)

Configure webhooks to receive events:

```json
{
  "webhookUrl": "https://your-app.com/monitoring/webhook",
  "events": ["incentive_change", "new_program"]
}
```

## Support Resources

- **API Documentation**: `/docs` endpoint
- **GitHub Repository**: https://github.com/hneal055/Tax_Incentive_Compliance_Platform
- **WebSocket API Guide**: `docs/WEBSOCKET_API.md`

## Example: Complete Setup

```python
import httpx
import asyncio

async def setup_california_monitoring():
    """Complete setup for California monitoring"""
    
    # First, ensure jurisdiction exists
    async with httpx.AsyncClient() as client:
        # Get or create California jurisdiction
        jurisdictions = await client.get("http://localhost:8000/api/v1/jurisdictions")
        ca_jurisdiction = next(
            (j for j in jurisdictions.json()['jurisdictions'] if j['code'] == 'CA'),
            None
        )
        
        if not ca_jurisdiction:
            ca_jurisdiction = await client.post(
                "http://localhost:8000/api/v1/jurisdictions",
                json={
                    "name": "California",
                    "code": "CA",
                    "country": "USA",
                    "type": "state",
                    "website": "https://film.ca.gov"
                }
            )
            ca_jurisdiction = ca_jurisdiction.json()
        
        # Create monitoring sources
        sources = [
            {
                "jurisdictionId": ca_jurisdiction['id'],
                "sourceType": "rss",
                "url": "https://film.ca.gov/feed",
                "checkInterval": 3600,
                "active": True
            },
            {
                "jurisdictionId": ca_jurisdiction['id'],
                "sourceType": "webpage",
                "url": "https://film.ca.gov/tax-credit",
                "checkInterval": 7200,
                "active": True
            }
        ]
        
        for source_data in sources:
            response = await client.post(
                "http://localhost:8000/api/v1/monitoring/sources",
                json=source_data
            )
            print(f"✓ Created source: {response.json()['url']}")

# Run setup
asyncio.run(setup_california_monitoring())
```

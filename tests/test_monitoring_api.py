"""
Comprehensive tests for Monitoring API endpoints
Tests coverage for monitoring events and sources
"""
import pytest
from datetime import datetime, timezone


class TestMonitoringModelValidation:
    """Test Pydantic model validation for monitoring"""
    
    def test_monitoring_source_create_valid(self):
        """Test creating a valid monitoring source"""
        from src.models.monitoring import MonitoringSourceCreate
        
        source = MonitoringSourceCreate(
            jurisdictionId="test-jurisdiction-id",
            sourceType="rss",
            url="https://example.com/feed.xml",
            checkInterval=3600,
            active=True
        )
        
        assert source.jurisdictionId == "test-jurisdiction-id"
        assert source.sourceType == "rss"
        assert source.url == "https://example.com/feed.xml"
        assert source.checkInterval == 3600
        assert source.active is True
    
    def test_monitoring_source_default_values(self):
        """Test monitoring source default values"""
        from src.models.monitoring import MonitoringSourceCreate
        
        source = MonitoringSourceCreate(
            jurisdictionId="test-id",
            sourceType="api",
            url="https://api.example.com/data"
        )
        
        assert source.checkInterval == 3600  # Default
        assert source.active is True  # Default
    
    def test_monitoring_source_update_optional(self):
        """Test that all fields in MonitoringSourceUpdate are optional"""
        from src.models.monitoring import MonitoringSourceUpdate
        
        # Empty update should work
        update = MonitoringSourceUpdate()
        assert update.model_dump(exclude_unset=True) == {}
        
        # Partial update should work
        update = MonitoringSourceUpdate(checkInterval=7200)
        assert update.checkInterval == 7200
    
    def test_monitoring_event_create_valid(self):
        """Test creating a valid monitoring event"""
        from src.models.monitoring import MonitoringEventCreate
        
        event = MonitoringEventCreate(
            jurisdictionId="test-jurisdiction-id",
            eventType="incentive_change",
            severity="warning",
            title="Tax Credit Percentage Changed",
            summary="California Film Tax Credit increased from 20% to 25%",
            sourceId="source-123",
            sourceUrl="https://example.com/news",
            metadata='{"old_value": 20, "new_value": 25}'
        )
        
        assert event.jurisdictionId == "test-jurisdiction-id"
        assert event.eventType == "incentive_change"
        assert event.severity == "warning"
        assert event.title == "Tax Credit Percentage Changed"
    
    def test_monitoring_event_optional_fields(self):
        """Test monitoring event optional fields"""
        from src.models.monitoring import MonitoringEventCreate
        
        event = MonitoringEventCreate(
            jurisdictionId="test-id",
            eventType="news",
            severity="info",
            title="Test Event",
            summary="Test summary"
        )
        
        assert event.sourceId is None
        assert event.sourceUrl is None
        assert event.metadata is None
    
    def test_monitoring_event_update_optional(self):
        """Test that MonitoringEventUpdate fields are optional"""
        from src.models.monitoring import MonitoringEventUpdate
        
        # Empty update
        update = MonitoringEventUpdate()
        assert update.model_dump(exclude_unset=True) == {}
        
        # Partial update with readAt
        update = MonitoringEventUpdate(readAt=datetime.now(timezone.utc))
        assert update.readAt is not None
    
    def test_unread_count_response(self):
        """Test UnreadCountResponse model"""
        from src.models.monitoring import UnreadCountResponse
        
        response = UnreadCountResponse(unreadCount=42)
        assert response.unreadCount == 42


class TestMonitoringEventsAPI:
    """Test monitoring events API endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_monitoring_events_empty(self, async_client, mock_prisma_db):
        """Test getting monitoring events when none exist"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringevent.find_many = AsyncMock(return_value=[])
        mock_prisma_db.monitoringevent.count = AsyncMock(return_value=0)
        
        response = await async_client.get("/api/v1/monitoring/events")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["events"] == []
    
    @pytest.mark.asyncio
    async def test_get_monitoring_events_with_data(self, async_client, mock_prisma_db):
        """Test getting monitoring events with data"""
        from unittest.mock import AsyncMock, MagicMock
        
        class MockEvent:
            def __init__(self):
                self.id = "event-1"
                self.jurisdictionId = "jurisdiction-1"
                self.sourceId = "source-1"
                self.eventType = "incentive_change"
                self.severity = "warning"
                self.title = "Tax Credit Updated"
                self.summary = "Credit percentage changed"
                self.sourceUrl = "https://example.com"
                self.detectedAt = datetime.now()
                self.readAt = None
                self.metadata = None
                self.createdAt = datetime.now()
                self.updatedAt = datetime.now()
        
        mock_events = [MockEvent()]
        mock_prisma_db.monitoringevent.find_many = AsyncMock(return_value=mock_events)
        mock_prisma_db.monitoringevent.count = AsyncMock(return_value=1)
        
        response = await async_client.get("/api/v1/monitoring/events")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["events"]) == 1
        assert data["events"][0]["eventType"] == "incentive_change"
    
    @pytest.mark.asyncio
    async def test_get_monitoring_events_with_filters(self, async_client, mock_prisma_db):
        """Test filtering monitoring events"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringevent.find_many = AsyncMock(return_value=[])
        mock_prisma_db.monitoringevent.count = AsyncMock(return_value=0)
        
        response = await async_client.get(
            "/api/v1/monitoring/events",
            params={
                "jurisdiction_id": "jur-1",
                "event_type": "new_program",
                "severity": "critical",
                "unread_only": True,
                "page": 1,
                "page_size": 20
            }
        )
        
        assert response.status_code == 200
        # Verify the filters were passed to the mock
        call_args = mock_prisma_db.monitoringevent.find_many.call_args
        where_clause = call_args.kwargs.get("where")
        assert where_clause["jurisdictionId"] == "jur-1"
        assert where_clause["eventType"] == "new_program"
        assert where_clause["severity"] == "critical"
        assert where_clause["readAt"] is None  # unread_only
    
    @pytest.mark.asyncio
    async def test_get_monitoring_events_pagination(self, async_client, mock_prisma_db):
        """Test pagination of monitoring events"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringevent.find_many = AsyncMock(return_value=[])
        mock_prisma_db.monitoringevent.count = AsyncMock(return_value=0)
        
        response = await async_client.get(
            "/api/v1/monitoring/events",
            params={"page": 2, "page_size": 10}
        )
        
        assert response.status_code == 200
        # Verify pagination parameters
        call_args = mock_prisma_db.monitoringevent.find_many.call_args
        assert call_args.kwargs["skip"] == 10  # (page 2 - 1) * 10
        assert call_args.kwargs["take"] == 10
    
    @pytest.mark.asyncio
    async def test_get_unread_count(self, async_client, mock_prisma_db):
        """Test getting unread event count"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringevent.count = AsyncMock(return_value=5)
        
        response = await async_client.get("/api/v1/monitoring/events/unread")
        
        assert response.status_code == 200
        data = response.json()
        assert data["unreadCount"] == 5
    
    @pytest.mark.asyncio
    async def test_get_unread_count_with_jurisdiction_filter(self, async_client, mock_prisma_db):
        """Test getting unread count filtered by jurisdiction"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringevent.count = AsyncMock(return_value=3)
        
        response = await async_client.get(
            "/api/v1/monitoring/events/unread",
            params={"jurisdiction_id": "jur-1"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["unreadCount"] == 3
        
        # Verify filter was applied
        call_args = mock_prisma_db.monitoringevent.count.call_args
        where_clause = call_args.kwargs.get("where")
        assert where_clause["readAt"] is None
        assert where_clause["jurisdictionId"] == "jur-1"
    
    @pytest.mark.asyncio
    async def test_mark_event_as_read_success(self, async_client, mock_prisma_db):
        """Test marking an event as read"""
        from unittest.mock import AsyncMock, MagicMock
        
        class MockEvent:
            def __init__(self):
                self.id = "event-1"
                self.jurisdictionId = "jurisdiction-1"
                self.sourceId = None
                self.eventType = "news"
                self.severity = "info"
                self.title = "Test Event"
                self.summary = "Test summary"
                self.sourceUrl = None
                self.detectedAt = datetime.now()
                self.readAt = datetime.now()
                self.metadata = None
                self.createdAt = datetime.now()
                self.updatedAt = datetime.now()
        
        mock_event = MockEvent()
        mock_prisma_db.monitoringevent.find_unique = AsyncMock(return_value=mock_event)
        mock_prisma_db.monitoringevent.update = AsyncMock(return_value=mock_event)
        
        response = await async_client.patch("/api/v1/monitoring/events/event-1/read")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "event-1"
        assert data["readAt"] is not None
    
    @pytest.mark.asyncio
    async def test_mark_event_as_read_not_found(self, async_client, mock_prisma_db):
        """Test marking non-existent event as read"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringevent.find_unique = AsyncMock(return_value=None)
        
        response = await async_client.patch("/api/v1/monitoring/events/invalid-id/read")
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()


class TestMonitoringSourcesAPI:
    """Test monitoring sources API endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_monitoring_sources_empty(self, async_client, mock_prisma_db):
        """Test getting monitoring sources when none exist"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringsource.find_many = AsyncMock(return_value=[])
        
        response = await async_client.get("/api/v1/monitoring/sources")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["sources"] == []
    
    @pytest.mark.asyncio
    async def test_get_monitoring_sources_with_data(self, async_client, mock_prisma_db):
        """Test getting monitoring sources with data"""
        from unittest.mock import AsyncMock
        
        class MockSource:
            def __init__(self):
                self.id = "source-1"
                self.jurisdictionId = "jurisdiction-1"
                self.sourceType = "rss"
                self.url = "https://example.com/feed.xml"
                self.checkInterval = 3600
                self.lastCheckedAt = None
                self.lastHash = None
                self.active = True
                self.createdAt = datetime.now()
                self.updatedAt = datetime.now()
        
        mock_sources = [MockSource()]
        mock_prisma_db.monitoringsource.find_many = AsyncMock(return_value=mock_sources)
        
        response = await async_client.get("/api/v1/monitoring/sources")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["sources"]) == 1
        assert data["sources"][0]["sourceType"] == "rss"
    
    @pytest.mark.asyncio
    async def test_get_monitoring_sources_with_filters(self, async_client, mock_prisma_db):
        """Test filtering monitoring sources"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.monitoringsource.find_many = AsyncMock(return_value=[])
        
        response = await async_client.get(
            "/api/v1/monitoring/sources",
            params={
                "jurisdiction_id": "jur-1",
                "source_type": "api",
                "active": True
            }
        )
        
        assert response.status_code == 200
        # Verify filters
        call_args = mock_prisma_db.monitoringsource.find_many.call_args
        where_clause = call_args.kwargs.get("where")
        assert where_clause["jurisdictionId"] == "jur-1"
        assert where_clause["sourceType"] == "api"
        assert where_clause["active"] is True
    
    @pytest.mark.asyncio
    async def test_create_monitoring_source_success(self, async_client, mock_prisma_db):
        """Test creating a monitoring source"""
        from unittest.mock import AsyncMock
        
        class MockJurisdiction:
            def __init__(self):
                self.id = "jurisdiction-1"
                self.name = "Test Jurisdiction"
                self.code = "TEST"
        
        class MockSource:
            def __init__(self):
                self.id = "source-1"
                self.jurisdictionId = "jurisdiction-1"
                self.sourceType = "rss"
                self.url = "https://example.com/feed.xml"
                self.checkInterval = 3600
                self.lastCheckedAt = None
                self.lastHash = None
                self.active = True
                self.createdAt = datetime.now()
                self.updatedAt = datetime.now()
        
        mock_prisma_db.jurisdiction.find_unique = AsyncMock(return_value=MockJurisdiction())
        mock_prisma_db.monitoringsource.create = AsyncMock(return_value=MockSource())
        
        source_data = {
            "jurisdictionId": "jurisdiction-1",
            "sourceType": "rss",
            "url": "https://example.com/feed.xml",
            "checkInterval": 3600,
            "active": True
        }
        
        response = await async_client.post("/api/v1/monitoring/sources", json=source_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["jurisdictionId"] == "jurisdiction-1"
        assert data["sourceType"] == "rss"
    
    @pytest.mark.asyncio
    async def test_create_monitoring_source_jurisdiction_not_found(self, async_client, mock_prisma_db):
        """Test creating source with non-existent jurisdiction"""
        from unittest.mock import AsyncMock
        
        mock_prisma_db.jurisdiction.find_unique = AsyncMock(return_value=None)
        
        source_data = {
            "jurisdictionId": "invalid-jurisdiction",
            "sourceType": "rss",
            "url": "https://example.com/feed.xml"
        }
        
        response = await async_client.post("/api/v1/monitoring/sources", json=source_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_create_monitoring_source_invalid_type(self, async_client, mock_prisma_db):
        """Test creating source with invalid source type"""
        from unittest.mock import AsyncMock
        
        class MockJurisdiction:
            def __init__(self):
                self.id = "jurisdiction-1"
                self.name = "Test Jurisdiction"
        
        mock_prisma_db.jurisdiction.find_unique = AsyncMock(return_value=MockJurisdiction())
        
        source_data = {
            "jurisdictionId": "jurisdiction-1",
            "sourceType": "invalid_type",
            "url": "https://example.com/feed.xml"
        }
        
        response = await async_client.post("/api/v1/monitoring/sources", json=source_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "invalid source type" in data["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_create_monitoring_source_with_defaults(self, async_client, mock_prisma_db):
        """Test creating source uses default values"""
        from unittest.mock import AsyncMock
        
        class MockJurisdiction:
            def __init__(self):
                self.id = "jurisdiction-1"
                self.name = "Test Jurisdiction"
        
        class MockSource:
            def __init__(self):
                self.id = "source-1"
                self.jurisdictionId = "jurisdiction-1"
                self.sourceType = "api"
                self.url = "https://api.example.com"
                self.checkInterval = 3600  # Default
                self.lastCheckedAt = None
                self.lastHash = None
                self.active = True  # Default
                self.createdAt = datetime.now()
                self.updatedAt = datetime.now()
        
        mock_prisma_db.jurisdiction.find_unique = AsyncMock(return_value=MockJurisdiction())
        mock_prisma_db.monitoringsource.create = AsyncMock(return_value=MockSource())
        
        # Minimal data (using defaults)
        source_data = {
            "jurisdictionId": "jurisdiction-1",
            "sourceType": "api",
            "url": "https://api.example.com"
        }
        
        response = await async_client.post("/api/v1/monitoring/sources", json=source_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["checkInterval"] == 3600
        assert data["active"] is True

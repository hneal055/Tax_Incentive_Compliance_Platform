"""
Tests for monitoring service - data collection and change detection
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.monitoring_service import MonitoringService


class TestMonitoringService:
    """Test monitoring service functionality"""
    
    def test_compute_hash(self):
        """Test content hashing"""
        service = MonitoringService()
        
        content1 = "This is test content"
        content2 = "This is test content"
        content3 = "Different content"
        
        hash1 = service.compute_hash(content1)
        hash2 = service.compute_hash(content2)
        hash3 = service.compute_hash(content3)
        
        # Same content should produce same hash
        assert hash1 == hash2
        # Different content should produce different hash
        assert hash1 != hash3
        # Hash should be 64 characters (SHA-256 hex)
        assert len(hash1) == 64
    
    @pytest.mark.asyncio
    async def test_initialize_and_shutdown(self):
        """Test service initialization and shutdown"""
        service = MonitoringService()
        
        assert service.session is None
        
        await service.initialize()
        assert service.session is not None
        
        await service.shutdown()
        assert service.session is None
    
    @pytest.mark.asyncio
    async def test_fetch_rss_feed_success(self):
        """Test successful RSS feed fetching"""
        service = MonitoringService()
        await service.initialize()
        
        # Mock RSS feed response
        mock_feed_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Test Feed</title>
        <item>
            <title>Test Item 1</title>
            <link>http://example.com/1</link>
            <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
            <description>Test description 1</description>
        </item>
    </channel>
</rss>"""
        
        with patch.object(service.session, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.text = AsyncMock(return_value=mock_feed_content)
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await service.fetch_rss_feed('http://example.com/feed.xml')
        
        assert result['success'] is True
        assert 'hash' in result
        assert len(result['entries']) > 0
        assert result['entries'][0]['title'] == 'Test Item 1'
        
        await service.shutdown()
    
    @pytest.mark.asyncio
    async def test_fetch_rss_feed_error(self):
        """Test RSS feed fetching with error"""
        service = MonitoringService()
        await service.initialize()
        
        with patch.object(service.session, 'get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            result = await service.fetch_rss_feed('http://example.com/feed.xml')
        
        assert result['success'] is False
        assert 'error' in result
        assert result['error'] == "Network error"
        
        await service.shutdown()
    
    @pytest.mark.asyncio
    async def test_fetch_webpage_success(self):
        """Test successful webpage fetching"""
        service = MonitoringService()
        await service.initialize()
        
        html_content = """
        <!DOCTYPE html>
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Test Content</h1>
                <p>This is test content</p>
                <script>console.log('remove me');</script>
            </body>
        </html>
        """
        
        with patch.object(service.session, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.text = AsyncMock(return_value=html_content)
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await service.fetch_webpage('http://example.com')
        
        assert result['success'] is True
        assert 'hash' in result
        assert result['title'] == 'Test Page'
        assert 'Test Content' in result['content']
        # Script should be removed
        assert 'console.log' not in result['content']
        
        await service.shutdown()
    
    @pytest.mark.asyncio
    async def test_fetch_api_endpoint_success(self):
        """Test successful API endpoint fetching"""
        service = MonitoringService()
        await service.initialize()
        
        json_data = {"key": "value", "number": 123}
        
        with patch.object(service.session, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=json_data)
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await service.fetch_api_endpoint('http://api.example.com/data')
        
        assert result['success'] is True
        assert 'hash' in result
        assert result['data'] == json_data
        
        await service.shutdown()
    
    @pytest.mark.asyncio
    async def test_check_source_detects_changes(self):
        """Test change detection"""
        service = MonitoringService()
        await service.initialize()
        
        json_data = {"value": 100}
        
        with patch.object(service.session, 'get') as mock_get:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=json_data)
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # First check - no previous hash
            result1 = await service.check_source('api', 'http://api.example.com', None)
            assert result1['is_new'] is True
            assert result1.get('changed') is False
            
            # Second check - same hash
            result2 = await service.check_source('api', 'http://api.example.com', result1['hash'])
            assert result2['is_new'] is False
            assert result2['changed'] is False
            
            # Third check - different hash
            different_hash = "0" * 64
            result3 = await service.check_source('api', 'http://api.example.com', different_hash)
            assert result3['changed'] is True
        
        await service.shutdown()
    
    @pytest.mark.asyncio
    async def test_check_source_invalid_type(self):
        """Test check_source with invalid source type"""
        service = MonitoringService()
        
        result = await service.check_source('invalid_type', 'http://example.com', None)
        
        assert result['success'] is False
        assert 'Unknown source type' in result['error']

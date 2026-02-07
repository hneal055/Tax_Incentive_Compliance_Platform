"""
Tests for event processor - event classification and creation
"""
import pytest
from unittest.mock import AsyncMock, patch
from src.services.event_processor import EventProcessor


class TestEventProcessor:
    """Test event processor functionality"""
    
    def test_classify_event_new_program(self):
        """Test classification of new program events"""
        content = "Announcing new tax credit program for film productions"
        event_type, severity = EventProcessor.classify_event(content)
        
        assert event_type == 'new_program'
        assert severity == 'warning'
    
    def test_classify_event_expiration(self):
        """Test classification of expiration events"""
        content = "Tax credit program expiring on December 31st"
        event_type, severity = EventProcessor.classify_event(content)
        
        assert event_type == 'expiration'
        assert severity == 'critical'
    
    def test_classify_event_incentive_change(self):
        """Test classification of incentive change events"""
        content = "Film tax credit percentage increased from 20% to 25%"
        event_type, severity = EventProcessor.classify_event(content)
        
        assert event_type == 'incentive_change'
        assert severity in ['info', 'warning']
    
    def test_classify_event_news(self):
        """Test classification of general news events"""
        content = "Local film industry celebrates successful year"
        event_type, severity = EventProcessor.classify_event(content)
        
        assert event_type == 'news'
        assert severity == 'info'
    
    def test_classify_event_critical_keywords(self):
        """Test that critical keywords upgrade severity"""
        content = "URGENT: Film incentive program deadline approaching"
        event_type, severity = EventProcessor.classify_event(content)
        
        assert severity == 'critical'
    
    @pytest.mark.asyncio
    async def test_create_event_from_rss(self, mock_prisma_db):
        """Test creating events from RSS entries"""
        entries = [
            {
                'title': 'New Tax Credit Announced',
                'summary': 'State announces new film tax credit program',
                'link': 'http://example.com/news/1'
            },
            {
                'title': 'Incentive Update',
                'summary': 'Changes to existing incentive program',
                'link': 'http://example.com/news/2'
            }
        ]
        
        # Mock prisma event creation
        mock_event = type('Event', (), {
            'id': 'test-event-id',
            'jurisdictionId': 'jurisdiction-1',
            'eventType': 'new_program',
            'severity': 'warning',
            'title': 'New Tax Credit Announced',
            'detectedAt': None
        })()
        
        mock_prisma_db.monitoringevent.create = AsyncMock(return_value=mock_event)
        
        with patch('src.services.event_processor.prisma', mock_prisma_db):
            event_ids = await EventProcessor.create_event_from_rss(
                jurisdiction_id='jurisdiction-1',
                source_id='source-1',
                entries=entries
            )
        
        # Should create events for the entries
        assert len(event_ids) == 2
        assert mock_prisma_db.monitoringevent.create.call_count == 2
    
    @pytest.mark.asyncio
    async def test_create_event_from_rss_limits_entries(self, mock_prisma_db):
        """Test that RSS events are limited to 5 most recent"""
        # Create 10 entries
        entries = [
            {
                'title': f'News Item {i}',
                'summary': f'Summary {i}',
                'link': f'http://example.com/news/{i}'
            }
            for i in range(10)
        ]
        
        mock_event = type('Event', (), {'id': 'test-id', 'detectedAt': None})()
        mock_prisma_db.monitoringevent.create = AsyncMock(return_value=mock_event)
        
        with patch('src.services.event_processor.prisma', mock_prisma_db):
            event_ids = await EventProcessor.create_event_from_rss(
                jurisdiction_id='jurisdiction-1',
                source_id='source-1',
                entries=entries
            )
        
        # Should only create 5 events
        assert len(event_ids) == 5
        assert mock_prisma_db.monitoringevent.create.call_count == 5
    
    @pytest.mark.asyncio
    async def test_create_event_from_change(self, mock_prisma_db):
        """Test creating event from detected change"""
        mock_event = type('Event', (), {
            'id': 'change-event-id',
            'jurisdictionId': 'jurisdiction-1',
            'eventType': 'incentive_change',
            'severity': 'warning',
            'title': 'Content Change Detected',
            'detectedAt': None
        })()
        
        mock_prisma_db.monitoringevent.create = AsyncMock(return_value=mock_event)
        
        with patch('src.services.event_processor.prisma', mock_prisma_db):
            event_id = await EventProcessor.create_event_from_change(
                jurisdiction_id='jurisdiction-1',
                source_id='source-1',
                source_type='webpage',
                title='Content Change Detected',
                content='Tax credit percentage updated',
                source_url='http://example.com'
            )
        
        assert event_id == 'change-event-id'
        assert mock_prisma_db.monitoringevent.create.called
    
    @pytest.mark.asyncio
    async def test_create_event_truncates_long_summary(self, mock_prisma_db):
        """Test that long summaries are truncated"""
        mock_event = type('Event', (), {'id': 'test-id', 'detectedAt': None})()
        mock_prisma_db.monitoringevent.create = AsyncMock(return_value=mock_event)
        
        # Create content longer than 300 characters
        long_content = "A" * 500
        
        with patch('src.services.event_processor.prisma', mock_prisma_db):
            event_id = await EventProcessor.create_event_from_change(
                jurisdiction_id='jurisdiction-1',
                source_id='source-1',
                source_type='api',
                title='Test',
                content=long_content,
                source_url='http://example.com'
            )
        
        # Check that summary was truncated
        call_args = mock_prisma_db.monitoringevent.create.call_args
        summary = call_args.kwargs['data']['summary']
        assert len(summary) <= 303  # 300 + "..."
        assert summary.endswith('...')

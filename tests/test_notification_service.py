"""
Tests for Notification Services
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.notification_service import (
    email_notification_service,
    slack_notification_service
)


@pytest.fixture
def sample_event():
    """Sample monitoring event for testing"""
    return {
        'id': 'test-event-id',
        'title': 'California Film Tax Credit Increased',
        'summary': 'California announced an increase in film tax credit from 20% to 25%.',
        'eventType': 'incentive_change',
        'severity': 'critical',
        'sourceUrl': 'https://film.ca.gov/news/2026-update',
        'detectedAt': '2026-01-15T10:00:00Z'
    }


@pytest.mark.asyncio
async def test_email_notification_disabled():
    """Test email notification when service is disabled"""
    # Temporarily disable service
    original_enabled = email_notification_service.enabled
    email_notification_service.enabled = False
    
    try:
        result = await email_notification_service.send_event_notification(
            {'title': 'Test', 'summary': 'Test event'},
            'California'
        )
        
        assert result is False
    finally:
        email_notification_service.enabled = original_enabled


@pytest.mark.asyncio
async def test_slack_notification_disabled():
    """Test Slack notification when service is disabled"""
    # Temporarily disable service
    original_enabled = slack_notification_service.enabled
    slack_notification_service.enabled = False
    
    try:
        result = await slack_notification_service.send_event_notification(
            {'title': 'Test', 'summary': 'Test event'},
            'California'
        )
        
        assert result is False
    finally:
        slack_notification_service.enabled = original_enabled


@pytest.mark.asyncio
async def test_slack_notification_success(sample_event):
    """Test successful Slack notification"""
    # Mock aiohttp session
    mock_response = AsyncMock()
    mock_response.status = 200
    
    mock_session = AsyncMock()
    mock_session.post.return_value.__aenter__.return_value = mock_response
    
    # Temporarily enable service and set mock session
    original_enabled = slack_notification_service.enabled
    original_session = slack_notification_service.session
    
    slack_notification_service.enabled = True
    slack_notification_service.session = mock_session
    
    try:
        result = await slack_notification_service.send_event_notification(
            sample_event,
            'California'
        )
        
        assert result is True
        assert mock_session.post.called
    finally:
        slack_notification_service.enabled = original_enabled
        slack_notification_service.session = original_session


@pytest.mark.asyncio
async def test_slack_notification_formats_message(sample_event):
    """Test Slack notification message formatting"""
    mock_response = AsyncMock()
    mock_response.status = 200
    
    mock_session = AsyncMock()
    mock_session.post.return_value.__aenter__.return_value = mock_response
    
    original_enabled = slack_notification_service.enabled
    original_session = slack_notification_service.session
    
    slack_notification_service.enabled = True
    slack_notification_service.session = mock_session
    
    try:
        await slack_notification_service.send_event_notification(
            sample_event,
            'California'
        )
        
        # Check that post was called with proper structure
        call_args = mock_session.post.call_args
        assert call_args is not None
        
        # Verify JSON payload contains expected fields
        json_payload = call_args[1]['json']
        assert 'blocks' in json_payload
        assert 'channel' in json_payload
        
        # Verify critical severity uses danger color
        assert any(
            attachment.get('color') == 'danger'
            for attachment in json_payload.get('attachments', [])
        )
        
    finally:
        slack_notification_service.enabled = original_enabled
        slack_notification_service.session = original_session


def test_email_service_initialization():
    """Test email service initialization"""
    # Service should read from environment
    assert hasattr(email_notification_service, 'smtp_host')
    assert hasattr(email_notification_service, 'smtp_port')
    assert hasattr(email_notification_service, 'from_email')


def test_slack_service_initialization():
    """Test Slack service initialization"""
    # Service should read from environment
    assert hasattr(slack_notification_service, 'webhook_url')
    assert hasattr(slack_notification_service, 'channel')

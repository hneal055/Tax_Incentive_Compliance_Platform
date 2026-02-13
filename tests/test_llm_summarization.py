"""
Tests for LLM Summarization Service
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.llm_summarization import llm_summarization_service


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    with patch('src.services.llm_summarization.AsyncOpenAI') as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value = mock_instance
        
        # Mock chat completions response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "California increased film tax credit from 20% to 25% effective January 1, 2026. Cap raised from $100M to $150M annually. Productions must meet new diversity requirements."
        
        mock_instance.chat.completions.create = AsyncMock(return_value=mock_response)
        
        yield mock_instance


@pytest.mark.asyncio
async def test_summarize_tax_incentive_change_with_llm(mock_openai_client):
    """Test LLM summarization of tax incentive change"""
    # Initialize service with mock client
    llm_summarization_service.client = mock_openai_client
    
    # Test summarization
    summary = await llm_summarization_service.summarize_tax_incentive_change(
        title="California Film Tax Credit Increased",
        content="The California Film Commission announced an increase in the film tax credit percentage from 20% to 25%. The annual cap has been raised from $100 million to $150 million. New diversity requirements are now in effect.",
        jurisdiction="California",
        source_url="https://film.ca.gov/news/2026-credit-increase"
    )
    
    assert summary is not None
    assert len(summary) > 0
    assert "25%" in summary or "California" in summary


@pytest.mark.asyncio
async def test_summarize_without_llm_client():
    """Test fallback when LLM client is not initialized"""
    # Temporarily set client to None
    original_client = llm_summarization_service.client
    llm_summarization_service.client = None
    
    try:
        # Test fallback to truncated content
        content = "This is a long content that should be truncated" * 20
        summary = await llm_summarization_service.summarize_tax_incentive_change(
            title="Test Title",
            content=content
        )
        
        assert summary is not None
        assert len(summary) <= 500  # Should be truncated
    finally:
        # Restore original client
        llm_summarization_service.client = original_client


@pytest.mark.asyncio
async def test_summarization_caching(mock_openai_client):
    """Test that repeated summarizations use cache"""
    llm_summarization_service.client = mock_openai_client
    llm_summarization_service._cache.clear()  # Clear cache
    
    title = "Test Caching"
    content = "This is test content for caching"
    
    # First call - should hit API
    summary1 = await llm_summarization_service.summarize_tax_incentive_change(title, content)
    call_count_1 = mock_openai_client.chat.completions.create.call_count
    
    # Second call - should use cache
    summary2 = await llm_summarization_service.summarize_tax_incentive_change(title, content)
    call_count_2 = mock_openai_client.chat.completions.create.call_count
    
    # Verify cache was used (API not called again)
    assert call_count_1 == call_count_2
    assert summary1 == summary2


@pytest.mark.asyncio
async def test_enhance_event_summary():
    """Test enhancing event summary"""
    llm_summarization_service.client = None  # Test without LLM
    
    event_data = {
        'title': 'Georgia Film Tax Credit Update',
        'summary': 'Georgia announced changes to their film tax credit program.',
        'jurisdictionId': 'test-jurisdiction-id',
        'sourceUrl': 'https://example.com/news'
    }
    
    enhanced = await llm_summarization_service.enhance_event_summary(event_data)
    
    # Should return original summary as fallback
    assert enhanced is not None
    assert len(enhanced) > 0

"""
LLM Summarization Service - Uses OpenAI to summarize monitoring events
"""
import logging
from typing import Optional, Dict, Any
import os
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class LLMSummarizationService:
    """Service for AI-powered event summarization"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.client: Optional[AsyncOpenAI] = None
        
        # Cache for summaries to avoid redundant API calls
        self._cache: Dict[str, str] = {}
        self._max_cache_size = 100
    
    async def initialize(self):
        """Initialize the OpenAI client"""
        if not self.api_key:
            logger.warning("⚠️  OPENAI_API_KEY not configured - LLM summarization disabled")
            return
        
        try:
            self.client = AsyncOpenAI(api_key=self.api_key)
            logger.info("✅ OpenAI client initialized for summarization")
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI client: {e}")
    
    async def shutdown(self):
        """Clean up resources"""
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("🛑 OpenAI client shut down")
    
    def _get_cache_key(self, content: str) -> str:
        """Generate cache key from content"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()
    
    async def summarize_tax_incentive_change(
        self,
        title: str,
        content: str,
        jurisdiction: Optional[str] = None,
        source_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Summarize a tax incentive change using LLM
        
        Args:
            title: Event title
            content: Event content/description
            jurisdiction: Optional jurisdiction name
            source_url: Optional source URL
            
        Returns:
            Summarized text or None if summarization fails
        """
        if not self.client:
            logger.debug("OpenAI client not initialized - returning original content")
            return content[:500]  # Fallback to truncated content
        
        # Check cache
        cache_key = self._get_cache_key(f"{title}:{content}")
        if cache_key in self._cache:
            logger.debug("📋 Using cached summary")
            return self._cache[cache_key]
        
        # Build prompt
        jurisdiction_text = f" for {jurisdiction}" if jurisdiction else ""
        prompt = f"""You are an expert analyst for film production companies monitoring tax incentive programs.

Summarize this tax incentive update{jurisdiction_text} for a film production executive. Focus on:
1. What changed (credit percentage, cap amounts, qualifying expenses, etc.)
2. Effective date or deadline (if mentioned)
3. Impact on qualifying productions
4. Any action items or important notes

Be concise (max 3-4 sentences) and highlight only the most critical information.

Title: {title}
Content: {content[:1000]}
"""
        
        if source_url:
            prompt += f"\nSource: {source_url}"
        
        try:
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a concise tax incentive analyst for the film industry."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.3,  # Lower temperature for more factual summaries
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Cache the result
            if len(self._cache) >= self._max_cache_size:
                # Remove oldest entry (simple FIFO)
                self._cache.pop(next(iter(self._cache)))
            self._cache[cache_key] = summary
            
            logger.info(f"✨ Generated LLM summary ({len(summary)} chars)")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating LLM summary: {e}")
            return content[:500]  # Fallback to truncated content
    
    async def enhance_event_summary(self, event_data: Dict[str, Any]) -> str:
        """
        Enhance an event summary using LLM
        
        Args:
            event_data: Event data dictionary with title, summary, etc.
            
        Returns:
            Enhanced summary text
        """
        title = event_data.get('title', '')
        current_summary = event_data.get('summary', '')
        jurisdiction_id = event_data.get('jurisdictionId')
        source_url = event_data.get('sourceUrl')
        
        # Get jurisdiction name if available
        jurisdiction_name = None
        if jurisdiction_id:
            try:
                from src.utils.database import prisma
                jurisdiction = await prisma.jurisdiction.find_unique(
                    where={'id': jurisdiction_id}
                )
                if jurisdiction:
                    jurisdiction_name = jurisdiction.name
            except Exception as e:
                logger.debug(f"Could not fetch jurisdiction: {e}")
        
        # Generate enhanced summary
        enhanced = await self.summarize_tax_incentive_change(
            title=title,
            content=current_summary,
            jurisdiction=jurisdiction_name,
            source_url=source_url
        )
        
        return enhanced or current_summary


# Global LLM summarization service instance
llm_summarization_service = LLMSummarizationService()

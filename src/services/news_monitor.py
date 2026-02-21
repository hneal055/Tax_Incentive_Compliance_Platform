"""
News Monitor Service - Integrates with NewsAPI for legislative monitoring
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import os
from newsapi import NewsApiClient

from src.utils.database import prisma
from src.services.event_processor import event_processor

logger = logging.getLogger(__name__)


class NewsMonitorService:
    """Service for monitoring news sources via NewsAPI"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.client: Optional[NewsApiClient] = None
        
        # Keywords for film tax incentive monitoring
        self.base_keywords = [
            'film tax credit',
            'production incentive', 
            'film rebate',
            'entertainment tax',
            'film commission',
            'production tax credit'
        ]
        
        # Jurisdiction-specific keywords
        self.jurisdiction_keywords = {
            'california': ['California film tax credit', 'CA film incentive'],
            'new_york': ['New York film tax credit', 'NY production incentive'],
            'georgia': ['Georgia film tax credit', 'GA entertainment tax'],
            'louisiana': ['Louisiana film tax credit', 'LA production incentive'],
            'new_mexico': ['New Mexico film tax credit', 'NM film incentive'],
            'illinois': ['Illinois film tax credit', 'IL film production'],
            'massachusetts': ['Massachusetts film tax credit', 'MA production incentive'],
            'pennsylvania': ['Pennsylvania film tax credit', 'PA production incentive'],
            'texas': ['Texas film incentive', 'TX production tax'],
            'florida': ['Florida film tax credit', 'FL entertainment incentive'],
        }
    
    async def initialize(self):
        """Initialize the NewsAPI client"""
        if not self.api_key:
            logger.warning("⚠️  NEWS_API_KEY not configured - news monitoring disabled")
            return
        
        try:
            self.client = NewsApiClient(api_key=self.api_key)
            logger.info("✅ NewsAPI client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize NewsAPI client: {e}")
    
    async def search_news(
        self, 
        query: str, 
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        language: str = 'en',
        sort_by: str = 'publishedAt'
    ) -> List[Dict[str, Any]]:
        """
        Search news articles via NewsAPI
        
        Args:
            query: Search query
            from_date: Start date for search
            to_date: End date for search
            language: Language code (default: 'en')
            sort_by: Sort order (publishedAt, relevancy, popularity)
            
        Returns:
            List of article dictionaries
        """
        if not self.client:
            logger.warning("NewsAPI client not initialized")
            return []
        
        try:
            # Default to last 24 hours if no date range specified
            if not from_date:
                from_date = datetime.now(timezone.utc) - timedelta(hours=24)
            if not to_date:
                to_date = datetime.now(timezone.utc)
            
            # Format dates for API
            from_param = from_date.strftime('%Y-%m-%d')
            to_param = to_date.strftime('%Y-%m-%d')
            
            # Call NewsAPI
            response = self.client.get_everything(
                q=query,
                from_param=from_param,
                to=to_param,
                language=language,
                sort_by=sort_by,
                page_size=20  # Limit results to avoid quota
            )
            
            if response.get('status') == 'ok':
                articles = response.get('articles', [])
                logger.info(f"📰 Found {len(articles)} articles for query: {query}")
                return articles
            else:
                logger.warning(f"NewsAPI error: {response.get('message', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching news: {e}")
            return []
    
    async def monitor_jurisdiction(self, jurisdiction_code: str, jurisdiction_id: str) -> int:
        """
        Monitor news for a specific jurisdiction
        
        Args:
            jurisdiction_code: Jurisdiction code (e.g., 'california', 'new_york')
            jurisdiction_id: Database jurisdiction ID
            
        Returns:
            Number of events created
        """
        events_created = 0
        
        # Get jurisdiction-specific keywords
        keywords = self.jurisdiction_keywords.get(
            jurisdiction_code.lower().replace(' ', '_').replace('-', '_'),
            []
        )
        
        # Add base keywords
        all_keywords = keywords + self.base_keywords[:3]  # Limit to avoid quota
        
        for keyword in all_keywords:
            articles = await self.search_news(keyword)
            
            for article in articles[:5]:  # Limit to 5 most relevant per keyword
                # Check for duplicates
                existing = await prisma.monitoringevent.find_first(
                    where={
                        'sourceUrl': article.get('url', ''),
                        'jurisdictionId': jurisdiction_id
                    }
                )
                
                if existing:
                    continue  # Skip duplicates
                
                # Create event from article
                title = article.get('title', 'News Update')
                description = article.get('description', article.get('content', ''))[:500]
                source_url = article.get('url', '')
                published_at = article.get('publishedAt')
                
                # Parse published date
                detected_at = datetime.now(timezone.utc)
                if published_at:
                    try:
                        detected_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    except:
                        pass
                
                # Classify event
                from src.services.event_processor import EventProcessor
                event_type, severity = EventProcessor.classify_event(
                    f"{title} {description}"
                )
                
                # Create monitoring event
                try:
                    event = await prisma.monitoringevent.create(
                        data={
                            'jurisdictionId': jurisdiction_id,
                            'eventType': event_type,
                            'severity': severity,
                            'title': title,
                            'summary': description or "News article detected",
                            'sourceUrl': source_url,
                            'detectedAt': detected_at,
                            'metadata': f'{{"source": "NewsAPI", "keyword": "{keyword}"}}'
                        }
                    )
                    
                    events_created += 1
                    logger.info(f"📰 Created news event: {title}")
                    
                    # Broadcast via WebSocket
                    await EventProcessor._broadcast_event(event)
                    
                except Exception as e:
                    logger.error(f"Error creating news event: {e}")
        
        return events_created
    
    async def monitor_all_jurisdictions(self) -> Dict[str, int]:
        """
        Monitor news for all active jurisdictions
        
        Returns:
            Dictionary mapping jurisdiction codes to event counts
        """
        if not self.client:
            logger.warning("NewsAPI client not initialized - skipping monitoring")
            return {}
        
        results = {}
        
        try:
            # Get all active jurisdictions
            jurisdictions = await prisma.jurisdiction.find_many(
                where={'active': True}
            )
            
            logger.info(f"🔍 Monitoring news for {len(jurisdictions)} jurisdictions")
            
            for jurisdiction in jurisdictions[:10]:  # Limit to 10 to avoid quota
                code = jurisdiction.code.lower()
                events = await self.monitor_jurisdiction(code, jurisdiction.id)
                results[code] = events
            
            total_events = sum(results.values())
            logger.info(f"📊 News monitoring complete: {total_events} total events created")
            
        except Exception as e:
            logger.error(f"Error in monitor_all_jurisdictions: {e}")
        
        return results


# Global news monitor service instance
news_monitor_service = NewsMonitorService()

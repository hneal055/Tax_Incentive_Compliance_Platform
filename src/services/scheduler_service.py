"""
Scheduler Service - Background task scheduler for monitoring sources
"""
import logging
from datetime import datetime, timezone
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.utils.database import prisma
from src.services.monitoring_service import monitoring_service
from src.services.event_processor import event_processor
from src.services.news_monitor import news_monitor_service
from src.services.llm_summarization import llm_summarization_service
from src.services.notification_service import (
    email_notification_service,
    slack_notification_service
)
import os

logger = logging.getLogger(__name__)


class SchedulerService:
    """Manages scheduled monitoring tasks"""
    
    def __init__(self):
        self.scheduler: Optional[AsyncIOScheduler] = None
        self._is_running = False
    
    async def initialize(self):
        """Initialize the scheduler"""
        if self.scheduler is None:
            self.scheduler = AsyncIOScheduler()
            
            # Add job to check all active sources (RSS, webpage, API)
            self.scheduler.add_job(
                self.check_all_sources,
                IntervalTrigger(seconds=300),  # Check every 5 minutes
                id='check_all_sources',
                name='Check all monitoring sources',
                replace_existing=True
            )
            
            # Add job for news monitoring
            monitor_interval_hours = int(os.getenv('MONITOR_INTERVAL_HOURS', '4'))
            self.scheduler.add_job(
                self.check_news_sources,
                IntervalTrigger(hours=monitor_interval_hours),
                id='check_news_sources',
                name='Monitor news sources via NewsAPI',
                replace_existing=True
            )
            
            self.scheduler.start()
            self._is_running = True
            logger.info("✅ Scheduler service initialized")
    
    async def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler and self._is_running:
            self.scheduler.shutdown(wait=False)
            self._is_running = False
            logger.info("🛑 Scheduler service shut down")
    
    async def check_all_sources(self):
        """Check all active monitoring sources"""
        try:
            # Ensure monitoring service is initialized
            if not monitoring_service.session:
                await monitoring_service.initialize()
            
            # Get all active sources
            sources = await prisma.monitoringsource.find_many(
                where={'active': True},
                include={'jurisdiction': True}
            )
            
            logger.info(f"🔍 Checking {len(sources)} active monitoring sources")
            
            for source in sources:
                await self.check_source(source)
                
        except Exception as e:
            logger.error(f"Error in check_all_sources: {e}")
    
    async def check_source(self, source):
        """
        Check a single monitoring source
        
        Args:
            source: MonitoringSource database object
        """
        try:
            source_id = source.id
            source_type = source.sourceType
            url = source.url
            last_hash = source.lastHash
            jurisdiction_id = source.jurisdictionId
            
            logger.debug(f"Checking {source_type} source: {url}")
            
            # Fetch and check for changes
            result = await monitoring_service.check_source(
                source_type=source_type,
                url=url,
                last_hash=last_hash
            )
            
            if not result.get('success'):
                logger.warning(f"Failed to fetch {source_type} from {url}: {result.get('error')}")
                return
            
            # Update last checked time and hash
            await prisma.monitoringsource.update(
                where={'id': source_id},
                data={
                    'lastCheckedAt': datetime.now(timezone.utc),
                    'lastHash': result.get('hash', '')
                }
            )
            
            # Process changes
            if result.get('changed'):
                logger.info(f"🔔 Change detected in {source_type} source: {url}")
                
                # Create events based on source type
                if source_type == 'rss' and result.get('entries'):
                    # Create events from RSS entries
                    await event_processor.create_event_from_rss(
                        jurisdiction_id=jurisdiction_id,
                        source_id=source_id,
                        entries=result.get('entries', [])
                    )
                else:
                    # Create single change event
                    title = result.get('title', f"Update from {source_type} source")
                    content = result.get('content', '')[:500]
                    
                    await event_processor.create_event_from_change(
                        jurisdiction_id=jurisdiction_id,
                        source_id=source_id,
                        source_type=source_type,
                        title=title,
                        content=content,
                        source_url=url
                    )
            
            elif result.get('is_new'):
                logger.info(f"📝 First check of {source_type} source: {url} - baseline established")
            else:
                logger.debug(f"✓ No changes in {source_type} source: {url}")
                
        except Exception as e:
            logger.error(f"Error checking source {source.id}: {e}")
    
    async def check_news_sources(self):
        """Check news sources via NewsAPI"""
        try:
            logger.info("📰 Starting news monitoring cycle")
            
            # Initialize news monitor if needed
            if not news_monitor_service.client:
                await news_monitor_service.initialize()
            
            # Monitor all jurisdictions
            results = await news_monitor_service.monitor_all_jurisdictions()
            
            total_events = sum(results.values())
            if total_events > 0:
                logger.info(f"✅ News monitoring complete: {total_events} events created")
            
        except Exception as e:
            logger.error(f"Error in check_news_sources: {e}")


# Global scheduler service instance
scheduler_service = SchedulerService()

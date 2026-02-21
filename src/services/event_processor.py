"""
Event Processor - Creates monitoring events from detected changes
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from src.utils.database import prisma

logger = logging.getLogger(__name__)


class EventProcessor:
    """Process monitoring data and create events"""
    
    @staticmethod
    def classify_event(content: str, feed_data: Optional[Dict[str, Any]] = None) -> tuple[str, str]:
        """
        Classify event type and severity based on content
        
        Args:
            content: Content text to analyze
            feed_data: Optional additional data from feed
            
        Returns:
            Tuple of (event_type, severity)
        """
        content_lower = content.lower()
        
        # Keywords for classification
        incentive_keywords = ['tax credit', 'incentive', 'rebate', 'grant', 'percentage', 'credit rate']
        new_program_keywords = ['new program', 'launch', 'introduced', 'announcing']
        expiration_keywords = ['expir', 'sunset', 'ending', 'deadline', 'last day']
        critical_keywords = ['urgent', 'immediate', 'critical', 'deadline', 'expir']
        warning_keywords = ['change', 'update', 'modif', 'adjust']
        
        # Determine event type
        if any(keyword in content_lower for keyword in new_program_keywords):
            event_type = 'new_program'
            severity = 'warning'
        elif any(keyword in content_lower for keyword in expiration_keywords):
            event_type = 'expiration'
            severity = 'critical'
        elif any(keyword in content_lower for keyword in incentive_keywords):
            event_type = 'incentive_change'
            severity = 'warning' if any(kw in content_lower for kw in warning_keywords) else 'info'
        else:
            event_type = 'news'
            severity = 'info'
        
        # Upgrade to critical if urgent keywords found
        if any(keyword in content_lower for keyword in critical_keywords):
            severity = 'critical'
        
        return event_type, severity
    
    @staticmethod
    async def _broadcast_event(event):
        """Broadcast event via WebSocket (import here to avoid circular dependency)"""
        try:
            from src.services.websocket_manager import connection_manager
            event_data = {
                'id': event.id,
                'jurisdictionId': event.jurisdictionId,
                'eventType': event.eventType,
                'severity': event.severity,
                'title': event.title,
                'summary': event.summary,
                'sourceUrl': event.sourceUrl,
                'detectedAt': event.detectedAt.isoformat() if event.detectedAt else None,
            }
            await connection_manager.broadcast_event(event_data)
        except Exception as e:
            logger.error(f"Error broadcasting event: {e}")
    
    @staticmethod
    async def create_event_from_rss(
        jurisdiction_id: str,
        source_id: str,
        entries: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Create events from RSS feed entries
        
        Args:
            jurisdiction_id: Jurisdiction ID
            source_id: Source ID
            entries: List of RSS entries
            
        Returns:
            List of created event IDs
        """
        created_events = []
        
        for entry in entries[:5]:  # Limit to 5 most recent to avoid spam
            title = entry.get('title', 'No title')
            summary = entry.get('summary', '')[:500]  # Limit summary length
            link = entry.get('link', '')
            
            # Classify the entry
            event_type, severity = EventProcessor.classify_event(f"{title} {summary}")
            
            # Enhance summary with LLM if available
            try:
                from src.services.llm_summarization import llm_summarization_service
                if llm_summarization_service.client:
                    enhanced_summary = await llm_summarization_service.summarize_tax_incentive_change(
                        title=title,
                        content=summary or title,
                        source_url=link
                    )
                    if enhanced_summary:
                        summary = enhanced_summary
            except Exception as e:
                logger.debug(f"LLM summarization not available: {e}")
            
            try:
                event = await prisma.monitoringevent.create(
                    data={
                        'jurisdictionId': jurisdiction_id,
                        'sourceId': source_id,
                        'eventType': event_type,
                        'severity': severity,
                        'title': title,
                        'summary': summary or f"New update from monitoring source",
                        'sourceUrl': link,
                        'detectedAt': datetime.now(timezone.utc)
                    }
                )
                created_events.append(event.id)
                logger.info(f"📰 Created event: {title} ({event_type}/{severity})")
                
                # Broadcast via WebSocket
                await EventProcessor._broadcast_event(event)
                
                # Send notifications for critical events
                if severity == 'critical':
                    await EventProcessor._send_notifications(event, jurisdiction_id)
                
            except Exception as e:
                logger.error(f"Error creating event from RSS entry: {e}")
        
        return created_events
    
    @staticmethod
    async def create_event_from_change(
        jurisdiction_id: str,
        source_id: str,
        source_type: str,
        title: str,
        content: str,
        source_url: str
    ) -> Optional[str]:
        """
        Create event from detected change
        
        Args:
            jurisdiction_id: Jurisdiction ID
            source_id: Source ID  
            source_type: Type of source
            title: Event title
            content: Content snippet
            source_url: Original source URL
            
        Returns:
            Created event ID or None
        """
        # Classify the change
        event_type, severity = EventProcessor.classify_event(content)
        
        # Create summary
        summary = content[:300] if content else "Content change detected"
        if len(content) > 300:
            summary += "..."
        
        # Enhance summary with LLM if available
        try:
            from src.services.llm_summarization import llm_summarization_service
            if llm_summarization_service.client:
                enhanced_summary = await llm_summarization_service.summarize_tax_incentive_change(
                    title=title,
                    content=content,
                    source_url=source_url
                )
                if enhanced_summary:
                    summary = enhanced_summary
        except Exception as e:
            logger.debug(f"LLM summarization not available: {e}")
        
        try:
            event = await prisma.monitoringevent.create(
                data={
                    'jurisdictionId': jurisdiction_id,
                    'sourceId': source_id,
                    'eventType': event_type,
                    'severity': severity,
                    'title': title,
                    'summary': summary,
                    'sourceUrl': source_url,
                    'detectedAt': datetime.now(timezone.utc),
                    'metadata': f'{{"sourceType": "{source_type}"}}'
                }
            )
            logger.info(f"🔔 Created change event: {title} ({event_type}/{severity})")
            
            # Broadcast via WebSocket
            await EventProcessor._broadcast_event(event)
            
            # Send notifications for critical events
            if severity == 'critical':
                await EventProcessor._send_notifications(event, jurisdiction_id)
            
            return event.id
            
        except Exception as e:
            logger.error(f"Error creating change event: {e}")
            return None
    
    @staticmethod
    async def _send_notifications(event, jurisdiction_id: str):
        """Send notifications for critical events"""
        try:
            # Get jurisdiction name
            jurisdiction = await prisma.jurisdiction.find_unique(
                where={'id': jurisdiction_id}
            )
            jurisdiction_name = jurisdiction.name if jurisdiction else None
            
            # Convert event to dict
            event_data = {
                'title': event.title,
                'summary': event.summary,
                'eventType': event.eventType,
                'severity': event.severity,
                'sourceUrl': event.sourceUrl,
                'detectedAt': event.detectedAt.isoformat() if event.detectedAt else None
            }
            
            # Send email notification
            from src.services.notification_service import email_notification_service
            if email_notification_service.enabled:
                await email_notification_service.send_event_notification(
                    event_data, jurisdiction_name
                )
            
            # Send Slack notification
            from src.services.notification_service import slack_notification_service
            if slack_notification_service.enabled:
                await slack_notification_service.send_event_notification(
                    event_data, jurisdiction_name
                )
                
        except Exception as e:
            logger.error(f"Error sending notifications: {e}")


# Global event processor instance
event_processor = EventProcessor()

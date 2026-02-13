"""
Notification Services - Email and Slack notifications for monitoring events
"""
import logging
from typing import List, Optional, Dict, Any
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiohttp

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service for sending email notifications"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('NOTIFICATION_FROM_EMAIL', 'noreply@pilotforge.com')
        self.to_emails = os.getenv('NOTIFICATION_TO_EMAILS', '').split(',')
        self.enabled = bool(self.smtp_user and self.smtp_password)
    
    async def initialize(self):
        """Initialize email service"""
        if not self.enabled:
            logger.warning("⚠️  Email notifications not configured - missing SMTP credentials")
        else:
            logger.info(f"✅ Email notifications enabled (to: {', '.join(self.to_emails)})")
    
    async def send_event_notification(
        self,
        event: Dict[str, Any],
        jurisdiction_name: Optional[str] = None
    ) -> bool:
        """
        Send email notification for a monitoring event
        
        Args:
            event: Event data dictionary
            jurisdiction_name: Optional jurisdiction name
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.debug("Email notifications disabled")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🔔 PilotForge Alert: {event.get('title', 'Tax Incentive Update')}"
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            
            # Build email body
            jurisdiction_text = f" - {jurisdiction_name}" if jurisdiction_name else ""
            severity_emoji = {
                'critical': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(event.get('severity', 'info'), 'ℹ️')
            
            # Plain text version
            text = f"""
{severity_emoji} Tax Incentive Alert{jurisdiction_text}

{event.get('title', 'Update')}

{event.get('summary', 'No details available')}

Type: {event.get('eventType', 'unknown')}
Severity: {event.get('severity', 'info')}
Detected: {event.get('detectedAt', 'Unknown')}

{f"Source: {event.get('sourceUrl', '')}" if event.get('sourceUrl') else ''}

---
This is an automated alert from PilotForge
Tax Incentive Intelligence for Film & TV
"""
            
            # HTML version
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1e3a8a; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9fafb; padding: 20px; border: 1px solid #e5e7eb; }}
        .severity-critical {{ color: #dc2626; font-weight: bold; }}
        .severity-warning {{ color: #f59e0b; font-weight: bold; }}
        .severity-info {{ color: #3b82f6; font-weight: bold; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; }}
        a {{ color: #2563eb; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>{severity_emoji} Tax Incentive Alert{jurisdiction_text}</h2>
        </div>
        <div class="content">
            <h3>{event.get('title', 'Update')}</h3>
            <p>{event.get('summary', 'No details available')}</p>
            
            <p>
                <strong>Type:</strong> {event.get('eventType', 'unknown')}<br>
                <strong>Severity:</strong> <span class="severity-{event.get('severity', 'info')}">{event.get('severity', 'info').upper()}</span><br>
                <strong>Detected:</strong> {event.get('detectedAt', 'Unknown')}
            </p>
            
            {f'<p><a href="{event.get("sourceUrl")}">View Source</a></p>' if event.get('sourceUrl') else ''}
        </div>
        <div class="footer">
            <p>This is an automated alert from <strong>PilotForge</strong></p>
            <p>Tax Incentive Intelligence for Film & TV</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Attach both versions
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"📧 Email notification sent: {event.get('title', 'Update')}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False


class SlackNotificationService:
    """Service for sending Slack notifications"""
    
    def __init__(self):
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.channel = os.getenv('SLACK_CHANNEL', '#pilotforge-alerts')
        self.enabled = bool(self.webhook_url)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self):
        """Initialize Slack service"""
        if not self.enabled:
            logger.warning("⚠️  Slack notifications not configured - missing webhook URL")
        else:
            self.session = aiohttp.ClientSession()
            logger.info(f"✅ Slack notifications enabled (channel: {self.channel})")
    
    async def shutdown(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def send_event_notification(
        self,
        event: Dict[str, Any],
        jurisdiction_name: Optional[str] = None
    ) -> bool:
        """
        Send Slack notification for a monitoring event
        
        Args:
            event: Event data dictionary
            jurisdiction_name: Optional jurisdiction name
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled or not self.session:
            logger.debug("Slack notifications disabled")
            return False
        
        try:
            # Build Slack message
            jurisdiction_text = f" - {jurisdiction_name}" if jurisdiction_name else ""
            severity_emoji = {
                'critical': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(event.get('severity', 'info'), 'ℹ️')
            
            color = {
                'critical': 'danger',
                'warning': 'warning',
                'info': 'good'
            }.get(event.get('severity', 'info'), 'good')
            
            # Build Slack blocks
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{severity_emoji} Tax Incentive Alert{jurisdiction_text}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{event.get('title', 'Update')}*\n\n{event.get('summary', 'No details available')}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Type:*\n{event.get('eventType', 'unknown')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Severity:*\n{event.get('severity', 'info').upper()}"
                        }
                    ]
                }
            ]
            
            # Add source link if available
            if event.get('sourceUrl'):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{event.get('sourceUrl')}|View Source>"
                    }
                })
            
            # Send to Slack
            payload = {
                "channel": self.channel,
                "blocks": blocks,
                "attachments": [{
                    "color": color,
                    "footer": "PilotForge - Tax Incentive Intelligence",
                    "ts": int(event.get('detectedAt', 0))
                }]
            }
            
            async with self.session.post(self.webhook_url, json=payload) as response:
                if response.status == 200:
                    logger.info(f"💬 Slack notification sent: {event.get('title', 'Update')}")
                    return True
                else:
                    logger.error(f"Slack API error: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
            return False


# Global notification service instances
email_notification_service = EmailNotificationService()
slack_notification_service = SlackNotificationService()

"""
Monitoring Service - Fetches content from external sources and detects changes
"""
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import aiohttp
import feedparser
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class MonitoringService:
    """Service for fetching and monitoring external sources"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self):
        """Initialize the service with an aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            logger.info("✅ Monitoring service initialized")
    
    async def shutdown(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("🛑 Monitoring service shut down")
    
    @staticmethod
    def compute_hash(content: str) -> str:
        """
        Compute SHA-256 hash of content for change detection
        
        Args:
            content: String content to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    async def fetch_rss_feed(self, url: str) -> Dict[str, Any]:
        """
        Fetch and parse RSS feed
        
        Args:
            url: RSS feed URL
            
        Returns:
            Dictionary with content and metadata
        """
        try:
            if not self.session:
                await self.initialize()
            
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                response.raise_for_status()
                feed_content = await response.text()
            
            # Parse RSS feed
            feed = feedparser.parse(feed_content)
            
            # Extract entries
            entries = []
            for entry in feed.entries[:10]:  # Limit to 10 most recent
                entries.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', entry.get('description', ''))
                })
            
            # Create content string for hashing
            content = '\n'.join([
                f"{e['title']}|{e['link']}|{e['published']}"
                for e in entries
            ])
            
            return {
                'success': True,
                'content': content,
                'hash': self.compute_hash(content),
                'entries': entries,
                'feed_title': feed.feed.get('title', 'Unknown Feed')
            }
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'hash': '',
                'entries': []
            }
    
    async def fetch_webpage(self, url: str) -> Dict[str, Any]:
        """
        Fetch and parse webpage content
        
        Args:
            url: Webpage URL
            
        Returns:
            Dictionary with content and metadata
        """
        try:
            if not self.session:
                await self.initialize()
            
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                response.raise_for_status()
                html_content = await response.text()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Extract title
            title = soup.title.string if soup.title else "No title"
            
            return {
                'success': True,
                'content': text_content[:10000],  # Limit content size
                'hash': self.compute_hash(text_content[:10000]),
                'title': title,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error fetching webpage {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'hash': ''
            }
    
    async def fetch_api_endpoint(self, url: str) -> Dict[str, Any]:
        """
        Fetch JSON data from API endpoint
        
        Args:
            url: API endpoint URL
            
        Returns:
            Dictionary with content and metadata
        """
        try:
            if not self.session:
                await self.initialize()
            
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                response.raise_for_status()
                json_data = await response.json()
            
            # Convert to string for hashing
            import json
            content = json.dumps(json_data, sort_keys=True)
            
            return {
                'success': True,
                'content': content,
                'hash': self.compute_hash(content),
                'data': json_data
            }
            
        except Exception as e:
            logger.error(f"Error fetching API {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'hash': '',
                'data': None
            }
    
    async def check_source(self, source_type: str, url: str, last_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Check a monitoring source and detect changes
        
        Args:
            source_type: Type of source (rss, api, webpage)
            url: Source URL
            last_hash: Previous content hash for change detection
            
        Returns:
            Dictionary with fetch results and change detection
        """
        # Fetch based on source type
        if source_type == 'rss':
            result = await self.fetch_rss_feed(url)
        elif source_type == 'api':
            result = await self.fetch_api_endpoint(url)
        elif source_type == 'webpage':
            result = await self.fetch_webpage(url)
        else:
            return {
                'success': False,
                'error': f'Unknown source type: {source_type}'
            }
        
        # Check for changes
        if result.get('success'):
            current_hash = result.get('hash', '')
            result['changed'] = last_hash is not None and current_hash != last_hash
            result['is_new'] = last_hash is None
        
        return result


# Global monitoring service instance
monitoring_service = MonitoringService()

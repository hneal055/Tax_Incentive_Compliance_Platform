"""
WebSocket Manager - Real-time event notifications
"""
import logging
from typing import Dict, Set, Optional
from fastapi import WebSocket
import json

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time notifications"""
    
    def __init__(self):
        # Store active connections: {websocket: {jurisdiction_ids}}
        self.active_connections: Dict[WebSocket, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, jurisdiction_ids: Optional[Set[str]] = None):
        """
        Accept and store a WebSocket connection
        
        Args:
            websocket: WebSocket connection
            jurisdiction_ids: Optional set of jurisdiction IDs to filter events
        """
        await websocket.accept()
        self.active_connections[websocket] = jurisdiction_ids or set()
        logger.info(f"📡 WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection
        
        Args:
            websocket: WebSocket connection to remove
        """
        if websocket in self.active_connections:
            del self.active_connections[websocket]
            logger.info(f"📴 WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send a message to a specific WebSocket connection
        
        Args:
            message: Message dictionary to send
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict, jurisdiction_id: Optional[str] = None):
        """
        Broadcast a message to all connected clients
        
        Args:
            message: Message dictionary to broadcast
            jurisdiction_id: Optional jurisdiction ID to filter recipients
        """
        disconnected = []
        
        for websocket, subscribed_jurisdictions in self.active_connections.items():
            # Filter by jurisdiction if specified
            if jurisdiction_id:
                # If client has subscribed to specific jurisdictions
                if subscribed_jurisdictions and jurisdiction_id not in subscribed_jurisdictions:
                    continue
            
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.append(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def broadcast_event(self, event_data: dict):
        """
        Broadcast a monitoring event to relevant clients
        
        Args:
            event_data: Event data dictionary
        """
        jurisdiction_id = event_data.get('jurisdictionId')
        
        message = {
            'type': 'monitoring_event',
            'event': event_data
        }
        
        await self.broadcast(message, jurisdiction_id=jurisdiction_id)
        logger.debug(f"📢 Broadcasted event: {event_data.get('title')}")


# Global connection manager instance
connection_manager = ConnectionManager()

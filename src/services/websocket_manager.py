"""
WebSocket Manager - Real-time event notifications
"""
import asyncio
import logging
from typing import Dict, Set, Optional
from fastapi import WebSocket

logger = logging.getLogger(__name__)

# Heartbeat interval in seconds – sent to all clients to keep connections alive
HEARTBEAT_INTERVAL = 30


class ConnectionManager:
    """Manages WebSocket connections for real-time notifications.

    Thread/async-safety: all mutations to ``active_connections`` are
    serialised through ``_lock`` (an :class:`asyncio.Lock`) so that
    concurrent broadcast/connect/disconnect calls cannot corrupt the
    registry.
    """

    def __init__(self):
        # Store active connections: {websocket: {jurisdiction_ids}}
        self.active_connections: Dict[WebSocket, Set[str]] = {}
        self._lock: asyncio.Lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, jurisdiction_ids: Optional[Set[str]] = None):
        """Accept and register a WebSocket connection.

        Args:
            websocket: The incoming WebSocket connection.
            jurisdiction_ids: Optional set of jurisdiction IDs the client
                wants to subscribe to.  An empty/missing set means "all".
        """
        await websocket.accept()
        async with self._lock:
            self.active_connections[websocket] = jurisdiction_ids or set()
        logger.info("📡 WebSocket connected. Total connections: %d", len(self.active_connections))

    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from the registry.

        Args:
            websocket: The connection to remove.
        """
        async with self._lock:
            self.active_connections.pop(websocket, None)
        logger.info("📴 WebSocket disconnected. Total connections: %d", len(self.active_connections))

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a single WebSocket connection.

        Args:
            message: JSON-serialisable payload.
            websocket: Target connection.
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error("Error sending message to WebSocket: %s", e)
            await self.disconnect(websocket)

    async def broadcast(self, message: dict, jurisdiction_id: Optional[str] = None):
        """Broadcast *message* to all (or filtered) connected clients.

        Args:
            message: JSON-serialisable payload.
            jurisdiction_id: When provided only clients that have not
                specified a subscription list *or* that explicitly
                subscribed to this jurisdiction will receive the message.
        """
        disconnected = []

        async with self._lock:
            snapshot = list(self.active_connections.items())

        for websocket, subscribed_jurisdictions in snapshot:
            # Jurisdiction filtering: skip clients that have a non-empty
            # subscription list that does not include this jurisdiction.
            if jurisdiction_id and subscribed_jurisdictions:
                if jurisdiction_id not in subscribed_jurisdictions:
                    continue

            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error("Error broadcasting to WebSocket: %s", e)
                disconnected.append(websocket)

        for websocket in disconnected:
            await self.disconnect(websocket)

    async def broadcast_event(self, event_data: dict):
        """Broadcast a monitoring event to relevant clients.

        Args:
            event_data: Event data dictionary (must contain at least ``id``
                and ``title``).
        """
        jurisdiction_id = event_data.get("jurisdictionId")

        message = {
            "type": "monitoring_event",
            "event": event_data,
        }

        await self.broadcast(message, jurisdiction_id=jurisdiction_id)
        logger.debug("📢 Broadcasted event: %s", event_data.get("title"))

    async def send_heartbeat(self):
        """Send a heartbeat ping to all connected clients.

        Clients that fail to receive the ping (broken connections) are
        removed from the registry automatically.
        """
        heartbeat = {"type": "heartbeat"}
        await self.broadcast(heartbeat)


# Global connection manager instance
connection_manager = ConnectionManager()

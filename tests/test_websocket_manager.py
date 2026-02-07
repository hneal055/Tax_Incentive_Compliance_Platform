"""
Tests for WebSocket connection manager
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.websocket_manager import ConnectionManager


class TestConnectionManager:
    """Test WebSocket connection manager"""
    
    @pytest.mark.asyncio
    async def test_connect_and_disconnect(self):
        """Test connecting and disconnecting WebSocket"""
        manager = ConnectionManager()
        mock_websocket = AsyncMock()
        
        # Connect
        await manager.connect(mock_websocket)
        assert mock_websocket in manager.active_connections
        assert manager.active_connections[mock_websocket] == set()
        
        # Disconnect
        manager.disconnect(mock_websocket)
        assert mock_websocket not in manager.active_connections
    
    @pytest.mark.asyncio
    async def test_connect_with_jurisdiction_filter(self):
        """Test connecting with jurisdiction filter"""
        manager = ConnectionManager()
        mock_websocket = AsyncMock()
        jurisdiction_ids = {'jur-1', 'jur-2'}
        
        await manager.connect(mock_websocket, jurisdiction_ids)
        
        assert mock_websocket in manager.active_connections
        assert manager.active_connections[mock_websocket] == jurisdiction_ids
    
    @pytest.mark.asyncio
    async def test_send_personal_message(self):
        """Test sending message to specific connection"""
        manager = ConnectionManager()
        mock_websocket = AsyncMock()
        
        await manager.connect(mock_websocket)
        
        message = {'type': 'test', 'data': 'hello'}
        await manager.send_personal_message(message, mock_websocket)
        
        mock_websocket.send_json.assert_called_once_with(message)
    
    @pytest.mark.asyncio
    async def test_broadcast_to_all(self):
        """Test broadcasting to all connections"""
        manager = ConnectionManager()
        
        # Create multiple mock WebSockets
        ws1 = AsyncMock()
        ws2 = AsyncMock()
        ws3 = AsyncMock()
        
        await manager.connect(ws1)
        await manager.connect(ws2)
        await manager.connect(ws3)
        
        message = {'type': 'broadcast', 'data': 'hello all'}
        await manager.broadcast(message)
        
        # All should receive the message
        ws1.send_json.assert_called_once_with(message)
        ws2.send_json.assert_called_once_with(message)
        ws3.send_json.assert_called_once_with(message)
    
    @pytest.mark.asyncio
    async def test_broadcast_with_jurisdiction_filter(self):
        """Test broadcasting with jurisdiction filter"""
        manager = ConnectionManager()
        
        # Create connections with different subscriptions
        ws1 = AsyncMock()  # Subscribed to jur-1
        ws2 = AsyncMock()  # Subscribed to jur-2
        ws3 = AsyncMock()  # Subscribed to all
        
        await manager.connect(ws1, {'jur-1'})
        await manager.connect(ws2, {'jur-2'})
        await manager.connect(ws3, set())
        
        message = {'type': 'event', 'jurisdictionId': 'jur-1'}
        await manager.broadcast(message, jurisdiction_id='jur-1')
        
        # Only ws1 and ws3 should receive (ws3 subscribes to all)
        ws1.send_json.assert_called_once_with(message)
        ws2.send_json.assert_not_called()
        ws3.send_json.assert_called_once_with(message)
    
    @pytest.mark.asyncio
    async def test_broadcast_handles_disconnected_clients(self):
        """Test that broadcast removes failed connections"""
        manager = ConnectionManager()
        
        ws_good = AsyncMock()
        ws_bad = AsyncMock()
        ws_bad.send_json.side_effect = Exception("Connection lost")
        
        await manager.connect(ws_good)
        await manager.connect(ws_bad)
        
        assert len(manager.active_connections) == 2
        
        message = {'type': 'test'}
        await manager.broadcast(message)
        
        # Bad connection should be removed
        assert len(manager.active_connections) == 1
        assert ws_good in manager.active_connections
        assert ws_bad not in manager.active_connections
    
    @pytest.mark.asyncio
    async def test_broadcast_event(self):
        """Test broadcasting monitoring event"""
        manager = ConnectionManager()
        mock_websocket = AsyncMock()
        
        await manager.connect(mock_websocket, {'jur-1'})
        
        event_data = {
            'id': 'event-1',
            'jurisdictionId': 'jur-1',
            'title': 'Test Event',
            'severity': 'info'
        }
        
        await manager.broadcast_event(event_data)
        
        # Should receive wrapped event
        calls = mock_websocket.send_json.call_args_list
        assert len(calls) == 1
        sent_message = calls[0][0][0]
        assert sent_message['type'] == 'monitoring_event'
        assert sent_message['event'] == event_data

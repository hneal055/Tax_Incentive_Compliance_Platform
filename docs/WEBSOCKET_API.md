# Real-Time Monitoring System - WebSocket API Documentation

## Overview

The PilotForge Real-Time Monitoring System provides WebSocket connectivity for receiving live updates about tax incentive program changes, new programs, expirations, and related news.

## WebSocket Endpoint

### Connection URL
```
ws://localhost:8000/api/v1/monitoring/ws
```

### Query Parameters

- `jurisdiction_ids` (optional): Comma-separated list of jurisdiction IDs to subscribe to
  - If not provided, receives all events
  - Example: `?jurisdiction_ids=jur-123,jur-456`

## Connection Example

### JavaScript
```javascript
// Connect to monitoring WebSocket
const ws = new WebSocket('ws://localhost:8000/api/v1/monitoring/ws?jurisdiction_ids=california-001');

ws.onopen = () => {
    console.log('Connected to monitoring system');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'connection') {
        console.log('Connection confirmed:', data);
    }
    
    if (data.type === 'monitoring_event') {
        console.log('New monitoring event:', data.event);
        // Handle event notification
        handleMonitoringEvent(data.event);
    }
};

// Send ping for keepalive
setInterval(() => {
    ws.send('ping');
}, 30000);

ws.onclose = () => {
    console.log('Disconnected from monitoring system');
};
```

### Python
```python
import asyncio
import websockets
import json

async def monitor_events(jurisdiction_ids=None):
    url = "ws://localhost:8000/api/v1/monitoring/ws"
    if jurisdiction_ids:
        url += f"?jurisdiction_ids={','.join(jurisdiction_ids)}"
    
    async with websockets.connect(url) as websocket:
        # Receive welcome message
        welcome = await websocket.recv()
        print(f"Connected: {welcome}")
        
        # Listen for events
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'monitoring_event':
                event = data['event']
                print(f"Event: {event['title']} - {event['severity']}")

# Run
asyncio.run(monitor_events(['california-001', 'georgia-001']))
```

## Message Types

### Connection Message
Sent immediately upon successful connection.

```json
{
  "type": "connection",
  "status": "connected",
  "subscriptions": ["california-001", "georgia-001"] // or "all"
}
```

### Monitoring Event Message
Sent when a new monitoring event is detected.

```json
{
  "type": "monitoring_event",
  "event": {
    "id": "evt_12345",
    "jurisdictionId": "california-001",
    "eventType": "incentive_change",
    "severity": "warning",
    "title": "Film Tax Credit Percentage Updated",
    "summary": "California film tax credit increased from 20% to 25% for qualifying productions...",
    "sourceUrl": "https://film.ca.gov/incentives/changes",
    "detectedAt": "2026-02-07T16:30:00Z"
  }
}
```

### Pong Message
Response to client ping.

```json
{
  "type": "pong"
}
```

## Event Types

The `eventType` field can be:

- **incentive_change**: Changes to existing tax incentive programs
- **new_program**: Launch of new incentive programs
- **expiration**: Program deadlines or expirations
- **news**: General news related to film incentives

## Event Severity Levels

The `severity` field indicates importance:

- **info**: General information, no immediate action required
- **warning**: Important changes that may affect planning
- **critical**: Urgent updates requiring immediate attention (e.g., approaching deadlines)

## Best Practices

### Connection Management

1. **Reconnection Logic**: Implement automatic reconnection with exponential backoff
   ```javascript
   let reconnectDelay = 1000;
   
   function connect() {
       const ws = new WebSocket(wsUrl);
       
       ws.onclose = () => {
           setTimeout(() => {
               reconnectDelay = Math.min(reconnectDelay * 2, 30000);
               connect();
           }, reconnectDelay);
       };
       
       ws.onopen = () => {
           reconnectDelay = 1000; // Reset delay on successful connection
       };
   }
   ```

2. **Keepalive**: Send periodic ping messages to maintain connection
   ```javascript
   setInterval(() => {
       if (ws.readyState === WebSocket.OPEN) {
           ws.send('ping');
       }
   }, 30000);
   ```

### Error Handling

```javascript
ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    // Log error, notify user, attempt reconnection
};
```

### Event Processing

```javascript
function handleMonitoringEvent(event) {
    // Display notification
    if (event.severity === 'critical') {
        showUrgentAlert(event);
    } else if (event.severity === 'warning') {
        showNotification(event);
    }
    
    // Update UI
    updateEventFeed(event);
    
    // Store locally
    storeEvent(event);
}
```

## Security Considerations

1. **Authentication**: In production, implement token-based authentication
   ```javascript
   const ws = new WebSocket('wss://api.pilotforge.com/monitoring/ws?token=your_auth_token');
   ```

2. **HTTPS/WSS**: Always use secure WebSocket (wss://) in production

3. **Rate Limiting**: The server may implement rate limiting on connections

## Testing

### Test Connection
```bash
# Using wscat
wscat -c "ws://localhost:8000/api/v1/monitoring/ws"

# Subscribe to specific jurisdictions
wscat -c "ws://localhost:8000/api/v1/monitoring/ws?jurisdiction_ids=california-001"
```

### Monitor Events
The WebSocket will automatically receive events as they are detected by the monitoring system.

## Integration Examples

### React Hook
```javascript
import { useEffect, useState } from 'react';

function useMonitoringEvents(jurisdictionIds) {
    const [events, setEvents] = useState([]);
    const [connected, setConnected] = useState(false);
    
    useEffect(() => {
        const url = `ws://localhost:8000/api/v1/monitoring/ws?jurisdiction_ids=${jurisdictionIds.join(',')}`;
        const ws = new WebSocket(url);
        
        ws.onopen = () => setConnected(true);
        ws.onclose = () => setConnected(false);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'monitoring_event') {
                setEvents(prev => [data.event, ...prev]);
            }
        };
        
        return () => ws.close();
    }, [jurisdictionIds]);
    
    return { events, connected };
}
```

### Vue Composable
```javascript
import { ref, onMounted, onUnmounted } from 'vue';

export function useMonitoring(jurisdictionIds) {
    const events = ref([]);
    const connected = ref(false);
    let ws = null;
    
    onMounted(() => {
        const url = `ws://localhost:8000/api/v1/monitoring/ws?jurisdiction_ids=${jurisdictionIds.join(',')}`;
        ws = new WebSocket(url);
        
        ws.onopen = () => connected.value = true;
        ws.onclose = () => connected.value = false;
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'monitoring_event') {
                events.value.unshift(data.event);
            }
        };
    });
    
    onUnmounted(() => {
        ws?.close();
    });
    
    return { events, connected };
}
```

## Support

For issues or questions about the WebSocket API, please refer to:
- API Documentation: `/docs`
- GitHub Issues: https://github.com/hneal055/Tax_Incentive_Compliance_Platform/issues

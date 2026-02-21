/**
 * WebSocket Client Manager for Real-Time Monitoring Events
 */

export type WebSocketMessage = {
  type: 'connection' | 'monitoring_event' | 'pong';
  status?: string;
  subscriptions?: string[];
  event?: any;
};

export type WebSocketConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

class WebSocketManager {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000; // Start with 1 second
  private maxReconnectDelay = 30000; // Max 30 seconds
  private pingInterval: number | null = null;
  private listeners: Set<(message: WebSocketMessage) => void> = new Set();
  private statusListeners: Set<(status: WebSocketConnectionStatus) => void> = new Set();
  private currentStatus: WebSocketConnectionStatus = 'disconnected';

  private baseUrl: string;

  constructor(baseUrl: string = 'ws://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  /**
   * Connect to WebSocket server
   */
  connect(jurisdictionIds?: string[]): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    this.updateStatus('connecting');

    // Build WebSocket URL with optional filters
    const wsUrl = jurisdictionIds && jurisdictionIds.length > 0
      ? `${this.baseUrl}/api/v1/monitoring/ws?jurisdiction_ids=${jurisdictionIds.join(',')}`
      : `${this.baseUrl}/api/v1/monitoring/ws`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected');
        this.reconnectAttempts = 0;
        this.reconnectDelay = 1000;
        this.updateStatus('connected');
        this.startPingInterval();
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.notifyListeners(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.updateStatus('error');
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.updateStatus('disconnected');
        this.stopPingInterval();
        this.attemptReconnect(jurisdictionIds);
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      this.updateStatus('error');
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.stopPingInterval();
    this.updateStatus('disconnected');
  }

  /**
   * Send a message to the server
   */
  send(message: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(typeof message === 'string' ? message : JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected, cannot send message');
    }
  }

  /**
   * Add a message listener
   */
  addListener(callback: (message: WebSocketMessage) => void): () => void {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  /**
   * Add a status listener
   */
  addStatusListener(callback: (status: WebSocketConnectionStatus) => void): () => void {
    this.statusListeners.add(callback);
    // Immediately call with current status
    callback(this.currentStatus);
    return () => this.statusListeners.delete(callback);
  }

  /**
   * Get current connection status
   */
  getStatus(): WebSocketConnectionStatus {
    return this.currentStatus;
  }

  /**
   * Private: Update status and notify listeners
   */
  private updateStatus(status: WebSocketConnectionStatus): void {
    this.currentStatus = status;
    this.statusListeners.forEach(listener => listener(status));
  }

  /**
   * Private: Notify all message listeners
   */
  private notifyListeners(message: WebSocketMessage): void {
    this.listeners.forEach(listener => listener(message));
  }

  /**
   * Private: Attempt to reconnect with exponential backoff
   */
  private attemptReconnect(jurisdictionIds?: string[]): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnect attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1),
      this.maxReconnectDelay
    );

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    setTimeout(() => {
      this.connect(jurisdictionIds);
    }, delay);
  }

  /**
   * Private: Start sending periodic ping messages
   */
  private startPingInterval(): void {
    this.stopPingInterval();
    this.pingInterval = window.setInterval(() => {
      this.send('ping');
    }, 30000); // Ping every 30 seconds
  }

  /**
   * Private: Stop ping interval
   */
  private stopPingInterval(): void {
    if (this.pingInterval !== null) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }
}

// Create singleton instance
const wsManager = new WebSocketManager(
  import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
);

export default wsManager;

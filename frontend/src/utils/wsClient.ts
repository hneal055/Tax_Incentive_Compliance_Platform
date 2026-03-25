/**
 * WebSocket client for real-time monitoring events.
 *
 * Features:
 * - Connects to ws://localhost:8000/ws/events (configurable via VITE_WS_URL or
 *   derived from VITE_API_URL).
 * - Auto-reconnects with exponential back-off (capped at MAX_DELAY_MS).
 * - Parses incoming payloads into typed MonitoringEvent objects.
 * - Provides subscribe/unsubscribe API for consumers.
 */

import type { MonitoringEvent } from '../types';

// ─── Configuration ────────────────────────────────────────────────────────────

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE = (import.meta.env.VITE_WS_URL as string | undefined) ||
  API_BASE.replace(/^http/, 'ws');

const DEFAULT_WS_URL = `${WS_BASE}/ws/events`;

const INITIAL_DELAY_MS = 1_000;   // 1 s
const MAX_DELAY_MS     = 30_000;  // 30 s
const BACKOFF_FACTOR   = 2;

// ─── Types ───────────────────────────────────────────────────────────────────

/** Parsed WebSocket message from the server. */
export type WsMessage =
  | { type: 'connection'; status: string; subscriptions: string | string[] }
  | { type: 'monitoring_event'; event: MonitoringEvent }
  | { type: 'heartbeat' }
  | { type: 'pong' };

/** Callback signature for monitoring-event subscribers. */
export type EventSubscriber = (event: MonitoringEvent) => void;

// ─── WsClient ────────────────────────────────────────────────────────────────

class WsClient {
  private url: string;
  private ws: WebSocket | null = null;
  private subscribers = new Set<EventSubscriber>();
  private reconnectDelay = INITIAL_DELAY_MS;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private stopped = false;

  constructor(url: string = DEFAULT_WS_URL) {
    this.url = url;
  }

  // ─── Public API ──────────────────────────────────────────────────────────

  /**
   * Open the WebSocket connection.  Call once, usually from a top-level
   * React effect.
   */
  connect(): void {
    this.stopped = false;
    this._open();
  }

  /**
   * Permanently close the connection and cancel any pending reconnect.
   */
  disconnect(): void {
    this.stopped = true;
    this._clearReconnect();
    this.ws?.close();
    this.ws = null;
  }

  /**
   * Register a callback that is invoked on every incoming monitoring event.
   *
   * @returns An unsubscribe function.
   */
  subscribe(cb: EventSubscriber): () => void {
    this.subscribers.add(cb);
    return () => this.unsubscribe(cb);
  }

  /** Remove a previously registered subscriber. */
  unsubscribe(cb: EventSubscriber): void {
    this.subscribers.delete(cb);
  }

  // ─── Internal ────────────────────────────────────────────────────────────

  private _open(): void {
    if (this.ws) {
      // Already open or connecting — don't create a duplicate.
      if (
        this.ws.readyState === WebSocket.OPEN ||
        this.ws.readyState === WebSocket.CONNECTING
      ) {
        return;
      }
      this.ws.close();
      this.ws = null;
    }

    try {
      const ws = new WebSocket(this.url);

      ws.onopen = () => {
        this.reconnectDelay = INITIAL_DELAY_MS; // reset back-off on success
      };

      ws.onmessage = (evt: MessageEvent<string>) => {
        this._handleMessage(evt.data);
      };

      ws.onerror = () => {
        // onerror is always followed by onclose; actual reconnect happens there.
      };

      ws.onclose = () => {
        this.ws = null;
        if (!this.stopped) {
          this._scheduleReconnect();
        }
      };

      this.ws = ws;
    } catch {
      if (!this.stopped) {
        this._scheduleReconnect();
      }
    }
  }

  private _handleMessage(raw: string): void {
    let msg: WsMessage;
    try {
      msg = JSON.parse(raw) as WsMessage;
    } catch {
      return; // ignore malformed frames
    }

    if (msg.type === 'monitoring_event') {
      const event = msg.event;
      this.subscribers.forEach((cb) => cb(event));
    }
    // heartbeat / connection / pong – no action needed from the client side
  }

  private _scheduleReconnect(): void {
    this._clearReconnect();
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this._open();
      // Increase delay for next failure (capped at MAX_DELAY_MS)
      this.reconnectDelay = Math.min(
        this.reconnectDelay * BACKOFF_FACTOR,
        MAX_DELAY_MS,
      );
    }, this.reconnectDelay);
  }

  private _clearReconnect(): void {
    if (this.reconnectTimer !== null) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }
}

// ─── Singleton ───────────────────────────────────────────────────────────────

/** Application-wide WebSocket client singleton. */
export const wsClient = new WsClient();

export default wsClient;

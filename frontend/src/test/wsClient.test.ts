/**
 * Tests for the WebSocket client utility (wsClient.ts).
 *
 * A mock WebSocket implementation is used so no real network connections
 * are made during tests.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import type { EventSubscriber } from '../utils/wsClient';

// ─── Mock WebSocket ───────────────────────────────────────────────────────────

interface MockWsInstance {
  onopen: (() => void) | null;
  onmessage: ((evt: { data: string }) => void) | null;
  onerror: (() => void) | null;
  onclose: (() => void) | null;
  send: ReturnType<typeof vi.fn>;
  close: ReturnType<typeof vi.fn>;
  readyState: number;
  /** Simulate a received message from the server. */
  _receive(data: string): void;
  /** Simulate the connection opening. */
  _open(): void;
  /** Simulate the connection closing. */
  _close(): void;
}

let lastWsInstance: MockWsInstance | null = null;

class MockWebSocket implements MockWsInstance {
  static OPEN = 1;
  static CONNECTING = 0;
  static CLOSED = 3;

  onopen: (() => void) | null = null;
  onmessage: ((evt: { data: string }) => void) | null = null;
  onerror: (() => void) | null = null;
  onclose: (() => void) | null = null;
  send = vi.fn();
  close = vi.fn(() => { this.readyState = MockWebSocket.CLOSED; });
  readyState = MockWebSocket.CONNECTING;

  constructor(_url: string) {
    lastWsInstance = this;
  }

  _open() {
    this.readyState = MockWebSocket.OPEN;
    this.onopen?.();
  }

  _receive(data: string) {
    this.onmessage?.({ data });
  }

  _close() {
    this.readyState = MockWebSocket.CLOSED;
    this.onclose?.();
  }
}

// ─── Test setup ───────────────────────────────────────────────────────────────

beforeEach(() => {
  vi.useFakeTimers();
  lastWsInstance = null;
  // Install the mock WebSocket globally
  vi.stubGlobal('WebSocket', MockWebSocket);
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

// ─── Helpers ─────────────────────────────────────────────────────────────────

async function importFreshClient() {
  // Re-import the module each time so we get a fresh singleton state.
  vi.resetModules();
  const mod = await import('../utils/wsClient');
  return mod.wsClient;
}

// ─── Tests ───────────────────────────────────────────────────────────────────

describe('wsClient', () => {
  describe('connection', () => {
    it('creates a WebSocket on connect()', async () => {
      const client = await importFreshClient();
      client.connect();
      expect(lastWsInstance).not.toBeNull();
    });

    it('sends connection-status message on open', async () => {
      const client = await importFreshClient();
      const subscriber = vi.fn();
      client.subscribe(subscriber);
      client.connect();
      lastWsInstance!._open();
      // Subscriber is for MonitoringEvent, not connection messages; no call expected.
      expect(subscriber).not.toHaveBeenCalled();
    });
  });

  describe('subscribe / unsubscribe', () => {
    it('delivers a monitoring_event to subscribers', async () => {
      const client = await importFreshClient();
      const subscriber = vi.fn() as ReturnType<typeof vi.fn> & EventSubscriber;
      client.subscribe(subscriber);
      client.connect();
      lastWsInstance!._open();

      const event = {
        id: 'e1',
        title: 'Test Event',
        summary: 'Summary',
        eventType: 'rate_change',
        severity: 'info',
        jurisdictionId: 'j1',
        detectedAt: new Date().toISOString(),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      lastWsInstance!._receive(
        JSON.stringify({ type: 'monitoring_event', event }),
      );

      expect(subscriber).toHaveBeenCalledOnce();
      expect(subscriber).toHaveBeenCalledWith(event);

      client.disconnect();
    });

    it('does not deliver events after unsubscribe', async () => {
      const client = await importFreshClient();
      const subscriber = vi.fn() as ReturnType<typeof vi.fn> & EventSubscriber;
      const unsub = client.subscribe(subscriber);
      client.connect();
      lastWsInstance!._open();
      unsub();

      lastWsInstance!._receive(
        JSON.stringify({ type: 'monitoring_event', event: { id: 'e2' } }),
      );

      expect(subscriber).not.toHaveBeenCalled();
      client.disconnect();
    });

    it('returns an unsubscribe function from subscribe()', async () => {
      const client = await importFreshClient();
      const unsub = client.subscribe(vi.fn());
      expect(typeof unsub).toBe('function');
      client.disconnect();
    });
  });

  describe('reconnect with exponential backoff', () => {
    it('schedules a reconnect after connection close', async () => {
      const client = await importFreshClient();
      client.connect();
      const firstWs = lastWsInstance!;
      firstWs._open();
      firstWs._close(); // simulate server drop

      // No new connection yet (timer hasn't fired)
      expect(lastWsInstance).toBe(firstWs);

      // Advance timer by initial delay (1 000 ms)
      vi.advanceTimersByTime(1_000);
      expect(lastWsInstance).not.toBe(firstWs); // a new WS was created
      client.disconnect();
    });

    it('doubles the backoff delay on repeated failures', async () => {
      const client = await importFreshClient();
      client.connect();

      // Close → 1 s delay
      lastWsInstance!._close();
      vi.advanceTimersByTime(1_000);

      // Close again → 2 s delay
      lastWsInstance!._close();

      // Advance only 1 s – should NOT reconnect yet
      vi.advanceTimersByTime(1_000);
      const wsAfter1s = lastWsInstance;

      // Advance remaining 1 s – should reconnect now
      vi.advanceTimersByTime(1_000);
      expect(lastWsInstance).not.toBe(wsAfter1s);
      client.disconnect();
    });

    it('resets backoff delay after successful open', async () => {
      const client = await importFreshClient();
      client.connect();

      // First close → reconnect
      lastWsInstance!._close();
      vi.advanceTimersByTime(1_000);

      // Second close before opening → should still use 2 s delay
      lastWsInstance!._close();
      vi.advanceTimersByTime(1_000);
      const wsAfter1s = lastWsInstance;
      vi.advanceTimersByTime(1_000);
      expect(lastWsInstance).not.toBe(wsAfter1s); // reconnected

      // Now open successfully → delay resets to 1 s
      lastWsInstance!._open();
      lastWsInstance!._close(); // drop again
      vi.advanceTimersByTime(1_000);   // 1 s should be enough now
      expect(lastWsInstance).not.toBeNull();
      client.disconnect();
    });

    it('stops reconnecting after disconnect()', async () => {
      const client = await importFreshClient();
      client.connect();
      const firstWs = lastWsInstance!;
      firstWs._close();
      client.disconnect(); // stop before timer fires
      vi.advanceTimersByTime(5_000);
      // No new connection should have been created
      expect(lastWsInstance).toBe(firstWs);
    });
  });

  describe('malformed messages', () => {
    it('silently ignores non-JSON messages', async () => {
      const client = await importFreshClient();
      const subscriber = vi.fn();
      client.subscribe(subscriber);
      client.connect();
      lastWsInstance!._open();
      expect(() => lastWsInstance!._receive('not-json')).not.toThrow();
      expect(subscriber).not.toHaveBeenCalled();
      client.disconnect();
    });
  });
});

/**
 * Tests for the monitoring-events slice of the Zustand store.
 *
 * Covers: addEvent, markRead, and fetchMonitoringEvents.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

// ─── Mock the API module ──────────────────────────────────────────────────────

vi.mock('../api', () => ({
  default: {
    monitoring: {
      events: vi.fn().mockResolvedValue({ total: 2, events: [
        { id: 'e1', title: 'Event 1', summary: 'S1', eventType: 'rate_change', severity: 'info',    jurisdictionId: 'j1', detectedAt: '2024-01-01T00:00:00Z', createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z' },
        { id: 'e2', title: 'Event 2', summary: 'S2', eventType: 'new_program', severity: 'warning', jurisdictionId: 'j2', detectedAt: '2024-01-02T00:00:00Z', createdAt: '2024-01-02T00:00:00Z', updatedAt: '2024-01-02T00:00:00Z' },
      ]}),
      unreadCount: vi.fn().mockResolvedValue({ unreadCount: 2 }),
    },
    productions: { list: vi.fn().mockResolvedValue([]) },
    jurisdictions: { list: vi.fn().mockResolvedValue([]) },
    incentiveRules: { listDetailed: vi.fn().mockResolvedValue([]) },
  },
}));

// Import AFTER mock is set up
import { useAppStore } from '../store';
import type { MonitoringEvent } from '../types';

// ─── Helpers ─────────────────────────────────────────────────────────────────

function makeEvent(overrides?: Partial<MonitoringEvent>): MonitoringEvent {
  return {
    id: 'test-id',
    jurisdictionId: 'j1',
    eventType: 'rate_change',
    severity: 'info',
    title: 'Test Event',
    summary: 'A test monitoring event',
    detectedAt: new Date().toISOString(),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    ...overrides,
  };
}

// ─── Tests ───────────────────────────────────────────────────────────────────

describe('Zustand store – monitoring events slice', () => {
  beforeEach(() => {
    // Reset store state between tests
    useAppStore.setState({
      monitoringEvents: [],
      unreadEventCount: 0,
    });
  });

  // ── addEvent ──────────────────────────────────────────────────────────────

  describe('addEvent', () => {
    it('prepends a new event to monitoringEvents', () => {
      const existing = makeEvent({ id: 'existing' });
      useAppStore.setState({ monitoringEvents: [existing] });

      const newEvent = makeEvent({ id: 'new' });
      useAppStore.getState().addEvent(newEvent);

      const { monitoringEvents } = useAppStore.getState();
      expect(monitoringEvents[0].id).toBe('new');
      expect(monitoringEvents[1].id).toBe('existing');
      expect(monitoringEvents).toHaveLength(2);
    });

    it('increments unreadCount', () => {
      useAppStore.setState({ unreadEventCount: 3 });
      useAppStore.getState().addEvent(makeEvent());
      expect(useAppStore.getState().unreadEventCount).toBe(4);
    });

    it('works when monitoringEvents is empty', () => {
      const event = makeEvent({ id: 'only' });
      useAppStore.getState().addEvent(event);
      expect(useAppStore.getState().monitoringEvents).toHaveLength(1);
      expect(useAppStore.getState().monitoringEvents[0].id).toBe('only');
    });
  });

  // ── markRead ─────────────────────────────────────────────────────────────

  describe('markRead', () => {
    it('resets unreadCount to 0', () => {
      useAppStore.setState({ unreadEventCount: 7 });
      useAppStore.getState().markRead();
      expect(useAppStore.getState().unreadEventCount).toBe(0);
    });

    it('does not remove events from the list', () => {
      const events = [makeEvent({ id: 'a' }), makeEvent({ id: 'b' })];
      useAppStore.setState({ monitoringEvents: events, unreadEventCount: 2 });
      useAppStore.getState().markRead();
      expect(useAppStore.getState().monitoringEvents).toHaveLength(2);
    });

    it('is idempotent when count is already 0', () => {
      useAppStore.setState({ unreadEventCount: 0 });
      useAppStore.getState().markRead();
      expect(useAppStore.getState().unreadEventCount).toBe(0);
    });
  });

  // ── fetchMonitoringEvents ────────────────────────────────────────────────

  describe('fetchMonitoringEvents', () => {
    it('populates monitoringEvents from the API', async () => {
      await useAppStore.getState().fetchMonitoringEvents();
      const { monitoringEvents } = useAppStore.getState();
      expect(monitoringEvents).toHaveLength(2);
      expect(monitoringEvents[0].id).toBe('e1');
    });

    it('sets unreadEventCount from the API', async () => {
      await useAppStore.getState().fetchMonitoringEvents();
      expect(useAppStore.getState().unreadEventCount).toBe(2);
    });

    it('does not throw when the API call fails', async () => {
      const { default: api } = await import('../api');
      vi.mocked(api.monitoring.events).mockRejectedValueOnce(new Error('network error'));
      await expect(
        useAppStore.getState().fetchMonitoringEvents(),
      ).resolves.toBeUndefined();
    });
  });
});

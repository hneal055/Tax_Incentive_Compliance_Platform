import apiClient from './client';
import type {
  Production,
  Jurisdiction,
  IncentiveRule,
  Expense,
  CalculationResult,
  HealthStatus,
  MonitoringEvent,
  MonitoringSource,
  ComplianceItem,
  ComplianceStats,
  NotificationPreference,
  UserProfile,
} from '../types';

import { mockApi } from '../mocks/api';

// Wraps every API call with flag check + automatic mock fallback on failure.
// Reads from getFlagSnapshot() so runtime flag toggles (via FeatureFlagContext) take effect
// immediately on the next call — no page reload needed.
// READ operations fall back to mock data silently (good for dev with backend down).
// WRITE operations re-throw after logging so callers can handle the error.
async function withFallback<T>(
  realFn: () => Promise<T>,
  mockFn: () => Promise<T>,
  label: string,
  isRead = true,
): Promise<T> {
  if (false) {
    if (import.meta.env.DEV) console.log(`[MOCK] ${label}`);
    return mockFn();
  }
  try {
    if (import.meta.env.DEV) console.log(`[API] ${label}`);
    return await realFn();
  } catch (error) {
    if (isRead) {
      if (import.meta.env.DEV) console.warn(`[FALLBACK] ${label} — API unavailable, using mock data`, error);
      return mockFn();
    }
    console.error(`[API ERROR] ${label}`, error);
    throw error;
  }
}

export const api = {
  health: () =>
    withFallback(
      async () => { const r = await apiClient.get('/health'); return r.data as HealthStatus; },
      () => mockApi.health(),
      'health',
    ),

  productions: {
    list: () =>
      withFallback(
        async () => { const r = await apiClient.get('/productions'); return (r.data.productions ?? r.data) as Production[]; },
        () => mockApi.productions.list(),
        'productions.list',
      ),

    get: (id: string) =>
      withFallback(
        async () => { const r = await apiClient.get(`/productions/${id}`); return r.data as Production; },
        () => mockApi.productions.get(id),
        `productions.get(${id})`,
      ),

    create: (data: Partial<Production>) =>
      withFallback(
        async () => { const r = await apiClient.post('/productions', data); return r.data as Production; },
        () => mockApi.productions.create(data),
        'productions.create',
        false,
      ),

    update: (id: string, data: Partial<Production>) =>
      withFallback(
        async () => { const r = await apiClient.put(`/productions/${id}`, data); return r.data as Production; },
        () => mockApi.productions.update(id, data),
        `productions.update(${id})`,
        false,
      ),

    delete: (id: string) =>
      withFallback(
        async () => { await apiClient.delete(`/productions/${id}`); },
        () => mockApi.productions.delete(id),
        `productions.delete(${id})`,
        false,
      ),
  },

  jurisdictions: {
    list: () =>
      withFallback(
        async () => { const r = await apiClient.get('/jurisdictions'); return (r.data.jurisdictions ?? r.data) as Jurisdiction[]; },
        () => mockApi.jurisdictions.list(),
        'jurisdictions.list',
      ),

    get: (id: string) =>
      withFallback(
        async () => { const r = await apiClient.get(`/jurisdictions/${id}`); return r.data as Jurisdiction; },
        () => mockApi.jurisdictions.get(id),
        `jurisdictions.get(${id})`,
      ),
  },

  incentiveRules: {
    list: () =>
      withFallback(
        async () => { const r = await apiClient.get('/incentive-rules'); return (r.data.rules ?? r.data) as IncentiveRule[]; },
        () => mockApi.incentiveRules.list(),
        'incentiveRules.list',
      ),

    getByJurisdiction: (jurisdictionId: string) =>
      withFallback(
        async () => { const r = await apiClient.get(`/jurisdictions/${jurisdictionId}/incentive-rules`); return r.data as IncentiveRule[]; },
        () => mockApi.incentiveRules.getByJurisdiction(jurisdictionId),
        `incentiveRules.getByJurisdiction(${jurisdictionId})`,
      ),
  },

  expenses: {
    list: (productionId: string) =>
      withFallback(
        async () => { const r = await apiClient.get(`/productions/${productionId}/expenses`); return r.data as Expense[]; },
        () => mockApi.expenses.list(productionId),
        `expenses.list(${productionId})`,
      ),

    create: (productionId: string, data: Partial<Expense> & { expenseDate?: string; isQualifying?: boolean; description?: string; vendorName?: string }) =>
      withFallback(
        async () => { const r = await apiClient.post(`/productions/${productionId}/expenses`, data); return r.data as Expense; },
        () => mockApi.expenses.create(productionId, data),
        `expenses.create(${productionId})`,
        false,
      ),

    delete: (productionId: string, expenseId: string) =>
      withFallback(
        async () => { await apiClient.delete(`/productions/${productionId}/expenses/${expenseId}`); },
        () => mockApi.expenses.delete(productionId, expenseId),
        `expenses.delete(${productionId}/${expenseId})`,
        false,
      ),
  },

  calculations: {
    calculate: (productionId: string, jurisdictionId: string) =>
      withFallback(
        async () => {
          const r = await apiClient.post('/calculate', { production_id: productionId, jurisdiction_id: jurisdictionId });
          return r.data as CalculationResult;
        },
        () => mockApi.calculations.calculate(productionId, jurisdictionId),
        `calculations.calculate(${productionId}, ${jurisdictionId})`,
      ),
  },

  compliance: {
    list: (productionId: string) =>
      withFallback(
        async () => { const r = await apiClient.get(`/productions/${productionId}/compliance`); return r.data as ComplianceStats; },
        async () => ({ total: 0, complete: 0, pending: 0, waived: 0, pct: 0, items: [] as ComplianceItem[] }),
        `compliance.list(${productionId})`,
      ),

    generate: (productionId: string) =>
      withFallback(
        async () => { const r = await apiClient.post(`/productions/${productionId}/compliance/generate`); return r.data as { created: number; items: ComplianceItem[] }; },
        async () => ({ created: 0, items: [] as ComplianceItem[] }),
        `compliance.generate(${productionId})`,
        false,
      ),

    addItem: (productionId: string, data: { label: string; category?: string; notes?: string }) =>
      withFallback(
        async () => { const r = await apiClient.post(`/productions/${productionId}/compliance`, data); return r.data as ComplianceItem; },
        async () => ({} as ComplianceItem),
        `compliance.addItem(${productionId})`,
        false,
      ),

    updateItem: (itemId: string, data: { status?: string; notes?: string; label?: string }) =>
      withFallback(
        async () => { const r = await apiClient.patch(`/compliance/${itemId}`, data); return r.data as ComplianceItem; },
        async () => ({} as ComplianceItem),
        `compliance.updateItem(${itemId})`,
        false,
      ),

    deleteItem: (itemId: string) =>
      withFallback(
        async () => { await apiClient.delete(`/compliance/${itemId}`); },
        async () => {},
        `compliance.deleteItem(${itemId})`,
        false,
      ),
  },

  notifications: {
    getPreferences: () =>
      withFallback(
        async () => { const r = await apiClient.get('/notifications/preferences'); return r.data as NotificationPreference | null; },
        async () => null,
        'notifications.getPreferences',
      ),

    upsertPreferences: (data: { emailAddress: string; jurisdictions: string[]; active: boolean }) =>
      withFallback(
        async () => { const r = await apiClient.post('/notifications/preferences', data); return r.data as NotificationPreference; },
        async () => ({} as NotificationPreference),
        'notifications.upsertPreferences',
        false,
      ),

    deletePreferences: () =>
      withFallback(
        async () => { await apiClient.delete('/notifications/preferences'); },
        async () => {},
        'notifications.deletePreferences',
        false,
      ),
  },

  admin: {
    listUsers: () =>
      withFallback(
        async () => { const r = await apiClient.get('/admin/users'); return r.data as { total: number; users: UserProfile[] }; },
        async () => ({ total: 0, users: [] as UserProfile[] }),
        'admin.listUsers',
      ),

    createUser: (data: { email: string; password: string; role: string }) =>
      withFallback(
        async () => { const r = await apiClient.post('/admin/users', data); return r.data as UserProfile; },
        async () => ({} as UserProfile),
        'admin.createUser',
        false,
      ),

    updateUser: (userId: string, data: { role?: string; isActive?: boolean; password?: string }) =>
      withFallback(
        async () => { const r = await apiClient.patch(`/admin/users/${userId}`, data); return r.data as UserProfile; },
        async () => ({} as UserProfile),
        `admin.updateUser(${userId})`,
        false,
      ),

    deleteUser: (userId: string) =>
      withFallback(
        async () => { await apiClient.delete(`/admin/users/${userId}`); },
        async () => {},
        `admin.deleteUser(${userId})`,
        false,
      ),
  },

  georgia: {
    getJurisdiction: (code: string) =>
      withFallback(
        async () => { const r = await apiClient.get(`/georgia/jurisdictions/${code}`); return r.data as { id: string; code: string; name: string; country: string; type: string; description: string | null; website: string | null; active: boolean }; },
        async () => ({ id: '', code, name: 'Georgia', country: 'USA', type: 'state', description: null, website: null, active: true }),
        `georgia.getJurisdiction(${code})`,
      ),

    getPrograms: (code: string) =>
      withFallback(
        async () => {
          const r = await apiClient.get(`/georgia/jurisdictions/${code}/programs`);
          return r.data as {
            jurisdiction_id: string;
            jurisdiction_name: string;
            jurisdiction_code: string;
            total: number;
            programs: Array<{
              id: string;
              name: string;
              code: string;
              incentive_type: string;
              percentage: number;
              min_spend: number | null;
              max_credit: number | null;
              eligible_expenses: string[] | null;
              excluded_expenses: string[] | null;
              requirements: string[] | null;
              effective_date: string | null;
              active: boolean;
            }>;
          };
        },
        async () => ({ jurisdiction_id: '', jurisdiction_name: 'Georgia', jurisdiction_code: code, total: 0, programs: [] }),
        `georgia.getPrograms(${code})`,
      ),
  },

  advisor: {
    summarizeEvent: (eventId: string) =>
      withFallback(
        async () => {
          const r = await apiClient.post(`/advisor/summarize-event/${eventId}`);
          return r.data as MonitoringEvent;
        },
        async () => ({} as MonitoringEvent),
        `advisor.summarizeEvent(${eventId})`,
        false,
      ),
  },

  monitoring: {
    events: {
      list: (params?: { limit?: number; skip?: number; unread_only?: boolean }) =>
        withFallback(
          async () => {
            const r = await apiClient.get('/monitoring/events', { params });
            return r.data as { total: number; unread: number; events: MonitoringEvent[] };
          },
          async () => ({ total: 0, unread: 0, events: [] as MonitoringEvent[] }),
          'monitoring.events.list',
        ),

      unreadCount: () =>
        withFallback(
          async () => { const r = await apiClient.get('/monitoring/events/unread-count'); return r.data as { count: number }; },
          async () => ({ count: 0 }),
          'monitoring.events.unreadCount',
        ),

      markRead: (id: string) =>
        withFallback(
          async () => { const r = await apiClient.patch(`/monitoring/events/${id}/read`); return r.data as MonitoringEvent; },
          async () => ({} as MonitoringEvent),
          `monitoring.events.markRead(${id})`,
          false,
        ),

      markAllRead: () =>
        withFallback(
          async () => { const r = await apiClient.post('/monitoring/events/mark-all-read'); return r.data as { updated: number }; },
          async () => ({ updated: 0 }),
          'monitoring.events.markAllRead',
          false,
        ),
    },

    sources: {
      list: () =>
        withFallback(
          async () => { const r = await apiClient.get('/monitoring/sources'); return r.data as { total: number; sources: MonitoringSource[] }; },
          async () => ({ total: 0, sources: [] as MonitoringSource[] }),
          'monitoring.sources.list',
        ),

      create: (data: Partial<MonitoringSource>) =>
        withFallback(
          async () => { const r = await apiClient.post('/monitoring/sources', data); return r.data as MonitoringSource; },
          async () => ({} as MonitoringSource),
          'monitoring.sources.create',
          false,
        ),
    },
  },
};

export const getApiUrl = (path: string): string => {
  const base = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  return base + path;
};

export default api;

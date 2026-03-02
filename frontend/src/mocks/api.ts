import { getFlagSnapshot } from '../contexts/FeatureFlagContext';
import type { Production, Jurisdiction, IncentiveRule, Expense, CalculationResult, HealthStatus } from '../types';
import { mockJurisdictions, mockIncentiveRules, mockProductionsInitial } from './data';

// In-memory mutable state — resets on page refresh
let productions: Production[] = [...mockProductionsInitial];
const expenses: Record<string, Expense[]> = {};

// Reads from snapshot on every call so the dev panel's delay slider takes effect immediately
function delay<T>(value: T): Promise<T> {
  return new Promise(resolve => setTimeout(() => resolve(value), getFlagSnapshot().MOCK_DELAY_MS));
}

function uuid(): string {
  return 'mock-' + Math.random().toString(36).slice(2, 10);
}

function now(): string {
  return new Date().toISOString();
}

export const mockApi = {
  health: (): Promise<HealthStatus> =>
    delay({ status: 'ok', database: 'mock', version: '0.1.0', environment: 'development' }),

  productions: {
    list: (): Promise<Production[]> =>
      delay([...productions]),

    get: (id: string): Promise<Production> => {
      const p = productions.find(p => p.id === id);
      if (!p) return Promise.reject(new Error('Production not found'));
      return delay({ ...p });
    },

    create: (data: Partial<Production>): Promise<Production> => {
      const p: Production = {
        id: uuid(),
        title: data.title ?? 'Untitled',
        productionType: data.productionType ?? 'feature_film',
        productionCompany: data.productionCompany ?? '',
        budgetTotal: data.budgetTotal ?? 0,
        budgetQualifying: data.budgetQualifying,
        startDate: data.startDate ?? now().split('T')[0],
        endDate: data.endDate,
        jurisdictionId: data.jurisdictionId ?? '',
        status: data.status ?? 'planning',
        createdAt: now(),
        updatedAt: now(),
      };
      productions = [...productions, p];
      return delay(p);
    },

    update: (id: string, data: Partial<Production>): Promise<Production> => {
      const idx = productions.findIndex(p => p.id === id);
      if (idx === -1) return Promise.reject(new Error('Production not found'));
      const updated = { ...productions[idx], ...data, updatedAt: now() };
      productions = productions.map((p, i) => (i === idx ? updated : p));
      return delay(updated);
    },

    delete: (id: string): Promise<void> => {
      productions = productions.filter(p => p.id !== id);
      return delay(undefined);
    },
  },

  jurisdictions: {
    list: (): Promise<Jurisdiction[]> =>
      delay([...mockJurisdictions]),

    get: (id: string): Promise<Jurisdiction> => {
      const j = mockJurisdictions.find(j => j.id === id);
      if (!j) return Promise.reject(new Error('Jurisdiction not found'));
      return delay({ ...j });
    },
  },

  incentiveRules: {
    list: (): Promise<IncentiveRule[]> =>
      delay([...mockIncentiveRules]),

    getByJurisdiction: (jurisdictionId: string): Promise<IncentiveRule[]> =>
      delay(mockIncentiveRules.filter(r => r.jurisdictionId === jurisdictionId)),
  },

  expenses: {
    list: (productionId: string): Promise<Expense[]> =>
      delay(expenses[productionId] ?? []),

    create: (productionId: string, data: Partial<Expense>): Promise<Expense> => {
      const e: Expense = {
        id: uuid(),
        production_id: productionId,
        category: data.category ?? 'other',
        amount: data.amount ?? 0,
        date: data.date ?? now().split('T')[0],
        vendor: data.vendor,
        created_at: now(),
        updated_at: now(),
      };
      expenses[productionId] = [...(expenses[productionId] ?? []), e];
      return delay(e);
    },

    delete: (productionId: string, expenseId: string): Promise<void> => {
      expenses[productionId] = (expenses[productionId] ?? []).filter(e => e.id !== expenseId);
      return delay(undefined);
    },
  },

  calculations: {
    calculate: (productionId: string, jurisdictionId: string): Promise<CalculationResult> => {
      const production = productions.find(p => p.id === productionId);
      const rule = mockIncentiveRules.find(r => r.jurisdictionId === jurisdictionId);
      const totalExpenses = production?.budgetTotal ?? 1000000;
      const qualifiedExpenses = production?.budgetQualifying ?? totalExpenses * 0.8;
      const rate = (rule?.percentage ?? 20) / 100;
      const maxCredit = rule?.maxCredit ?? Infinity;
      const incentiveAmount = Math.min(qualifiedExpenses * rate, maxCredit);
      return delay({
        production_id: productionId,
        jurisdiction_id: jurisdictionId,
        total_expenses: totalExpenses,
        qualified_expenses: qualifiedExpenses,
        incentive_amount: incentiveAmount,
        effective_rate: qualifiedExpenses > 0 ? incentiveAmount / qualifiedExpenses : 0,
      });
    },
  },
};

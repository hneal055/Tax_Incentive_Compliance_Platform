import { create } from 'zustand';
import type { Production, Jurisdiction, IncentiveRule, IncentiveRuleDetailed, MonitoringEvent } from '../types';
import api from '../api';

interface DashboardMetrics {
  totalBudget: number;
  estimatedCredits: number;
  complianceRate: number | null;
  lastUpdated: Date | null;
}

interface AppState {
  // Productions
  productions: Production[];
  selectedProduction: Production | null;

  // Jurisdictions
  jurisdictions: Jurisdiction[];

  // Incentive Rules
  incentiveRules: IncentiveRule[];
  detailedRules: IncentiveRuleDetailed[];
  rulesByJurisdiction: Record<string, IncentiveRuleDetailed[]>;

  // Dashboard metrics (computed from real data)
  dashboardMetrics: DashboardMetrics;

  // Monitoring events
  monitoringEvents: MonitoringEvent[];
  unreadEventCount: number;

  // Loading states
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchProductions: () => Promise<void>;
  fetchJurisdictions: () => Promise<void>;
  fetchIncentiveRules: () => Promise<void>;
  fetchDetailedRules: () => Promise<void>;
  fetchAllRulesGrouped: () => Promise<void>;
  fetchIncentiveRulesForJurisdiction: (id: string) => Promise<IncentiveRuleDetailed[]>;
  fetchMonitoringEvents: () => Promise<void>;
  computeDashboardMetrics: () => void;
  refreshAll: () => Promise<void>;
  selectProduction: (production: Production | null) => void;
  createProduction: (data: Partial<Production>) => Promise<void>;
  updateProduction: (id: string, data: Partial<Production>) => Promise<void>;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  productions: [],
  selectedProduction: null,
  jurisdictions: [],
  incentiveRules: [],
  detailedRules: [],
  rulesByJurisdiction: {},
  dashboardMetrics: {
    totalBudget: 0,
    estimatedCredits: 0,
    complianceRate: null,
    lastUpdated: null,
  },
  monitoringEvents: [],
  unreadEventCount: 0,
  isLoading: false,
  error: null,

  fetchProductions: async () => {
    set({ isLoading: true, error: null });
    try {
      const productions = await api.productions.list();
      set({ productions, isLoading: false });
    } catch {
      set({ error: 'Failed to fetch productions', isLoading: false });
    }
  },

  fetchJurisdictions: async () => {
    set({ isLoading: true, error: null });
    try {
      const jurisdictions = await api.jurisdictions.list();
      set({ jurisdictions, isLoading: false });
    } catch {
      set({ error: 'Failed to fetch jurisdictions', isLoading: false });
    }
  },

  fetchIncentiveRules: async () => {
    set({ isLoading: true, error: null });
    try {
      const incentiveRules = await api.incentiveRules.list();
      set({ incentiveRules, isLoading: false });
    } catch {
      set({ error: 'Failed to fetch incentive rules', isLoading: false });
    }
  },

  fetchDetailedRules: async () => {
    try {
      const detailedRules = await api.incentiveRules.listDetailed();
      const rulesByJurisdiction: Record<string, IncentiveRuleDetailed[]> = {};
      detailedRules.forEach((rule) => {
        const jId = rule.jurisdictionId;
        if (jId) {
          if (!rulesByJurisdiction[jId]) rulesByJurisdiction[jId] = [];
          rulesByJurisdiction[jId].push(rule);
        }
      });
      set({ detailedRules, rulesByJurisdiction });
    } catch {
      // Non-critical; don't set error to avoid blocking UI
    }
  },

  fetchAllRulesGrouped: async () => {
    try {
      const detailedRules = await api.incentiveRules.listDetailed();
      const rulesByJurisdiction: Record<string, IncentiveRuleDetailed[]> = {};
      detailedRules.forEach((rule) => {
        const jId = rule.jurisdictionId;
        if (jId) {
          if (!rulesByJurisdiction[jId]) rulesByJurisdiction[jId] = [];
          rulesByJurisdiction[jId].push(rule);
        }
      });
      set({ detailedRules, rulesByJurisdiction });
    } catch {
      // Silent fail for grouped rules
    }
  },

  fetchIncentiveRulesForJurisdiction: async (id: string) => {
    try {
      const rules = await api.incentiveRules.getByJurisdiction(id);
      set((state) => ({
        rulesByJurisdiction: { ...state.rulesByJurisdiction, [id]: rules },
      }));
      return rules;
    } catch {
      return [];
    }
  },

  fetchMonitoringEvents: async () => {
    try {
      const result = await api.monitoring.events({ page_size: 20 });
      const unreadResult = await api.monitoring.unreadCount();
      set({
        monitoringEvents: result.events,
        unreadEventCount: unreadResult.unreadCount,
      });
    } catch {
      // Non-critical; monitoring may not be running
    }
  },

  computeDashboardMetrics: () => {
    const { productions, rulesByJurisdiction } = get();
    const totalBudget = productions.reduce(
      (acc, p) => acc + (p.budgetTotal || p.budget || 0),
      0
    );

    let estimatedCredits = 0;
    let productionsWithRules = 0;
    let productionsMeetingMinimum = 0;

    productions.forEach((prod) => {
      const budget = prod.budgetTotal || prod.budget || 0;
      const jId = prod.jurisdictionId;
      if (jId && rulesByJurisdiction[jId]?.length) {
        const rules = rulesByJurisdiction[jId];
        // Prefer the production's selected rule, fall back to best available
        const selectedRule = prod.preferredRuleId
          ? rules.find((r) => r.id === prod.preferredRuleId)
          : undefined;
        const bestRule = selectedRule || rules.reduce((best, rule) =>
          (rule.percentage || 0) > (best.percentage || 0) ? rule : best
        , rules[0]);
        const rate = (bestRule.percentage || 0) / 100;
        estimatedCredits += budget * rate;
        productionsWithRules++;

        const minSpend = bestRule.minSpend || 0;
        if (budget >= minSpend) {
          productionsMeetingMinimum++;
        }
      }
    });

    const complianceRate = productionsWithRules > 0
      ? (productionsMeetingMinimum / productionsWithRules) * 100
      : null;

    set({
      dashboardMetrics: {
        totalBudget,
        estimatedCredits,
        complianceRate,
        lastUpdated: new Date(),
      },
    });
  },

  refreshAll: async () => {
    set({ isLoading: true, error: null });
    try {
      const [productions, jurisdictions] = await Promise.all([
        api.productions.list(),
        api.jurisdictions.list(),
      ]);
      set({ productions, jurisdictions });

      // Fetch rules and monitoring in parallel (non-blocking)
      const fetchRules = api.incentiveRules.listDetailed().catch(() => [] as IncentiveRuleDetailed[]);
      const fetchEvents = api.monitoring.events({ page_size: 20 }).catch(() => ({ total: 0, events: [] as MonitoringEvent[] }));
      const fetchUnread = api.monitoring.unreadCount().catch(() => ({ unreadCount: 0 }));

      const [detailedRules, eventsResult, unreadResult] = await Promise.all([
        fetchRules,
        fetchEvents,
        fetchUnread,
      ]);

      const rulesByJurisdiction: Record<string, IncentiveRuleDetailed[]> = {};
      detailedRules.forEach((rule) => {
        const jId = rule.jurisdictionId;
        if (jId) {
          if (!rulesByJurisdiction[jId]) rulesByJurisdiction[jId] = [];
          rulesByJurisdiction[jId].push(rule);
        }
      });

      set({
        detailedRules,
        rulesByJurisdiction,
        monitoringEvents: eventsResult.events,
        unreadEventCount: unreadResult.unreadCount,
        isLoading: false,
      });

      get().computeDashboardMetrics();
    } catch {
      set({ error: 'Failed to refresh data', isLoading: false });
    }
  },

  selectProduction: (production) => {
    set({ selectedProduction: production });
  },

  createProduction: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const newProduction = await api.productions.create(data);
      set((state) => ({
        productions: [...state.productions, newProduction],
        isLoading: false,
      }));
    } catch {
      set({ error: 'Failed to create production', isLoading: false });
    }
  },

  updateProduction: async (id, data) => {
    try {
      const updated = await api.productions.update(id, data);
      set((state) => ({
        productions: state.productions.map((p) => (p.id === id ? updated : p)),
        selectedProduction:
          state.selectedProduction?.id === id ? updated : state.selectedProduction,
      }));
      get().computeDashboardMetrics();
    } catch {
      set({ error: 'Failed to update production' });
    }
  },

  setError: (error) => {
    set({ error });
  },
}));

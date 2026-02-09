import apiClient from './client';
import type {
  Production,
  Jurisdiction,
  IncentiveRule,
  IncentiveRuleDetailed,
  Expense,
  CalculationResult,
  HealthStatus,
  SimpleCalculationResult,
  CompareCalculationResult,
  ComplianceCheckResult,
  ScenarioCalculationResult,
  MonitoringEvent,
} from '../types';

export const api = {
  // Health check
  health: async (): Promise<HealthStatus> => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // Productions
  productions: {
    list: async (): Promise<Production[]> => {
      const response = await apiClient.get('/productions/');
      return response.data.productions;
    },
    get: async (id: string): Promise<Production> => {
      const response = await apiClient.get(`/productions/${id}`);
      return response.data;
    },
    create: async (data: Partial<Production>): Promise<Production> => {
      const response = await apiClient.post('/productions/quick', data);
      return response.data;
    },
    createFull: async (data: Partial<Production>): Promise<Production> => {
      const response = await apiClient.post('/productions/', data);
      return response.data;
    },
    update: async (id: string, data: Partial<Production>): Promise<Production> => {
      const response = await apiClient.put(`/productions/${id}`, data);
      return response.data;
    },
    delete: async (id: string): Promise<void> => {
      await apiClient.delete(`/productions/${id}`);
    },
  },

  // Jurisdictions
  jurisdictions: {
    list: async (): Promise<Jurisdiction[]> => {
      const response = await apiClient.get('/jurisdictions/');
      return response.data.jurisdictions;
    },
    get: async (id: string): Promise<Jurisdiction> => {
      const response = await apiClient.get(`/jurisdictions/${id}`);
      return response.data;
    },
  },

  // Incentive Rules
  incentiveRules: {
    list: async (): Promise<IncentiveRule[]> => {
      const response = await apiClient.get('/incentive-rules/');
      return response.data.rules;
    },
    listDetailed: async (): Promise<IncentiveRuleDetailed[]> => {
      const response = await apiClient.get('/incentive-rules/');
      return response.data.rules;
    },
    getByJurisdiction: async (jurisdictionId: string): Promise<IncentiveRuleDetailed[]> => {
      const response = await apiClient.get(`/jurisdictions/${jurisdictionId}/incentive-rules`);
      return response.data;
    },
  },

  // Expenses
  expenses: {
    list: async (productionId: string): Promise<Expense[]> => {
      const response = await apiClient.get(`/productions/${productionId}/expenses`);
      return response.data;
    },
    create: async (productionId: string, data: Partial<Expense>): Promise<Expense> => {
      const response = await apiClient.post(`/productions/${productionId}/expenses`, data);
      return response.data;
    },
    delete: async (productionId: string, expenseId: string): Promise<void> => {
      await apiClient.delete(`/productions/${productionId}/expenses/${expenseId}`);
    },
  },

  // Calculations (legacy)
  calculations: {
    calculate: async (productionId: string, jurisdictionId: string): Promise<CalculationResult> => {
      const response = await apiClient.post('/calculate', {
        production_id: productionId,
        jurisdiction_id: jurisdictionId,
      });
      return response.data;
    },
  },

  // Calculator (real backend endpoints)
  calculator: {
    simple: async (data: {
      productionBudget: number;
      jurisdictionId: string;
      ruleId: string;
      qualifyingBudget?: number;
    }): Promise<SimpleCalculationResult> => {
      const response = await apiClient.post('/calculate/simple', data);
      return response.data;
    },
    compare: async (data: {
      productionBudget: number;
      jurisdictionIds: string[];
      qualifyingBudget?: number;
    }): Promise<CompareCalculationResult> => {
      const response = await apiClient.post('/calculate/compare', data);
      return response.data;
    },
    compliance: async (data: {
      ruleId: string;
      productionId?: string;
      productionBudget?: number;
      qualifyingBudget?: number;
    }): Promise<ComplianceCheckResult> => {
      const response = await apiClient.post('/calculate/compliance', data);
      return response.data;
    },
    scenario: async (data: {
      productionBudget: number;
      jurisdictionId: string;
      scenarios?: Array<Record<string, unknown>>;
    }): Promise<ScenarioCalculationResult> => {
      const response = await apiClient.post('/calculate/scenario', data);
      return response.data;
    },
    jurisdictionOptions: async (
      jurisdictionId: string,
      budget: number
    ): Promise<{
      jurisdiction: string;
      jurisdictionId: string;
      budget: number;
      options: Array<{
        ruleName: string;
        ruleCode: string;
        ruleId: string;
        incentiveType: string;
        percentage: number;
        estimatedCredit: number;
        meetsMinimum: boolean;
        minimumRequired: number;
        maximumCap: number;
      }>;
      bestOption: Record<string, unknown> | null;
    }> => {
      const response = await apiClient.get(
        `/calculate/jurisdiction/${jurisdictionId}?budget=${budget}`
      );
      return response.data;
    },
  },

  // Reports (PDF generation)
  reports: {
    comparison: async (data: {
      productionTitle: string;
      budget: number;
      jurisdictionIds: string[];
    }): Promise<Blob> => {
      const response = await apiClient.post('/reports/comparison', data, {
        responseType: 'blob',
      });
      return response.data;
    },
    compliance: async (data: {
      productionTitle: string;
      ruleId: string;
      productionBudget: number;
    }): Promise<Blob> => {
      const response = await apiClient.post('/reports/compliance', data, {
        responseType: 'blob',
      });
      return response.data;
    },
    scenario: async (data: {
      productionTitle: string;
      jurisdictionId: string;
      baseProductionBudget: number;
      scenarios: Array<Record<string, unknown>>;
    }): Promise<Blob> => {
      const response = await apiClient.post('/reports/scenario', data, {
        responseType: 'blob',
      });
      return response.data;
    },
  },

  // Monitoring
  monitoring: {
    events: async (params?: {
      jurisdiction_id?: string;
      event_type?: string;
      severity?: string;
      unread_only?: boolean;
      page?: number;
      page_size?: number;
    }): Promise<{ total: number; events: MonitoringEvent[] }> => {
      const response = await apiClient.get('/monitoring/events', { params });
      return response.data;
    },
    unreadCount: async (): Promise<{ unreadCount: number }> => {
      const response = await apiClient.get('/monitoring/events/unread');
      return response.data;
    },
    markRead: async (eventId: string): Promise<MonitoringEvent> => {
      const response = await apiClient.post(`/monitoring/events/${eventId}`);
      return response.data;
    },
  },
};

export default api;

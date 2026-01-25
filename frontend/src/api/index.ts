import apiClient from './client';
import type { 
  Production, 
  Jurisdiction, 
  IncentiveRule, 
  Expense, 
  CalculationResult,
  HealthStatus 
} from '../types';

export const api = {
  // Health check
  health: async (): Promise<HealthStatus> => {
    const response = await apiClient.get('/health', { baseURL: 'http://localhost:8000' });
    return response.data;
  },

  // Productions
  productions: {
    list: async (): Promise<Production[]> => {
      const response = await apiClient.get('/productions');
      return response.data;
    },
    get: async (id: string): Promise<Production> => {
      const response = await apiClient.get(`/productions/${id}`);
      return response.data;
    },
    create: async (data: Partial<Production>): Promise<Production> => {
      const response = await apiClient.post('/productions', data);
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
      const response = await apiClient.get('/jurisdictions');
      return response.data;
    },
    get: async (id: string): Promise<Jurisdiction> => {
      const response = await apiClient.get(`/jurisdictions/${id}`);
      return response.data;
    },
  },

  // Incentive Rules
  incentiveRules: {
    list: async (): Promise<IncentiveRule[]> => {
      const response = await apiClient.get('/incentive-rules');
      return response.data;
    },
    getByJurisdiction: async (jurisdictionId: string): Promise<IncentiveRule[]> => {
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

  // Calculations
  calculations: {
    calculate: async (productionId: string, jurisdictionId: string): Promise<CalculationResult> => {
      const response = await apiClient.post('/calculate', {
        production_id: productionId,
        jurisdiction_id: jurisdictionId,
      });
      return response.data;
    },
  },
};

export const getApiUrl = (path: string): string => {
  return apiClient.getBaseUrl() + path;
};

export default api;

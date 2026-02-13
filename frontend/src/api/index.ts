import apiClient from './client';
import type { 
  Production, 
  Jurisdiction, 
  IncentiveRule, 
  Expense, 
  CalculationResult,
  HealthStatus,
  ApiKey,
  ApiKeyCreated
} from '../types';

export const api = {
  // Health check
  health: async (): Promise<HealthStatus> => {
    const response = await apiClient.get('/health', { baseURL: 'http://127.0.0.1:8000' });
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
      // Use quick-create endpoint for simplified creation
      const response = await apiClient.post('/productions/quick', data);
      return response.data;
    },
    createFull: async (data: Partial<Production>): Promise<Production> => {
      // Use full create endpoint when all fields provided
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

  // API Keys
  apiKeys: {
    list: async (): Promise<ApiKey[]> => {
      const response = await apiClient.get('/api-keys/');
      return response.data;
    },
    get: async (id: string): Promise<ApiKey> => {
      const response = await apiClient.get(`/api-keys/${id}`);
      return response.data;
    },
    create: async (data: { name: string; permissions?: string[]; expiresAt?: string }): Promise<ApiKeyCreated> => {
      const response = await apiClient.post('/api-keys/', data);
      return response.data;
    },
    update: async (id: string, data: { name?: string; permissions?: string[] }): Promise<ApiKey> => {
      const response = await apiClient.patch(`/api-keys/${id}`, data);
      return response.data;
    },
    delete: async (id: string): Promise<void> => {
      await apiClient.delete(`/api-keys/${id}`);
    },
    rotate: async (id: string): Promise<ApiKeyCreated> => {
      const response = await apiClient.post(`/api-keys/${id}/rotate`);
      return response.data;
    },
  },
};

export default api;

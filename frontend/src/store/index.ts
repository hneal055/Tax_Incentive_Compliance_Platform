import { create } from 'zustand';
import type { Production, Jurisdiction, IncentiveRule } from '../types';
import api from '../api';

interface AppState {
  // Productions
  productions: Production[];
  selectedProduction: Production | null;
  
  // Jurisdictions
  jurisdictions: Jurisdiction[];
  
  // Incentive Rules
  incentiveRules: IncentiveRule[];
  
  // Loading states
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchProductions: () => Promise<void>;
  fetchJurisdictions: () => Promise<void>;
  fetchIncentiveRules: () => Promise<void>;
  selectProduction: (production: Production | null) => void;
  createProduction: (data: Partial<Production>) => Promise<void>;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  productions: [],
  selectedProduction: null,
  jurisdictions: [],
  incentiveRules: [],
  isLoading: false,
  error: null,

  fetchProductions: async () => {
    set({ isLoading: true, error: null });
    try {
      const productions = await api.productions.list();
      set({ productions, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch productions', isLoading: false });
    }
  },

  fetchJurisdictions: async () => {
    set({ isLoading: true, error: null });
    try {
      const jurisdictions = await api.jurisdictions.list();
      set({ jurisdictions, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch jurisdictions', isLoading: false });
    }
  },

  fetchIncentiveRules: async () => {
    set({ isLoading: true, error: null });
    try {
      const incentiveRules = await api.incentiveRules.list();
      set({ incentiveRules, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch incentive rules', isLoading: false });
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
    } catch (error) {
      set({ error: 'Failed to create production', isLoading: false });
    }
  },

  setError: (error) => {
    set({ error });
  },
}));

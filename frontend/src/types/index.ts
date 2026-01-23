export interface Production {
  id: string;
  title: string;
  budget: number;
  jurisdiction_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Jurisdiction {
  id: string;
  code: string;
  name: string;
  country: string;
  type: string;
  created_at: string;
  updated_at: string;
}

export interface IncentiveRule {
  id: string;
  jurisdiction_id: string;
  name: string;
  type: string;
  rate: number;
  min_spend?: number;
  max_credit?: number;
  created_at: string;
  updated_at: string;
}

export interface Expense {
  id: string;
  production_id: string;
  category: string;
  amount: number;
  date: string;
  vendor?: string;
  created_at: string;
  updated_at: string;
}

export interface CalculationResult {
  production_id: string;
  jurisdiction_id: string;
  total_expenses: number;
  qualified_expenses: number;
  incentive_amount: number;
  effective_rate: number;
}

export interface HealthStatus {
  status: string;
  database: string;
  version: string;
  environment: string;
}

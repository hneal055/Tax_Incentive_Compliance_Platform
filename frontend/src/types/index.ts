export interface Production {
  id: string;
  title: string;
  productionType: string;
  productionCompany: string;
  budgetTotal: number;
  budgetQualifying?: number;
  startDate: string;
  endDate?: string;
  jurisdictionId: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}

export interface Jurisdiction {
  id: string;
  code: string;
  name: string;
  country: string;
  type: string;
  description?: string;
  website?: string;
  active: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface IncentiveRule {
  id: string;
  jurisdictionId: string;
  ruleName: string;
  ruleCode: string;
  incentiveType: string;
  percentage?: number;
  fixedAmount?: number;
  minSpend?: number;
  maxCredit?: number;
  eligibleExpenses: string[];
  excludedExpenses: string[];
  effectiveDate: string;
  expirationDate?: string;
  requirements: Record<string, unknown>;
  active: boolean;
  createdAt: string;
  updatedAt: string;
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

export interface Production {
  id: string;
  title: string;
  budget?: number;
  productionType?: string;
  jurisdictionId?: string;
  preferredRuleId?: string;
  budgetTotal?: number;
  budgetQualifying?: number;
  startDate?: string;
  endDate?: string;
  productionCompany?: string;
  status?: string;
  created_at?: string;
  updated_at?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface Jurisdiction {
  id: string;
  code: string;
  name: string;
  country: string;
  type: string;
  description?: string;
  website?: string;
  active?: boolean;
  created_at?: string;
  updated_at?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface IncentiveRule {
  id: string;
  jurisdiction_id?: string;
  jurisdictionId?: string;
  name: string;
  type: string;
  rate: number;
  min_spend?: number;
  max_credit?: number;
  created_at?: string;
  updated_at?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface Expense {
  id: string;
  production_id?: string;
  productionId?: string;
  category: string;
  amount: number;
  date: string;
  vendor?: string;
  created_at?: string;
  updated_at?: string;
  createdAt?: string;
  updatedAt?: string;
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
  version?: string;
  database?: string;
  environment?: string;
}

// ─── Calculator Response Types ────────────────────────────────

export interface SimpleCalculationResult {
  jurisdiction: string;
  ruleName: string;
  ruleCode: string;
  incentiveType: string;
  totalBudget: number;
  qualifyingBudget: number;
  percentage: number | null;
  estimatedCredit: number;
  meetsMinimumSpend: boolean;
  minimumSpendRequired: number | null;
  underMaximumCap: boolean;
  maximumCapAmount: number | null;
  requirements: Record<string, unknown>;
  notes: string[];
}

export interface ComparisonResult {
  jurisdiction: string;
  jurisdictionId: string;
  ruleName: string;
  ruleCode: string;
  incentiveType: string;
  percentage: number | null;
  estimatedCredit: number;
  meetsRequirements: boolean;
  rank: number;
  savings: number;
}

export interface CompareCalculationResult {
  totalBudget: number;
  comparisons: ComparisonResult[];
  bestOption: ComparisonResult;
  savingsVsWorst: number;
  notes: string[];
}

export interface RequirementCheck {
  requirement: string;
  description: string;
  status: 'met' | 'not_met' | 'unknown' | 'not_applicable';
  required: boolean;
  userValue?: unknown;
  requiredValue?: unknown;
  notes?: string;
}

export interface ComplianceCheckResult {
  overallCompliance: 'compliant' | 'non_compliant' | 'partial' | 'insufficient_data';
  jurisdiction: string;
  ruleName: string;
  ruleCode: string;
  totalRequirements: number;
  requirementsMet: number;
  requirementsNotMet: number;
  requirementsUnknown: number;
  requirements: RequirementCheck[];
  estimatedCredit: number | null;
  actionItems: string[];
  warnings: string[];
  nextSteps: string[];
}

export interface ScenarioResult {
  scenarioName: string;
  scenarioParams: Record<string, unknown>;
  bestRuleName: string;
  bestRuleCode: string;
  ruleId: string;
  estimatedCredit: number;
  effectiveRate: number;
  meetsRequirements: boolean;
  isActive: boolean;
  isExpired: boolean;
  effectiveDate: string | null;
  expirationDate: string | null;
  notes: string[];
}

export interface ScenarioCalculationResult {
  jurisdiction: string;
  baseProductionBudget: number;
  productionDate: string | null;
  scenarios: ScenarioResult[];
  bestScenario: ScenarioResult;
  worstScenario: ScenarioResult;
  savingsDifference: number;
  recommendations: string[];
  availableRules: number;
  expiredRules: number;
}

// ─── Monitoring Types ─────────────────────────────────────────

export interface MonitoringEvent {
  id: string;
  jurisdictionId: string;
  eventType: string;
  severity: string;
  title: string;
  summary: string;
  sourceId?: string;
  sourceUrl?: string;
  detectedAt: string;
  readAt?: string | null;
  metadata?: string;
  createdAt: string;
  updatedAt: string;
}

// ─── Incentive Rule (Extended) ────────────────────────────────

export interface IncentiveRuleDetailed {
  id: string;
  jurisdictionId: string;
  ruleName: string;
  ruleCode: string;
  incentiveType: string;
  percentage: number | null;
  fixedAmount: number | null;
  minSpend: number | null;
  maxCredit: number | null;
  eligibleExpenses: string[];
  excludedExpenses: string[];
  effectiveDate: string;
  expirationDate: string | null;
  requirements: Record<string, unknown>;
  active: boolean;
  createdAt: string;
  updatedAt: string;
}

// ─── Settings Types ───────────────────────────────────────────

export interface UserSettings {
  currency: string;
  defaultJurisdiction: string;
  notificationsEnabled: boolean;
  darkMode: boolean;
  autoRefresh: boolean;
  refreshInterval: number;
  compactMode: boolean;
  showSparklines: boolean;
  severityFilters: { info: boolean; warning: boolean; critical: boolean };
}

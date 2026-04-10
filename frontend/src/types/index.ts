// frontend/src/types.ts

export interface Production {
  id: string;
  title: string;
  productionType: string;
  productionCompany: string;
  budgetTotal: number;
  budgetQualifying?: number;
  budget_id?: string;            // <-- ADD THIS LINE
  startDate: string;
  endDate?: string;
  jurisdictionId: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}

// All other interfaces remain unchanged...
export interface Jurisdiction {
  id: string;
  code: string;
  name: string;
  country: string;
  type: string;
  description?: string;
  website?: string;
  currency: string;
  treatyPartners: string[];
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
  creditType: string;
  percentage?: number;
  fixedAmount?: number;
  minSpend?: number;
  maxCredit?: number;
  eligibleExpenses: string[];
  excludedExpenses: string[];
  effectiveDate: string;
  expirationDate?: string;
  requirements: string;
  active: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Expense {
  id: string;
  productionId: string;
  category: string;
  subcategory?: string;
  description: string;
  amount: number;
  expenseDate: string;
  isQualifying: boolean;
  qualifyingNote?: string;
  vendorName?: string;
  createdAt: string;
  updatedAt: string;
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

export interface MonitoringSource {
  id: string;
  name: string;
  url: string;
  feedUrl?: string;
  sourceType: string;
  jurisdiction?: string;
  active: boolean;
  lastFetched?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ComplianceItem {
  id: string;
  productionId: string;
  label: string;
  category: string;
  status: 'pending' | 'complete' | 'waived' | 'na';
  notes?: string;
  dueDate?: string;
  completedAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ComplianceStats {
  total: number;
  complete: number;
  pending: number;
  waived: number;
  pct: number;
  items: ComplianceItem[];
}

export interface NotificationPreference {
  id: string;
  userId: string;
  jurisdictions: string[];
  emailAddress: string;
  active: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface UserProfile {
  id: string;
  email: string;
  role: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface MonitoringEvent {
  id: string;
  sourceId: string;
  source?: MonitoringSource;
  title: string;
  summary?: string;
  url?: string;
  severity: 'info' | 'warning' | 'critical';
  isRead: boolean;
  publishedAt?: string;
  createdAt: string;
}

export interface ExtractedRule {
  name: string;
  category: string;
  rule_type: string;
  amount: number | null;
  percentage: number | null;
  description: string;
  requirements: string | null;
  effective_date: string | null;
  expiration_date: string | null;
}

export interface ExtractedData {
  rules: ExtractedRule[];
  confidence: number;
  summary: string;
  no_rules_found: boolean;
}

export interface PendingRule {
  id: string;
  jurisdictionId: string;
  jurisdiction?: { id: string; name: string; code: string };
  sourceUrl: string;
  extractedData: ExtractedData;
  confidence: number | null;
  status: 'pending' | 'approved' | 'rejected';
  reviewNotes: string | null;
  reviewedBy: string | null;
  reviewedAt: string | null;
  createdAt: string;
  updatedAt: string;
}
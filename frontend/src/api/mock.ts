/**
 * Mock API — mirrors the shape of api/index.ts for offline / dev testing.
 * Activated when localStorage["pilotforge_settings"].useMockData === true.
 */
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

// ─── Helper ───────────────────────────────────────────────────────────────────

export function isMockMode(): boolean {
  try {
    const s = localStorage.getItem('pilotforge_settings');
    return s ? JSON.parse(s).useMockData === true : false;
  } catch {
    return false;
  }
}

function delay<T>(value: T, ms = 120): Promise<T> {
  return new Promise((res) => setTimeout(() => res(value), ms));
}

// ─── Mock Jurisdictions ───────────────────────────────────────────────────────

export const MOCK_JURISDICTIONS: Jurisdiction[] = [
  { id: 'jur-ca', code: 'CA', name: 'California', country: 'US', type: 'state', description: 'California Film & TV Tax Credit', website: 'https://film.ca.gov', active: true },
  { id: 'jur-ny', code: 'NY', name: 'New York', country: 'US', type: 'state', description: 'Empire State Film Production Credit', website: 'https://esd.ny.gov', active: true },
  { id: 'jur-ga', code: 'GA', name: 'Georgia', country: 'US', type: 'state', description: 'Georgia Film & TV Tax Credit', website: 'https://georgia.org', active: true },
  { id: 'jur-la', code: 'LA', name: 'Louisiana', country: 'US', type: 'state', description: 'Louisiana Entertainment Incentive', website: 'https://entertainment.la.gov', active: true },
  { id: 'jur-nm', code: 'NM', name: 'New Mexico', country: 'US', type: 'state', description: 'New Mexico Film Production Tax Credit', website: 'https://nmfilm.com', active: true },
  { id: 'jur-uk', code: 'UK', name: 'United Kingdom', country: 'GB', type: 'country', description: 'UK Film Tax Relief', website: 'https://britishfilmcommission.org.uk', active: true },
  { id: 'jur-ca-fed', code: 'CA-FED', name: 'Canada (Federal)', country: 'CA', type: 'country', description: 'Canadian Film or Video Production Tax Credit', website: 'https://canada.ca', active: true },
  { id: 'jur-nz', code: 'NZ', name: 'New Zealand', country: 'NZ', type: 'country', description: 'NZ Screen Production Grant', website: 'https://nzfilm.co.nz', active: true },
];

// ─── Mock Incentive Rules ─────────────────────────────────────────────────────

export const MOCK_INCENTIVE_RULES: IncentiveRuleDetailed[] = [
  {
    id: 'rule-ca-1', jurisdictionId: 'jur-ca', ruleName: 'CA Film Tax Credit 3.0', ruleCode: 'CA-FTC3',
    incentiveType: 'tax_credit', percentage: 20, fixedAmount: null, minSpend: 1000000, maxCredit: 20000000,
    eligibleExpenses: ['labor', 'equipment', 'locations'], excludedExpenses: ['marketing'],
    effectiveDate: '2025-01-01', expirationDate: '2030-12-31',
    requirements: { minimum_shooting_days_ca: 75, local_hire_percentage: 75 }, active: true,
    createdAt: '2025-01-01T00:00:00Z', updatedAt: '2025-01-01T00:00:00Z',
  },
  {
    id: 'rule-ny-1', jurisdictionId: 'jur-ny', ruleName: 'Empire State Film Production Credit', ruleCode: 'NY-ESFC',
    incentiveType: 'tax_credit', percentage: 25, fixedAmount: null, minSpend: 500000, maxCredit: null,
    eligibleExpenses: ['labor', 'equipment', 'locations', 'vfx'], excludedExpenses: [],
    effectiveDate: '2024-01-01', expirationDate: '2029-12-31',
    requirements: { minimum_shoot_days_ny: 10, above_line_ny_labor: true }, active: true,
    createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-ga-1', jurisdictionId: 'jur-ga', ruleName: 'Georgia Entertainment Industry Credit', ruleCode: 'GA-EIC',
    incentiveType: 'tax_credit', percentage: 20, fixedAmount: null, minSpend: 500000, maxCredit: null,
    eligibleExpenses: ['below_line_labor', 'equipment', 'locations'], excludedExpenses: ['above_line'],
    effectiveDate: '2023-01-01', expirationDate: null,
    requirements: { georgia_qualified_spend: 500000 }, active: true,
    createdAt: '2023-01-01T00:00:00Z', updatedAt: '2023-01-01T00:00:00Z',
  },
  {
    id: 'rule-ga-2', jurisdictionId: 'jur-ga', ruleName: 'GA Uplift — Georgia Promotion', ruleCode: 'GA-EIC-UPLIFT',
    incentiveType: 'tax_credit', percentage: 10, fixedAmount: null, minSpend: 500000, maxCredit: null,
    eligibleExpenses: ['all'], excludedExpenses: [],
    effectiveDate: '2023-01-01', expirationDate: null,
    requirements: { embed_georgia_peach_logo: true }, active: true,
    createdAt: '2023-01-01T00:00:00Z', updatedAt: '2023-01-01T00:00:00Z',
  },
  {
    id: 'rule-la-1', jurisdictionId: 'jur-la', ruleName: 'Louisiana Motion Picture Incentive', ruleCode: 'LA-MPI',
    incentiveType: 'tax_credit', percentage: 25, fixedAmount: null, minSpend: 300000, maxCredit: null,
    eligibleExpenses: ['below_line_labor', 'equipment', 'locations'], excludedExpenses: [],
    effectiveDate: '2024-01-01', expirationDate: '2031-12-31',
    requirements: { louisiana_resident_payroll_minimum: 0.5 }, active: true,
    createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-nm-1', jurisdictionId: 'jur-nm', ruleName: 'NM Film Production Tax Credit', ruleCode: 'NM-FPTC',
    incentiveType: 'tax_credit', percentage: 25, fixedAmount: null, minSpend: 500000, maxCredit: 5000000,
    eligibleExpenses: ['below_line_labor', 'equipment', 'locations'], excludedExpenses: [],
    effectiveDate: '2024-07-01', expirationDate: '2028-06-30',
    requirements: { nm_qualified_production_costs: 500000 }, active: true,
    createdAt: '2024-07-01T00:00:00Z', updatedAt: '2024-07-01T00:00:00Z',
  },
  {
    id: 'rule-uk-1', jurisdictionId: 'jur-uk', ruleName: 'UK Film Tax Relief (Enhanced)', ruleCode: 'UK-FTR-E',
    incentiveType: 'tax_credit', percentage: 53, fixedAmount: null, minSpend: 100000, maxCredit: null,
    eligibleExpenses: ['uk_core_expenditure'], excludedExpenses: [],
    effectiveDate: '2024-04-01', expirationDate: null,
    requirements: { bfi_cultural_test_score: 18, uk_core_expenditure_min: 0.1 }, active: true,
    createdAt: '2024-04-01T00:00:00Z', updatedAt: '2024-04-01T00:00:00Z',
  },
  {
    id: 'rule-nz-1', jurisdictionId: 'jur-nz', ruleName: 'NZ Screen Production Grant (International)', ruleCode: 'NZ-SPG-INT',
    incentiveType: 'grant', percentage: 20, fixedAmount: null, minSpend: 15000000, maxCredit: null,
    eligibleExpenses: ['nz_qualifying_production_expenditure'], excludedExpenses: [],
    effectiveDate: '2025-01-01', expirationDate: null,
    requirements: { minimum_nz_spend: 15000000, significant_nz_content: true }, active: true,
    createdAt: '2025-01-01T00:00:00Z', updatedAt: '2025-01-01T00:00:00Z',
  },
];

// ─── Mock Productions ─────────────────────────────────────────────────────────

export const MOCK_PRODUCTIONS: Production[] = [
  {
    id: 'prod-1', title: 'Sunset Boulevard Redux', productionType: 'Drama', status: 'pre_production',
    budget: 8500000, budgetTotal: 8500000, budgetQualifying: 6200000,
    jurisdictionId: 'jur-ga', preferredRuleId: 'rule-ga-1',
    startDate: '2026-04-01', endDate: '2026-09-30',
    productionCompany: 'Nightfall Studios', createdAt: '2026-01-15T00:00:00Z', updatedAt: '2026-02-01T00:00:00Z',
  },
  {
    id: 'prod-2', title: 'Pacific Storm', productionType: 'Action', status: 'development',
    budget: 25000000, budgetTotal: 25000000, budgetQualifying: 18500000,
    jurisdictionId: 'jur-nz', preferredRuleId: 'rule-nz-1',
    startDate: '2026-08-01', endDate: '2027-02-28',
    productionCompany: 'Atlas Pictures', createdAt: '2026-01-20T00:00:00Z', updatedAt: '2026-02-10T00:00:00Z',
  },
  {
    id: 'prod-3', title: 'The Last Algorithm', productionType: 'Sci-Fi', status: 'production',
    budget: 15000000, budgetTotal: 15000000, budgetQualifying: 11000000,
    jurisdictionId: 'jur-nm', preferredRuleId: 'rule-nm-1',
    startDate: '2025-11-01', endDate: '2026-04-30',
    productionCompany: 'Zenith Films', createdAt: '2025-10-01T00:00:00Z', updatedAt: '2026-01-15T00:00:00Z',
  },
  {
    id: 'prod-4', title: 'Harbor District', productionType: 'Documentary', status: 'post_production',
    budget: 2500000, budgetTotal: 2500000, budgetQualifying: 2200000,
    jurisdictionId: 'jur-ny', preferredRuleId: 'rule-ny-1',
    startDate: '2025-06-01', endDate: '2025-12-31',
    productionCompany: 'True North Docs', createdAt: '2025-05-01T00:00:00Z', updatedAt: '2026-01-10T00:00:00Z',
  },
];

// ─── Mock Monitoring Events ───────────────────────────────────────────────────

export const MOCK_MONITORING_EVENTS: MonitoringEvent[] = [
  {
    id: 'evt-1', jurisdictionId: 'jur-ga', eventType: 'incentive_change', severity: 'info',
    title: 'Georgia FY Cap Status: 65% Utilized',
    summary: 'The Georgia Entertainment Industry Credit fiscal year cap is now 65% utilized. Approximately $105M remaining. Applications remain open.',
    sourceUrl: 'https://georgia.org', detectedAt: '2026-03-05T14:30:00Z', readAt: null,
    createdAt: '2026-03-05T14:30:00Z', updatedAt: '2026-03-05T14:30:00Z',
  },
  {
    id: 'evt-2', jurisdictionId: 'jur-uk', eventType: 'incentive_change', severity: 'warning',
    title: 'UK Enhanced Film Tax Relief — New Cultural Test Guidance',
    summary: 'HMRC has issued updated guidance on the BFI Cultural Test for projects applying under the enhanced rate (53%). VFX expenditure now separately qualifying.',
    sourceUrl: 'https://britishfilmcommission.org.uk', detectedAt: '2026-03-04T09:00:00Z', readAt: null,
    createdAt: '2026-03-04T09:00:00Z', updatedAt: '2026-03-04T09:00:00Z',
  },
  {
    id: 'evt-3', jurisdictionId: 'jur-ca', eventType: 'expiration', severity: 'critical',
    title: 'California Film Tax Credit — Application Window Closing',
    summary: 'The next California Film Tax Credit application window closes March 31, 2026. FY 2026-27 allocations will be announced in April.',
    sourceUrl: 'https://film.ca.gov', detectedAt: '2026-03-01T08:00:00Z', readAt: '2026-03-02T10:00:00Z',
    createdAt: '2026-03-01T08:00:00Z', updatedAt: '2026-03-02T10:00:00Z',
  },
  {
    id: 'evt-4', jurisdictionId: 'jur-nm', eventType: 'new_program', severity: 'info',
    title: 'New Mexico Raises Annual Film Credit Cap to $110M',
    summary: 'Governor signs HB 252 increasing the annual cap for the NM Film Production Tax Credit from $75M to $110M, effective July 1, 2026.',
    sourceUrl: 'https://nmfilm.com', detectedAt: '2026-02-28T16:00:00Z', readAt: null,
    createdAt: '2026-02-28T16:00:00Z', updatedAt: '2026-02-28T16:00:00Z',
  },
  {
    id: 'evt-5', jurisdictionId: 'jur-la', eventType: 'incentive_change', severity: 'info',
    title: 'Louisiana Restores Uncapped Transferable Credits',
    summary: 'Louisiana legislature votes to remove the annual $180M cap on transferable film credits, restoring the uncapped program retroactive to January 1, 2026.',
    sourceUrl: 'https://entertainment.la.gov', detectedAt: '2026-02-20T11:00:00Z', readAt: null,
    createdAt: '2026-02-20T11:00:00Z', updatedAt: '2026-02-20T11:00:00Z',
  },
];

// ─── Mock Expenses ────────────────────────────────────────────────────────────

const MOCK_EXPENSES: Record<string, Expense[]> = {
  'prod-1': [
    { id: 'exp-1', productionId: 'prod-1', category: 'Below-Line Labor', amount: 2800000, date: '2026-04-15', vendor: 'GA Crew Guild' },
    { id: 'exp-2', productionId: 'prod-1', category: 'Equipment Rental', amount: 950000, date: '2026-04-20', vendor: 'Panavision Atlanta' },
    { id: 'exp-3', productionId: 'prod-1', category: 'Location Fees', amount: 320000, date: '2026-05-01', vendor: 'Savannah Film Office' },
  ],
};

// ─── Mock API ─────────────────────────────────────────────────────────────────

const mockApi = {
  health: async (): Promise<HealthStatus> =>
    delay({ status: 'healthy', database: 'mock', monitoring: 'mock', version: 'v1', environment: 'mock' }),

  productions: {
    list: async (): Promise<Production[]> => delay([...MOCK_PRODUCTIONS]),
    get: async (id: string): Promise<Production> =>
      delay(MOCK_PRODUCTIONS.find((p) => p.id === id) ?? MOCK_PRODUCTIONS[0]),
    create: async (data: Partial<Production>): Promise<Production> =>
      delay({ id: `prod-${Date.now()}`, title: 'New Production', budget: 0, ...data } as Production),
    createFull: async (data: Partial<Production>): Promise<Production> =>
      delay({ id: `prod-${Date.now()}`, title: 'New Production', budget: 0, ...data } as Production),
    update: async (id: string, data: Partial<Production>): Promise<Production> =>
      delay({ ...(MOCK_PRODUCTIONS.find((p) => p.id === id) ?? MOCK_PRODUCTIONS[0]), ...data }),
    delete: async (): Promise<void> => delay(undefined),
  },

  jurisdictions: {
    list: async (): Promise<Jurisdiction[]> => delay([...MOCK_JURISDICTIONS]),
    get: async (id: string): Promise<Jurisdiction> =>
      delay(MOCK_JURISDICTIONS.find((j) => j.id === id) ?? MOCK_JURISDICTIONS[0]),
  },

  incentiveRules: {
    list: async (): Promise<IncentiveRule[]> =>
      delay(MOCK_INCENTIVE_RULES.map((r) => ({
        id: r.id, jurisdiction_id: r.jurisdictionId, jurisdictionId: r.jurisdictionId,
        name: r.ruleName, type: r.incentiveType, rate: r.percentage ?? 0,
        min_spend: r.minSpend ?? undefined, max_credit: r.maxCredit ?? undefined,
      } as IncentiveRule))),
    listDetailed: async (): Promise<IncentiveRuleDetailed[]> => delay([...MOCK_INCENTIVE_RULES]),
    getByJurisdiction: async (jurisdictionId: string): Promise<IncentiveRuleDetailed[]> =>
      delay(MOCK_INCENTIVE_RULES.filter((r) => r.jurisdictionId === jurisdictionId)),
  },

  expenses: {
    list: async (productionId: string): Promise<Expense[]> =>
      delay(MOCK_EXPENSES[productionId] ?? []),
    create: async (productionId: string, data: Partial<Expense>): Promise<Expense> =>
      delay({ id: `exp-${Date.now()}`, productionId, category: '', amount: 0, date: new Date().toISOString().slice(0, 10), ...data } as Expense),
    delete: async (): Promise<void> => delay(undefined),
  },

  calculations: {
    calculate: async (productionId: string, jurisdictionId: string): Promise<CalculationResult> =>
      delay({ production_id: productionId, jurisdiction_id: jurisdictionId, total_expenses: 1000000, qualified_expenses: 800000, incentive_amount: 200000, effective_rate: 0.2 }),
  },

  calculator: {
    simple: async (data: { productionBudget: number; jurisdictionId: string; ruleId: string; qualifyingBudget?: number }): Promise<SimpleCalculationResult> => {
      const rule = MOCK_INCENTIVE_RULES.find((r) => r.id === data.ruleId) ?? MOCK_INCENTIVE_RULES[0];
      const rate = (rule.percentage ?? 20) / 100;
      const qualifying = data.qualifyingBudget ?? data.productionBudget;
      return delay({
        jurisdiction: MOCK_JURISDICTIONS.find((j) => j.id === data.jurisdictionId)?.name ?? 'Unknown',
        ruleName: rule.ruleName, ruleCode: rule.ruleCode, incentiveType: rule.incentiveType,
        totalBudget: data.productionBudget, qualifyingBudget: qualifying,
        percentage: rule.percentage, estimatedCredit: qualifying * rate,
        meetsMinimumSpend: qualifying >= (rule.minSpend ?? 0),
        minimumSpendRequired: rule.minSpend, underMaximumCap: true, maximumCapAmount: rule.maxCredit,
        requirements: rule.requirements, notes: ['Mock calculation — enable live data for real results'],
      });
    },
    compare: async (data: { productionBudget: number; jurisdictionIds: string[]; qualifyingBudget?: number }): Promise<CompareCalculationResult> => {
      const qualifying = data.qualifyingBudget ?? data.productionBudget;
      const comparisons = data.jurisdictionIds.map((jId, i) => {
        const jur = MOCK_JURISDICTIONS.find((j) => j.id === jId);
        const rule = MOCK_INCENTIVE_RULES.find((r) => r.jurisdictionId === jId) ?? MOCK_INCENTIVE_RULES[0];
        const rate = (rule.percentage ?? 20) / 100;
        return { jurisdiction: jur?.name ?? jId, jurisdictionId: jId, ruleName: rule.ruleName, ruleCode: rule.ruleCode, incentiveType: rule.incentiveType, percentage: rule.percentage, estimatedCredit: qualifying * rate, meetsRequirements: qualifying >= (rule.minSpend ?? 0), rank: i + 1, savings: 0 };
      }).sort((a, b) => (b.estimatedCredit) - (a.estimatedCredit)).map((c, i) => ({ ...c, rank: i + 1 }));
      const best = comparisons[0];
      const worst = comparisons[comparisons.length - 1];
      return delay({ totalBudget: data.productionBudget, comparisons, bestOption: best, savingsVsWorst: best.estimatedCredit - worst.estimatedCredit, notes: ['Mock comparison'] });
    },
    compliance: async (): Promise<ComplianceCheckResult> =>
      delay({ overallCompliance: 'partial', jurisdiction: 'Mock', ruleName: 'Mock Rule', ruleCode: 'MOCK', totalRequirements: 3, requirementsMet: 2, requirementsNotMet: 1, requirementsUnknown: 0, requirements: [], estimatedCredit: 250000, actionItems: ['Verify local hire percentage'], warnings: [], nextSteps: ['Submit application before deadline'] }),
    scenario: async (): Promise<ScenarioCalculationResult> =>
      delay({ jurisdiction: 'Mock', baseProductionBudget: 10000000, productionDate: null, scenarios: [], bestScenario: {} as never, worstScenario: {} as never, savingsDifference: 0, recommendations: ['Use live data for scenario analysis'], availableRules: 2, expiredRules: 0 }),
    jurisdictionOptions: async (jurisdictionId: string, budget: number) => {
      const rules = MOCK_INCENTIVE_RULES.filter((r) => r.jurisdictionId === jurisdictionId);
      const jur = MOCK_JURISDICTIONS.find((j) => j.id === jurisdictionId);
      return delay({ jurisdiction: jur?.name ?? jurisdictionId, jurisdictionId, budget, options: rules.map((r) => ({ ruleName: r.ruleName, ruleCode: r.ruleCode, ruleId: r.id, incentiveType: r.incentiveType, percentage: r.percentage ?? 0, estimatedCredit: budget * ((r.percentage ?? 0) / 100), meetsMinimum: budget >= (r.minSpend ?? 0), minimumRequired: r.minSpend ?? 0, maximumCap: r.maxCredit ?? 0 })), bestOption: null });
    },
  },

  reports: {
    comparison: async (): Promise<Blob> => delay(new Blob(['Mock PDF report'], { type: 'application/pdf' })),
    compliance: async (): Promise<Blob> => delay(new Blob(['Mock PDF report'], { type: 'application/pdf' })),
    scenario: async (): Promise<Blob> => delay(new Blob(['Mock PDF report'], { type: 'application/pdf' })),
  },

  monitoring: {
    events: async (): Promise<{ total: number; events: MonitoringEvent[] }> =>
      delay({ total: MOCK_MONITORING_EVENTS.length, events: [...MOCK_MONITORING_EVENTS] }),
    unreadCount: async (): Promise<{ unreadCount: number }> =>
      delay({ unreadCount: MOCK_MONITORING_EVENTS.filter((e) => !e.readAt).length }),
    markRead: async (eventId: string): Promise<MonitoringEvent> => {
      const ev = MOCK_MONITORING_EVENTS.find((e) => e.id === eventId) ?? MOCK_MONITORING_EVENTS[0];
      return delay({ ...ev, readAt: new Date().toISOString() });
    },
  },
};

export default mockApi;

// ─── Mock data for App.tsx apiFetch paths ─────────────────────────────────────

export const MOCK_FETCH_RESPONSES: Record<string, unknown> = {
  '/api/v1/jurisdictions': { jurisdictions: MOCK_JURISDICTIONS },
  '/api/v1/incentive-rules': { rules: MOCK_INCENTIVE_RULES },
  '/api/v1/productions': { productions: MOCK_PRODUCTIONS },
  '/api/v1/monitoring/events': { total: MOCK_MONITORING_EVENTS.length, events: MOCK_MONITORING_EVENTS },
};

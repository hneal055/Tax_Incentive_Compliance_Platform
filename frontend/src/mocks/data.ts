import type { Production, Jurisdiction, IncentiveRule } from '../types';

const J = (id: string, code: string, name: string, country: string, type: string, description: string, website: string): Jurisdiction => ({
  id, code, name, country, type, description, website, active: true,
  currency: 'USD', treatyPartners: [],
  createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
});

export const mockJurisdictions: Jurisdiction[] = [
  J('jur-ca-001', 'CA', 'California', 'USA', 'state', 'California Film & Television Tax Credit Program 3.0 — competitive credit up to 25% of qualified expenditures.', 'https://film.ca.gov/tax-credit/'),
  J('jur-ga-001', 'GA', 'Georgia', 'USA', 'state', 'Georgia Entertainment Industry Investment Act — 20% base + 10% uplift with Georgia logo.', 'https://www.georgia.org/film'),
  J('jur-ny-001', 'NY', 'New York', 'USA', 'state', 'New York Film Tax Credit — 25–35% of qualified below-the-line production costs.', 'https://esd.ny.gov/nyc-film-tv-production'),
  J('jur-la-001', 'LA', 'Louisiana', 'USA', 'state', 'Louisiana Entertainment Tax Credit — 25% base rebate on qualified production costs.', 'https://www.louisianaentertainment.gov'),
  J('jur-nm-001', 'NM', 'New Mexico', 'USA', 'state', 'New Mexico Film Production Tax Credit — 25–40% refundable tax credit.', 'https://nmfilm.com/incentives/'),
  J('jur-uk-001', 'UK', 'United Kingdom', 'GBR', 'national', 'UK Film Tax Relief — 25% on qualifying UK production expenditure.', 'https://www.bfi.org.uk/get-funding-and-support/film-tax-relief'),
];

export const mockIncentiveRules: IncentiveRule[] = [
  {
    id: 'rule-ca-001', jurisdictionId: 'jur-ca-001',
    ruleName: 'California Film Tax Credit 3.0', ruleCode: 'CA-FTC-3',
    incentiveType: 'tax_credit', creditType: 'non_refundable',
    percentage: 25, minSpend: 1000000, maxCredit: 25000000,
    eligibleExpenses: ['labor', 'equipment', 'locations', 'post_production'],
    excludedExpenses: ['story_rights', 'music_rights', 'marketing'],
    effectiveDate: '2020-07-01',
    requirements: 'Minimum 75 shooting days in California. Competitive allocation.',
    active: true, createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-ga-001', jurisdictionId: 'jur-ga-001',
    ruleName: 'Georgia Entertainment Tax Credit — Base', ruleCode: 'GA-ETC-BASE',
    incentiveType: 'tax_credit', creditType: 'transferable',
    percentage: 20, minSpend: 500000,
    eligibleExpenses: ['labor', 'equipment', 'locations', 'post_production', 'catering'],
    excludedExpenses: ['story_rights'],
    effectiveDate: '2008-01-01',
    requirements: 'No Georgia promotional logo required.',
    active: true, createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-ga-002', jurisdictionId: 'jur-ga-001',
    ruleName: 'Georgia Entertainment Tax Credit — Logo Uplift', ruleCode: 'GA-ETC-LOGO',
    incentiveType: 'tax_credit', creditType: 'transferable',
    percentage: 10, minSpend: 500000,
    eligibleExpenses: ['labor', 'equipment', 'locations', 'post_production'],
    excludedExpenses: ['story_rights'],
    effectiveDate: '2008-01-01',
    requirements: 'Must include Georgia promotional logo in end credits.',
    active: true, createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-ny-001', jurisdictionId: 'jur-ny-001',
    ruleName: 'New York Film Tax Credit', ruleCode: 'NY-FTC',
    incentiveType: 'tax_credit', creditType: 'refundable',
    percentage: 25, minSpend: 1000000, maxCredit: 7000000,
    eligibleExpenses: ['labor', 'equipment', 'locations'],
    excludedExpenses: ['story_rights', 'above_the_line'],
    effectiveDate: '2004-01-01',
    requirements: '75% of shooting days must occur in New York.',
    active: true, createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-la-001', jurisdictionId: 'jur-la-001',
    ruleName: 'Louisiana Entertainment Tax Credit', ruleCode: 'LA-ETC',
    incentiveType: 'rebate', creditType: 'refundable',
    percentage: 25, minSpend: 300000,
    eligibleExpenses: ['labor', 'equipment', 'locations', 'post_production'],
    excludedExpenses: ['story_rights'],
    effectiveDate: '2002-07-01',
    requirements: 'Must be a Louisiana-based production entity.',
    active: true, createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-nm-001', jurisdictionId: 'jur-nm-001',
    ruleName: 'New Mexico Film Production Tax Credit', ruleCode: 'NM-FPTC',
    incentiveType: 'tax_credit', creditType: 'refundable',
    percentage: 25, minSpend: 0,
    eligibleExpenses: ['labor', 'equipment', 'locations', 'post_production'],
    excludedExpenses: ['story_rights', 'music_rights'],
    effectiveDate: '2003-04-01',
    requirements: 'Must employ New Mexico residents.',
    active: true, createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
  {
    id: 'rule-uk-001', jurisdictionId: 'jur-uk-001',
    ruleName: 'UK Film Tax Relief', ruleCode: 'UK-FTR',
    incentiveType: 'tax_credit', creditType: 'refundable',
    percentage: 25, minSpend: 0,
    eligibleExpenses: ['labor', 'equipment', 'locations', 'post_production', 'visual_effects'],
    excludedExpenses: ['marketing', 'distribution'],
    effectiveDate: '2007-01-01',
    requirements: 'Must pass BFI Cultural Test. Minimum 10% core UK expenditure.',
    active: true, createdAt: '2024-01-01T00:00:00Z', updatedAt: '2024-01-01T00:00:00Z',
  },
];

export const mockProductionsInitial: Production[] = [
  {
    id: 'prod-001', title: 'Neon Meridian', productionType: 'feature_film',
    productionCompany: 'Watershed Pictures', budgetTotal: 12500000, budgetQualifying: 9800000,
    startDate: '2025-03-01', endDate: '2025-09-30', jurisdictionId: 'jur-ca-001',
    status: 'production', createdAt: '2025-01-15T10:00:00Z', updatedAt: '2025-03-01T08:00:00Z',
  },
  {
    id: 'prod-002', title: 'The Holloway Protocol', productionType: 'tv_series',
    productionCompany: 'Crescent Bay Studios', budgetTotal: 6200000, budgetQualifying: 5100000,
    startDate: '2025-05-15', endDate: '2025-11-30', jurisdictionId: 'jur-ga-001',
    status: 'pre_production', createdAt: '2025-02-01T09:30:00Z', updatedAt: '2025-02-20T14:00:00Z',
  },
  {
    id: 'prod-003', title: 'Dust & Light', productionType: 'documentary',
    productionCompany: 'Parallax Films', budgetTotal: 850000, budgetQualifying: 720000,
    startDate: '2025-07-01', jurisdictionId: 'jur-ny-001',
    status: 'planning', createdAt: '2025-03-10T11:00:00Z', updatedAt: '2025-03-10T11:00:00Z',
  },
];

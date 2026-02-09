import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Dashboard from '../pages/Dashboard'

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useNavigate: () => mockNavigate };
});

const mockSelectProduction = vi.fn();
const mockRefreshAll = vi.fn().mockResolvedValue(undefined);
vi.mock('../store', () => ({
  useAppStore: vi.fn(() => ({
    productions: [
      { id: '1', title: 'Bad Boys', budgetTotal: 35000000, status: 'PRODUCTION', productionCompany: 'Neal Studio' },
      { id: '2', title: 'Test Movie', budgetTotal: 5000000, status: 'planning', productionCompany: 'Default Co' },
    ],
    jurisdictions: [
      { id: 'j1', code: 'CA', name: 'California' },
      { id: 'j2', code: 'GA', name: 'Georgia' },
    ],
    dashboardMetrics: {
      totalBudget: 40000000,
      estimatedCredits: 8000000,
      complianceRate: 100,
      lastUpdated: new Date(),
    },
    rulesByJurisdiction: {
      j1: [{ id: 'r1', jurisdictionId: 'j1', ruleName: 'CA Film Credit', percentage: 20, minSpend: 1000000 }],
      j2: [{ id: 'r2', jurisdictionId: 'j2', ruleName: 'GA Film Credit', percentage: 20, minSpend: 0 }],
    },
    monitoringEvents: [
      { id: 'e1', title: 'Audit Completed', summary: 'Audit done', eventType: 'audit', severity: 'info', detectedAt: new Date().toISOString(), jurisdictionId: 'j1', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
      { id: 'e2', title: 'Incentive Updated', summary: 'Rate changed', eventType: 'rate_change', severity: 'warning', detectedAt: new Date().toISOString(), jurisdictionId: 'j2', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
      { id: 'e3', title: 'Flag Raised', summary: 'Review needed', eventType: 'compliance', severity: 'critical', detectedAt: new Date().toISOString(), jurisdictionId: 'j1', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    ],
    unreadEventCount: 3,
    refreshAll: mockRefreshAll,
    fetchProductions: vi.fn().mockResolvedValue([]),
    fetchJurisdictions: vi.fn().mockResolvedValue([]),
    selectProduction: mockSelectProduction,
    isLoading: false,
  })),
}))

global.fetch = vi.fn().mockResolvedValue({
  ok: true,
  json: () => Promise.resolve({ status: 'healthy' }),
});

const renderDashboard = () => render(<BrowserRouter><Dashboard /></BrowserRouter>)

describe('Dashboard Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    localStorage.getItem = vi.fn().mockReturnValue(null)
    mockNavigate.mockClear()
    mockSelectProduction.mockClear()
  })

  describe('Rendering', () => {
    it('renders dashboard title', async () => {
      renderDashboard()
      await waitFor(() => { expect(screen.getByText('Dashboard')).toBeInTheDocument() })
    })

    it('renders metric cards', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText('Total Productions')).toBeInTheDocument()
        expect(screen.getByText('Total Jurisdictions')).toBeInTheDocument()
        expect(screen.getByText('Total Expenses')).toBeInTheDocument()
        expect(screen.getByText('Credits Awarded')).toBeInTheDocument()
      })
    })

    it('shows correct monitoring subtitle', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText(/Monitoring 2 productions across 2 jurisdictions/)).toBeInTheDocument()
      })
    })
  })

  describe('Navigation & Quick Actions', () => {
    it('navigates to reports from compliance card', async () => {
      renderDashboard()
      await waitFor(() => {
        const button = screen.getByText('View Full Report')
        fireEvent.click(button)
        expect(mockNavigate).toHaveBeenCalledWith('/reports')
      })
    })

    it('navigates to productions from View All button', async () => {
      renderDashboard()
      await waitFor(() => {
        const button = screen.getByText('View All')
        fireEvent.click(button)
        expect(mockNavigate).toHaveBeenCalledWith('/productions')
      })
    })
  })

  describe('Recent Activity', () => {
    it('renders recent activity items from monitoring events', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText('Audit Completed')).toBeInTheDocument()
        expect(screen.getByText('Incentive Updated')).toBeInTheDocument()
        expect(screen.getByText('Flag Raised')).toBeInTheDocument()
      })
    })
  })

  describe('Quick Overview - Production List', () => {
    it('renders production titles in the overview', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText('Bad Boys')).toBeInTheDocument()
        expect(screen.getByText('Test Movie')).toBeInTheDocument()
      })
    })

    it('selects production and navigates when clicking a production row', async () => {
      renderDashboard()
      await waitFor(() => {
        const badBoys = screen.getByText('Bad Boys')
        fireEvent.click(badBoys)
        expect(mockSelectProduction).toHaveBeenCalledWith(
          expect.objectContaining({ id: '1', title: 'Bad Boys' })
        )
        expect(mockNavigate).toHaveBeenCalledWith('/productions')
      })
    })
  })

  describe('Compliance Card', () => {
    it('renders the compliance status', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText('Compliance Status')).toBeInTheDocument()
        expect(screen.getByText('100.0%')).toBeInTheDocument()
      })
    })
  })

  describe('Data Refresh', () => {
    it('calls refreshAll on mount', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(mockRefreshAll).toHaveBeenCalled()
      })
    })
  })
})

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

    it('shows correct monitoring count', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText(/Monitoring/)).toBeInTheDocument()
        expect(screen.getByText(/2 production/)).toBeInTheDocument()
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
    it('renders recent activity items', async () => {
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

  describe('Production Overview', () => {
    it('renders production list section title', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText('Top Productions')).toBeInTheDocument()
      })
    })
  })
})

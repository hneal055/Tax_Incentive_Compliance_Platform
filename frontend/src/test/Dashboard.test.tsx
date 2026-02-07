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
        expect(screen.getByText('Active Productions')).toBeInTheDocument()
        expect(screen.getByText('Jurisdictions')).toBeInTheDocument()
        expect(screen.getByText('Compliance Rate')).toBeInTheDocument()
        expect(screen.getByText('Total Budget')).toBeInTheDocument()
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
    it('navigates to productions when New Production is clicked', async () => {
      renderDashboard()
      await waitFor(() => {
        const button = screen.getByText('New Production')
        fireEvent.click(button)
        expect(mockNavigate).toHaveBeenCalledWith('/productions')
      })
    })

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
        const button = screen.getByText('View All Productions')
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

  describe('Zoom Controls', () => {
    it('renders zoom controls with default 100%', async () => {
      renderDashboard()
      await waitFor(() => {
        expect(screen.getByText('100%')).toBeInTheDocument()
        expect(screen.getByTitle('Zoom in')).toBeInTheDocument()
        expect(screen.getByTitle('Zoom out')).toBeInTheDocument()
        expect(screen.getByTitle('Reset zoom')).toBeInTheDocument()
      })
    })

    it('changes zoom display when zoom in is clicked', async () => {
      renderDashboard()
      await waitFor(() => { expect(screen.getByText('100%')).toBeInTheDocument() })
      fireEvent.click(screen.getByTitle('Zoom in'))
      // ZOOM_LEVELS: [0.75, 0.85, 1, 1.15, 1.25] - from 100% (index 2) zoom in goes to 115% (index 3)
      await waitFor(() => { expect(screen.getByText('115%')).toBeInTheDocument() })
    })

    it('changes zoom display when zoom out is clicked', async () => {
      renderDashboard()
      await waitFor(() => { expect(screen.getByText('100%')).toBeInTheDocument() })
      fireEvent.click(screen.getByTitle('Zoom out'))
      // ZOOM_LEVELS: [0.75, 0.85, 1, 1.15, 1.25] - from 100% (index 2) zoom out goes to 85% (index 1)
      await waitFor(() => { expect(screen.getByText('85%')).toBeInTheDocument() })
    })
  })

  describe('System Health', () => {
    it('renders the system health indicator', async () => {
      renderDashboard()
      await waitFor(() => { expect(screen.getByText('Healthy')).toBeInTheDocument() })
    })
  })
})

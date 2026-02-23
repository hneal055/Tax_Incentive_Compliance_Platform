import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CreateProductionModal from '../components/CreateProductionModal'

// Mock the store
const mockCreateProduction = vi.fn()
vi.mock('../store', () => ({
  useAppStore: vi.fn(() => ({
    createProduction: mockCreateProduction,
  })),
}))

describe('CreateProductionModal Component', () => {
  const defaultProps = {
    isOpen: true,
    onClose: vi.fn(),
    jurisdictions: [
      { id: 'j1', code: 'CA', name: 'California' },
      { id: 'j2', code: 'GA', name: 'Georgia' },
    ],
    onSuccess: vi.fn(),
  }

  beforeEach(() => {
    vi.clearAllMocks()
    mockCreateProduction.mockResolvedValue({})
  })

  it('renders modal title', () => {
    render(<CreateProductionModal {...defaultProps} />)
    expect(screen.getByText('Create New Production')).toBeInTheDocument()
  })

  it('renders form fields', () => {
    render(<CreateProductionModal {...defaultProps} />)
    expect(screen.getByText('Production Title')).toBeInTheDocument()
    expect(screen.getByText('Budget ($)')).toBeInTheDocument()
    expect(screen.getByText('Production Type')).toBeInTheDocument()
    expect(screen.getByText('Jurisdiction (Optional)')).toBeInTheDocument()
    expect(screen.getByText('Production Company (Optional)')).toBeInTheDocument()
  })

  it('renders Cancel and Create buttons', () => {
    render(<CreateProductionModal {...defaultProps} />)
    expect(screen.getByText('Cancel')).toBeInTheDocument()
    expect(screen.getByText('Create Production')).toBeInTheDocument()
  })

  it('Create button is disabled when form is empty', () => {
    render(<CreateProductionModal {...defaultProps} />)
    const createButton = screen.getByText('Create Production')
    expect(createButton.closest('button')).toBeDisabled()
  })

  it('calls onClose when Cancel is clicked', () => {
    const onClose = vi.fn()
    render(<CreateProductionModal {...defaultProps} onClose={onClose} />)
    fireEvent.click(screen.getByText('Cancel'))
    expect(onClose).toHaveBeenCalled()
  })

  it('allows entering production title', async () => {
    const user = userEvent.setup()
    render(<CreateProductionModal {...defaultProps} />)
    
    const titleInput = screen.getByPlaceholderText('Enter production title')
    await user.type(titleInput, 'New Movie')
    expect(titleInput).toHaveValue('New Movie')
  })

  it('allows entering budget', async () => {
    const user = userEvent.setup()
    render(<CreateProductionModal {...defaultProps} />)
    
    const budgetInput = screen.getByPlaceholderText('1,000,000')
    await user.type(budgetInput, '5000000')
    expect(budgetInput).toHaveValue(5000000)
  })

  it('allows selecting production type', async () => {
    render(<CreateProductionModal {...defaultProps} />)
    
    const typeSelect = screen.getByTitle('Select production type')
    fireEvent.change(typeSelect, { target: { value: 'tv_series' } })
    expect(typeSelect).toHaveValue('tv_series')
  })

  it('allows selecting jurisdiction', async () => {
    render(<CreateProductionModal {...defaultProps} />)
    
    const jurisdictionSelect = screen.getByTitle('Select jurisdiction')
    fireEvent.change(jurisdictionSelect, { target: { value: 'j1' } })
    expect(jurisdictionSelect).toHaveValue('j1')
  })

  it('does not render when isOpen is false', () => {
    render(<CreateProductionModal {...defaultProps} isOpen={false} />)
    expect(screen.queryByText('Create New Production')).not.toBeInTheDocument()
  })

  it('shows production type options', () => {
    render(<CreateProductionModal {...defaultProps} />)
    expect(screen.getByText('Feature Film')).toBeInTheDocument()
    expect(screen.getByText('TV Series')).toBeInTheDocument()
    expect(screen.getByText('Commercial')).toBeInTheDocument()
    expect(screen.getByText('Documentary')).toBeInTheDocument()
  })
})

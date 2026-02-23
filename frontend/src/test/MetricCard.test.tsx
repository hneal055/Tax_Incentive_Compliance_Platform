import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import MetricCard from '../components/MetricCard'
import { Film } from 'lucide-react'

describe('MetricCard Component', () => {
  const defaultProps = {
    title: 'Active Productions',
    value: 5,
    icon: Film,
  }

  it('renders title', () => {
    render(<MetricCard {...defaultProps} />)
    expect(screen.getByText('Active Productions')).toBeInTheDocument()
  })

  it('renders numeric value after animation', async () => {
    render(<MetricCard {...defaultProps} />)
    await waitFor(() => {
      expect(screen.getByText('5')).toBeInTheDocument()
    }, { timeout: 2000 })
  })

  it('renders string value immediately', () => {
    render(<MetricCard {...defaultProps} value="33+" />)
    expect(screen.getByText('33+')).toBeInTheDocument()
  })
})

import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import Card from '../components/Card'

describe('Card Component', () => {
  it('renders with title', () => {
    render(<Card title="Test Card">Content</Card>)
    expect(screen.getByText('Test Card')).toBeInTheDocument()
  })

  it('applies hoverable class', () => {
    const { container } = render(<Card title="Hover" hoverable>Content</Card>)
    expect(container.firstChild).toHaveClass('hover:shadow-xl')
  })
})

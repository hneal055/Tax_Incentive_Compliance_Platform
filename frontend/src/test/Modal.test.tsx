import { describe, it, expect, vi, afterEach } from 'vitest'
import { render, screen, fireEvent, cleanup } from '@testing-library/react'
import Modal from '../components/Modal'

describe('Modal Component', () => {
  afterEach(() => {
    cleanup()
    // Clean up any portal content from document.body
    document.body.innerHTML = ''
  })

  it('renders when isOpen is true', () => {
    render(
      <Modal isOpen={true} onClose={() => {}} title="Test Modal">
        Modal content
      </Modal>
    )
    expect(screen.getByText('Test Modal')).toBeInTheDocument()
    expect(screen.getByText('Modal content')).toBeInTheDocument()
  })

  it('does not render when isOpen is false', () => {
    render(
      <Modal isOpen={false} onClose={() => {}} title="Test Modal">
        Modal content
      </Modal>
    )
    expect(screen.queryByText('Test Modal')).not.toBeInTheDocument()
  })

  it('calls onClose when close button is clicked', () => {
    const handleClose = vi.fn()
    render(
      <Modal isOpen={true} onClose={handleClose} title="Test Modal">
        Content
      </Modal>
    )
    
    const closeButton = screen.getByRole('button', { name: /close/i })
    fireEvent.click(closeButton)
    expect(handleClose).toHaveBeenCalledTimes(1)
  })

  it('calls onClose when backdrop is clicked', () => {
    const handleClose = vi.fn()
    render(
      <Modal isOpen={true} onClose={handleClose} title="Test Modal">
        Content
      </Modal>
    )
    
    // Find backdrop by its position (absolute inset-0) - it has the click handler
    const backdrop = document.querySelector('.absolute.inset-0')
    if (backdrop) fireEvent.click(backdrop)
    expect(handleClose).toHaveBeenCalled()
  })

  it('calls onClose when Escape key is pressed', () => {
    const handleClose = vi.fn()
    render(
      <Modal isOpen={true} onClose={handleClose} title="Test Modal">
        Content
      </Modal>
    )
    
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(handleClose).toHaveBeenCalled()
  })

  it('applies correct size class', () => {
    render(
      <Modal isOpen={true} onClose={() => {}} title="Large Modal" size="lg">
        Content
      </Modal>
    )
    
    // Portal renders to document.body, so check there
    expect(document.body.innerHTML).toContain('max-w-lg')
  })
})

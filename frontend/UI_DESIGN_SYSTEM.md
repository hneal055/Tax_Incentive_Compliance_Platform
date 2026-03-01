# PilotForge UI Design System

## Design Overview

Modern, professional dashboard for film production tax incentive management. Built with React, TypeScript, Tailwind CSS, and Recharts.

## Color Palette

- **Primary Blue**: #0ea5e9 (Cyan-600)
- **Dark Blue**: #0284c7 (Cyan-700)
- **Success Green**: #16a34a (Green-600)
- **Purple Accent**: #7c3aed (Violet-600)
- **Amber Alert**: #d97706 (Amber-600)
- **Slate Background**: #f8fafc (Slate-50)
- **Dark Slate**: #0f172a (Slate-900)

## Typography

- **Headings**: Inter, Bold (h1-h3)
- **Body**: Inter, Regular (400)
- **Buttons**: Inter, Medium (500)
- **Small**: Inter, Regular (12px)

## Components

### 1. Sidebar Navigation
- Fixed left sidebar (collapsible on mobile)
- Dark slate background with blue accents
- Active state highlighting
- NEW badge for new features
- User profile footer

### 2. Metric Cards
- Grid layout (1-4 columns responsive)
- Icon with background color
- Title, value, subtitle
- Hover shadow effect
- Clean borders

### 3. Charts
- Recharts bar charts with gradient colors
- Responsive container sizing
- Custom tooltips
- Grid background
- Legend below chart

### 4. Data Tables
- Production cards with status badges
- Progress bars
- Metric breakdowns
- Hover states
- Search and filter capabilities

### 5. Calculator Input
- Range sliders
- Number inputs
- Dropdown selectors
- Real-time calculations
- Result cards

## Pages

### Executive Dashboard
- 4 metric cards (Budget, Tax Credits, Active Projects, Alerts)
- Budget vs. Actual Spend chart
- Production performance overview

### Productions
- Searchable production list
- Status filters (All, Active, Planning, Completed)
- Production cards with details
- Progress tracking
- Quick metrics

### Incentive Calculator
- Budget input with slider
- Jurisdiction selector
- Qualifying expenses calculator
- Real-time tax credit calculation
- Export and save functionality

### Jurisdictions (Planned)
- Tax incentive rates by jurisdiction
- Comparison tools
- Incentive details

### AI Advisor (Planned)
- AI-powered recommendations
- Production optimization
- Risk assessment

## Responsive Design

- **Desktop**: Full sidebar + main content
- **Tablet**: Collapsible sidebar
- **Mobile**: Hamburger menu, full-width content

## Animations

- Smooth transitions (300ms)
- Hover state changes
- Progress bar animations
- Chart animations on load

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Focus states on interactive elements


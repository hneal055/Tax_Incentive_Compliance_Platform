# 🎬 PilotForge Developer Portal

A lightweight Next.js-based developer portal for the PilotForge API, featuring interactive OpenAPI documentation.

## Overview

This developer portal provides comprehensive API documentation for PilotForge - Tax Incentive Intelligence for Film & TV Productions. It includes:

- **Interactive Swagger UI** - Try out API endpoints directly in the browser
- **ReDoc Documentation** - Clean, professional API reference
- **Getting Started Guide** - Quick start examples and integration guides
- **OpenAPI 3.1 Specification** - Full API specification in JSON format

## Features

- 🚀 Built with Next.js 16 and React 19
- 📚 Dual documentation interfaces (Swagger UI & ReDoc)
- 🎨 Modern, responsive design with Tailwind CSS
- ⚡ Fast page loads with static generation
- 🔍 Interactive API exploration and testing
- 📱 Mobile-friendly interface

## Prerequisites

- Node.js 20+ and npm 10+
- The PilotForge backend API running on `http://localhost:8000`

## Quick Start

### Installation

```bash
cd developer-portal
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The portal will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
developer-portal/
├── app/
│   ├── docs/              # API documentation pages
│   │   ├── page.tsx       # Swagger UI page
│   │   └── redoc/
│   │       └── page.tsx   # ReDoc page
│   ├── layout.tsx         # Root layout with navigation
│   ├── page.tsx           # Homepage
│   └── globals.css        # Global styles
├── public/
│   └── openapi.json       # OpenAPI specification
└── package.json           # Dependencies
```

## Available Pages

### Homepage (`/`)
Welcome page with:
- API overview and features
- Quick start guide
- Example requests
- Links to documentation

### Swagger UI (`/docs`)
Interactive API documentation where you can:
- Browse all endpoints
- View request/response schemas
- Test API calls directly
- See example payloads

### ReDoc (`/docs/redoc`)
Professional API reference with:
- Clean, scrollable documentation
- Search functionality
- Code samples
- Schema explorer

## Customization

### Update OpenAPI Specification

The portal uses the OpenAPI spec from `/public/openapi.json`. To update it:

1. Generate the latest spec from the backend:
   ```bash
   cd ..
   python -m uvicorn src.main:app --reload
   # Visit http://localhost:8000/openapi.json
   ```

2. Copy the updated spec:
   ```bash
   cp ../openapi.json public/openapi.json
   ```

### Styling

The portal uses Tailwind CSS for styling. Customize colors and themes in:
- `tailwind.config.js` - Tailwind configuration
- `app/globals.css` - Global styles
- Component files - Individual page styles

### Branding

Update branding elements in:
- `app/layout.tsx` - Site title and metadata
- `app/page.tsx` - Homepage content
- `public/` - Add your logo and favicon

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```bash
docker build -t pilotforge-portal .
docker run -p 3000:3000 pilotforge-portal
```

### Static Export

```bash
npm run build
# Deploy the 'out' directory to any static host
```

## Technologies Used

- **Next.js 16** - React framework with App Router
- **React 19** - Latest React with concurrent features
- **TypeScript 5** - Type-safe development
- **Tailwind CSS 4** - Utility-first styling
- **Swagger UI React** - Interactive API documentation
- **ReDoc** - Professional API reference
- **OpenAPI 3.1** - API specification standard

## Configuration

### Development Port

To change the development port, edit `package.json`:

```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

### API Base URL

Update API references in `app/page.tsx` if your backend runs on a different URL.

## Contributing

1. Make your changes
2. Test locally: `npm run dev`
3. Build: `npm run build`
4. Submit a pull request

## License

MIT License - Part of the PilotForge project

## Support

For questions or issues:
- Check the main [PilotForge README](../README.md)
- Review API documentation at `/docs`
- Contact the development team

---

**Part of PilotForge** - Tax Incentive Intelligence for Film & TV Productions


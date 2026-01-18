# 🛠️ Development Tips & Workflow

## For Reviewers and Testers

### Getting Started
1. **Clone the repository**
2. **Start the full stack** using `./start-fullstack.sh` (Linux/Mac) or `.\start-fullstack.ps1` (Windows)
3. **Open your browser** to http://localhost:3000
4. **Review the application** - all features should be functional

### What to Review
- ✅ Dashboard displays correctly
- ✅ Navigation between pages works smoothly
- ✅ Productions page loads (may be empty initially)
- ✅ Jurisdictions page shows the list of tax incentive programs
- ✅ Calculator page accepts input
- ✅ No JavaScript errors in browser console (F12 → Console)
- ✅ Responsive design works on different screen sizes

### Making Changes

The frontend uses **Hot Module Replacement (HMR)**, so changes appear instantly:

1. Edit any file in `src/`
2. Save the file
3. Browser updates automatically (no refresh needed)

### File Structure

```
frontend/src/
├── components/     # Reusable UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   ├── Layout.tsx
│   ├── Navbar.tsx
│   └── Spinner.tsx
├── pages/          # Page components (routes)
│   ├── Dashboard.tsx
│   ├── Productions.tsx
│   ├── Jurisdictions.tsx
│   └── Calculator.tsx
├── store/          # Zustand state management
├── App.tsx         # Root component with routing
└── main.tsx        # Entry point
```

## For Developers

### Development Workflow

1. **Start with the startup script** for automatic checks and setup
2. **Keep the backend running** - the frontend needs API access
3. **Use TypeScript** - fix type errors before committing
4. **Run ESLint** before committing: `npm run lint`
5. **Test the production build** occasionally: `npm run build && npm run preview`

### Environment Variables

Create `.env` file (optional):
```bash
VITE_API_URL=http://localhost:8000
```

All environment variables must be prefixed with `VITE_` to be accessible in code.

### API Integration

The frontend uses Axios for HTTP requests. API proxy is configured in `vite.config.ts`:

```typescript
// Requests to /api/* are proxied to http://localhost:8000
fetch('/api/v1/jurisdictions')  // → http://localhost:8000/api/v1/jurisdictions
```

### State Management

Uses **Zustand** for simple, lightweight state management:

```typescript
// Example: Using a store
const productions = useProductionStore((state) => state.productions);
const addProduction = useProductionStore((state) => state.addProduction);
```

### Styling

Uses **TailwindCSS 4** with utility classes:

```tsx
<div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
  <h1 className="text-2xl font-bold text-gray-900">Title</h1>
</div>
```

### Common Tasks

**Adding a new page:**
1. Create component in `src/pages/MyPage.tsx`
2. Add route in `src/App.tsx`
3. Add navigation link in `src/components/Navbar.tsx`

**Adding a new component:**
1. Create in `src/components/MyComponent.tsx`
2. Export it
3. Import and use in pages

**Debugging:**
1. Check browser console (F12) for errors
2. Use React DevTools browser extension
3. Check Network tab for API calls
4. Verify backend is responding: `curl http://localhost:8000/health`

### Testing Locally

Before submitting changes:

```bash
# Check types
npm run type-check

# Check code quality
npm run lint

# Build production version
npm run build

# Test production build
npm run preview
```

### Port Conflicts

If port 3000 is in use:

```bash
# Use a different port
npm run dev -- --port 3001

# Or find and stop the process using port 3000
# Linux/Mac:
lsof -ti:3000 | xargs kill

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

## Browser DevTools

### Essential Shortcuts

- **F12** - Open DevTools
- **Ctrl+Shift+C** (Cmd+Shift+C on Mac) - Inspect element
- **Ctrl+Shift+J** (Cmd+Option+J on Mac) - Console
- **Ctrl+Shift+R** (Cmd+Shift+R on Mac) - Hard refresh

### DevTools Tabs to Use

1. **Console** - JavaScript errors and logs
2. **Network** - API calls and responses
3. **Elements** - Inspect HTML/CSS
4. **React DevTools** - React component tree (install extension)

## Performance Tips

1. **Vite is fast** - builds are near-instant
2. **HMR is instant** - changes appear in milliseconds
3. **Use React DevTools Profiler** for performance analysis
4. **Check bundle size** - `npm run build` shows gzipped size

## Deployment Checklist

Before deploying to production:

- [ ] All TypeScript errors fixed (`npm run type-check`)
- [ ] No ESLint errors (`npm run lint`)
- [ ] Production build succeeds (`npm run build`)
- [ ] Production build tested (`npm run preview`)
- [ ] Environment variables configured for production
- [ ] API URL points to production backend
- [ ] All features tested manually
- [ ] No console errors in production build

## Need Help?

1. Check [UI_SETUP.md](../UI_SETUP.md) for troubleshooting
2. Check [FRONTEND_README.md](./FRONTEND_README.md) for tech stack info
3. Review Vite docs: https://vite.dev/
4. Review React docs: https://react.dev/

---

**Happy coding! 🎬**

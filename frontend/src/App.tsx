/**
 * PilotForge - Tax Incentive Intelligence for Film & TV
 * Copyright (c) 2026 PilotForge - Tax Incentive Compliance Platform
 * All Rights Reserved.
 * 
 * PROPRIETARY AND CONFIDENTIAL
 * This software is proprietary and confidential. Unauthorized copying,
 * distribution, modification, or use is strictly prohibited.
 */
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import Layout from './components/Layout';
import Spinner from './components/Spinner';

// Import Dashboard directly - it's the main page accessed immediately
import Dashboard from './pages/Dashboard';

// Lazy load other pages for better performance
const Productions = lazy(() => import('./pages/Productions'));
const Jurisdictions = lazy(() => import('./pages/Jurisdictions'));
const Calculator = lazy(() => import('./pages/Calculator'));
const MonitoringDashboard = lazy(() => import('./pages/MonitoringDashboard'));

function App() {
  return (
    <Router>
      <Layout>
        <Suspense fallback={<div className="flex items-center justify-center h-full"><Spinner size="lg" /></div>}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/productions" element={<Productions />} />
            <Route path="/jurisdictions" element={<Jurisdictions />} />
            <Route path="/calculator" element={<Calculator />} />
            <Route path="/monitoring" element={<MonitoringDashboard />} />
          </Routes>
        </Suspense>
      </Layout>
    </Router>
  );
}

export default App;

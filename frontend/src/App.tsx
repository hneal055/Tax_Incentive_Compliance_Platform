import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import Layout from './components/Layout';
import Spinner from './components/Spinner';

// Lazy load pages for better performance
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Productions = lazy(() => import('./pages/Productions'));
const Jurisdictions = lazy(() => import('./pages/Jurisdictions'));
const Calculator = lazy(() => import('./pages/Calculator'));

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
          </Routes>
        </Suspense>
      </Layout>
    </Router>
  );
}

export default App;

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Productions from './pages/Productions';
import Jurisdictions from './pages/Jurisdictions';
import Calculator from './pages/Calculator';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/productions" element={<Productions />} />
          <Route path="/jurisdictions" element={<Jurisdictions />} />
          <Route path="/calculator" element={<Calculator />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;

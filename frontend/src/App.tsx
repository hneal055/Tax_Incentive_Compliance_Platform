import { useState } from 'react';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Productions from './pages/Productions';
import Calculator from './pages/Calculator';
import Jurisdictions from './pages/Jurisdictions';
import AIAdvisor from './components/AIAdvisor';
import type { Production } from './types';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [productions, setProductions] = useState<Production[]>([]);

  const handleAddProduction = (newProduction: Production) => {
    setProductions((prev) => [...prev, newProduction]);
  };

  const handleUpdateProduction = (updatedProduction: Production) => {
    setProductions((prev) =>
      prev.map(p => p.id === updatedProduction.id ? updatedProduction : p)
    );
  };

  const handleDeleteProduction = (id: string) => {
    setProductions((prev) => prev.filter(p => p.id !== id));
  };

  // Shared production handlers
  const productionHandlers = {
    onAddProduction: handleAddProduction,
    onUpdateProduction: handleUpdateProduction,
    onDeleteProduction: handleDeleteProduction,
  };

  // Tab component map for cleaner rendering
  const tabComponents: Record<string, React.ReactNode> = {
    // Dashboard updated to static design, no props needed
    dashboard: <Dashboard />, 
    productions: (
      <Productions
        productions={productions}
        {...productionHandlers}
      />
    ),
    calculator: <Calculator productions={productions} {...productionHandlers} />,
    jurisdictions: (
      <Jurisdictions
        productions={productions}
        {...productionHandlers}
      />
    ),
    advisor: <AIAdvisor />,
  };

  return (
    <Layout activeTab={activeTab} onTabChange={setActiveTab}>
      {tabComponents[activeTab] || tabComponents.dashboard}
    </Layout>
  );
}

export default App;

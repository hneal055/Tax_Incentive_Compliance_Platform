import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import { useAppStore } from '../store';

const Calculator: React.FC = () => {
  const { productions, jurisdictions, fetchProductions, fetchJurisdictions, isLoading } = useAppStore();
  const [selectedProduction, setSelectedProduction] = useState('');
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('');
  const [results, setResults] = useState<any>(null);
  const [calculating, setCalculating] = useState(false);

  useEffect(() => {
    fetchProductions();
    fetchJurisdictions();
  }, [fetchProductions, fetchJurisdictions]);

  const handleCalculate = async () => {
    if (!selectedProduction || !selectedJurisdiction) {
      alert('Please select both a production and a jurisdiction');
      return;
    }

    setCalculating(true);
    // Simulate calculation - in real app would call API
    setTimeout(() => {
      const production = productions.find(p => p.id === selectedProduction);
      if (production) {
        setResults({
          production: production.title,
          jurisdiction: jurisdictions.find(j => j.id === selectedJurisdiction)?.name,
          totalExpenses: production.budget,
          qualifiedExpenses: production.budget * 0.85,
          incentiveAmount: production.budget * 0.85 * 0.25,
          effectiveRate: 21.25,
        });
      }
      setCalculating(false);
    }, 1500);
  };

  if (isLoading && productions.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Tax Incentive Calculator</h1>
        <p className="text-gray-600 mt-1">Calculate potential tax incentives for your production</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Select Production & Jurisdiction">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Production
              </label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-pilotforge-blue focus:border-pilotforge-blue"
                value={selectedProduction}
                onChange={(e) => setSelectedProduction(e.target.value)}
              >
                <option value="">Select a production</option>
                {productions.map((prod) => (
                  <option key={prod.id} value={prod.id}>
                    {prod.title} - ${prod.budget.toLocaleString()}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Jurisdiction
              </label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-pilotforge-blue focus:border-pilotforge-blue"
                value={selectedJurisdiction}
                onChange={(e) => setSelectedJurisdiction(e.target.value)}
              >
                <option value="">Select a jurisdiction</option>
                {jurisdictions.map((jur) => (
                  <option key={jur.id} value={jur.id}>
                    {jur.code} - {jur.name}
                  </option>
                ))}
              </select>
            </div>

            <Button 
              onClick={handleCalculate} 
              disabled={calculating || !selectedProduction || !selectedJurisdiction}
              className="w-full"
            >
              {calculating ? 'Calculating...' : 'Calculate Incentives'}
            </Button>
          </div>
        </Card>

        <Card title="Results" className={results ? '' : 'opacity-50'}>
          {calculating ? (
            <div className="flex justify-center py-12">
              <Spinner size="lg" />
            </div>
          ) : results ? (
            <div className="space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-700 font-medium mb-1">Estimated Incentive</p>
                <p className="text-3xl font-bold text-green-800">
                  ${results.incentiveAmount.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Production:</span>
                  <span className="font-semibold">{results.production}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Jurisdiction:</span>
                  <span className="font-semibold">{results.jurisdiction}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Total Expenses:</span>
                  <span className="font-semibold">${results.totalExpenses.toLocaleString()}</span>
                </div>
                <div className="flex justify-between py-2 border-b">
                  <span className="text-gray-600">Qualified Expenses:</span>
                  <span className="font-semibold">${results.qualifiedExpenses.toLocaleString()}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-gray-600">Effective Rate:</span>
                  <span className="font-semibold text-pilotforge-blue">{results.effectiveRate}%</span>
                </div>
              </div>

              <div className="pt-4">
                <Button variant="secondary" className="w-full">
                  Generate Report
                </Button>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <p>Select a production and jurisdiction to calculate incentives</p>
            </div>
          )}
        </Card>
      </div>

      <Card title="How It Works">
        <div className="prose prose-sm max-w-none">
          <p className="text-gray-600">
            The PilotForge calculator analyzes your production's expenses against jurisdiction-specific
            tax incentive rules to estimate your potential savings. Results include:
          </p>
          <ul className="list-disc list-inside text-gray-600 mt-2 space-y-1">
            <li>Qualified expenses based on jurisdiction criteria</li>
            <li>Estimated incentive amount</li>
            <li>Effective tax rate</li>
            <li>Detailed breakdown of calculations</li>
          </ul>
        </div>
      </Card>
    </div>
  );
};

export default Calculator;

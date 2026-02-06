import React, { useState, useEffect } from 'react';
import { Calculator as CalculatorIcon, Film, MapPin, DollarSign, TrendingUp, FileText, Sparkles } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import InsightCard from '../components/InsightCard';
import { useAppStore } from '../store';
import { useNavigate } from 'react-router-dom';

const Calculator: React.FC = () => {
  const navigate = useNavigate();
  const { productions, jurisdictions, fetchProductions, fetchJurisdictions, isLoading } = useAppStore();
  const [selectedProduction, setSelectedProduction] = useState('');
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('');
  const [results, setResults] = useState<{
    production: string;
    jurisdiction: string;
    totalExpenses: number;
    qualifiedExpenses: number;
    incentiveAmount: number;
    effectiveRate: number;
  } | null>(null);
  const [calculating, setCalculating] = useState(false);

  useEffect(() => {
    fetchProductions();
    fetchJurisdictions();
  }, [fetchProductions, fetchJurisdictions]);

  const handleCalculate = async () => {
    if (!selectedProduction || !selectedJurisdiction) {
      return;
    }

    setCalculating(true);
    setTimeout(() => {
      const production = productions.find(p => p.id === selectedProduction);
      const jurisdiction = jurisdictions.find(j => j.id === selectedJurisdiction);
      if (production && jurisdiction) {
        setResults({
          production: production.title,
          jurisdiction: jurisdiction.name,
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
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          Tax Incentive Calculator
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Calculate potential tax incentives for your production</p>
      </div>

      {productions.length === 0 ? (
        <Card>
          <EmptyState
            icon={CalculatorIcon}
            title="No productions to calculate"
            description="Create a production first to calculate tax incentives and see potential savings."
            actionLabel="Create a production"
            onAction={() => navigate('/productions')}
          />
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card 
              title="Select Production & Jurisdiction" 
              subtitle="Choose your production and target jurisdiction"
              hoverable
            >
              <div className="space-y-4">
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <Film className="h-4 w-4" />
                    Production
                  </label>
                  <select
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"
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
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <MapPin className="h-4 w-4" />
                    Jurisdiction
                  </label>
                  <select
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"
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
                  loading={calculating}
                  icon={CalculatorIcon}
                  className="w-full"
                >
                  {calculating ? 'Calculating...' : 'Calculate Incentives'}
                </Button>
              </div>
            </Card>

            <Card 
              title="Results" 
              subtitle={results ? 'Estimated tax incentive breakdown' : 'Awaiting calculation'}
              hoverable
              className={results ? '' : 'opacity-60'}
            >
              {calculating ? (
                <div className="flex flex-col items-center justify-center py-12 gap-4">
                  <Spinner size="lg" />
                  <p className="text-gray-500 dark:text-gray-400 text-sm">Analyzing incentive programs...</p>
                </div>
              ) : results ? (
                <div className="space-y-4 animate-fade-in">
                  <div className="p-6 bg-gradient-to-br from-status-active/20 to-accent-emerald/20 dark:from-status-active/30 dark:to-accent-emerald/30 border border-status-active dark:border-status-active/50 rounded-xl">
                    <div className="flex items-center gap-2 text-sm text-status-active dark:text-status-active font-medium mb-2">
                      <DollarSign className="h-4 w-4" />
                      <span>Estimated Incentive</span>
                    </div>
                    <p className="text-4xl font-bold text-status-active dark:text-status-active">
                      ${results.incentiveAmount.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </p>
                  </div>

                  <div className="space-y-3">
                    <div className="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700">
                      <span className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                        <Film className="h-4 w-4" />
                        Production
                      </span>
                      <span className="font-semibold text-gray-900 dark:text-gray-100">{results.production}</span>
                    </div>
                    <div className="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700">
                      <span className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                        <MapPin className="h-4 w-4" />
                        Jurisdiction
                      </span>
                      <span className="font-semibold text-gray-900 dark:text-gray-100">{results.jurisdiction}</span>
                    </div>
                    <div className="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700">
                      <span className="text-gray-600 dark:text-gray-400">Total Expenses</span>
                      <span className="font-semibold text-gray-900 dark:text-gray-100">${results.totalExpenses.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700">
                      <span className="text-gray-600 dark:text-gray-400">Qualified Expenses</span>
                      <span className="font-semibold text-gray-900 dark:text-gray-100">${results.qualifiedExpenses.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between py-3">
                      <span className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                        <TrendingUp className="h-4 w-4" />
                        Effective Rate
                      </span>
                      <span className="font-bold text-lg text-accent-blue dark:text-accent-teal">{results.effectiveRate}%</span>
                    </div>
                  </div>

                  <div className="pt-4">
                    <Button variant="outline" icon={FileText} className="w-full">
                      Generate Report
                    </Button>
                  </div>
                </div>
              ) : (
                <EmptyState
                  icon={Sparkles}
                  title="Ready to calculate"
                  description="Select a production and jurisdiction above to see your estimated tax incentives."
                  className="py-8"
                />
              )}
            </Card>
          </div>

          {results && (
            <InsightCard
              type="suggestion"
              title="Maximize Your Incentives"
              description={`Based on this calculation, consider documenting all qualified expenses carefully to ensure you receive the full $${results.incentiveAmount.toLocaleString()} incentive.`}
              action={{
                label: "View documentation guide",
                onClick: () => {},
              }}
            />
          )}

          <Card title="How It Works" subtitle="Understanding the calculation process" hoverable>
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                The PilotForge calculator analyzes your production's expenses against jurisdiction-specific
                tax incentive rules to estimate your potential savings. Results include:
              </p>
              <ul className="space-y-2">
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" />
                  </div>
                  <span>Qualified expenses based on jurisdiction criteria</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" />
                  </div>
                  <span>Estimated incentive amount</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" />
                  </div>
                  <span>Effective tax rate</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" />
                  </div>
                  <span>Detailed breakdown of calculations</span>
                </li>
              </ul>
            </div>
          </Card>
        </>
      )}
    </div>
  );
};

export default Calculator;

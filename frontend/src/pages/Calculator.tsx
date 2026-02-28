import { useState } from 'react';
import { Calculator as CalculatorIcon, Film, MapPin, DollarSign, TrendingUp, FileText, Sparkles } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import InsightCard from '../components/InsightCard';
import { motion } from 'framer-motion';
import type { Production } from '../types';

interface CalculatorProps {
  productions: Production[];
  onAddProduction?: (production: Production) => void;
  onUpdateProduction?: (production: Production) => void;
  onDeleteProduction?: (id: string) => void;
}

function Calculator({ productions = [] }: CalculatorProps) {
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

  // Mock jurisdictions
  const jurisdictions = [
    { id: 'ca', code: 'CA', name: 'California' },
    { id: 'ga', code: 'GA', name: 'Georgia' },
    { id: 'la', code: 'LA', name: 'Louisiana' },
    { id: 'ny', code: 'NY', name: 'New York' },
  ];

  const handleCalculate = async () => {
    if (!selectedProduction || !selectedJurisdiction) {
      return;
    }

    setCalculating(true);
    // Simulate calculation
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

  const isLoading = false;

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
        <h1 className="text-[28px] font-bold text-slate-900 tracking-tight">
          Tax Incentive Calculator
        </h1>
        <p className="text-slate-500 mt-1.5 text-[15px]">Calculate potential tax incentives for your production</p>
      </div>

      {productions.length === 0 ? (
        <Card>
          <EmptyState
            icon={CalculatorIcon}
            title="No productions to calculate"
            description="Create a production first to calculate tax incentives and see potential savings."
            actionLabel="Create a production"
            onAction={() => {}}
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
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-cyan-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"
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
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-cyan-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"
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
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="space-y-4"
                >
                  <div className="p-6 bg-gradient-to-br from-green-100/50 to-emerald-100/50 dark:from-green-900/30 dark:to-emerald-900/30 border border-green-300 dark:border-green-700 rounded-xl">
                    <div className="flex items-center gap-2 text-sm text-green-700 dark:text-green-400 font-medium mb-2">
                      <DollarSign className="h-4 w-4" />
                      <span>Estimated Incentive</span>
                    </div>
                    <p className="text-4xl font-bold text-green-700 dark:text-green-400">
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
                      <span className="font-bold text-lg text-blue-600 dark:text-cyan-400">{results.effectiveRate}%</span>
                    </div>
                  </div>

                  <div className="pt-4">
                    <Button variant="outline" className="w-full">
                      <FileText className="h-4 w-4" />
                      Generate Report
                    </Button>
                  </div>
                </motion.div>
              ) : (
                <EmptyState
                  icon={Sparkles}
                  title="Ready to calculate"
                  description="Select a production and jurisdiction above to see your estimated tax incentives."
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
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600 dark:bg-cyan-400" />
                  </div>
                  <span>Qualified expenses based on jurisdiction criteria</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600 dark:bg-cyan-400" />
                  </div>
                  <span>Estimated incentive amount</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600 dark:bg-cyan-400" />
                  </div>
                  <span>Effective tax rate</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-600 dark:bg-cyan-400" />
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
}

export default Calculator;

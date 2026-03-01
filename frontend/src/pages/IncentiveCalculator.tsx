import { useState } from 'react';
import { Calculator, TrendingUp } from 'lucide-react';

export default function IncentiveCalculator() {
  const [budget, setBudget] = useState(10000000);
  const [jurisdiction, setJurisdiction] = useState('california');
  const [qualifyingExpenses, setQualifyingExpenses] = useState(8000000);

  const jurisdictions = {
    california: { rate: 0.25, label: 'California' },
    georgia: { rate: 0.20, label: 'Georgia' },
    louisiana: { rate: 0.30, label: 'Louisiana' },
    texas: { rate: 0.15, label: 'Texas' },
    newyork: { rate: 0.10, label: 'New York' },
  };

  const currentJurisdiction = jurisdictions[jurisdiction as keyof typeof jurisdictions];
  const taxCredit = qualifyingExpenses * currentJurisdiction.rate;
  const creditPercentage = (taxCredit / budget) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-8 py-6">
        <div className="flex items-center gap-3 mb-2">
          <Calculator className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-slate-900">Incentive Calculator</h1>
        </div>
        <p className="text-slate-600">Estimate tax credits and incentives for your production.</p>
      </div>

      {/* Content */}
      <div className="p-8 max-w-4xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-lg border border-slate-200 p-6">
            <h2 className="text-xl font-bold text-slate-900 mb-6">Production Details</h2>

            {/* Budget Input */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-900 mb-2">
                Total Budget
              </label>
              <div className="relative">
                <span className="absolute left-3 top-2.5 text-slate-600 font-semibold">$</span>
                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  className="w-full pl-8 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <input
                type="range"
                min="1000000"
                max="100000000"
                step="1000000"
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full mt-2"
              />
            </div>

            {/* Jurisdiction Select */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-900 mb-2">
                Jurisdiction
              </label>
              <select
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {Object.entries(jurisdictions).map(([key, { label }]) => (
                  <option key={key} value={key}>{label}</option>
                ))}
              </select>
            </div>

            {/* Qualifying Expenses */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-900 mb-2">
                Qualifying Expenses
              </label>
              <div className="relative">
                <span className="absolute left-3 top-2.5 text-slate-600 font-semibold">$</span>
                <input
                  type="number"
                  value={qualifyingExpenses}
                  onChange={(e) => setQualifyingExpenses(Number(e.target.value))}
                  className="w-full pl-8 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <p className="text-xs text-slate-600 mt-1">
                {((qualifyingExpenses / budget) * 100).toFixed(1)}% of total budget
              </p>
            </div>

            {/* Credit Rate Info */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-slate-700">
                <span className="font-medium">{currentJurisdiction.label}</span> offers{' '}
                <span className="font-bold text-blue-600">{(currentJurisdiction.rate * 100).toFixed(0)}%</span> tax credit on qualifying expenses
              </p>
            </div>
          </div>

          {/* Results */}
          <div className="space-y-4">
            {/* Main Result Card */}
            <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg text-white p-8">
              <p className="text-blue-100 text-sm font-medium mb-2">Estimated Tax Credit</p>
              <h3 className="text-4xl font-bold mb-1">${(taxCredit / 1000000).toFixed(2)}M</h3>
              <p className="text-blue-100">{creditPercentage.toFixed(1)}% of budget</p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 gap-4">
              <div className="bg-white rounded-lg border border-slate-200 p-4">
                <p className="text-slate-600 text-xs font-medium">Qualifying Expenses</p>
                <p className="text-2xl font-bold text-slate-900">
                  ${(qualifyingExpenses / 1000000).toFixed(1)}M
                </p>
              </div>

              <div className="bg-white rounded-lg border border-slate-200 p-4">
                <p className="text-slate-600 text-xs font-medium">Credit Rate</p>
                <p className="text-2xl font-bold text-slate-900">
                  {(currentJurisdiction.rate * 100).toFixed(0)}%
                </p>
              </div>

              <div className="bg-white rounded-lg border border-slate-200 p-4">
                <p className="text-slate-600 text-xs font-medium">Estimated ROI</p>
                <div className="flex items-center gap-2 mt-2">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                  <p className="text-2xl font-bold text-green-600">
                    +{creditPercentage.toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                Save Calculation
              </button>
              <button className="flex-1 bg-slate-200 text-slate-900 px-4 py-2 rounded-lg hover:bg-slate-300 transition-colors font-medium">
                Export Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

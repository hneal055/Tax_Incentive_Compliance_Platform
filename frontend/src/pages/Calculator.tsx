import React, { useState, useEffect } from 'react';
import { Calculator as CalculatorIcon, Film, MapPin, DollarSign, TrendingUp, Sparkles, Download, ExternalLink, RefreshCw, AlertTriangle, CheckCircle2, Info } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import InsightCard from '../components/InsightCard';
import { useAppStore } from '../store';
import { useNavigate } from 'react-router-dom';
import { openReportWindow, downloadReport } from '../utils/generateReport';
import type { ReportData } from '../utils/generateReport';
import type { IncentiveRuleDetailed, SimpleCalculationResult } from '../types';
import api from '../api';

const getBudget = (prod: { budgetTotal?: number; budget?: number }): number =>
  prod.budgetTotal ?? prod.budget ?? 0;

const Calculator: React.FC = () => {
  const navigate = useNavigate();
  const { productions, jurisdictions, fetchProductions, fetchJurisdictions, isLoading } = useAppStore();
  const [selectedProduction, setSelectedProduction] = useState('');
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('');
  const [selectedRule, setSelectedRule] = useState('');
  const [availableRules, setAvailableRules] = useState<IncentiveRuleDetailed[]>([]);
  const [loadingRules, setLoadingRules] = useState(false);
  const [results, setResults] = useState<ReportData | null>(null);
  const [calcDetails, setCalcDetails] = useState<SimpleCalculationResult | null>(null);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showReportMenu, setShowReportMenu] = useState(false);

  useEffect(() => {
    fetchProductions();
    fetchJurisdictions();
  }, [fetchProductions, fetchJurisdictions]);

  // Load rules when jurisdiction changes
  useEffect(() => {
    if (!selectedJurisdiction) {
      setAvailableRules([]);
      setSelectedRule('');
      return;
    }
    setLoadingRules(true);
    setError(null);
    api.incentiveRules.getByJurisdiction(selectedJurisdiction)
      .then((rules) => {
        setAvailableRules(rules);
        if (rules.length === 1) {
          setSelectedRule(rules[0].id);
        } else {
          setSelectedRule('');
        }
      })
      .catch(() => {
        setAvailableRules([]);
        setError('Failed to load incentive rules for this jurisdiction');
      })
      .finally(() => setLoadingRules(false));
  }, [selectedJurisdiction]);

  // Close report menu on outside click
  useEffect(() => {
    if (!showReportMenu) return;
    const handler = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('[data-report-menu]')) setShowReportMenu(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [showReportMenu]);

  const handleCalculate = async () => {
    if (!selectedProduction || !selectedJurisdiction) return;

    const production = productions.find(p => p.id === selectedProduction);
    const jurisdiction = jurisdictions.find(j => j.id === selectedJurisdiction);
    if (!production || !jurisdiction) return;

    const budget = getBudget(production);

    // If no rules available, show error
    if (availableRules.length === 0) {
      setError('No incentive rules found for this jurisdiction. Please select a different jurisdiction.');
      return;
    }

    const ruleId = selectedRule || availableRules[0]?.id;
    if (!ruleId) {
      setError('Please select an incentive rule.');
      return;
    }

    setCalculating(true);
    setError(null);
    setShowReportMenu(false);

    try {
      const result = await api.calculator.simple({
        productionBudget: budget,
        jurisdictionId: selectedJurisdiction,
        ruleId: ruleId,
      });

      const rule = availableRules.find(r => r.id === ruleId);

      setCalcDetails(result);
      setResults({
        production: production.title,
        jurisdiction: jurisdiction.name,
        totalExpenses: result.totalBudget,
        qualifiedExpenses: result.qualifyingBudget,
        incentiveAmount: result.estimatedCredit,
        effectiveRate: result.percentage
          ? parseFloat(((result.qualifyingBudget / result.totalBudget) * result.percentage).toFixed(2))
          : 0,
        ruleName: result.ruleName,
        incentiveRate: result.percentage ?? undefined,
      });

      // Save to localStorage for Reports page
      const saved = JSON.parse(localStorage.getItem('pilotforge_calculations') || '[]');
      saved.unshift({
        production: production.title,
        jurisdiction: jurisdiction.name,
        ruleName: result.ruleName,
        incentiveAmount: result.estimatedCredit,
        effectiveRate: result.percentage,
        date: new Date().toISOString(),
      });
      localStorage.setItem('pilotforge_calculations', JSON.stringify(saved.slice(0, 20)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Calculation failed. Please check the backend is running.');
      setCalcDetails(null);
    } finally {
      setCalculating(false);
    }
  };

  const handleGenerateReport = (mode: 'preview' | 'download') => {
    if (!results) return;
    setShowReportMenu(false);
    if (mode === 'preview') {
      openReportWindow(results);
    } else {
      downloadReport(results);
    }
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
                  <label htmlFor="production-select" className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <Film className="h-4 w-4" />
                    Production
                  </label>
                  <select
                    id="production-select"
                    title="Select Production"
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"
                    value={selectedProduction}
                    onChange={(e) => setSelectedProduction(e.target.value)}
                  >
                    <option value="">Select a production</option>
                    {productions.map((prod) => (
                      <option key={prod.id} value={prod.id}>
                        {prod.title} - ${getBudget(prod).toLocaleString()}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="jurisdiction-select" className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <MapPin className="h-4 w-4" />
                    Jurisdiction
                  </label>
                  <select
                    id="jurisdiction-select"
                    title="Select Jurisdiction"
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

                {/* Rule selector - shown when jurisdiction has multiple rules */}
                {selectedJurisdiction && (
                  <div>
                    <label htmlFor="rule-select" className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      <TrendingUp className="h-4 w-4" />
                      Incentive Program
                      {loadingRules && <Spinner size="sm" />}
                    </label>
                    {availableRules.length === 0 && !loadingRules ? (
                      <p className="text-sm text-amber-600 dark:text-amber-400 flex items-center gap-2">
                        <AlertTriangle className="h-4 w-4" />
                        No incentive programs found for this jurisdiction
                      </p>
                    ) : availableRules.length === 1 ? (
                      <div className="px-4 py-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                        <p className="text-sm font-semibold text-green-800 dark:text-green-300">
                          {availableRules[0].ruleName}
                        </p>
                        <p className="text-xs text-green-600 dark:text-green-400">
                          {availableRules[0].incentiveType} - {availableRules[0].percentage}%
                          {availableRules[0].minSpend && ` (Min: $${(availableRules[0].minSpend / 1000).toFixed(0)}K)`}
                        </p>
                      </div>
                    ) : (
                      <select
                        id="rule-select"
                        title="Select Incentive Program"
                        className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors"
                        value={selectedRule}
                        onChange={(e) => setSelectedRule(e.target.value)}
                      >
                        <option value="">Select an incentive program</option>
                        {availableRules.map((rule) => (
                          <option key={rule.id} value={rule.id}>
                            {rule.ruleName} - {rule.percentage}% ({rule.incentiveType})
                          </option>
                        ))}
                      </select>
                    )}
                  </div>
                )}

                {error && (
                  <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <p className="text-sm text-red-700 dark:text-red-300 flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4 flex-shrink-0" />
                      {error}
                    </p>
                  </div>
                )}

                <Button
                  onClick={handleCalculate}
                  disabled={calculating || !selectedProduction || !selectedJurisdiction || (availableRules.length > 1 && !selectedRule) || availableRules.length === 0}
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
                    {calcDetails?.ruleName && (
                      <p className="text-xs text-status-active/70 mt-1">
                        via {calcDetails.ruleName}
                      </p>
                    )}
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
                    <div className="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700">
                      <span className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                        <TrendingUp className="h-4 w-4" />
                        Effective Rate
                      </span>
                      <span className="font-bold text-lg text-accent-blue dark:text-accent-teal">{results.effectiveRate}%</span>
                    </div>
                  </div>

                  {/* Compliance indicators */}
                  {calcDetails && (
                    <div className="flex gap-3">
                      <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold ${calcDetails.meetsMinimumSpend ? 'bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-50 text-red-700 dark:bg-red-900/30 dark:text-red-400'}`}>
                        {calcDetails.meetsMinimumSpend ? <CheckCircle2 className="h-3.5 w-3.5" /> : <AlertTriangle className="h-3.5 w-3.5" />}
                        Min Spend {calcDetails.meetsMinimumSpend ? 'Met' : 'Not Met'}
                      </div>
                      <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold ${calcDetails.underMaximumCap ? 'bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'}`}>
                        {calcDetails.underMaximumCap ? <CheckCircle2 className="h-3.5 w-3.5" /> : <Info className="h-3.5 w-3.5" />}
                        {calcDetails.underMaximumCap ? 'Under Cap' : 'At Cap Limit'}
                      </div>
                    </div>
                  )}

                  {/* Notes from backend */}
                  {calcDetails?.notes && calcDetails.notes.length > 0 && (
                    <div className="space-y-2">
                      {calcDetails.notes.map((note, i) => (
                        <div key={i} className="flex items-start gap-2 px-3 py-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                          <Info className="h-4 w-4 text-accent-blue dark:text-accent-teal mt-0.5 flex-shrink-0" />
                          <p className="text-xs text-blue-700 dark:text-blue-300">{note}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Report actions */}
                  <div className="pt-4 relative" data-report-menu>
                    <div className="flex gap-3">
                      <Button
                        variant="outline"
                        icon={ExternalLink}
                        className="flex-1"
                        onClick={() => handleGenerateReport('preview')}
                      >
                        Preview Report
                      </Button>
                      <Button
                        variant="primary"
                        icon={Download}
                        className="flex-1"
                        onClick={() => handleGenerateReport('download')}
                      >
                        Download Report
                      </Button>
                    </div>
                  </div>

                  {/* Recalculate */}
                  <Button
                    variant="ghost"
                    icon={RefreshCw}
                    className="w-full"
                    onClick={handleCalculate}
                  >
                    Recalculate
                  </Button>
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
                The PilotForge calculator analyzes your production expenses against jurisdiction-specific
                tax incentive rules to estimate your potential savings. Results include:
              </p>
              <ul className="space-y-2">
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1"><div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" /></div>
                  <span>Qualified expenses based on jurisdiction criteria</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1"><div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" /></div>
                  <span>Estimated incentive amount using real jurisdiction rates</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1"><div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" /></div>
                  <span>Compliance checks for minimum spend and maximum cap</span>
                </li>
                <li className="flex items-start gap-2 text-gray-600 dark:text-gray-400">
                  <div className="flex-shrink-0 mt-1"><div className="h-1.5 w-1.5 rounded-full bg-accent-blue dark:bg-accent-teal" /></div>
                  <span>Detailed breakdown with program-specific notes</span>
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

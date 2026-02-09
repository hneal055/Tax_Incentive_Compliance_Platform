import React, { useState, useEffect, useMemo } from 'react';
import {
  BarChart3,
  FileText,
  Scale,
  TrendingUp,
  Download,
  Loader2,
  AlertCircle,
  Trash2,
  RefreshCw,
  MapPin,
  Percent,
  BookOpen,
  Plus,
  Minus,
} from 'lucide-react';
import Card from '../components/Card';
import Spinner from '../components/Spinner';
import MetricCard from '../components/MetricCard';
import { useAppStore } from '../store';
import api from '../api';
import { downloadBlob } from '../utils/downloadPdf';

// ─── Saved Calculation from localStorage (set by Calculator page) ──────
interface SavedCalculation {
  id: string;
  production: string;
  jurisdiction: string;
  jurisdictionId: string;
  ruleId: string;
  ruleName: string;
  budget: number;
  credit: number;
  rate: number;
  date: string;
}

function loadSavedCalculations(): SavedCalculation[] {
  try {
    const raw = localStorage.getItem('pilotforge_calculations');
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function clearSavedCalculations() {
  localStorage.removeItem('pilotforge_calculations');
}

const fmtCurrency = (n: number) =>
  `$${n.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

// ─── Report Generator Card ─────────────────────────────────────────────
interface GeneratorCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  loading: boolean;
  error: string | null;
  onGenerate: () => void;
  disabled?: boolean;
}

function GeneratorCard({ title, description, icon, children, loading, error, onGenerate, disabled }: GeneratorCardProps) {
  return (
    <Card className="h-full">
      <div className="space-y-4">
        <div className="flex items-start gap-3">
          <div className="p-2.5 bg-gradient-to-br from-accent-blue/10 to-accent-teal/10 dark:from-accent-blue/20 dark:to-accent-teal/20 rounded-lg flex-shrink-0">
            {icon}
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{description}</p>
          </div>
        </div>

        <div className="space-y-3">
          {children}
        </div>

        {error && (
          <div className="flex items-center gap-2 text-xs text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-lg px-3 py-2">
            <AlertCircle className="h-3.5 w-3.5 flex-shrink-0" />
            {error}
          </div>
        )}

        <button
          type="button"
          onClick={onGenerate}
          disabled={loading || disabled}
          className="w-full flex items-center justify-center gap-2 rounded-lg bg-accent-blue hover:bg-accent-blue/90 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white font-semibold text-sm px-4 py-2.5 transition-colors"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Download className="h-4 w-4" />
              Generate PDF
            </>
          )}
        </button>
      </div>
    </Card>
  );
}

// ─── Input helpers ──────────────────────────────────────────────────────
function InputField({ label, value, onChange, type = 'text', placeholder }: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
  placeholder?: string;
}) {
  return (
    <div>
      <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm px-3 py-2 focus:ring-2 focus:ring-accent-blue/40 focus:border-accent-blue outline-none transition-colors"
      />
    </div>
  );
}

// ─── Main Reports Page ──────────────────────────────────────────────────
const Reports: React.FC = () => {
  const { jurisdictions, rulesByJurisdiction, detailedRules, isLoading, fetchJurisdictions, fetchDetailedRules } = useAppStore();

  useEffect(() => {
    if (jurisdictions.length === 0) fetchJurisdictions();
    if (detailedRules.length === 0) fetchDetailedRules();
  }, [jurisdictions.length, detailedRules.length, fetchJurisdictions, fetchDetailedRules]);

  // ─── Comparison Report State ──────────────────────────────────────
  const [compTitle, setCompTitle] = useState('');
  const [compBudget, setCompBudget] = useState('');
  const [compJurisdictions, setCompJurisdictions] = useState<string[]>([]);
  const [compLoading, setCompLoading] = useState(false);
  const [compError, setCompError] = useState<string | null>(null);

  const toggleJurisdiction = (id: string) => {
    setCompJurisdictions((prev) =>
      prev.includes(id) ? prev.filter((j) => j !== id) : [...prev, id]
    );
  };

  const handleComparisonReport = async () => {
    if (!compTitle.trim() || !compBudget || compJurisdictions.length < 2) {
      setCompError('Please provide a title, budget, and at least 2 jurisdictions.');
      return;
    }
    setCompLoading(true);
    setCompError(null);
    try {
      const blob = await api.reports.comparison({
        productionTitle: compTitle,
        budget: parseFloat(compBudget),
        jurisdictionIds: compJurisdictions,
      });
      downloadBlob(blob, `PilotForge_Comparison_${compTitle.replace(/\s+/g, '_')}.pdf`);
    } catch {
      setCompError('Failed to generate comparison report. Ensure the backend is running.');
    } finally {
      setCompLoading(false);
    }
  };

  // ─── Compliance Report State ──────────────────────────────────────
  const [complTitle, setComplTitle] = useState('');
  const [complBudget, setComplBudget] = useState('');
  const [complRuleId, setComplRuleId] = useState('');
  const [complLoading, setComplLoading] = useState(false);
  const [complError, setComplError] = useState<string | null>(null);

  const handleComplianceReport = async () => {
    if (!complTitle.trim() || !complBudget || !complRuleId) {
      setComplError('Please provide a title, budget, and select a rule.');
      return;
    }
    setComplLoading(true);
    setComplError(null);
    try {
      const blob = await api.reports.compliance({
        productionTitle: complTitle,
        ruleId: complRuleId,
        productionBudget: parseFloat(complBudget),
      });
      downloadBlob(blob, `PilotForge_Compliance_${complTitle.replace(/\s+/g, '_')}.pdf`);
    } catch {
      setComplError('Failed to generate compliance report. Ensure the backend is running.');
    } finally {
      setComplLoading(false);
    }
  };

  // ─── Scenario Report State ───────────────────────────────────────
  const [scenTitle, setScenTitle] = useState('');
  const [scenJurisdiction, setScenJurisdiction] = useState('');
  const [scenBaseBudget, setScenBaseBudget] = useState('');
  const [scenVariations, setScenVariations] = useState<string[]>(['']);
  const [scenLoading, setScenLoading] = useState(false);
  const [scenError, setScenError] = useState<string | null>(null);

  const addVariation = () => setScenVariations((v) => [...v, '']);
  const removeVariation = (i: number) =>
    setScenVariations((v) => v.filter((_, idx) => idx !== i));
  const updateVariation = (i: number, val: string) =>
    setScenVariations((v) => v.map((item, idx) => (idx === i ? val : item)));

  const handleScenarioReport = async () => {
    const budget = parseFloat(scenBaseBudget);
    if (!scenTitle.trim() || !scenJurisdiction || !budget) {
      setScenError('Please provide a title, jurisdiction, and base budget.');
      return;
    }
    setScenLoading(true);
    setScenError(null);
    try {
      const scenarios = scenVariations
        .filter((v) => v.trim())
        .map((v) => ({ budget_variation: parseFloat(v) || 0 }));
      const blob = await api.reports.scenario({
        productionTitle: scenTitle,
        jurisdictionId: scenJurisdiction,
        baseProductionBudget: budget,
        scenarios: scenarios.length > 0 ? scenarios : [{ budget_variation: 0 }],
      });
      downloadBlob(blob, `PilotForge_Scenario_${scenTitle.replace(/\s+/g, '_')}.pdf`);
    } catch {
      setScenError('Failed to generate scenario report. Ensure the backend is running.');
    } finally {
      setScenLoading(false);
    }
  };

  // ─── Quick Stats ─────────────────────────────────────────────────
  const stats = useMemo(() => {
    const allRates = detailedRules.map((r) => r.percentage || 0).filter(Boolean);
    const avgRate = allRates.length > 0 ? allRates.reduce((a, b) => a + b, 0) / allRates.length : 0;
    const bestRate = allRates.length > 0 ? Math.max(...allRates) : 0;
    return {
      activeJurisdictions: jurisdictions.filter((j) => j.active !== false).length,
      avgRate: Math.round(avgRate * 10) / 10,
      bestRate,
      totalRules: detailedRules.length,
    };
  }, [jurisdictions, detailedRules]);

  // ─── Recent Calculations ─────────────────────────────────────────
  const [savedCalcs, setSavedCalcs] = useState<SavedCalculation[]>(loadSavedCalculations);

  const handleClearHistory = () => {
    clearSavedCalculations();
    setSavedCalcs([]);
  };

  if (isLoading && jurisdictions.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          Reports
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Generate PDF reports and review calculation history
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard title="Active Jurisdictions" value={stats.activeJurisdictions} icon={MapPin} />
        <MetricCard title="Average Incentive Rate" value={`${stats.avgRate}%`} icon={Percent} />
        <MetricCard title="Best Available Rate" value={`${stats.bestRate}%`} icon={TrendingUp} />
        <MetricCard title="Total Rules Tracked" value={stats.totalRules} icon={BookOpen} />
      </div>

      {/* Report Generators */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Report Generator
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Jurisdiction Comparison */}
          <GeneratorCard
            title="Jurisdiction Comparison"
            description="Compare incentive programs across multiple jurisdictions"
            icon={<Scale className="h-5 w-5 text-accent-blue dark:text-accent-teal" />}
            loading={compLoading}
            error={compError}
            onGenerate={handleComparisonReport}
            disabled={compJurisdictions.length < 2 || !compTitle.trim() || !compBudget}
          >
            <InputField label="Production Title" value={compTitle} onChange={setCompTitle} placeholder="e.g. My Film Production" />
            <InputField label="Budget ($)" value={compBudget} onChange={setCompBudget} type="number" placeholder="e.g. 1000000" />
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Jurisdictions (select 2+)
              </label>
              <div className="flex flex-wrap gap-1.5">
                {jurisdictions.map((j) => (
                  <button
                    key={j.id}
                    type="button"
                    onClick={() => toggleJurisdiction(j.id)}
                    className={`px-2.5 py-1 text-xs font-medium rounded-full border transition-colors ${
                      compJurisdictions.includes(j.id)
                        ? 'bg-accent-blue text-white border-accent-blue'
                        : 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:border-accent-blue'
                    }`}
                  >
                    {j.code}
                  </button>
                ))}
              </div>
            </div>
          </GeneratorCard>

          {/* Compliance Report */}
          <GeneratorCard
            title="Compliance Report"
            description="Detailed compliance check against a specific incentive rule"
            icon={<FileText className="h-5 w-5 text-accent-blue dark:text-accent-teal" />}
            loading={complLoading}
            error={complError}
            onGenerate={handleComplianceReport}
            disabled={!complRuleId || !complTitle.trim() || !complBudget}
          >
            <InputField label="Production Title" value={complTitle} onChange={setComplTitle} placeholder="e.g. My Film Production" />
            <InputField label="Budget ($)" value={complBudget} onChange={setComplBudget} type="number" placeholder="e.g. 1000000" />
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Incentive Rule
              </label>
              <select
                value={complRuleId}
                onChange={(e) => setComplRuleId(e.target.value)}
                aria-label="Incentive Rule"
                className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm px-3 py-2 focus:ring-2 focus:ring-accent-blue/40 outline-none"
              >
                <option value="">Select a rule...</option>
                {detailedRules.map((rule) => {
                  const jName = jurisdictions.find((j) => j.id === rule.jurisdictionId)?.code || '';
                  return (
                    <option key={rule.id} value={rule.id}>
                      {jName} - {rule.ruleName} ({rule.percentage || 0}%)
                    </option>
                  );
                })}
              </select>
            </div>
          </GeneratorCard>

          {/* Scenario Analysis */}
          <GeneratorCard
            title="Scenario Analysis"
            description="Model budget variations to find optimal incentive outcomes"
            icon={<TrendingUp className="h-5 w-5 text-accent-blue dark:text-accent-teal" />}
            loading={scenLoading}
            error={scenError}
            onGenerate={handleScenarioReport}
            disabled={!scenJurisdiction || !scenTitle.trim() || !scenBaseBudget}
          >
            <InputField label="Production Title" value={scenTitle} onChange={setScenTitle} placeholder="e.g. My Film Production" />
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Jurisdiction
              </label>
              <select
                value={scenJurisdiction}
                onChange={(e) => setScenJurisdiction(e.target.value)}
                aria-label="Jurisdiction"
                className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm px-3 py-2 focus:ring-2 focus:ring-accent-blue/40 outline-none"
              >
                <option value="">Select jurisdiction...</option>
                {jurisdictions.map((j) => (
                  <option key={j.id} value={j.id}>{j.name} ({j.code})</option>
                ))}
              </select>
            </div>
            <InputField label="Base Budget ($)" value={scenBaseBudget} onChange={setScenBaseBudget} type="number" placeholder="e.g. 1000000" />
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Budget Variations ($)
              </label>
              <div className="space-y-2">
                {scenVariations.map((v, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input
                      type="number"
                      value={v}
                      onChange={(e) => updateVariation(i, e.target.value)}
                      placeholder={`Variation ${i + 1}`}
                      className="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm px-3 py-1.5 focus:ring-2 focus:ring-accent-blue/40 outline-none"
                    />
                    {scenVariations.length > 1 && (
                      <button type="button" onClick={() => removeVariation(i)} className="text-gray-400 hover:text-red-500" aria-label={`Remove variation ${i + 1}`}>
                        <Minus className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  onClick={addVariation}
                  className="flex items-center gap-1 text-xs text-accent-blue hover:text-accent-blue/80 font-medium"
                >
                  <Plus className="h-3.5 w-3.5" /> Add Variation
                </button>
              </div>
            </div>
          </GeneratorCard>
        </div>
      </div>

      {/* Recent Calculations */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Recent Calculations
          </h2>
          {savedCalcs.length > 0 && (
            <button
              type="button"
              onClick={handleClearHistory}
              className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-red-500 transition-colors"
            >
              <Trash2 className="h-3.5 w-3.5" /> Clear History
            </button>
          )}
        </div>
        <Card>
          {savedCalcs.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-10 text-gray-500">
              <BarChart3 className="h-10 w-10 mb-3 opacity-20" />
              <p className="text-sm">No calculations yet. Use the Calculator to get started.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-3 px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Production</th>
                    <th className="text-left py-3 px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Jurisdiction</th>
                    <th className="text-left py-3 px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Rule</th>
                    <th className="text-right py-3 px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Budget</th>
                    <th className="text-right py-3 px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Credit</th>
                    <th className="text-right py-3 px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Rate</th>
                    <th className="text-right py-3 px-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {savedCalcs.slice(0, 10).map((calc) => (
                    <tr key={calc.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                      <td className="py-3 px-4 font-medium text-gray-900 dark:text-gray-100">{calc.production}</td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">{calc.jurisdiction}</td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">{calc.ruleName}</td>
                      <td className="py-3 px-4 text-right font-mono text-gray-700 dark:text-gray-300">{fmtCurrency(calc.budget)}</td>
                      <td className="py-3 px-4 text-right font-mono font-semibold text-green-600 dark:text-green-400">{fmtCurrency(calc.credit)}</td>
                      <td className="py-3 px-4 text-right text-gray-600 dark:text-gray-400">{calc.rate}%</td>
                      <td className="py-3 px-4 text-right text-gray-500 dark:text-gray-400 text-xs">{new Date(calc.date).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default Reports;

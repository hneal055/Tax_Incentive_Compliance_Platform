import { useState } from 'react';
import {
  Calculator as CalcIcon,
  TrendingUp,
  DollarSign,
  Film,
  Download,
  RotateCcw,
  CheckCircle,
} from 'lucide-react';
import type { Production } from '../types';

interface CalculatorProps {
  productions: Production[];
  onAddProduction?: (production: Production) => void;
  onUpdateProduction?: (production: Production) => void;
  onDeleteProduction?: (id: string) => void;
}

// ─── Static data ────────────────────────────────────────────────────────────

const MOCK_PRODUCTIONS: Production[] = [
  { id: 'mock-1', title: 'The Silent Horizon',  budget: 15000000, jurisdiction_id: 'ga', created_at: '2025-01-15T00:00:00Z', updated_at: '2025-01-15T00:00:00Z' },
  { id: 'mock-2', title: 'Echoes of Midnight',  budget: 8000000,  jurisdiction_id: 'ny', created_at: '2025-02-01T00:00:00Z', updated_at: '2025-02-01T00:00:00Z' },
  { id: 'mock-3', title: 'Neon Pulse',           budget: 4000000,  jurisdiction_id: 'la', created_at: '2025-03-01T00:00:00Z', updated_at: '2025-03-01T00:00:00Z' },
];

const JURISDICTIONS = [
  { id: 'ga', regionCode: 'us', name: 'Georgia',          creditRate: 0.20, qualifiedRatio: 0.85 },
  { id: 'ca', regionCode: 'us', name: 'California',       creditRate: 0.25, qualifiedRatio: 0.80 },
  { id: 'la', regionCode: 'us', name: 'Louisiana',        creditRate: 0.25, qualifiedRatio: 0.85 },
  { id: 'ny', regionCode: 'us', name: 'New York',         creditRate: 0.30, qualifiedRatio: 0.80 },
  { id: 'bc', regionCode: 'ca', name: 'British Columbia', creditRate: 0.28, qualifiedRatio: 0.85 },
  { id: 'on', regionCode: 'ca', name: 'Ontario',          creditRate: 0.35, qualifiedRatio: 0.75 },
  { id: 'gb', regionCode: 'gb', name: 'United Kingdom',   creditRate: 0.25, qualifiedRatio: 0.80 },
  { id: 'au', regionCode: 'au', name: 'Australia',        creditRate: 0.20, qualifiedRatio: 0.90 },
];

// ─── Types ───────────────────────────────────────────────────────────────────

interface CalcResult {
  productionTitle: string;
  jurisdictionName: string;
  totalBudget: number;
  qualifiedExpenses: number;
  creditRate: number;
  estimatedCredit: number;
  effectiveRate: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function fmt(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}k`;
  return `$${n.toLocaleString()}`;
}

// ─── Main component ──────────────────────────────────────────────────────────

export default function Calculator({ productions = [] }: CalculatorProps) {
  const displayProductions = productions.length > 0 ? productions : MOCK_PRODUCTIONS;

  const [prodId,   setProdId]   = useState(displayProductions[0]?.id ?? '');
  const [jurId,    setJurId]    = useState(JURISDICTIONS[0].id);
  const [loading,  setLoading]  = useState(false);
  const [result,   setResult]   = useState<CalcResult | null>(null);
  const [reported, setReported] = useState(false);

  function handleCalculate() {
    const prod = displayProductions.find(p => p.id === prodId);
    const jur  = JURISDICTIONS.find(j => j.id === jurId);
    if (!prod || !jur) return;

    setLoading(true);
    setResult(null);
    setReported(false);

    setTimeout(() => {
      const qualified = prod.budget * jur.qualifiedRatio;
      const credit    = qualified * jur.creditRate;
      setResult({
        productionTitle:  prod.title,
        jurisdictionName: jur.name,
        totalBudget:      prod.budget,
        qualifiedExpenses: qualified,
        creditRate:       jur.creditRate * 100,
        estimatedCredit:  credit,
        effectiveRate:    (credit / prod.budget) * 100,
      });
      setLoading(false);
    }, 1200);
  }

  function handleReset() {
    setResult(null);
    setReported(false);
  }

  function handleDownload() {
    setReported(true);
    setTimeout(() => setReported(false), 3000);
  }

  const canCalculate = !!prodId && !!jurId;

  return (
    <div className="flex gap-6 h-full min-h-0">

      {/* ── Left: Quick Estimate form ───────────────────────────── */}
      <div className="w-80 shrink-0">
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
          {/* Card header */}
          <div className="flex items-center gap-2.5 mb-6">
            <CalcIcon className="w-5 h-5 text-slate-600" strokeWidth={1.8} />
            <h2 className="text-base font-bold text-slate-900">Quick Estimate</h2>
          </div>

          <div className="space-y-5">
            {/* Production select */}
            <div>
              <label className="block text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-2">
                Production
              </label>
              <select
                value={prodId}
                onChange={e => { setProdId(e.target.value); setResult(null); }}
                title="Production"
                aria-label="Production"
                className="select-arrow w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none"
              >
                {displayProductions.map(p => (
                  <option key={p.id} value={p.id}>{p.title}</option>
                ))}
              </select>
            </div>

            {/* Jurisdiction select */}
            <div>
              <label className="block text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-2">
                Jurisdiction
              </label>
              <select
                value={jurId}
                onChange={e => { setJurId(e.target.value); setResult(null); }}
                title="Jurisdiction"
                aria-label="Jurisdiction"
                className="select-arrow w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none"
              >
                {JURISDICTIONS.map(j => (
                  <option key={j.id} value={j.id}>{j.regionCode} {j.name}</option>
                ))}
              </select>
            </div>

            {/* Run Calculation button */}
            <button
              type="button"
              onClick={handleCalculate}
              disabled={!canCalculate || loading}
              className="w-full py-2.5 bg-blue-600 text-white text-sm font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Calculating…' : 'Run Calculation'}
            </button>
          </div>

          {/* How it works — compact */}
          <div className="mt-6 pt-5 border-t border-slate-100">
            <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-3">How It Works</p>
            <ul className="space-y-2">
              {[
                'Budget × qualified ratio = qualified expenses',
                'Qualified expenses × credit rate = incentive',
                'Effective rate = credit ÷ total budget',
              ].map(line => (
                <li key={line} className="flex items-start gap-2 text-xs text-slate-500">
                  <span className="mt-1.5 w-1 h-1 rounded-full bg-blue-400 shrink-0" />
                  {line}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* ── Right: Results panel ────────────────────────────────── */}
      <div className="flex-1 min-w-0">

        {/* Loading state */}
        {loading && (
          <div className="h-full flex flex-col items-center justify-center gap-4 border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/60">
            <div className="w-12 h-12 border-[3px] border-blue-200 border-t-blue-600 rounded-full animate-spin" />
            <p className="text-slate-500 text-sm font-medium">Analyzing incentive programs…</p>
          </div>
        )}

        {/* Empty state */}
        {!loading && !result && (
          <div className="h-full flex flex-col items-center justify-center gap-3 border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/60 min-h-[400px]">
            <CalcIcon className="w-12 h-12 text-slate-300" strokeWidth={1.2} />
            <p className="text-slate-400 text-sm">Select project details to run estimate.</p>
          </div>
        )}

        {/* Results */}
        {!loading && result && (
          <div className="space-y-5">

            {/* Top stat cards */}
            <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
              {[
                { label: 'Total Budget',        value: fmt(result.totalBudget),       icon: Film,        color: 'text-blue-600',    bg: 'bg-blue-50'   },
                { label: 'Qualified Expenses',  value: fmt(result.qualifiedExpenses),  icon: DollarSign,  color: 'text-violet-600',  bg: 'bg-violet-50' },
                { label: 'Credit Rate',         value: `${result.creditRate.toFixed(0)}%`, icon: TrendingUp, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                { label: 'Est. Tax Credit',     value: fmt(result.estimatedCredit),   icon: DollarSign,  color: 'text-emerald-600', bg: 'bg-emerald-50', highlight: true },
              ].map(s => {
                const Icon = s.icon;
                return (
                  <div
                    key={s.label}
                    className={`bg-white rounded-2xl border p-5 ${s.highlight ? 'border-emerald-200 shadow-sm shadow-emerald-50' : 'border-slate-100'}`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <p className="text-xs font-medium text-slate-500">{s.label}</p>
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${s.bg}`}>
                        <Icon className={`w-4 h-4 ${s.color}`} strokeWidth={2} />
                      </div>
                    </div>
                    <p className={`text-2xl font-bold tracking-tight ${s.highlight ? 'text-emerald-600' : 'text-slate-900'}`}>
                      {s.value}
                    </p>
                  </div>
                );
              })}
            </div>

            {/* Breakdown card */}
            <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-slate-900">Incentive Breakdown</h3>
                  <p className="text-xs text-slate-500 mt-0.5">{result.productionTitle} · {result.jurisdictionName}</p>
                </div>
                <span className="px-2.5 py-1 bg-emerald-100 text-emerald-700 text-xs font-bold rounded-lg">
                  {result.effectiveRate.toFixed(1)}% effective rate
                </span>
              </div>

              <div className="divide-y divide-slate-100">
                {[
                  { label: 'Production',           value: result.productionTitle,                              mono: false },
                  { label: 'Jurisdiction',          value: result.jurisdictionName,                             mono: false },
                  { label: 'Total Budget',          value: `$${result.totalBudget.toLocaleString()}`,           mono: true  },
                  { label: 'Qualified Ratio',       value: `${((result.qualifiedExpenses / result.totalBudget) * 100).toFixed(0)}% of budget`, mono: true },
                  { label: 'Qualified Expenses',    value: `$${result.qualifiedExpenses.toLocaleString()}`,     mono: true  },
                  { label: 'Credit Rate',           value: `${result.creditRate.toFixed(0)}%`,                 mono: true  },
                  { label: 'Estimated Tax Credit',  value: `$${result.estimatedCredit.toLocaleString(undefined, { maximumFractionDigits: 0 })}`, mono: true, bold: true },
                ].map(row => (
                  <div key={row.label} className="flex items-center justify-between px-6 py-3.5 hover:bg-slate-50 transition-colors">
                    <span className="text-sm text-slate-500">{row.label}</span>
                    <span className={`text-sm ${row.bold ? 'font-bold text-emerald-600 text-base' : row.mono ? 'font-semibold text-slate-900 font-mono' : 'font-semibold text-slate-900'}`}>
                      {row.value}
                    </span>
                  </div>
                ))}
              </div>

              {/* Budget utilization summary */}
              <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-500">Budget utilization</span>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-lg">
                    {((result.qualifiedExpenses / result.totalBudget) * 100).toFixed(0)}% qualifies
                  </span>
                  <span className="text-xs font-semibold text-slate-400 bg-slate-100 px-2.5 py-1 rounded-lg">
                    {(100 - (result.qualifiedExpenses / result.totalBudget) * 100).toFixed(0)}% excluded
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                type="button"
                onClick={handleDownload}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold transition-colors ${
                  reported
                    ? 'bg-emerald-600 text-white'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {reported
                  ? <><CheckCircle className="w-4 h-4" /> Report Generated</>
                  : <><Download className="w-4 h-4" /> Download Report</>
                }
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="flex items-center gap-2 px-5 py-2.5 border border-slate-200 rounded-lg text-sm font-semibold text-slate-600 hover:bg-slate-50 transition-colors"
              >
                <RotateCcw className="w-4 h-4" />
                Recalculate
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

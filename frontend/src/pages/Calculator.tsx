import { useState, useEffect } from 'react';
import {
  Calculator as CalcIcon,
  TrendingUp,
  DollarSign,
  Film,
  Download,
  RotateCcw,
  CheckCircle,
  Loader2,
  Copy,
  Printer,
  FolderOpen,
} from 'lucide-react';
import type { Production, Jurisdiction } from '../types';
import api from '../api';

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

export default function Calculator() {
  const [productions,  setProductions]  = useState<Production[]>([]);
  const [jurisdictions, setJurisdictions] = useState<Jurisdiction[]>([]);
  const [dataLoading,  setDataLoading]  = useState(true);

  const [prodId,   setProdId]   = useState('');
  const [jurId,    setJurId]    = useState('');
  const [loading,  setLoading]  = useState(false);
  const [result,   setResult]   = useState<CalcResult | null>(null);
  const [reported,          setReported]          = useState(false);
  const [copied,            setCopied]            = useState(false);
  const [downloadedFileName, setDownloadedFileName] = useState<string | null>(null);
  const [calcError, setCalcError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.productions.list(), api.jurisdictions.list()])
      .then(([prods, jurs]) => {
        setProductions(prods);
        setJurisdictions(jurs.filter(j => j.active));
        if (prods.length)  setProdId(prods[0].id);
        if (jurs.length)   setJurId(jurs[0].id);
      })
      .catch(() => {})
      .finally(() => setDataLoading(false));
  }, []);

  async function handleCalculate() {
    const prod = productions.find(p => p.id === prodId);
    const jur  = jurisdictions.find(j => j.id === jurId);
    if (!prod || !jur) return;

    setLoading(true);
    setResult(null);
    setReported(false);
    setCalcError(null);

    try {
      const data = await api.calculations.calculate(prodId, jurId);

      const creditRate = data.qualified_expenses > 0
        ? (data.incentive_amount / data.qualified_expenses) * 100
        : 0;
      const effectiveRate = data.total_expenses > 0
        ? (data.incentive_amount / data.total_expenses) * 100
        : 0;

      setResult({
        productionTitle:   prod.title,
        jurisdictionName:  jur.name,
        totalBudget:       data.total_expenses,
        qualifiedExpenses: data.qualified_expenses,
        creditRate,
        estimatedCredit:   data.incentive_amount,
        effectiveRate,
      });
    } catch {
      setCalcError('Calculation failed. Ensure this production has qualifying expenses.');
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setResult(null);
    setReported(false);
    setCalcError(null);
  }

  function buildReportText(r: CalcResult): string {
    const date = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    const qualPct = r.totalBudget > 0 ? ((r.qualifiedExpenses / r.totalBudget) * 100).toFixed(0) : '0';
    return [
      'TAX INCENTIVE CALCULATION REPORT',
      `Generated: ${date}`,
      '',
      `Production:          ${r.productionTitle}`,
      `Jurisdiction:        ${r.jurisdictionName}`,
      '',
      `Total Budget:        $${r.totalBudget.toLocaleString()}`,
      `Qualified Expenses:  $${r.qualifiedExpenses.toLocaleString()}`,
      `Qualified Ratio:     ${qualPct}% of budget`,
      `Credit Rate:         ${r.creditRate.toFixed(0)}%`,
      `Estimated Tax Credit: $${r.estimatedCredit.toLocaleString(undefined, { maximumFractionDigits: 0 })}`,
      `Effective Rate:      ${r.effectiveRate.toFixed(1)}%`,
      '',
      'This estimate is for planning purposes only.',
      'Consult a qualified production accountant for final tax decisions.',
    ].join('\n');
  }

  function handleDownload() {
    if (!result) return;
    const text     = buildReportText(result);
    const fileName = `tax-incentive-report-${result.productionTitle.replace(/\s+/g, '-').toLowerCase()}.txt`;
    const blob     = new Blob([text], { type: 'text/plain' });
    const url      = URL.createObjectURL(blob);
    const a        = document.createElement('a');
    a.href         = url;
    a.download     = fileName;
    a.click();
    URL.revokeObjectURL(url);
    setReported(true);
    setDownloadedFileName(fileName);
    setTimeout(() => { setReported(false); setDownloadedFileName(null); }, 8000);
  }

  function handleCopy() {
    if (!result) return;
    navigator.clipboard.writeText(buildReportText(result)).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 3000);
    });
  }

  function handlePrint() {
    window.print();
  }

  const canCalculate = !!prodId && !!jurId && !dataLoading;

  // ── No productions prompt ─────────────────────────────────────────────────
  if (!dataLoading && productions.length === 0) {
    return (
      <div className="flex items-center justify-center h-full min-h-[400px]">
        <div className="text-center">
          <CalcIcon className="w-12 h-12 text-slate-300 mx-auto mb-3" strokeWidth={1.2} />
          <p className="text-slate-600 font-semibold mb-1">No productions yet</p>
          <p className="text-slate-400 text-sm">Add a production on the Productions page before running a calculation.</p>
        </div>
      </div>
    );
  }

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

          {dataLoading ? (
            <div className="flex justify-center py-8">
              <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
            </div>
          ) : (
            <div className="space-y-5">
              {/* Production select */}
              <div>
                <label className="block text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-2">
                  Production
                </label>
                <select
                  value={prodId}
                  onChange={e => { setProdId(e.target.value); setResult(null); setCalcError(null); }}
                  title="Production"
                  aria-label="Production"
                  className="select-arrow w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none"
                >
                  {productions.map(p => (
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
                  onChange={e => { setJurId(e.target.value); setResult(null); setCalcError(null); }}
                  title="Jurisdiction"
                  aria-label="Jurisdiction"
                  className="select-arrow w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none"
                >
                  {jurisdictions.map(j => (
                    <option key={j.id} value={j.id}>{j.code} — {j.name}</option>
                  ))}
                </select>
              </div>

              {/* Error */}
              {calcError && (
                <p className="text-red-500 text-xs bg-red-50 border border-red-100 rounded-lg px-3 py-2">
                  {calcError}
                </p>
              )}

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
          )}

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
                { label: 'Total Budget',        value: fmt(result.totalBudget),                        icon: Film,       color: 'text-blue-600',    bg: 'bg-blue-50'    },
                { label: 'Qualified Expenses',  value: fmt(result.qualifiedExpenses),                  icon: DollarSign, color: 'text-violet-600',  bg: 'bg-violet-50'  },
                { label: 'Credit Rate',         value: `${result.creditRate.toFixed(0)}%`,             icon: TrendingUp, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                { label: 'Est. Tax Credit',     value: fmt(result.estimatedCredit), icon: DollarSign,  color: 'text-emerald-600', bg: 'bg-emerald-50', highlight: true },
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
                  { label: 'Production',           value: result.productionTitle,                                                mono: false },
                  { label: 'Jurisdiction',         value: result.jurisdictionName,                                               mono: false },
                  { label: 'Total Budget',         value: `$${result.totalBudget.toLocaleString()}`,                             mono: true  },
                  { label: 'Qualified Ratio',      value: `${result.totalBudget > 0 ? ((result.qualifiedExpenses / result.totalBudget) * 100).toFixed(0) : 0}% of budget`, mono: true },
                  { label: 'Qualified Expenses',   value: `$${result.qualifiedExpenses.toLocaleString()}`,                       mono: true  },
                  { label: 'Credit Rate',          value: `${result.creditRate.toFixed(0)}%`,                                    mono: true  },
                  { label: 'Estimated Tax Credit', value: `$${result.estimatedCredit.toLocaleString(undefined, { maximumFractionDigits: 0 })}`, mono: true, bold: true },
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
                    {result.totalBudget > 0 ? ((result.qualifiedExpenses / result.totalBudget) * 100).toFixed(0) : 0}% qualifies
                  </span>
                  <span className="text-xs font-semibold text-slate-400 bg-slate-100 px-2.5 py-1 rounded-lg">
                    {result.totalBudget > 0 ? (100 - (result.qualifiedExpenses / result.totalBudget) * 100).toFixed(0) : 100}% excluded
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-3 flex-wrap">
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
                  ? <><CheckCircle className="w-4 h-4" /> Downloaded</>
                  : <><Download className="w-4 h-4" /> Download Report</>
                }
              </button>
              <button
                type="button"
                onClick={handleCopy}
                className={`flex items-center gap-2 px-5 py-2.5 border rounded-lg text-sm font-semibold transition-colors ${
                  copied
                    ? 'border-emerald-300 bg-emerald-50 text-emerald-700'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                {copied
                  ? <><CheckCircle className="w-4 h-4" /> Copied</>
                  : <><Copy className="w-4 h-4" /> Copy Report</>
                }
              </button>
              <button
                type="button"
                onClick={handlePrint}
                className="flex items-center gap-2 px-5 py-2.5 border border-slate-200 rounded-lg text-sm font-semibold text-slate-600 hover:bg-slate-50 transition-colors"
              >
                <Printer className="w-4 h-4" />
                Print
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

            {/* Download confirmation banner */}
            {downloadedFileName && (
              <div className="flex items-start gap-3 px-4 py-3 bg-emerald-50 border border-emerald-200 rounded-xl text-sm">
                <FolderOpen className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-emerald-800">Report saved to your Downloads folder</p>
                  <p className="text-emerald-600 text-xs mt-0.5">
                    File: <span className="font-mono">{downloadedFileName}</span>
                  </p>
                  <p className="text-emerald-600 text-xs mt-1">
                    Open it in any text editor, or use <strong>Print</strong> above to save as PDF.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import {
  ArrowLeft,
  DollarSign,
  TrendingUp,
  CheckCircle2,
  XCircle,
  Loader2,
  Calculator as CalcIcon,
  BookOpen,
  ReceiptText,
  LayoutList,
  PlayCircle,
  ClipboardCheck,
  Plus,
  Trash2,
  RefreshCw,
  Check,
  Minus,
} from 'lucide-react';
import api from '../api';
import type {
  Production,
  Jurisdiction,
  IncentiveRule,
  Expense,
  CalculationResult,
  ComplianceItem,
  ComplianceStats,
} from '../types';

// ─── Types ─────────────────────────────────────────────────────────────────

type Tab = 'overview' | 'expenses' | 'calculator' | 'rules' | 'compliance';
type ExpenseWithQualifying = Expense & {
  isQualifying?: boolean;
  expenseDate?: string;
  vendorName?: string;
  description?: string;
};

// ─── Constants ──────────────────────────────────────────────────────────────

const STATUS_COLORS: Record<string, string> = {
  planning:        'bg-blue-100 text-blue-800',
  pre_production:  'bg-violet-100 text-violet-800',
  production:      'bg-green-100 text-green-800',
  post_production: 'bg-amber-100 text-amber-800',
  completed:       'bg-slate-100 text-slate-700',
};

const STATUS_LABELS: Record<string, string> = {
  planning:        'Planning',
  pre_production:  'Pre-Production',
  production:      'Production',
  post_production: 'Post-Production',
  completed:       'Completed',
};

const EXPENSE_CATEGORIES = [
  'labor', 'equipment', 'locations', 'post_production',
  'travel', 'catering', 'legal', 'insurance', 'visual_effects', 'other',
];

const COMPLIANCE_STATUS_CONFIG: Record<string, { label: string; cls: string }> = {
  pending:  { label: 'Pending',  cls: 'bg-slate-100 text-slate-600' },
  complete: { label: 'Complete', cls: 'bg-emerald-100 text-emerald-700' },
  waived:   { label: 'Waived',   cls: 'bg-amber-100 text-amber-700' },
  na:       { label: 'N/A',      cls: 'bg-slate-50 text-slate-400' },
};

// ─── Helpers ────────────────────────────────────────────────────────────────

function fmt(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(1)}K`;
  return `$${n.toFixed(0)}`;
}
function fmtPct(n: number) { return `${n.toFixed(1)}%`; }
function capitalize(s: string) { return s.charAt(0).toUpperCase() + s.slice(1).replace(/_/g, ' '); }

// ─── Sub-components ─────────────────────────────────────────────────────────

function StatCard({ label, value, sub, accent = false }: {
  label: string; value: string; sub?: string; accent?: boolean;
}) {
  return (
    <div className={`rounded-xl border p-5 ${accent ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white border-slate-200'}`}>
      <p className={`text-xs font-semibold uppercase tracking-wider mb-1 ${accent ? 'text-blue-200' : 'text-slate-500'}`}>{label}</p>
      <p className={`text-2xl font-bold ${accent ? 'text-white' : 'text-slate-900'}`}>{value}</p>
      {sub && <p className={`text-xs mt-1 ${accent ? 'text-blue-200' : 'text-slate-500'}`}>{sub}</p>}
    </div>
  );
}

// ─── Tabs config ─────────────────────────────────────────────────────────────

const TABS: { id: Tab; label: string; icon: React.ReactNode }[] = [
  { id: 'overview',    label: 'Overview',        icon: <LayoutList className="w-3.5 h-3.5" /> },
  { id: 'expenses',    label: 'Expenses',         icon: <ReceiptText className="w-3.5 h-3.5" /> },
  { id: 'compliance',  label: 'Compliance',       icon: <ClipboardCheck className="w-3.5 h-3.5" /> },
  { id: 'calculator',  label: 'Calculator',       icon: <CalcIcon className="w-3.5 h-3.5" /> },
  { id: 'rules',       label: 'Incentive Rules',  icon: <BookOpen className="w-3.5 h-3.5" /> },
];

// ─── Main component ──────────────────────────────────────────────────────────

interface Props {
  productionId: string;
  onBack: () => void;
}

export default function ProductionDetail({ productionId, onBack }: Props) {
  const [tab, setTab] = useState<Tab>('overview');

  // Data
  const [production,    setProduction]    = useState<Production | null>(null);
  const [expenses,      setExpenses]      = useState<ExpenseWithQualifying[]>([]);
  const [jurisdictions, setJurisdictions] = useState<Jurisdiction[]>([]);
  const [rules,         setRules]         = useState<IncentiveRule[]>([]);
  const [calcResult,    setCalcResult]    = useState<CalculationResult | null>(null);
  const [calcJurId,     setCalcJurId]     = useState('');
  const [compliance,    setCompliance]    = useState<ComplianceStats | null>(null);

  // UI state
  const [loading,       setLoading]       = useState(true);
  const [calcLoading,   setCalcLoading]   = useState(false);
  const [calcError,     setCalcError]     = useState<string | null>(null);
  const [compLoading,   setCompLoading]   = useState(false);
  const [deleteExpId,   setDeleteExpId]   = useState<string | null>(null);

  // Expense form
  const EMPTY_EXP = { category: 'labor', description: '', amount: '', expenseDate: '', isQualifying: true, vendorName: '' };
  const [expForm,       setExpForm]       = useState(EMPTY_EXP);
  const [expSubmitting, setExpSubmitting] = useState(false);
  const [showExpForm,   setShowExpForm]   = useState(false);

  // ── Data loading ─────────────────────────────────────────────────────────

  useEffect(() => {
    setLoading(true);
    Promise.all([
      api.productions.get(productionId),
      api.expenses.list(productionId),
      api.jurisdictions.list(),
    ])
      .then(([prod, exps, jurs]) => {
        setProduction(prod);
        setExpenses(exps as ExpenseWithQualifying[]);
        const activeJurs = jurs.filter(j => j.active);
        setJurisdictions(activeJurs);
        setCalcJurId(prod.jurisdictionId || (activeJurs[0]?.id ?? ''));
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [productionId]);

  useEffect(() => {
    if (!production?.jurisdictionId) return;
    api.incentiveRules.getByJurisdiction(production.jurisdictionId)
      .then(r => setRules((r as IncentiveRule[]).filter(rule => rule.active)))
      .catch(() => {});
  }, [production?.jurisdictionId]);

  function loadCompliance() {
    setCompLoading(true);
    api.compliance.list(productionId)
      .then(setCompliance)
      .catch(() => {})
      .finally(() => setCompLoading(false));
  }

  useEffect(() => {
    if (tab === 'compliance' && !compliance) loadCompliance();
  }, [tab]);

  // ── Calculator ────────────────────────────────────────────────────────────

  async function handleCalculate() {
    if (!calcJurId) return;
    setCalcLoading(true); setCalcResult(null); setCalcError(null);
    try {
      setCalcResult(await api.calculations.calculate(productionId, calcJurId));
    } catch (e: unknown) {
      setCalcError(e instanceof Error ? e.message : 'Calculation failed');
    } finally {
      setCalcLoading(false);
    }
  }

  // ── Expense add ───────────────────────────────────────────────────────────

  async function handleAddExpense(e: React.FormEvent) {
    e.preventDefault();
    if (!expForm.description.trim() || !expForm.amount || !expForm.expenseDate) return;
    setExpSubmitting(true);
    try {
      const created = await api.expenses.create(productionId, {
        category:    expForm.category,
        description: expForm.description.trim(),
        amount:      Number(expForm.amount),
        expenseDate: expForm.expenseDate,
        isQualifying: expForm.isQualifying,
        vendorName:  expForm.vendorName.trim() || undefined,
      } as Parameters<typeof api.expenses.create>[1]);
      setExpenses(prev => [created as ExpenseWithQualifying, ...prev]);
      setExpForm(EMPTY_EXP);
      setShowExpForm(false);
    } catch {
      // keep form open on error
    } finally {
      setExpSubmitting(false);
    }
  }

  async function handleDeleteExpense(expId: string) {
    setDeleteExpId(expId);
    try {
      await api.expenses.delete(productionId, expId);
      setExpenses(prev => prev.filter(e => e.id !== expId));
    } catch { /* silent */ } finally {
      setDeleteExpId(null);
    }
  }

  // ── Compliance ────────────────────────────────────────────────────────────

  async function handleGenerateChecklist() {
    setCompLoading(true);
    try {
      await api.compliance.generate(productionId);
      loadCompliance();
    } catch { setCompLoading(false); }
  }

  async function cycleStatus(item: ComplianceItem) {
    const cycle: ComplianceItem['status'][] = ['pending', 'complete', 'waived', 'na'];
    const next = cycle[(cycle.indexOf(item.status) + 1) % cycle.length];
    try {
      const updated = await api.compliance.updateItem(item.id, { status: next });
      setCompliance(prev => prev ? {
        ...prev,
        items: prev.items.map(i => i.id === item.id ? (updated as ComplianceItem) : i),
        complete: prev.items.filter(i => (i.id === item.id ? next : i.status) === 'complete').length,
        pct: 0, // recalculated on next load
      } : prev);
      // Refresh stats
      loadCompliance();
    } catch { /* silent */ }
  }

  // ── Derived analytics ─────────────────────────────────────────────────────

  const totalSpend      = expenses.reduce((s, e) => s + e.amount, 0);
  const qualifyingSpend = expenses.reduce((s, e) => s + (e.isQualifying !== false ? e.amount : 0), 0);
  const nonQualifying   = totalSpend - qualifyingSpend;

  const byCategory = expenses.reduce<Record<string, ExpenseWithQualifying[]>>((acc, e) => {
    const cat = e.category || 'other';
    (acc[cat] ||= []).push(e);
    return acc;
  }, {});

  const categoryRows = Object.entries(byCategory)
    .map(([cat, exps]) => ({
      category:   cat,
      total:      exps.reduce((s, e) => s + e.amount, 0),
      qualifying: exps.reduce((s, e) => s + (e.isQualifying !== false ? e.amount : 0), 0),
      count:      exps.length,
    }))
    .sort((a, b) => b.total - a.total);

  const compByCategory = compliance
    ? Object.entries(
        compliance.items.reduce<Record<string, ComplianceItem[]>>((acc, i) => {
          (acc[i.category] ||= []).push(i);
          return acc;
        }, {})
      ).sort(([a], [b]) => a.localeCompare(b))
    : [];

  const jur = jurisdictions.find(j => j.id === production?.jurisdictionId);

  // ── Loading / not found ───────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
      </div>
    );
  }
  if (!production) {
    return (
      <div className="p-8 text-center text-slate-500">
        Production not found.{' '}
        <button onClick={onBack} className="text-blue-600 underline">Go back</button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">

      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div className="bg-white border-b border-slate-200 px-8 py-6">
        <button
          onClick={onBack}
          className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 mb-4 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Productions
        </button>
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-[26px] font-bold text-slate-900">{production.title}</h1>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${STATUS_COLORS[production.status] ?? 'bg-slate-100 text-slate-700'}`}>
                {STATUS_LABELS[production.status] ?? production.status}
              </span>
            </div>
            <p className="text-slate-500 text-sm">
              {production.productionCompany}
              {jur ? ` · ${jur.name}` : ''}
              {' · '}{capitalize(production.productionType)}
              {' · Started '}{production.startDate?.split('T')[0]}
            </p>
          </div>
          <div className="flex items-center gap-5">
            <div className="text-right">
              <p className="text-xs text-slate-400 font-medium">Total Budget</p>
              <p className="text-xl font-bold text-slate-900">{fmt(production.budgetTotal)}</p>
            </div>
            {compliance && compliance.total > 0 && (
              <div className="text-right">
                <p className="text-xs text-slate-400 font-medium">Compliance</p>
                <p className="text-xl font-bold text-emerald-600">{compliance.pct}%</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ── Tab bar ────────────────────────────────────────────────────── */}
      <div className="bg-white border-b border-slate-200 px-8">
        <div className="flex gap-1">
          {TABS.map(t => (
            <button
              key={t.id}
              type="button"
              onClick={() => setTab(t.id)}
              className={`flex items-center gap-1.5 px-4 py-3.5 text-sm font-medium border-b-2 transition-colors ${
                tab === t.id
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`}
            >
              {t.icon}{t.label}
              {t.id === 'compliance' && compliance && compliance.total > 0 && (
                <span className={`ml-1 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                  compliance.pct === 100 ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'
                }`}>{compliance.pct}%</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* ── Content ────────────────────────────────────────────────────── */}
      <div className="p-8 max-w-6xl mx-auto">

        {/* ── Overview ──────────────────────────────────────────────────── */}
        {tab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard label="Total Budget"     value={fmt(production.budgetTotal)} />
              <StatCard label="Total Expenses"   value={expenses.length ? fmt(totalSpend) : '—'} sub={`${expenses.length} items`} />
              <StatCard label="Qualifying Spend" value={expenses.length ? fmt(qualifyingSpend) : '—'}
                sub={totalSpend ? fmtPct((qualifyingSpend / totalSpend) * 100) + ' of spend' : undefined} accent />
              <StatCard label="Incentive Rules"  value={String(rules.length)} sub={jur?.name ?? 'No jurisdiction'} />
            </div>
            <div className="bg-white rounded-xl border border-slate-200 p-6">
              <h2 className="text-sm font-bold text-slate-900 mb-4">Production Details</h2>
              <dl className="grid grid-cols-2 md:grid-cols-3 gap-x-8 gap-y-4 text-sm">
                {([
                  ['Title',             production.title],
                  ['Type',              capitalize(production.productionType)],
                  ['Company',           production.productionCompany],
                  ['Status',            STATUS_LABELS[production.status] ?? production.status],
                  ['Jurisdiction',      jur ? `${jur.name} (${jur.code})` : '—'],
                  ['Total Budget',      fmt(production.budgetTotal)],
                  ['Qualifying Budget', production.budgetQualifying ? fmt(production.budgetQualifying) : '—'],
                  ['Start Date',        production.startDate?.split('T')[0] ?? '—'],
                  ['End Date',          production.endDate?.split('T')[0] ?? '—'],
                  ['Created',           production.createdAt?.split('T')[0] ?? '—'],
                ] as [string, string][]).map(([label, value]) => (
                  <div key={label}>
                    <dt className="text-slate-500 font-medium mb-0.5">{label}</dt>
                    <dd className="text-slate-900 font-semibold">{value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        )}

        {/* ── Expenses ──────────────────────────────────────────────────── */}
        {tab === 'expenses' && (
          <div className="space-y-6">
            {/* Summary cards */}
            <div className="grid grid-cols-3 gap-4">
              <StatCard label="Total Spend"      value={fmt(totalSpend)}      sub={`${expenses.length} items`} />
              <StatCard label="Qualifying Spend" value={fmt(qualifyingSpend)} sub={totalSpend ? fmtPct((qualifyingSpend / totalSpend) * 100) + ' of total' : undefined} accent />
              <StatCard label="Non-Qualifying"   value={fmt(nonQualifying)}   sub={totalSpend ? fmtPct((nonQualifying / totalSpend) * 100) + ' of total' : undefined} />
            </div>

            {/* Progress bar */}
            {totalSpend > 0 && (
              <div className="bg-white rounded-xl border border-slate-200 p-5">
                <div className="flex justify-between text-sm mb-2">
                  <span className="font-semibold text-slate-700">Qualifying Breakdown</span>
                  <span className="text-slate-500">{fmt(qualifyingSpend)} of {fmt(totalSpend)}</span>
                </div>
                <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full transition-all"
                    style={{ width: `${Math.min((qualifyingSpend / totalSpend) * 100, 100)}%` }} />
                </div>
              </div>
            )}

            {/* Add expense */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
                <h2 className="text-sm font-bold text-slate-900">Expenses</h2>
                <button
                  type="button"
                  onClick={() => setShowExpForm(v => !v)}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-blue-600 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors"
                >
                  <Plus className="w-3.5 h-3.5" />
                  Add Expense
                </button>
              </div>

              {showExpForm && (
                <form onSubmit={handleAddExpense} className="px-6 py-5 border-b border-slate-100 bg-slate-50">
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-500 mb-1">Category *</label>
                      <select
                        value={expForm.category}
                        onChange={e => setExpForm(f => ({ ...f, category: e.target.value }))}
                        title="Category"
                        aria-label="Category"
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        {EXPENSE_CATEGORIES.map(c => <option key={c} value={c}>{capitalize(c)}</option>)}
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-500 mb-1">Amount (USD) *</label>
                      <div className="relative">
                        <span className="absolute left-3 top-2 text-slate-400 text-sm">$</span>
                        <input
                          type="number" min="0.01" step="0.01" required
                          placeholder="0.00"
                          value={expForm.amount}
                          onChange={e => setExpForm(f => ({ ...f, amount: e.target.value }))}
                          className="w-full pl-6 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-500 mb-1">Date *</label>
                      <input
                        type="date" required
                        title="Expense date"
                        value={expForm.expenseDate}
                        onChange={e => setExpForm(f => ({ ...f, expenseDate: e.target.value }))}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-xs font-semibold text-slate-500 mb-1">Description *</label>
                      <input
                        type="text" required
                        placeholder="e.g. Camera package rental — week 3"
                        value={expForm.description}
                        onChange={e => setExpForm(f => ({ ...f, description: e.target.value }))}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-500 mb-1">Vendor</label>
                      <input
                        type="text"
                        placeholder="Vendor name (optional)"
                        value={expForm.vendorName}
                        onChange={e => setExpForm(f => ({ ...f, vendorName: e.target.value }))}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <label className="flex items-center gap-2 text-sm text-slate-700 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        checked={expForm.isQualifying}
                        onChange={e => setExpForm(f => ({ ...f, isQualifying: e.target.checked }))}
                        className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                      />
                      Qualifying expense
                    </label>
                    <div className="flex gap-2">
                      <button type="button" onClick={() => { setShowExpForm(false); setExpForm(EMPTY_EXP); }}
                        className="px-4 py-2 text-xs border border-slate-300 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors">
                        Cancel
                      </button>
                      <button type="submit" disabled={expSubmitting}
                        className="px-4 py-2 text-xs bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors flex items-center gap-1.5">
                        {expSubmitting ? <Loader2 className="w-3 h-3 animate-spin" /> : <Plus className="w-3 h-3" />}
                        {expSubmitting ? 'Saving…' : 'Add Expense'}
                      </button>
                    </div>
                  </div>
                </form>
              )}

              {categoryRows.length > 0 ? (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-slate-100 bg-slate-50">
                      {['Category','Items','Total','Qualifying','Non-Qual.','% of Total'].map(h => (
                        <th key={h} className={`px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider ${h === 'Category' ? 'text-left' : 'text-right'}`}>{h}</th>
                      ))}
                      <th className="px-4 py-3" />
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {categoryRows.map(row => (
                      <tr key={row.category} className="hover:bg-slate-50">
                        <td className="px-6 py-3.5 font-medium text-slate-800">{capitalize(row.category)}</td>
                        <td className="px-6 py-3.5 text-right text-slate-600">{row.count}</td>
                        <td className="px-6 py-3.5 text-right font-semibold text-slate-900">{fmt(row.total)}</td>
                        <td className="px-6 py-3.5 text-right text-emerald-700 font-medium">
                          <span className="flex items-center justify-end gap-1">
                            <CheckCircle2 className="w-3.5 h-3.5" />{fmt(row.qualifying)}
                          </span>
                        </td>
                        <td className="px-6 py-3.5 text-right text-slate-400">
                          {row.total - row.qualifying > 0 ? (
                            <span className="flex items-center justify-end gap-1">
                              <XCircle className="w-3.5 h-3.5 text-slate-300" />{fmt(row.total - row.qualifying)}
                            </span>
                          ) : '—'}
                        </td>
                        <td className="px-6 py-3.5 text-right text-slate-500">
                          {totalSpend ? fmtPct((row.total / totalSpend) * 100) : '—'}
                        </td>
                        <td className="px-4 py-3.5" />
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr className="bg-slate-50 border-t-2 border-slate-200 font-bold">
                      <td className="px-6 py-3.5 text-slate-900">Total</td>
                      <td className="px-6 py-3.5 text-right text-slate-600">{expenses.length}</td>
                      <td className="px-6 py-3.5 text-right text-slate-900">{fmt(totalSpend)}</td>
                      <td className="px-6 py-3.5 text-right text-emerald-700">{fmt(qualifyingSpend)}</td>
                      <td className="px-6 py-3.5 text-right text-slate-500">{fmt(nonQualifying)}</td>
                      <td className="px-6 py-3.5 text-right text-slate-500">100%</td>
                      <td className="px-4 py-3.5" />
                    </tr>
                  </tfoot>
                </table>
              ) : (
                <div className="p-16 text-center">
                  <DollarSign className="w-8 h-8 text-slate-300 mx-auto mb-3" />
                  <p className="text-slate-700 font-semibold mb-1">No expenses recorded</p>
                  <p className="text-slate-400 text-sm">Click "Add Expense" to start tracking spend.</p>
                </div>
              )}

              {/* Individual expense rows */}
              {expenses.length > 0 && (
                <div className="border-t border-slate-100">
                  <div className="px-6 py-3 bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    All Expenses ({expenses.length})
                  </div>
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-slate-100">
                        {(['Date','Description','Category','Amount','Qual.'] as const).map(h => (
                          <th key={h} className={`px-6 py-2.5 text-xs font-semibold text-slate-400 ${h === 'Amount' || h === 'Qual.' ? 'text-right' : 'text-left'}`}>{h}</th>
                        ))}
                        <th className="px-4 py-2.5 text-right"><span className="sr-only">Delete</span></th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-50">
                      {expenses.map(exp => (
                        <tr key={exp.id} className="hover:bg-slate-50">
                          <td className="px-6 py-2.5 text-slate-500 text-xs whitespace-nowrap">
                            {(exp.expenseDate || (exp as { date?: string }).date || '').split('T')[0]}
                          </td>
                          <td className="px-6 py-2.5 text-slate-800">
                            {exp.description || '—'}
                            {exp.vendorName && <span className="text-slate-400 ml-1 text-xs">· {exp.vendorName}</span>}
                          </td>
                          <td className="px-6 py-2.5 text-slate-500">{capitalize(exp.category)}</td>
                          <td className="px-6 py-2.5 text-right font-semibold text-slate-900">{fmt(exp.amount)}</td>
                          <td className="px-6 py-2.5 text-right">
                            {exp.isQualifying !== false
                              ? <CheckCircle2 className="w-4 h-4 text-emerald-500 ml-auto" />
                              : <XCircle className="w-4 h-4 text-slate-300 ml-auto" />}
                          </td>
                          <td className="px-4 py-2.5 text-right">
                            <button type="button" onClick={() => handleDeleteExpense(exp.id)}
                              disabled={deleteExpId === exp.id}
                              title="Delete expense" aria-label="Delete expense"
                              className="text-slate-300 hover:text-red-500 transition-colors disabled:opacity-40">
                              {deleteExpId === exp.id
                                ? <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                : <Trash2 className="w-3.5 h-3.5" />}
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── Compliance ─────────────────────────────────────────────────── */}
        {tab === 'compliance' && (
          <div className="space-y-5">
            {/* Header actions */}
            <div className="flex items-center justify-between">
              <div>
                {compliance && compliance.total > 0 && (
                  <p className="text-sm text-slate-500">
                    <span className="font-bold text-slate-900">{compliance.complete}</span> of{' '}
                    <span className="font-bold text-slate-900">{compliance.total}</span> items complete
                    {compliance.waived > 0 && ` · ${compliance.waived} waived`}
                  </p>
                )}
              </div>
              <div className="flex gap-2">
                {compliance && compliance.total > 0 && (
                  <button type="button" onClick={loadCompliance}
                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs border border-slate-300 rounded-lg text-slate-600 hover:bg-slate-50 transition-colors">
                    <RefreshCw className="w-3.5 h-3.5" />Refresh
                  </button>
                )}
                <button type="button" onClick={handleGenerateChecklist} disabled={compLoading}
                  className="flex items-center gap-1.5 px-4 py-1.5 text-xs bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors">
                  {compLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}
                  {compliance && compliance.total > 0 ? 'Regenerate Checklist' : 'Generate Checklist'}
                </button>
              </div>
            </div>

            {/* Progress bar */}
            {compliance && compliance.total > 0 && (
              <div className="bg-white rounded-xl border border-slate-200 p-5">
                <div className="flex justify-between text-sm mb-2">
                  <span className="font-semibold text-slate-700">Overall Completion</span>
                  <span className="text-slate-500">{compliance.pct}%</span>
                </div>
                <progress
                  value={compliance.pct}
                  max={100}
                  aria-label={`${compliance.pct}% of compliance items complete`}
                  className={`w-full h-3 rounded-full appearance-none [&::-webkit-progress-bar]:rounded-full [&::-webkit-progress-bar]:bg-slate-100 [&::-webkit-progress-value]:rounded-full [&::-webkit-progress-value]:transition-all ${
                    compliance.pct === 100
                      ? '[&::-webkit-progress-value]:bg-emerald-500 [&::-moz-progress-bar]:bg-emerald-500'
                      : '[&::-webkit-progress-value]:bg-blue-500 [&::-moz-progress-bar]:bg-blue-500'
                  } [&::-moz-progress-bar]:rounded-full`}
                />
                <div className="flex gap-4 mt-2.5 text-xs text-slate-500">
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-emerald-500 inline-block" /> Complete ({compliance.complete})</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-slate-200 inline-block" /> Pending ({compliance.pending})</span>
                  {compliance.waived > 0 && <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-amber-400 inline-block" /> Waived ({compliance.waived})</span>}
                </div>
              </div>
            )}

            {/* Items by category */}
            {compByCategory.map(([cat, items]) => (
              <div key={cat} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
                <div className="flex items-center justify-between px-6 py-3.5 border-b border-slate-100 bg-slate-50">
                  <h3 className="text-xs font-bold text-slate-600 uppercase tracking-widest">{capitalize(cat)}</h3>
                  <span className="text-xs text-slate-400">
                    {items.filter(i => i.status === 'complete').length}/{items.length} complete
                  </span>
                </div>
                <div className="divide-y divide-slate-50">
                  {items.map(item => {
                    const cfg = COMPLIANCE_STATUS_CONFIG[item.status] ?? COMPLIANCE_STATUS_CONFIG.pending;
                    return (
                      <div key={item.id} className="flex items-center gap-4 px-6 py-3.5 hover:bg-slate-50">
                        <button type="button" onClick={() => cycleStatus(item)}
                          title="Cycle status" aria-label="Cycle status"
                          className={`w-6 h-6 rounded-full border-2 flex items-center justify-center shrink-0 transition-colors ${
                            item.status === 'complete' ? 'bg-emerald-500 border-emerald-500' :
                            item.status === 'waived'   ? 'bg-amber-400 border-amber-400' :
                            item.status === 'na'       ? 'bg-slate-200 border-slate-200' :
                                                         'border-slate-300 hover:border-blue-400'
                          }`}>
                          {item.status === 'complete' && <Check className="w-3 h-3 text-white" />}
                          {item.status === 'waived'   && <Minus className="w-3 h-3 text-white" />}
                        </button>
                        <span className={`text-sm flex-1 ${item.status === 'complete' ? 'text-slate-400 line-through' : item.status === 'na' ? 'text-slate-300' : 'text-slate-800'}`}>
                          {item.label}
                        </span>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full shrink-0 ${cfg.cls}`}>
                          {cfg.label}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}

            {(!compliance || compliance.total === 0) && !compLoading && (
              <div className="bg-white rounded-xl border border-slate-200 p-16 text-center">
                <ClipboardCheck className="w-8 h-8 text-slate-300 mx-auto mb-3" />
                <p className="text-slate-700 font-semibold mb-1">No checklist yet</p>
                <p className="text-slate-400 text-sm">Click "Generate Checklist" to create compliance items from this production's jurisdiction rules.</p>
              </div>
            )}
            {compLoading && (
              <div className="flex justify-center py-10">
                <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
              </div>
            )}
          </div>
        )}

        {/* ── Calculator ─────────────────────────────────────────────────── */}
        {tab === 'calculator' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl border border-slate-200 p-6">
              <h2 className="text-sm font-bold text-slate-900 mb-4">Incentive Calculator</h2>
              <div className="flex gap-4 items-end">
                <div className="flex-1">
                  <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                    Calculate Against Jurisdiction
                  </label>
                  <select
                    value={calcJurId}
                    onChange={e => { setCalcJurId(e.target.value); setCalcResult(null); }}
                    title="Select jurisdiction"
                    aria-label="Select jurisdiction"
                    className="w-full px-3.5 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-slate-800"
                  >
                    {jurisdictions.map(j => (
                      <option key={j.id} value={j.id}>
                        {j.name} ({j.code}) — {j.country}
                        {j.id === production.jurisdictionId ? ' ★ primary' : ''}
                      </option>
                    ))}
                  </select>
                </div>
                <button
                  type="button"
                  onClick={handleCalculate}
                  disabled={!calcJurId || calcLoading}
                  className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shrink-0"
                >
                  {calcLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <PlayCircle className="w-4 h-4" />}
                  {calcLoading ? 'Calculating…' : 'Calculate'}
                </button>
              </div>
              {calcError && <p className="mt-3 text-sm text-red-600">{calcError}</p>}
            </div>

            {calcResult && (() => {
              const selectedJur = jurisdictions.find(j => j.id === calcResult.jurisdiction_id);
              const creditRate  = calcResult.qualified_expenses > 0
                ? (calcResult.incentive_amount / calcResult.qualified_expenses) * 100 : 0;
              return (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <StatCard label="Total Expenses"     value={fmt(calcResult.total_expenses)} />
                    <StatCard label="Qualified Expenses" value={fmt(calcResult.qualified_expenses)}
                      sub={calcResult.total_expenses ? fmtPct((calcResult.qualified_expenses / calcResult.total_expenses) * 100) + ' of total' : undefined} />
                    <StatCard label="Estimated Credit"   value={fmt(calcResult.incentive_amount)} accent />
                    <StatCard label="Effective Rate"     value={fmtPct(calcResult.effective_rate * 100 || calcResult.effective_rate)} />
                  </div>
                  <div className="bg-white rounded-xl border border-slate-200 p-6">
                    <h3 className="text-sm font-bold text-slate-900 mb-4">
                      Calculation Summary — {selectedJur?.name ?? 'Selected Jurisdiction'}
                    </h3>
                    <dl className="space-y-3 text-sm">
                      {([
                        ['Production',         production.title],
                        ['Jurisdiction',       selectedJur ? `${selectedJur.name} (${selectedJur.code})` : '—'],
                        ['Total Expenses',     fmt(calcResult.total_expenses)],
                        ['Qualified Expenses', fmt(calcResult.qualified_expenses)],
                        ['Qualification Rate', calcResult.total_expenses ? fmtPct((calcResult.qualified_expenses / calcResult.total_expenses) * 100) : '—'],
                        ['Credit Rate',        fmtPct(creditRate)],
                        ['Estimated Credit',   fmt(calcResult.incentive_amount)],
                        ['Effective Rate',     fmtPct(calcResult.effective_rate * 100 || calcResult.effective_rate)],
                      ] as [string, string][]).map(([label, value]) => (
                        <div key={label} className="flex justify-between py-2 border-b border-slate-50 last:border-0">
                          <dt className="text-slate-500">{label}</dt>
                          <dd className="font-semibold text-slate-900">{value}</dd>
                        </div>
                      ))}
                    </dl>
                  </div>
                </div>
              );
            })()}

            {!calcResult && !calcLoading && (
              <div className="bg-white rounded-xl border border-slate-200 p-16 text-center">
                <TrendingUp className="w-8 h-8 text-slate-300 mx-auto mb-3" />
                <p className="text-slate-700 font-semibold mb-1">Select a jurisdiction and calculate</p>
                <p className="text-slate-400 text-sm">Compare different jurisdictions to find the best incentive yield.</p>
              </div>
            )}
          </div>
        )}

        {/* ── Incentive Rules ─────────────────────────────────────────────── */}
        {tab === 'rules' && (
          <div className="space-y-4">
            {rules.length === 0 ? (
              <div className="bg-white rounded-xl border border-slate-200 p-16 text-center">
                <BookOpen className="w-8 h-8 text-slate-300 mx-auto mb-3" />
                <p className="text-slate-700 font-semibold mb-1">No incentive rules found</p>
                <p className="text-slate-400 text-sm">
                  {jur ? `No active rules for ${jur.name}.` : 'No jurisdiction assigned to this production.'}
                </p>
              </div>
            ) : (
              <>
                <p className="text-sm text-slate-500">
                  {rules.length} active rule{rules.length !== 1 ? 's' : ''} for{' '}
                  <span className="font-medium text-slate-700">{jur?.name ?? 'this jurisdiction'}</span>
                </p>
                {rules.map(rule => (
                  <div key={rule.id} className="bg-white rounded-xl border border-slate-200 p-6">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-900">{rule.ruleName}</h3>
                        <p className="text-xs text-slate-500 mt-0.5">{rule.ruleCode} · {capitalize(rule.incentiveType)}</p>
                      </div>
                      {rule.percentage != null && <span className="text-2xl font-bold text-blue-600">{rule.percentage}%</span>}
                      {rule.fixedAmount != null && <span className="text-2xl font-bold text-blue-600">{fmt(rule.fixedAmount)}</span>}
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs mb-4">
                      {rule.minSpend  != null && <div><p className="text-slate-400 font-medium mb-0.5">Min Spend</p><p className="text-slate-800 font-semibold">{fmt(rule.minSpend)}</p></div>}
                      {rule.maxCredit != null && <div><p className="text-slate-400 font-medium mb-0.5">Max Credit</p><p className="text-slate-800 font-semibold">{fmt(rule.maxCredit)}</p></div>}
                      <div><p className="text-slate-400 font-medium mb-0.5">Effective Date</p><p className="text-slate-800 font-semibold">{rule.effectiveDate?.split('T')[0] ?? '—'}</p></div>
                      {rule.expirationDate && <div><p className="text-slate-400 font-medium mb-0.5">Expires</p><p className="text-amber-700 font-semibold">{rule.expirationDate.split('T')[0]}</p></div>}
                    </div>
                    {rule.eligibleExpenses?.length > 0 && (
                      <div className="mb-3">
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Eligible Categories</p>
                        <div className="flex flex-wrap gap-1.5">
                          {rule.eligibleExpenses.map(exp => (
                            <span key={exp} className="px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-100 rounded-full text-xs font-medium">{capitalize(exp)}</span>
                          ))}
                        </div>
                      </div>
                    )}
                    {rule.excludedExpenses?.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Excluded Categories</p>
                        <div className="flex flex-wrap gap-1.5">
                          {rule.excludedExpenses.map(exp => (
                            <span key={exp} className="px-2.5 py-1 bg-red-50 text-red-600 border border-red-100 rounded-full text-xs font-medium">{capitalize(exp)}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

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
  RefreshCw,
} from 'lucide-react';
import api from '../api';
import type {
  Production,
  Jurisdiction,
  IncentiveRule,
  CalculationResult,
  ComplianceItem,
  ComplianceStats,
} from '../types';

type Tab = 'overview' | 'expenses' | 'calculator' | 'rules' | 'compliance';

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

const COMPLIANCE_STATUS_CONFIG: Record<string, { label: string; cls: string }> = {
  pending:  { label: 'Pending',  cls: 'bg-slate-100 text-slate-600' },
  complete: { label: 'Complete', cls: 'bg-emerald-100 text-emerald-700' },
  waived:   { label: 'Waived',   cls: 'bg-amber-100 text-amber-700' },
  na:       { label: 'N/A',      cls: 'bg-slate-50 text-slate-400' },
};

function fmt(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(1)}K`;
  return `$${n.toFixed(0)}`;
}
function fmtPct(n: number) { return `${n.toFixed(1)}%`; }
function capitalize(s: string) { return s.charAt(0).toUpperCase() + s.slice(1).replace(/_/g, ' '); }

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

const TABS: { id: Tab; label: string; icon: React.ReactNode }[] = [
  { id: 'overview',    label: 'Overview',        icon: <LayoutList className="w-3.5 h-3.5" /> },
  { id: 'expenses',    label: 'Expenses',         icon: <ReceiptText className="w-3.5 h-3.5" /> },
  { id: 'compliance',  label: 'Compliance',       icon: <ClipboardCheck className="w-3.5 h-3.5" /> },
  { id: 'calculator',  label: 'Calculator',       icon: <CalcIcon className="w-3.5 h-3.5" /> },
  { id: 'rules',       label: 'Incentive Rules',  icon: <BookOpen className="w-3.5 h-3.5" /> },
];

interface Props {
  productionId: string;
  onBack: () => void;
}

export default function ProductionDetail({ productionId, onBack }: Props) {
  const [tab, setTab] = useState<Tab>('overview');
  const [production, setProduction] = useState<Production | null>(null);
  const [budgetItems, setBudgetItems] = useState<any[]>([]);
  const [budgetLoading, setBudgetLoading] = useState(false);
  const [jurisdictions, setJurisdictions] = useState<Jurisdiction[]>([]);
  const [rules, setRules] = useState<IncentiveRule[]>([]);
  const [calcResult, setCalcResult] = useState<CalculationResult | null>(null);
  const [calcJurId, setCalcJurId] = useState('');
  const [compliance, setCompliance] = useState<ComplianceStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [calcLoading, setCalcLoading] = useState(false);
  const [calcError, setCalcError] = useState<string | null>(null);
  const [compLoading, setCompLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      api.productions.get(productionId),
      api.jurisdictions.list(),
    ])
      .then(([prod, jurs]) => {
        setProduction(prod);
        const activeJurs = jurs.filter((j: Jurisdiction) => j.active);
        setJurisdictions(activeJurs);
        setCalcJurId(prod.jurisdictionId || (activeJurs[0]?.id ?? ''));
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [productionId]);

  useEffect(() => {
    if (!production?.jurisdictionId) return;
    api.incentiveRules.getByJurisdiction(production.jurisdictionId)
      .then(rules => setRules(rules.filter(rule => rule.active)))
      .catch(() => {});
  }, [production?.jurisdictionId]);

  function loadCompliance() {
    setCompLoading(true);
    api.compliance.list(productionId)
      .then(data => setCompliance(data))
      .catch(() => {})
      .finally(() => setCompLoading(false));
  }

  useEffect(() => {
    if (tab === 'compliance' && !compliance) loadCompliance();
  }, [tab]);

  async function handleCalculate() {
    if (!calcJurId) return;
    setCalcLoading(true); setCalcResult(null); setCalcError(null);
    try {
      const result = await api.calculations.calculate(productionId, calcJurId);
      setCalcResult(result);
    } catch (e: any) {
      setCalcError(e.message);
    } finally {
      setCalcLoading(false);
    }
  }

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
      await api.compliance.updateItem(item.id, { status: next });
      loadCompliance();
    } catch { /* silent */ }
  }

  const totalSpend = budgetItems.reduce((s, i) => s + i.amount, 0);
  const qualifyingSpend = budgetItems.reduce((s, i) => s + (i.is_eligible ? i.amount : 0), 0);
  const nonQualifying = totalSpend - qualifyingSpend;

  const byCategory = budgetItems.reduce<Record<string, any[]>>((acc, i) => {
    const cat = i.category || 'other';
    (acc[cat] ||= []).push(i);
    return acc;
  }, {});

  const categoryRows = Object.entries(byCategory)
    .map(([cat, items]) => ({
      category: cat,
      total: items.reduce((s, i) => s + i.amount, 0),
      qualifying: items.reduce((s, i) => s + (i.is_eligible ? i.amount : 0), 0),
      count: items.length,
    }))
    .sort((a, b) => b.total - a.total);

  const jur = jurisdictions.find(j => j.id === production?.jurisdictionId);

  if (loading) {
    return <div className="flex justify-center py-32"><Loader2 className="w-6 h-6 animate-spin text-blue-500" /></div>;
  }
  if (!production) {
    return <div className="p-8 text-center">Production not found. <button onClick={onBack} className="text-blue-600 underline">Go back</button></div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-8 py-6">
        <button onClick={onBack} className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 mb-4">
          <ArrowLeft className="w-4 h-4" /> Back to Productions
        </button>
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-[26px] font-bold text-slate-900">{production.title}</h1>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${STATUS_COLORS[production.status] ?? 'bg-slate-100'}`}>
                {STATUS_LABELS[production.status] ?? production.status}
              </span>
            </div>
            <p className="text-slate-500 text-sm">
              {production.productionCompany}{jur ? ` · ${jur.name}` : ''} · {capitalize(production.productionType)} · Started {production.startDate?.split('T')[0]}
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

      {/* Tabs */}
      <div className="bg-white border-b border-slate-200 px-8">
        <div className="flex gap-1">
          {TABS.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)} className={`flex items-center gap-1.5 px-4 py-3.5 text-sm font-medium border-b-2 transition-colors ${tab === t.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}>
              {t.icon}{t.label}
              {t.id === 'compliance' && compliance && compliance.total > 0 && (
                <span className={`ml-1 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${compliance.pct === 100 ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'}`}>{compliance.pct}%</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="p-8 max-w-6xl mx-auto">
        {/* Overview Tab */}
        {tab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard label="Total Budget" value={fmt(production.budgetTotal)} />
              <StatCard label="Total Spend" value={budgetItems.length ? fmt(totalSpend) : '—'} sub={`${budgetItems.length} items`} />
              <StatCard label="Qualifying Spend" value={budgetItems.length ? fmt(qualifyingSpend) : '—'} sub={totalSpend ? fmtPct((qualifyingSpend / totalSpend) * 100) + ' of spend' : undefined} accent />
              <StatCard label="Incentive Rules" value={String(rules.length)} sub={jur?.name ?? 'No jurisdiction'} />
            </div>
            <div className="bg-white rounded-xl border border-slate-200 p-6">
              <h2 className="text-sm font-bold text-slate-900 mb-4">Production Details</h2>
              <dl className="grid grid-cols-2 md:grid-cols-3 gap-x-8 gap-y-4 text-sm">
                {[
                  ['Title', production.title], ['Type', capitalize(production.productionType)], ['Company', production.productionCompany],
                  ['Status', STATUS_LABELS[production.status] ?? production.status], ['Jurisdiction', jur ? `${jur.name} (${jur.code})` : '—'],
                  ['Total Budget', fmt(production.budgetTotal)], ['Qualifying Budget', production.budgetQualifying ? fmt(production.budgetQualifying) : '—'],
                  ['Start Date', production.startDate?.split('T')[0] ?? '—'], ['End Date', production.endDate?.split('T')[0] ?? '—'],
                  ['Created', production.createdAt?.split('T')[0] ?? '—'],
                ].map(([label, value]) => (
                  <div key={label}><dt className="text-slate-500 font-medium mb-0.5">{label}</dt><dd className="text-slate-900 font-semibold">{value}</dd></div>
                ))}
              </dl>
            </div>
          </div>
        )}

        {/* Expenses Tab - Embedded working static page */}
        {tab === 'expenses' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl border border-slate-200 p-4">
              <iframe
                src="http://127.0.0.1:8001/static/budget_demo.html"
                title="Budget Line Items"
                className="w-full border-0"
                style={{ height: '600px' }}
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
              />
            </div>
          </div>
        )}

        {/* Compliance Tab */}
        {tab === 'compliance' && (
          <div className="space-y-5">
            <div className="flex items-center justify-between">
              {compliance && compliance.total > 0 && <p className="text-sm text-slate-500"><span className="font-bold">{compliance.complete}</span> of <span className="font-bold">{compliance.total}</span> items complete{compliance.waived > 0 && ` · ${compliance.waived} waived`}</p>}
              <div className="flex gap-2">
                {compliance && compliance.total > 0 && <button onClick={loadCompliance} className="flex items-center gap-1.5 px-3 py-1.5 text-xs border rounded-lg"><RefreshCw className="w-3.5 h-3.5" />Refresh</button>}
                <button onClick={handleGenerateChecklist} disabled={compLoading} className="flex items-center gap-1.5 px-4 py-1.5 text-xs bg-blue-600 text-white rounded-lg">{compLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5" />}{compliance ? 'Regenerate' : 'Generate'} Checklist</button>
              </div>
            </div>
            {compliance && compliance.total > 0 && <div className="bg-white rounded-xl border p-5"><div className="flex justify-between text-sm mb-2"><span className="font-semibold">Overall Completion</span><span>{compliance.pct}%</span></div><progress value={compliance.pct} max={100} className="w-full h-3 rounded-full" /><div className="flex gap-4 mt-2.5 text-xs"><span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-emerald-500" /> Complete ({compliance.complete})</span><span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-slate-200" /> Pending ({compliance.pending})</span>{compliance.waived > 0 && <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-amber-400" /> Waived ({compliance.waived})</span>}</div></div>}
            {compliance?.items?.length > 0 && Object.entries(compliance.items.reduce<Record<string, ComplianceItem[]>>((acc, i) => { (acc[i.category] ||= []).push(i); return acc; }, {})).sort(([a], [b]) => a.localeCompare(b)).map(([cat, items]) => (
              <div key={cat} className="bg-white rounded-xl border overflow-hidden"><div className="flex justify-between px-6 py-3.5 border-b bg-slate-50"><h3 className="text-xs font-bold uppercase">{capitalize(cat)}</h3><span className="text-xs">{items.filter(i => i.status === 'complete').length}/{items.length} complete</span></div><div className="divide-y divide-slate-50">{items.map(item => { const cfg = COMPLIANCE_STATUS_CONFIG[item.status]; return (<div key={item.id} className="flex items-center gap-4 px-6 py-3.5 hover:bg-slate-50"><button onClick={() => cycleStatus(item)} className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${item.status === 'complete' ? 'bg-emerald-500 border-emerald-500' : item.status === 'waived' ? 'bg-amber-400 border-amber-400' : item.status === 'na' ? 'bg-slate-200 border-slate-200' : 'border-slate-300'}`}>{item.status === 'complete' && <CheckCircle2 className="w-3 h-3 text-white" />}{item.status === 'waived' && <XCircle className="w-3 h-3 text-white" />}</button><span className={`text-sm flex-1 ${item.status === 'complete' ? 'line-through text-slate-400' : ''}`}>{item.label}</span><span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${cfg.cls}`}>{cfg.label}</span></div>); })}</div></div>
            ))}
            {(!compliance || compliance.total === 0) && !compLoading && <div className="bg-white rounded-xl border p-16 text-center"><ClipboardCheck className="w-8 h-8 text-slate-300 mx-auto mb-3" /><p className="text-slate-700 font-semibold">No checklist yet</p><p className="text-slate-400 text-sm">Click "Generate Checklist" to create compliance items.</p></div>}
            {compLoading && <div className="flex justify-center py-10"><Loader2 className="w-5 h-5 animate-spin text-blue-500" /></div>}
          </div>
        )}

        {/* Calculator Tab */}
        {tab === 'calculator' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl border p-6"><h2 className="text-sm font-bold mb-4">Incentive Calculator</h2><div className="flex gap-4 items-end"><div className="flex-1"><label className="block text-xs font-semibold uppercase mb-2">Jurisdiction</label><select value={calcJurId} onChange={e => { setCalcJurId(e.target.value); setCalcResult(null); }} className="w-full px-3.5 py-2.5 border rounded-lg">{jurisdictions.map(j => <option key={j.id} value={j.id}>{j.name} ({j.code}){j.id === production.jurisdictionId ? ' ★ primary' : ''}</option>)}</select></div><button onClick={handleCalculate} disabled={!calcJurId || calcLoading} className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-lg">{calcLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <PlayCircle className="w-4 h-4" />}{calcLoading ? 'Calculating…' : 'Calculate'}</button></div>{calcError && <p className="text-red-600 text-sm mt-3">{calcError}</p>}</div>
            {calcResult && (() => { const sel = jurisdictions.find(j => j.id === calcResult.jurisdiction_id); const rate = calcResult.qualified_expenses > 0 ? (calcResult.incentive_amount / calcResult.qualified_expenses) * 100 : 0; return (<div className="space-y-4"><div className="grid grid-cols-4 gap-4"><StatCard label="Total Expenses" value={fmt(calcResult.total_expenses)} /><StatCard label="Qualified Expenses" value={fmt(calcResult.qualified_expenses)} sub={calcResult.total_expenses ? fmtPct((calcResult.qualified_expenses / calcResult.total_expenses) * 100) : undefined} /><StatCard label="Estimated Credit" value={fmt(calcResult.incentive_amount)} accent /><StatCard label="Effective Rate" value={fmtPct(calcResult.effective_rate * 100)} /></div><div className="bg-white rounded-xl border p-6"><h3 className="text-sm font-bold mb-4">Summary — {sel?.name}</h3><dl className="space-y-3">{([['Production', production.title], ['Jurisdiction', sel ? `${sel.name} (${sel.code})` : '—'], ['Total Expenses', fmt(calcResult.total_expenses)], ['Qualified Expenses', fmt(calcResult.qualified_expenses)], ['Qualification Rate', fmtPct((calcResult.qualified_expenses / calcResult.total_expenses) * 100)], ['Credit Rate', fmtPct(rate)], ['Estimated Credit', fmt(calcResult.incentive_amount)], ['Effective Rate', fmtPct(calcResult.effective_rate * 100)]] as [string, string][]).map(([l, v]) => <div key={l} className="flex justify-between py-2 border-b"><dt className="text-slate-500">{l}</dt><dd className="font-semibold">{v}</dd></div>)}</dl></div></div>); })()}
            {!calcResult && !calcLoading && <div className="bg-white rounded-xl border p-16 text-center"><TrendingUp className="w-8 h-8 text-slate-300 mx-auto mb-3" /><p className="text-slate-700 font-semibold">Select a jurisdiction and calculate</p></div>}
          </div>
        )}

        {/* Rules Tab */}
        {tab === 'rules' && (
          <div className="space-y-4">
            {rules.length === 0 ? <div className="bg-white rounded-xl border p-16 text-center"><BookOpen className="w-8 h-8 text-slate-300 mx-auto mb-3" /><p className="text-slate-700 font-semibold">No rules found</p></div> : <>
              <p className="text-sm text-slate-500">{rules.length} active rule(s) for {jur?.name}</p>
              {rules.map(rule => (<div key={rule.id} className="bg-white rounded-xl border p-6"><div className="flex justify-between mb-3"><div><h3 className="text-sm font-bold">{rule.ruleName}</h3><p className="text-xs text-slate-500">{rule.ruleCode}</p></div>{rule.percentage && <span className="text-2xl font-bold text-blue-600">{rule.percentage}%</span>}{rule.fixedAmount && <span className="text-2xl font-bold text-blue-600">{fmt(rule.fixedAmount)}</span>}</div><div className="grid grid-cols-4 gap-4 text-xs mb-4">{rule.minSpend && <div><p className="text-slate-400">Min Spend</p><p className="font-semibold">{fmt(rule.minSpend)}</p></div>}{rule.maxCredit && <div><p className="text-slate-400">Max Credit</p><p className="font-semibold">{fmt(rule.maxCredit)}</p></div>}<div><p className="text-slate-400">Effective</p><p className="font-semibold">{rule.effectiveDate?.split('T')[0]}</p></div>{rule.expirationDate && <div><p className="text-slate-400">Expires</p><p className="font-semibold text-amber-700">{rule.expirationDate.split('T')[0]}</p></div>}</div><div className="flex flex-wrap gap-2">{rule.eligibleExpenses?.map(e => <span key={e} className="px-2 py-1 bg-emerald-50 text-emerald-700 rounded-full text-xs">{capitalize(e)}</span>)}</div></div>))}
            </>}
          </div>
        )}
      </div>
    </div>
  );
}
import { useState, useEffect } from 'react';
import { ExternalLink, Loader2, ChevronDown, ChevronUp, DollarSign, Percent, AlertCircle } from 'lucide-react';
import api from '../api';

// ─── Types ────────────────────────────────────────────────────────────────────

interface GaProgram {
  id: string;
  name: string;
  code: string;
  incentive_type: string;
  percentage: number;
  min_spend: number | null;
  max_credit: number | null;
  eligible_expenses: string[] | null;
  excluded_expenses: string[] | null;
  requirements: string[] | null;
  effective_date: string | null;
  active: boolean;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function fmt$(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function capitalize(s: string) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1).replace(/_/g, ' ') : s;
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function StatCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-white rounded-xl border border-slate-100 shadow-sm p-5">
      <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-1">{label}</p>
      <p className="text-3xl font-black text-slate-900 leading-none">{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-1.5">{sub}</p>}
    </div>
  );
}

function ProgramCard({ program }: { program: GaProgram }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-white rounded-xl border border-slate-100 shadow-sm overflow-hidden">
      <div
        className="flex items-center gap-4 px-5 py-4 cursor-pointer hover:bg-slate-50 transition-colors"
        onClick={() => setExpanded(e => !e)}
      >
        <div className="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center shrink-0">
          <span className="text-emerald-700 font-black text-lg">{program.percentage}%</span>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-bold text-slate-900 truncate">{program.name}</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            {program.code} &middot; {capitalize(program.incentive_type)}
            {program.min_spend != null && ` · Min spend ${fmt$(program.min_spend)}`}
            {program.max_credit != null && ` · Cap ${fmt$(program.max_credit)}`}
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide ${
            program.active ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'
          }`}>
            {program.active ? 'Active' : 'Inactive'}
          </span>
          {expanded
            ? <ChevronUp className="w-4 h-4 text-slate-400" />
            : <ChevronDown className="w-4 h-4 text-slate-400" />
          }
        </div>
      </div>

      {expanded && (
        <div className="border-t border-slate-100 px-5 py-4 space-y-4 bg-slate-50/50">
          {program.eligible_expenses && program.eligible_expenses.length > 0 && (
            <div>
              <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-2">Eligible Expenses</p>
              <div className="flex flex-wrap gap-1.5">
                {program.eligible_expenses.map(e => (
                  <span key={e} className="px-2.5 py-1 bg-blue-50 border border-blue-100 rounded-lg text-xs text-blue-700 font-medium">
                    {capitalize(e)}
                  </span>
                ))}
              </div>
            </div>
          )}

          {program.excluded_expenses && program.excluded_expenses.length > 0 && (
            <div>
              <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-2">Excluded Expenses</p>
              <div className="flex flex-wrap gap-1.5">
                {program.excluded_expenses.map(e => (
                  <span key={e} className="px-2.5 py-1 bg-red-50 border border-red-100 rounded-lg text-xs text-red-600 font-medium">
                    {capitalize(e)}
                  </span>
                ))}
              </div>
            </div>
          )}

          {program.requirements && program.requirements.length > 0 && (
            <div>
              <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-2">Requirements</p>
              <ul className="space-y-1">
                {program.requirements.map((req, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-600">
                    <span className="w-1.5 h-1.5 rounded-full bg-slate-400 mt-1.5 shrink-0" />
                    {req}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {program.effective_date && (
            <p className="text-xs text-slate-400">Effective: {new Date(program.effective_date).toLocaleDateString()}</p>
          )}
        </div>
      )}
    </div>
  );
}

// ─── Quick estimator ─────────────────────────────────────────────────────────

function Estimator({ programs }: { programs: GaProgram[] }) {
  const [budget, setBudget] = useState('');

  const activePrograms = programs.filter(p => p.active);
  const budgetNum = parseFloat(budget.replace(/[^0-9.]/g, '')) || 0;

  const estimates = activePrograms
    .filter(p => p.min_spend == null || budgetNum >= p.min_spend)
    .map(p => ({
      name: p.name,
      code: p.code,
      amount: Math.min(budgetNum * (p.percentage / 100), p.max_credit ?? Infinity),
      rate: p.percentage,
    }));

  const totalEstimate = estimates.reduce((sum, e) => sum + e.amount, 0);

  return (
    <div className="bg-white rounded-xl border border-slate-100 shadow-sm p-5">
      <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-3">Quick Estimator</p>

      <div className="relative mb-4">
        <DollarSign className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
        <input
          type="text"
          placeholder="Total budget"
          value={budget}
          onChange={e => setBudget(e.target.value)}
          className="w-full pl-8 pr-4 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {budgetNum > 0 ? (
        <div className="space-y-2">
          {estimates.length === 0 ? (
            <p className="text-xs text-slate-500 text-center py-2">Budget below minimum spend threshold for active programs.</p>
          ) : (
            <>
              {estimates.map(e => (
                <div key={e.code} className="flex items-center justify-between text-xs">
                  <span className="text-slate-600">{e.code} ({e.rate}%)</span>
                  <span className="font-bold text-emerald-700">{fmt$(e.amount)}</span>
                </div>
              ))}
              <div className="border-t border-slate-100 pt-2 flex items-center justify-between">
                <span className="text-xs font-bold text-slate-700">Est. Total Credit</span>
                <span className="text-base font-black text-emerald-700">{fmt$(totalEstimate)}</span>
              </div>
              <p className="text-[10px] text-slate-400 leading-relaxed">
                Estimate only. Actual credits depend on qualifying expenses and GDOT approval.
              </p>
            </>
          )}
        </div>
      ) : (
        <p className="text-xs text-slate-400 text-center py-2">Enter a budget to see estimated credits.</p>
      )}
    </div>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────

export default function Georgia() {
  const [programs, setPrograms]   = useState<GaProgram[]>([]);
  const [website, setWebsite]     = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError]         = useState<string | null>(null);

  useEffect(() => {
    api.georgia.getPrograms('GA')
      .then(res => {
        setPrograms(res.programs);
      })
      .catch(() => setError('Failed to load Georgia incentive data.'))
      .finally(() => setIsLoading(false));

    api.georgia.getJurisdiction('GA')
      .then(j => setWebsite(j.website))
      .catch(() => {});
  }, []);

  const activePrograms   = programs.filter(p => p.active);
  const bestRate         = activePrograms.reduce((max, p) => Math.max(max, p.percentage), 0);
  const minSpend         = activePrograms.reduce((min, p) => p.min_spend != null ? Math.min(min, p.min_spend) : min, Infinity);
  const totalPotential   = activePrograms.reduce((sum, p) => sum + p.percentage, 0);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-6 h-6 animate-spin text-blue-400" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <AlertCircle className="w-8 h-8 text-red-400 mx-auto mb-3" />
          <p className="text-slate-600 font-medium">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-6 h-full min-h-0">

      {/* ── Left panel ─────────────────────────────────────────── */}
      <div className="w-72 shrink-0 flex flex-col gap-4">

        {/* State badge */}
        <div className="bg-[#13151a] rounded-2xl p-5 text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-red-700 rounded-2xl flex items-center justify-center text-white font-black text-2xl mx-auto mb-3">
            GA
          </div>
          <h2 className="text-white font-bold text-lg">Georgia</h2>
          <p className="text-slate-400 text-xs mt-1">Film, Television &amp; Digital Entertainment</p>
          {website && (
            <a
              href={website}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 mt-3 text-xs text-blue-400 hover:text-blue-300 transition-colors"
            >
              <ExternalLink className="w-3 h-3" />
              Official Site
            </a>
          )}
        </div>

        {/* Stats */}
        <StatCard
          label="Base Credit Rate"
          value={`${bestRate}%`}
          sub="On qualified Georgia expenditures"
        />
        <StatCard
          label="Stackable Programs"
          value={`${activePrograms.length}`}
          sub={`Up to ${totalPotential}% combined potential`}
        />
        {minSpend < Infinity && (
          <StatCard
            label="Min Spend"
            value={fmt$(minSpend)}
            sub="Minimum qualifying expenditure"
          />
        )}

        {/* Estimator */}
        <Estimator programs={programs} />

        {/* Note */}
        <div className="flex items-start gap-2 px-1">
          <Percent className="w-3.5 h-3.5 text-slate-400 mt-0.5 shrink-0" />
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Georgia credits are transferable and may be sold. Consult a production accountant for application guidance.
          </p>
        </div>
      </div>

      {/* ── Main content ───────────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0 gap-4 overflow-y-auto">

        {/* Header */}
        <div>
          <h1 className="text-[28px] font-bold text-slate-900 tracking-tight leading-tight">
            Georgia Film Tax Credit
          </h1>
          <p className="text-slate-500 mt-1 text-[15px]">
            {activePrograms.length} active incentive program{activePrograms.length !== 1 ? 's' : ''} &middot; One of the most competitive production incentives in the US
          </p>
        </div>

        {/* Programs */}
        {programs.length === 0 ? (
          <div className="flex items-center justify-center h-48 bg-white rounded-xl border border-slate-100">
            <p className="text-slate-500 text-sm">No Georgia programs found in the database.</p>
          </div>
        ) : (
          <div className="space-y-3 pb-4">
            {programs.map(p => (
              <ProgramCard key={p.id} program={p} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

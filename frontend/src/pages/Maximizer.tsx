import { useState } from 'react';
import {
  Zap,
  MapPin,
  Hash,
  DollarSign,
  TrendingUp,
  AlertTriangle,
  ChevronRight,
  Loader2,
  Info,
} from 'lucide-react';
import api from '../api';
import type { MaximizeResult } from '../types';

// ── helpers ───────────────────────────────────────────────────────────────────

function fmtUSD(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toLocaleString()}`;
}

function fmtPct(n: number | null) {
  if (n === null) return '—';
  return `${(n * 100).toFixed(1)}%`;
}

const PROJECT_TYPES = [
  { value: 'film',        label: 'Feature Film' },
  { value: 'tv_series',   label: 'TV Series' },
  { value: 'commercial',  label: 'Commercial' },
  { value: 'documentary', label: 'Documentary' },
  { value: 'all',         label: 'All / Unknown' },
];

const RULE_TYPE_COLORS: Record<string, string> = {
  tax_credit:    'bg-emerald-100 text-emerald-700',
  rebate:        'bg-blue-100 text-blue-700',
  tax_abatement: 'bg-purple-100 text-purple-700',
  fee_waiver:    'bg-amber-100 text-amber-700',
  permit_fee:    'bg-red-100 text-red-700',
};

// ── component ─────────────────────────────────────────────────────────────────

type InputMode = 'latLng' | 'codes';

export default function Maximizer() {
  const [mode,          setMode]          = useState<InputMode>('codes');
  const [lat,           setLat]           = useState('');
  const [lng,           setLng]           = useState('');
  const [codesRaw,      setCodesRaw]      = useState('NY, NY-NYC');
  const [projectType,   setProjectType]   = useState('film');
  const [spendRaw,      setSpendRaw]      = useState('5000000');
  const [loading,       setLoading]       = useState(false);
  const [result,        setResult]        = useState<MaximizeResult | null>(null);
  const [error,         setError]         = useState<string | null>(null);

  const spendNum = parseFloat(spendRaw.replace(/[^0-9.]/g, '')) || undefined;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      const params: Parameters<typeof api.maximizer.maximize>[0] = {
        project_type: projectType,
        qualified_spend: spendNum,
      };

      if (mode === 'latLng') {
        const latN = parseFloat(lat);
        const lngN = parseFloat(lng);
        if (isNaN(latN) || isNaN(lngN)) {
          setError('Enter valid lat/lng coordinates.');
          setLoading(false);
          return;
        }
        params.lat = latN;
        params.lng = lngN;
      } else {
        const codes = codesRaw
          .split(/[\s,]+/)
          .map(s => s.trim().toUpperCase())
          .filter(Boolean);
        if (codes.length === 0) {
          setError('Enter at least one jurisdiction code.');
          setLoading(false);
          return;
        }
        params.jurisdiction_codes = codes;
      }

      const data = await api.maximizer.maximize(params);
      setResult(data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Unexpected error';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  const optInWarnings = result?.warnings.filter(w => w.includes('opt-in')) ?? [];
  const otherWarnings = result?.warnings.filter(w => !w.includes('opt-in')) ?? [];
  const nonZeroBreakdown = Object.entries(result?.breakdown ?? {}).filter(([, v]) => v !== 0);

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <Zap className="w-6 h-6 text-blue-600" />
          Incentive Maximizer
        </h1>
        <p className="text-slate-500 text-sm mt-1">
          Stack-optimize tax incentives across jurisdiction layers. Enter a location or explicit
          jurisdiction codes to see the best available package.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* ── Input Panel ── */}
        <form onSubmit={handleSubmit} className="lg:col-span-2 space-y-5">
          <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-5">

            {/* Mode toggle */}
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">
                Input Mode
              </p>
              <div className="flex rounded-lg border border-slate-200 overflow-hidden text-sm">
                <button
                  type="button"
                  onClick={() => setMode('codes')}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 font-medium transition-colors ${
                    mode === 'codes'
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <Hash className="w-3.5 h-3.5" />
                  Codes
                </button>
                <button
                  type="button"
                  onClick={() => setMode('latLng')}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 font-medium transition-colors ${
                    mode === 'latLng'
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <MapPin className="w-3.5 h-3.5" />
                  Lat / Lng
                </button>
              </div>
            </div>

            {/* Location inputs */}
            {mode === 'codes' ? (
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Jurisdiction Codes
                </label>
                <input
                  type="text"
                  value={codesRaw}
                  onChange={e => setCodesRaw(e.target.value)}
                  placeholder="e.g. NY, NY-NYC"
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-xs text-slate-400 mt-1">
                  Comma or space separated. Use parent + sub codes to stack (e.g. IL, IL-COOK).
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Latitude</label>
                  <input
                    type="number"
                    step="any"
                    value={lat}
                    onChange={e => setLat(e.target.value)}
                    placeholder="42.8864"
                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Longitude</label>
                  <input
                    type="number"
                    step="any"
                    value={lng}
                    onChange={e => setLng(e.target.value)}
                    placeholder="-78.8784"
                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            )}

            {/* Project type */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Project Type
              </label>
              <select
                value={projectType}
                onChange={e => setProjectType(e.target.value)}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              >
                {PROJECT_TYPES.map(pt => (
                  <option key={pt.value} value={pt.value}>{pt.label}</option>
                ))}
              </select>
            </div>

            {/* Qualified spend */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Qualified Spend (USD)
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  value={spendRaw}
                  onChange={e => setSpendRaw(e.target.value)}
                  placeholder="5000000"
                  className="w-full border border-slate-300 rounded-lg pl-8 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              {spendNum && (
                <p className="text-xs text-slate-400 mt-1">{fmtUSD(spendNum)}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold py-2.5 rounded-lg transition-colors text-sm"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Zap className="w-4 h-4" />
              )}
              {loading ? 'Calculating…' : 'Maximize Incentives'}
            </button>
          </div>

          {/* Quick presets */}
          <div className="bg-white rounded-xl border border-slate-200 p-4">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
              Quick Presets
            </p>
            <div className="space-y-1.5">
              {[
                { label: 'NYC — $5M Film',        codes: 'NY, NY-NYC',    spend: '5000000', type: 'film' },
                { label: 'Chicago — $5M Film',     codes: 'IL, IL-COOK',   spend: '5000000', type: 'film' },
                { label: 'Los Angeles — $5M Film', codes: 'CA, CA-LA',     spend: '5000000', type: 'film' },
                { label: 'Erie County — $5M Film', codes: 'NY, NY-ERIE',   spend: '5000000', type: 'film' },
              ].map(preset => (
                <button
                  key={preset.label}
                  type="button"
                  onClick={() => {
                    setMode('codes');
                    setCodesRaw(preset.codes);
                    setSpendRaw(preset.spend);
                    setProjectType(preset.type);
                  }}
                  className="w-full flex items-center justify-between px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 rounded-lg transition-colors group"
                >
                  <span>{preset.label}</span>
                  <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-slate-600" />
                </button>
              ))}
            </div>
          </div>
        </form>

        {/* ── Results Panel ── */}
        <div className="lg:col-span-3 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3">
              <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {!result && !loading && !error && (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-400">
              <Zap className="w-10 h-10 mx-auto mb-3 opacity-30" />
              <p className="text-sm">Enter location or jurisdiction codes and click Maximize.</p>
            </div>
          )}

          {loading && (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-400">
              <Loader2 className="w-8 h-8 mx-auto mb-3 animate-spin text-blue-500" />
              <p className="text-sm">Resolving jurisdictions and stacking rules…</p>
            </div>
          )}

          {result && !loading && (
            <>
              {/* Hero card */}
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 text-white">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-blue-200 text-sm font-medium mb-1">Maximum Incentive Package</p>
                    <p className="text-4xl font-bold tracking-tight">
                      {fmtUSD(result.total_incentive_usd)}
                    </p>
                    {result.effective_rate !== null && (
                      <p className="text-blue-200 text-sm mt-1 flex items-center gap-1">
                        <TrendingUp className="w-3.5 h-3.5" />
                        {fmtPct(result.effective_rate)} effective rate
                      </p>
                    )}
                  </div>
                  <div className="text-right text-sm text-blue-200 space-y-0.5">
                    {result.resolved_state && (
                      <p>State: <span className="text-white font-semibold">{result.resolved_state}</span></p>
                    )}
                    <p>Jurisdictions: <span className="text-white font-semibold">{result.jurisdictions_evaluated}</span></p>
                    {result.qualified_spend && (
                      <p>Spend: <span className="text-white font-semibold">{fmtUSD(result.qualified_spend)}</span></p>
                    )}
                  </div>
                </div>
              </div>

              {/* Applied rules */}
              {result.applied_rules.length > 0 && (
                <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
                  <div className="px-4 py-3 border-b border-slate-100">
                    <h3 className="text-sm font-semibold text-slate-700">Applied Rules</h3>
                  </div>
                  <div className="divide-y divide-slate-100">
                    {result.applied_rules.map((rule, i) => (
                      <div key={i} className="px-4 py-3 flex items-center gap-3">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-slate-800">{rule.rule_key}</p>
                          <p className="text-xs text-slate-400 truncate">{rule.jurisdiction_name}</p>
                        </div>
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${RULE_TYPE_COLORS[rule.rule_type] ?? 'bg-slate-100 text-slate-600'}`}>
                          {rule.rule_type.replace('_', ' ')}
                        </span>
                        <div className="text-right shrink-0">
                          <p className="text-sm font-semibold text-slate-900">
                            {fmtUSD(rule.computed_value)}
                          </p>
                          {rule.value_unit === 'percent' && (
                            <p className="text-xs text-slate-400">{rule.raw_value.toFixed(0)}%</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Breakdown */}
              {nonZeroBreakdown.length > 0 && (
                <div className="bg-white rounded-xl border border-slate-200 p-4">
                  <h3 className="text-sm font-semibold text-slate-700 mb-3">Breakdown by Category</h3>
                  <div className="space-y-2">
                    {nonZeroBreakdown.map(([cat, val]) => {
                      const total = result.total_incentive_usd || 1;
                      const pct = Math.abs(val / total) * 100;
                      return (
                        <div key={cat}>
                          <div className="flex justify-between text-xs text-slate-600 mb-1">
                            <span className="capitalize">{cat.replace('_', ' ')}</span>
                            <span className={val < 0 ? 'text-red-600' : 'font-medium'}>{fmtUSD(val)}</span>
                          </div>
                          <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${val < 0 ? 'bg-red-400' : 'bg-blue-500'}`}
                              style={{ width: `${Math.min(pct, 100)}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Opt-in upside */}
              {optInWarnings.length > 0 && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Info className="w-4 h-4 text-amber-600 shrink-0" />
                    <h3 className="text-sm font-semibold text-amber-800">Opt-In Upside Available</h3>
                  </div>
                  <p className="text-xs text-amber-700 mb-2">
                    These bonuses require a production-specific election and are excluded from the base total above.
                  </p>
                  <ul className="space-y-1">
                    {optInWarnings.map((w, i) => (
                      <li key={i} className="text-xs text-amber-700 flex items-start gap-1.5">
                        <span className="mt-0.5 shrink-0">→</span>
                        <span>{w.replace(' requires opt-in election — not included in base total', '')}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Other warnings */}
              {otherWarnings.length > 0 && (
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                  <h3 className="text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-slate-500" />
                    Notes
                  </h3>
                  <ul className="space-y-1">
                    {otherWarnings.map((w, i) => (
                      <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                        <span className="mt-0.5 shrink-0 text-slate-400">•</span>
                        <span>{w}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

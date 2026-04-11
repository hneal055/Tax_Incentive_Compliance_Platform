import { useState, useEffect } from 'react';
import {
  Layers, Plus, Trash2, Play, Trophy, AlertCircle,
  Loader2, ChevronDown, ChevronUp, ArrowRight
} from 'lucide-react';
import type { Jurisdiction } from '../types';
import api from '../api';
import apiClient from '../api/client';

// ── Types ─────────────────────────────────────────────────────────────────────

interface StackLayer {
  source: string;
  name: string;
  code: string;
  category: string;
  rule_type: string;
  rate: number | null;
  fixed_amount: number | null;
  incentive_value: number;
  notes: string | null;
}

interface StackResult {
  jurisdiction_code: string;
  jurisdiction_name: string;
  qualified_spend: number;
  layers: StackLayer[];
  total_incentive: number;
  effective_rate: number;
  warnings: string[];
}

interface ScenarioInput {
  jurisdiction_code: string;
  qualified_spend: number;
  local_hire_percent?: number;
  shooting_days?: number;
  production_start?: string;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const fmt = (n: number) =>
  n >= 1_000_000
    ? `$${(n / 1_000_000).toFixed(2)}M`
    : `$${n.toLocaleString()}`;

const pct = (n: number) => `${(n * 100).toFixed(1)}%`;

const SOURCE_STYLE: Record<string, string> = {
  state_incentive_rule: 'bg-blue-100 text-blue-700',
  local_rule:           'bg-purple-100 text-purple-700',
};

const SOURCE_LABEL: Record<string, string> = {
  state_incentive_rule: 'State',
  local_rule:           'Local',
};

// ── Scenario row ──────────────────────────────────────────────────────────────

function ScenarioRow({
  index,
  jurisdictions,
  onChange,
  onRemove,
  canRemove,
}: {
  index: number;
  jurisdictions: Jurisdiction[];
  onChange: (s: ScenarioInput) => void;
  onRemove: () => void;
  canRemove: boolean;
}) {
  const [jCode, setJCode] = useState('');
  const [spend, setSpend] = useState('');
  const [hire, setHire] = useState('');
  const [days, setDays] = useState('');
  const [startDate, setStartDate] = useState('');

  const emit = (overrides?: Partial<{ jCode: string; spend: string; hire: string; days: string; startDate: string }>) => {
    const s = { jCode, spend, hire, days, startDate, ...overrides };
    if (!s.jCode || !s.spend) return;
    onChange({
      jurisdiction_code: s.jCode,
      qualified_spend: parseFloat(s.spend) || 0,
      local_hire_percent: s.hire ? parseFloat(s.hire) : undefined,
      shooting_days: s.days ? parseInt(s.days) : undefined,
      production_start: s.startDate || undefined,
    });
  };

  return (
    <div className="border border-gray-200 rounded-xl p-4 bg-white space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">Scenario {index + 1}</span>
        {canRemove && (
          <button type="button" onClick={onRemove} className="text-gray-400 hover:text-red-500">
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        <div className="col-span-2 sm:col-span-1">
          <label className="block text-xs text-gray-500 mb-1">Jurisdiction</label>
          <select
            value={jCode}
            onChange={e => { setJCode(e.target.value); emit({ jCode: e.target.value }); }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select…</option>
            {jurisdictions.map(j => (
              <option key={j.id} value={j.code}>{j.name} ({j.code})</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs text-gray-500 mb-1">Qualified Spend ($)</label>
          <input
            type="number"
            min="0"
            placeholder="5000000"
            value={spend}
            onChange={e => { setSpend(e.target.value); emit({ spend: e.target.value }); }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-xs text-gray-500 mb-1">Local Hire %</label>
          <input
            type="number"
            min="0"
            max="100"
            placeholder="80"
            value={hire}
            onChange={e => { setHire(e.target.value); emit({ hire: e.target.value }); }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-xs text-gray-500 mb-1">Shooting Days</label>
          <input
            type="number"
            min="0"
            placeholder="60"
            value={days}
            onChange={e => { setDays(e.target.value); emit({ days: e.target.value }); }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-xs text-gray-500 mb-1">Production Start</label>
          <input
            type="date"
            value={startDate}
            onChange={e => { setStartDate(e.target.value); emit({ startDate: e.target.value }); }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  );
}

// ── Result card ───────────────────────────────────────────────────────────────

function ResultCard({ result, isBest }: { result: StackResult; isBest: boolean }) {
  const [expanded, setExpanded] = useState(isBest);

  return (
    <div className={`border rounded-xl overflow-hidden ${isBest ? 'border-green-400 shadow-md' : 'border-gray-200'}`}>
      {/* Header */}
      <div className={`px-4 py-3 flex items-center gap-3 ${isBest ? 'bg-green-50' : 'bg-white'}`}>
        {isBest && <Trophy className="w-5 h-5 text-green-500 shrink-0" />}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-gray-900">{result.jurisdiction_name}</span>
            <span className="text-xs text-gray-400">{result.jurisdiction_code}</span>
            {isBest && <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">Best Stack</span>}
          </div>
          <div className="flex items-center gap-4 mt-0.5 text-sm">
            <span className="font-bold text-green-700">{fmt(result.total_incentive)}</span>
            <span className="text-gray-500">{pct(result.effective_rate)} effective rate</span>
            <span className="text-gray-400">{result.layers.length} layer{result.layers.length !== 1 ? 's' : ''}</span>
          </div>
        </div>
        <button
          type="button"
          onClick={() => setExpanded(e => !e)}
          className="text-gray-400 hover:text-gray-600"
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {expanded && (
        <div className="border-t border-gray-100 bg-gray-50 divide-y divide-gray-100">
          {/* Layers */}
          {result.layers.map((layer, i) => (
            <div key={i} className="px-4 py-2.5 flex items-center gap-3">
              <span className={`px-2 py-0.5 rounded text-xs font-medium shrink-0 ${SOURCE_STYLE[layer.source] ?? 'bg-gray-100 text-gray-600'}`}>
                {SOURCE_LABEL[layer.source] ?? layer.source}
              </span>
              <div className="flex-1 min-w-0">
                <span className="text-sm text-gray-800">{layer.name}</span>
                {layer.notes && <span className="text-xs text-gray-400 ml-2">{layer.notes}</span>}
              </div>
              <div className="text-right shrink-0">
                <span className="text-sm font-medium text-gray-900">{fmt(layer.incentive_value)}</span>
                {layer.rate && <span className="text-xs text-gray-400 ml-1">({layer.rate}%)</span>}
              </div>
            </div>
          ))}

          {/* Total */}
          <div className="px-4 py-2.5 flex items-center justify-between bg-white">
            <span className="text-sm font-semibold text-gray-700">Total Incentive</span>
            <span className="text-base font-bold text-green-700">{fmt(result.total_incentive)}</span>
          </div>

          {/* Warnings */}
          {result.warnings.length > 0 && (
            <div className="px-4 py-3 space-y-1">
              {result.warnings.map((w, i) => (
                <div key={i} className="flex items-start gap-2 text-xs text-amber-700">
                  <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                  {w}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function ScenarioCalculator() {
  const [jurisdictions, setJurisdictions] = useState<Jurisdiction[]>([]);
  const [scenarios, setScenarios] = useState<(ScenarioInput | null)[]>([null, null]);
  const [results, setResults] = useState<{ scenarios: StackResult[]; best_jurisdiction: string | null; best_total_incentive: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.jurisdictions.list().then(res => setJurisdictions(res)).catch(() => {});
  }, []);

  const handleChange = (i: number, s: ScenarioInput) => {
    setScenarios(prev => { const next = [...prev]; next[i] = s; return next; });
    setResults(null);
  };

  const handleRemove = (i: number) => {
    setScenarios(prev => prev.filter((_, idx) => idx !== i));
    setResults(null);
  };

  const handleAdd = () => {
    if (scenarios.length < 6) setScenarios(prev => [...prev, null]);
  };

  const handleCalculate = async () => {
    const valid = scenarios.filter((s): s is ScenarioInput => s !== null && s.jurisdiction_code !== '' && s.qualified_spend > 0);
    if (valid.length < 2) {
      setError('Fill in at least 2 scenarios to compare');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await apiClient.post('/stacking-engine/compare', { scenarios: valid });
      setResults(res.data);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Calculation failed';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const validCount = scenarios.filter(s => s && s.jurisdiction_code && s.qualified_spend > 0).length;

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Layers className="w-6 h-6 text-blue-600" />
        <div>
          <h1 className="text-xl font-bold text-gray-900">Scenario Calculator</h1>
          <p className="text-sm text-gray-500">
            Compare state + local incentive stacks across jurisdictions
          </p>
        </div>
      </div>

      {/* Scenario inputs */}
      <div className="space-y-3">
        {scenarios.map((_, i) => (
          <ScenarioRow
            key={i}
            index={i}
            jurisdictions={jurisdictions}
            onChange={s => handleChange(i, s)}
            onRemove={() => handleRemove(i)}
            canRemove={scenarios.length > 2}
          />
        ))}

        <div className="flex gap-3">
          {scenarios.length < 6 && (
            <button
              type="button"
              onClick={handleAdd}
              className="flex items-center gap-2 px-4 py-2 rounded-lg border border-dashed border-gray-300 text-sm text-gray-500 hover:border-blue-400 hover:text-blue-600"
            >
              <Plus className="w-4 h-4" /> Add scenario
            </button>
          )}
          <button
            type="button"
            onClick={handleCalculate}
            disabled={loading || validCount < 2}
            className="flex items-center gap-2 px-5 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed ml-auto"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            {loading ? 'Calculating…' : 'Compare Stacks'}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          <AlertCircle className="w-4 h-4 shrink-0" /> {error}
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <ArrowRight className="w-4 h-4" />
            Best jurisdiction: <strong className="text-gray-900">{results.best_jurisdiction}</strong>
          </div>
          <div className="space-y-3">
            {results.scenarios.map((r, i) => (
              <ResultCard
                key={i}
                result={r}
                isBest={r.jurisdiction_code === results.best_jurisdiction}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

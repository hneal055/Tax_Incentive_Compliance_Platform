import { useState, useEffect } from 'react';
import {
  BookOpen, Search, Filter, ExternalLink, CheckCircle,
  AlertCircle, Loader2, RefreshCw, Bot, User, ChevronDown, ChevronUp
} from 'lucide-react';
import type { LocalRule } from '../types';
import { localRulesApi } from '../api';

// ── Constants ─────────────────────────────────────────────────────────────────

const CATEGORY_COLORS: Record<string, string> = {
  permit_fee:       'bg-blue-100 text-blue-700',
  business_license: 'bg-purple-100 text-purple-700',
  filming_tax:      'bg-orange-100 text-orange-700',
  wage_requirement: 'bg-pink-100 text-pink-700',
  incentive:        'bg-green-100 text-green-700',
  restriction:      'bg-red-100 text-red-700',
  other:            'bg-gray-100 text-gray-600',
};

const RULE_TYPE_COLORS: Record<string, string> = {
  fee:         'bg-amber-100 text-amber-700',
  tax:         'bg-red-100 text-red-700',
  requirement: 'bg-blue-100 text-blue-700',
  restriction: 'bg-rose-100 text-rose-700',
  credit:      'bg-green-100 text-green-700',
  exemption:   'bg-teal-100 text-teal-700',
};

const CATEGORIES = [
  '', 'permit_fee', 'business_license', 'filming_tax',
  'wage_requirement', 'incentive', 'restriction', 'other',
];

// ── Rule row ──────────────────────────────────────────────────────────────────

function RuleRow({ rule }: { rule: LocalRule }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="border border-gray-200 rounded-xl bg-white overflow-hidden">
      <div className="flex items-center gap-3 px-4 py-3">
        <button
          type="button"
          onClick={() => setExpanded(e => !e)}
          className="text-gray-400 hover:text-gray-600 shrink-0"
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-medium text-gray-900 text-sm">{rule.name}</span>
            <span className="text-xs text-gray-400 font-mono">{rule.code}</span>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${CATEGORY_COLORS[rule.category] ?? CATEGORY_COLORS.other}`}>
              {rule.category.replace(/_/g, ' ')}
            </span>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${RULE_TYPE_COLORS[rule.ruleType] ?? 'bg-gray-100 text-gray-600'}`}>
              {rule.ruleType}
            </span>
          </div>

          <div className="flex items-center gap-3 mt-0.5 text-xs text-gray-500 flex-wrap">
            <span className="font-medium text-gray-700">
              {rule.jurisdiction?.name ?? rule.jurisdictionId}
            </span>
            {rule.amount != null && (
              <span>${rule.amount.toLocaleString()}</span>
            )}
            {rule.percentage != null && (
              <span>{rule.percentage}%</span>
            )}
            <span>Effective {new Date(rule.effectiveDate).toLocaleDateString()}</span>
            {rule.expirationDate && (
              <span className="text-amber-600">Expires {new Date(rule.expirationDate).toLocaleDateString()}</span>
            )}
            <span className="flex items-center gap-1">
              {rule.extractedBy === 'claude'
                ? <><Bot className="w-3 h-3 text-purple-500" /> AI extracted</>
                : <><User className="w-3 h-3 text-gray-400" /> Manual</>}
            </span>
          </div>
        </div>

        <CheckCircle className="w-4 h-4 text-green-500 shrink-0" />
      </div>

      {expanded && (
        <div className="border-t border-gray-100 px-4 py-3 bg-gray-50 space-y-2 text-sm">
          <p className="text-gray-700">{rule.description}</p>
          {rule.requirements && (
            <p className="text-gray-500 italic text-xs">{rule.requirements}</p>
          )}
          {rule.sourceUrl && (
            <a
              href={rule.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-xs text-blue-600 hover:underline"
            >
              <ExternalLink className="w-3 h-3" /> Source
            </a>
          )}
        </div>
      )}
    </div>
  );
}

// ── Stats bar ─────────────────────────────────────────────────────────────────

function StatsBar({ stats }: { stats: { total: number; active: number; bySource: { extractedBy: string; count: number }[] } | null }) {
  if (!stats) return null;
  const aiCount = stats.bySource.find(s => s.extractedBy === 'claude')?.count ?? 0;
  const manualCount = stats.bySource.find(s => s.extractedBy === 'manual')?.count ?? 0;

  return (
    <div className="grid grid-cols-3 gap-3">
      {[
        { label: 'Total Rules', value: stats.total, color: 'text-gray-900' },
        { label: 'AI Extracted', value: aiCount, color: 'text-purple-600' },
        { label: 'Manual', value: manualCount, color: 'text-gray-600' },
      ].map(({ label, value, color }) => (
        <div key={label} className="bg-white border border-gray-200 rounded-xl p-4 text-center">
          <div className={`text-2xl font-bold ${color}`}>{value}</div>
          <div className="text-xs text-gray-500 mt-0.5">{label}</div>
        </div>
      ))}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function LocalRules() {
  const [rules, setRules] = useState<LocalRule[]>([]);
  const [stats, setStats] = useState<{ total: number; active: number; bySource: { extractedBy: string; count: number }[] } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const [rulesRes, statsRes] = await Promise.all([
        localRulesApi.list({ category: categoryFilter || undefined }),
        localRulesApi.stats(),
      ]);
      setRules(rulesRes.rules);
      setStats(statsRes);
    } catch {
      setError('Failed to load local rules');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [categoryFilter]);

  const filtered = rules.filter(r => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      r.name.toLowerCase().includes(q) ||
      r.code.toLowerCase().includes(q) ||
      r.description.toLowerCase().includes(q) ||
      (r.jurisdiction?.name ?? '').toLowerCase().includes(q)
    );
  });

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <BookOpen className="w-6 h-6 text-blue-600" />
          <div>
            <h1 className="text-xl font-bold text-gray-900">Local Rules</h1>
            <p className="text-sm text-gray-500">
              Approved county, city &amp; district-level incentives and requirements
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={load}
          className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-300 text-sm text-gray-600 hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </div>

      {/* Stats */}
      <StatsBar stats={stats} />

      {/* Filters */}
      <div className="flex gap-3 flex-wrap">
        <div className="relative flex-1 min-w-48">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search rules, jurisdictions…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <select
            value={categoryFilter}
            onChange={e => setCategoryFilter(e.target.value)}
            className="pl-9 pr-8 py-2 border border-gray-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none"
          >
            {CATEGORIES.map(c => (
              <option key={c} value={c}>
                {c ? c.replace(/_/g, ' ') : 'All categories'}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center py-20 text-gray-400">
          <Loader2 className="w-6 h-6 animate-spin mr-2" /> Loading…
        </div>
      ) : error ? (
        <div className="flex items-center gap-2 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          <AlertCircle className="w-4 h-4 shrink-0" /> {error}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          <BookOpen className="w-10 h-10 mx-auto mb-3 opacity-30" />
          <p className="text-sm">
            {rules.length === 0
              ? 'No local rules yet. Approve pending rules to populate this list.'
              : 'No rules match your search.'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <p className="text-xs text-gray-400">{filtered.length} rule{filtered.length !== 1 ? 's' : ''}</p>
          {filtered.map(rule => (
            <RuleRow key={rule.id} rule={rule} />
          ))}
        </div>
      )}
    </div>
  );
}

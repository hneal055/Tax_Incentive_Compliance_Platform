import { useState, useMemo } from 'react';
import { Search, RefreshCw, Bookmark, ChevronDown, X } from 'lucide-react';
import type { Production } from '../types';

interface JurisdictionsProps {
  productions?: Production[];
  onAddProduction?: (production: Production) => void;
  onUpdateProduction?: (production: Production) => void;
  onDeleteProduction?: (id: string) => void;
}

// ─── Static data ────────────────────────────────────────────────────────────

const FEED_ITEMS = [
  {
    agency: 'California Film Commission',
    time: '2h ago',
    text: 'Proposed expansion of the 30-mile studio zone currently under committee review.',
  },
  {
    agency: 'British Film Commission',
    time: '5h ago',
    text: 'New guidance issued for VFX expenditure qualification under updates.',
  },
  {
    agency: 'Georgia Dept. of Econ Dev',
    time: '1d ago',
    text: 'Fiscal year cap status: 65% utilized. Applications open.',
  },
];

const JURISDICTIONS = [
  { id: '1', regionCode: 'US', name: 'Georgia',        baseRate: 20, agency: 'Georgia Department of Commerce',   minSpend: '$500k',   type: 'State',    country: 'United States' },
  { id: '2', regionCode: 'US', name: 'California',     baseRate: 25, agency: 'California Film Commission',       minSpend: '$1,000k', type: 'State',    country: 'United States' },
  { id: '3', regionCode: 'US', name: 'New York',       baseRate: 30, agency: "Governor's Office of Motion Pic.", minSpend: '$0k',     type: 'State',    country: 'United States' },
  { id: '4', regionCode: 'GB', name: 'United Kingdom', baseRate: 25, agency: 'British Film Commission',          minSpend: '$0k',     type: 'Country',  country: 'United Kingdom' },
  { id: '5', regionCode: 'CA', name: 'Ontario',        baseRate: 35, agency: 'Ontario Creates',                 minSpend: '$100k',   type: 'Province', country: 'Canada' },
  { id: '6', regionCode: 'US', name: 'Louisiana',      baseRate: 25, agency: 'Louisiana Entertainment',         minSpend: '$300k',   type: 'State',    country: 'United States' },
];

const ALL_TYPES    = ['All Types',    'State', 'Province', 'Country'];
const ALL_COUNTRIES = ['All Countries', 'United States', 'Canada', 'United Kingdom'];

// ─── Sub-components ──────────────────────────────────────────────────────────

function FilterDropdown({ value, options, onChange }: { value: string; options: string[]; onChange: (v: string) => void }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:border-slate-300 transition-colors shadow-sm"
      >
        {value}
        <ChevronDown className="w-4 h-4 text-slate-400" />
      </button>
      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute top-full mt-1 left-0 bg-white border border-slate-200 rounded-lg shadow-lg z-20 min-w-[160px] py-1">
            {options.map(opt => (
              <button
                key={opt}
                type="button"
                onClick={() => { onChange(opt); setOpen(false); }}
                className={`w-full text-left px-4 py-2 text-sm transition-colors ${value === opt ? 'text-blue-600 font-semibold' : 'text-slate-700 hover:bg-slate-50'}`}
              >
                {opt}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function Toast({ message, onClose }: { message: string; onClose: () => void }) {
  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-3 bg-slate-900 text-white px-5 py-3 rounded-xl shadow-xl text-sm font-medium animate-in">
      <span>{message}</span>
      <button type="button" onClick={onClose} title="Dismiss" aria-label="Dismiss notification" className="text-slate-400 hover:text-white transition-colors">
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}

// ─── Main component ──────────────────────────────────────────────────────────

export default function Jurisdictions({ onAddProduction }: JurisdictionsProps) {
  const [search, setSearch]           = useState('');
  const [typeFilter, setTypeFilter]   = useState('All Types');
  const [countryFilter, setCountry]   = useState('All Countries');
  const [selectedId, setSelectedId]   = useState<string | null>(null);
  const [savedIds, setSavedIds]       = useState<Set<string>>(new Set());
  const [toast, setToast]             = useState<string | null>(null);

  function showToast(msg: string) {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  }

  function toggleSave(id: string, e: React.MouseEvent) {
    e.stopPropagation();
    setSavedIds(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  function handleAddToProduction(j: typeof JURISDICTIONS[0], e: React.MouseEvent) {
    e.stopPropagation();
    if (onAddProduction) {
      const now = new Date().toISOString();
      onAddProduction({ id: `jur-${j.id}-${Date.now()}`, title: `${j.name} Production`, budget: 0, jurisdiction_id: j.id, created_at: now, updated_at: now });
    }
    showToast(`${j.name} added to production`);
  }

  function handleReview(j: typeof JURISDICTIONS[0], e: React.MouseEvent) {
    e.stopPropagation();
    showToast(`Opening ${j.name} incentive profile…`);
  }

  function handleRefresh() {
    showToast('Jurisdiction data refreshed');
  }

  const filtered = useMemo(() => JURISDICTIONS.filter(j => {
    const matchType    = typeFilter    === 'All Types'     || j.type    === typeFilter;
    const matchCountry = countryFilter === 'All Countries' || j.country === countryFilter;
    const matchSearch  = !search.trim() || j.name.toLowerCase().includes(search.toLowerCase()) || j.agency.toLowerCase().includes(search.toLowerCase());
    return matchType && matchCountry && matchSearch;
  }), [search, typeFilter, countryFilter]);

  return (
    <div className="flex gap-6 h-full min-h-0">

      {/* ── Left panel ────────────────────────────────────────── */}
      <div className="w-72 shrink-0 flex flex-col gap-4">

        {/* Regulatory Feed */}
        <div className="bg-[#13151a] rounded-2xl overflow-hidden flex flex-col">
          <div className="flex items-center gap-2.5 px-5 py-4 border-b border-white/8">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75" />
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500" />
            </span>
            <span className="text-white text-xs font-bold tracking-widest uppercase">Regulatory Feed</span>
          </div>

          <div className="divide-y divide-white/8">
            {FEED_ITEMS.map((item, i) => (
              <div key={i} className="px-5 py-4 hover:bg-white/4 transition-colors cursor-pointer">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-blue-400 text-xs font-semibold">{item.agency}</span>
                  <span className="text-slate-500 text-xs">{item.time}</span>
                </div>
                <p className="text-slate-400 text-xs leading-relaxed">{item.text}</p>
              </div>
            ))}
          </div>

          <div className="px-5 py-3 text-center">
            <span className="text-slate-600 text-[11px] tracking-widest uppercase font-medium">Global Monitoring Active</span>
          </div>
        </div>

        {/* Agency Directory */}
        <div className="bg-indigo-50 border border-indigo-100 rounded-2xl p-5">
          <div className="flex items-center gap-2.5 mb-2">
            <div className="w-7 h-7 bg-indigo-100 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
              </svg>
            </div>
            <span className="text-indigo-700 font-bold text-sm">Agency Directory</span>
          </div>
          <p className="text-indigo-500 text-xs leading-relaxed mb-4">
            PilotForge connects with over 400 jurisdictions globally. Contact our concierge for help with custom applications.
          </p>
          <button
            type="button"
            className="w-full py-2 border border-indigo-300 rounded-lg text-indigo-600 text-sm font-semibold hover:bg-indigo-100 transition-colors"
          >
            Contact Concierge
          </button>
        </div>
      </div>

      {/* ── Main content ───────────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0">

        {/* Header */}
        <div className="mb-5">
          <h1 className="text-[28px] font-bold text-slate-900 tracking-tight leading-tight">
            Jurisdiction Intelligence
          </h1>
          <p className="text-slate-500 mt-1 text-[15px]">
            Explore and filter international tax incentive profiles.
          </p>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3 mb-5">
          <FilterDropdown value={typeFilter}    options={ALL_TYPES}     onChange={setTypeFilter} />
          <FilterDropdown value={countryFilter} options={ALL_COUNTRIES} onChange={setCountry}    />

          <div className="flex-1 relative">
            <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search by name or agency..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
            />
          </div>

          <button
            type="button"
            onClick={handleRefresh}
            title="Refresh"
            aria-label="Refresh jurisdictions"
            className="p-2 bg-white border border-slate-200 rounded-lg text-slate-500 hover:text-slate-700 hover:border-slate-300 transition-colors shadow-sm"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>

        {/* Grid */}
        {filtered.length === 0 ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <p className="text-slate-500 font-medium">No jurisdictions match your filters.</p>
              <button
                type="button"
                onClick={() => { setSearch(''); setTypeFilter('All Types'); setCountry('All Countries'); }}
                className="mt-3 text-blue-600 text-sm hover:underline"
              >
                Clear filters
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 overflow-y-auto pb-2">
            {filtered.map(j => {
              const isSelected = selectedId === j.id;
              const isSaved    = savedIds.has(j.id);
              return (
                <div
                  key={j.id}
                  onClick={() => setSelectedId(prev => prev === j.id ? null : j.id)}
                  className={`bg-white rounded-xl border-2 p-5 cursor-pointer flex flex-col gap-3 transition-all duration-150
                    ${isSelected
                      ? 'border-blue-500 shadow-md shadow-blue-100'
                      : 'border-slate-100 hover:border-blue-300 hover:shadow-md hover:shadow-slate-100'
                    }`}
                >
                  {/* Card header */}
                  <div className="flex items-start gap-3">
                    <span className="text-slate-400 text-sm font-semibold mt-1 shrink-0">{j.regionCode}</span>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-xl font-bold text-slate-900 leading-tight">{j.name}</h3>
                    </div>
                    <span className="shrink-0 px-2 py-0.5 bg-emerald-500 text-white text-[11px] font-bold rounded-md tracking-wide">
                      {j.baseRate}% BASE
                    </span>
                  </div>

                  {/* Details */}
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <span className="text-slate-400 text-xs w-16 shrink-0">Agency</span>
                      <span className="text-slate-700 text-xs font-semibold truncate">{j.agency}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-slate-400 text-xs w-16 shrink-0">Min Spend</span>
                      <span className="text-slate-700 text-xs font-semibold">{j.minSpend}</span>
                    </div>
                  </div>

                  {/* Divider */}
                  <div className="border-t border-slate-100" />

                  {/* Actions */}
                  <div className="flex items-center justify-between">
                    <button
                      type="button"
                      onClick={(e) => handleReview(j, e)}
                      className="flex items-center gap-1 text-[11px] font-bold text-slate-400 hover:text-slate-600 uppercase tracking-widest transition-colors"
                    >
                      Review
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                      </svg>
                    </button>

                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={(e) => handleAddToProduction(j, e)}
                        className="flex items-center gap-1 text-[11px] font-bold text-blue-600 hover:text-blue-700 uppercase tracking-widest transition-colors"
                      >
                        Add to Production
                      </button>
                      <button
                        type="button"
                        onClick={(e) => toggleSave(j.id, e)}
                        title={isSaved ? 'Remove bookmark' : 'Bookmark'}
                        aria-label={isSaved ? 'Remove bookmark' : 'Bookmark'}
                        className={`transition-colors ${isSaved ? 'text-blue-600' : 'text-slate-300 hover:text-slate-500'}`}
                      >
                        <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-blue-600' : ''}`} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Toast */}
      {toast && <Toast message={toast} onClose={() => setToast(null)} />}
    </div>
  );
}

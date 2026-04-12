import { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import {
  Zap, MapPin, Hash, DollarSign, TrendingUp, AlertTriangle,
  ChevronRight, Loader2, Info, SplitSquareHorizontal, Bookmark,
  BookmarkCheck, Trash2, Download, BarChart3, ClipboardList,
  GitCompare, Plus, X, ExternalLink,
} from 'lucide-react';
import api from '../api';
import type { MaximizeResult, ChecklistResponse } from '../types';

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

const REQ_CATEGORY_COLORS: Record<string, string> = {
  permit:       'bg-orange-100 text-orange-700',
  insurance:    'bg-blue-100 text-blue-700',
  registration: 'bg-purple-100 text-purple-700',
  notification: 'bg-yellow-100 text-yellow-700',
  bond:         'bg-red-100 text-red-700',
  other:        'bg-slate-100 text-slate-600',
};

// ── types ─────────────────────────────────────────────────────────────────────

type InputMode = 'latLng' | 'codes';
type PageMode  = 'maximize' | 'compare';
type ResultTab = 'incentives' | 'requirements';

interface SavedScenario {
  id: string;
  name: string;
  codes: string;
  spend: string;
  type: string;
  splitSpend: Record<string, string>;
  savedAt: string;
}

interface CompareSlot {
  id: string;
  label: string;
  codes: string;
  spend: string;
  type: string;
  result: MaximizeResult | null;
  loading: boolean;
  error: string | null;
}

// ── localStorage helpers ──────────────────────────────────────────────────────

const LS_KEY = 'pilotforge_scenarios';

function loadScenarios(): SavedScenario[] {
  try { return JSON.parse(localStorage.getItem(LS_KEY) || '[]'); }
  catch { return []; }
}
function saveScenarios(list: SavedScenario[]) {
  localStorage.setItem(LS_KEY, JSON.stringify(list));
}

// ── sub-components ────────────────────────────────────────────────────────────

/** Leaflet map rendered in lat/lng mode */
function LatLngMap({ lat, lng, onPick }: {
  lat: string;
  lng: string;
  onPick: (lat: string, lng: string) => void;
}) {
  const mapRef = useRef<HTMLDivElement>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const leafletMap = useRef<any>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const marker = useRef<any>(null);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const L = (window as any).L;

  useEffect(() => {
    if (!mapRef.current || !L) return;
    if (leafletMap.current) return; // already initialised

    const initLat = parseFloat(lat) || 40.7128;
    const initLng = parseFloat(lng) || -74.006;

    leafletMap.current = L.map(mapRef.current).setView([initLat, initLng], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(leafletMap.current);

    // draggable marker
    marker.current = L.marker([initLat, initLng], { draggable: true })
      .addTo(leafletMap.current);
    marker.current.on('dragend', () => {
      const pos = marker.current.getLatLng();
      onPick(pos.lat.toFixed(6), pos.lng.toFixed(6));
    });

    // click to move marker
    leafletMap.current.on('click', (e: { latlng: { lat: number; lng: number } }) => {
      marker.current.setLatLng([e.latlng.lat, e.latlng.lng]);
      onPick(e.latlng.lat.toFixed(6), e.latlng.lng.toFixed(6));
    });

    return () => {
      leafletMap.current?.remove();
      leafletMap.current = null;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [L]);

  // Keep marker in sync when lat/lng inputs change manually
  useEffect(() => {
    const latN = parseFloat(lat);
    const lngN = parseFloat(lng);
    if (!isNaN(latN) && !isNaN(lngN) && marker.current) {
      marker.current.setLatLng([latN, lngN]);
      leafletMap.current?.panTo([latN, lngN]);
    }
  }, [lat, lng]);

  return (
    <div
      ref={mapRef}
      className="relative w-full h-48 rounded-lg border border-slate-200 overflow-hidden z-0"
    />
  );
}

/** Single column card in Compare view */
function CompareColumn({
  slot, index, total, onChange, onRemove, onRun,
}: {
  slot: CompareSlot;
  index: number;
  total: number;
  onChange: (id: string, field: keyof CompareSlot, value: string) => void;
  onRemove: (id: string) => void;
  onRun: (id: string) => void;
}) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-100 bg-slate-50">
        <input
          value={slot.label}
          onChange={e => onChange(slot.id, 'label', e.target.value)}
          className="flex-1 text-sm font-semibold text-slate-700 bg-transparent border-none outline-none"
          placeholder={`Market ${index + 1}`}
        />
        {total > 2 && (
          <button type="button" aria-label="Remove market" onClick={() => onRemove(slot.id)} className="text-slate-400 hover:text-red-400 transition-colors">
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Inputs */}
      <div className="p-3 space-y-2 border-b border-slate-100">
        <input
          value={slot.codes}
          onChange={e => onChange(slot.id, 'codes', e.target.value)}
          placeholder="Jurisdiction codes (e.g. IL, IL-COOK)"
          className="w-full border border-slate-200 rounded px-2.5 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
        <div className="flex gap-2">
          <div className="relative flex-1">
            <DollarSign className="absolute left-2 top-1/2 -translate-y-1/2 w-3 h-3 text-slate-400" />
            <input
              value={slot.spend}
              onChange={e => onChange(slot.id, 'spend', e.target.value)}
              placeholder="Spend"
              className="w-full border border-slate-200 rounded pl-6 pr-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <select
            aria-label="Project type"
            value={slot.type}
            onChange={e => onChange(slot.id, 'type', e.target.value)}
            className="border border-slate-200 rounded px-1.5 py-1.5 text-xs bg-white focus:outline-none"
          >
            {PROJECT_TYPES.map(pt => (
              <option key={pt.value} value={pt.value}>{pt.label}</option>
            ))}
          </select>
        </div>
        <button
          type="button"
          onClick={() => onRun(slot.id)}
          disabled={slot.loading}
          className="w-full flex items-center justify-center gap-1.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs font-medium py-1.5 rounded transition-colors"
        >
          {slot.loading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Zap className="w-3 h-3" />}
          {slot.loading ? 'Running…' : 'Run'}
        </button>
      </div>

      {/* Result */}
      <div className="flex-1 p-3">
        {slot.error && (
          <p className="text-xs text-red-600">{slot.error}</p>
        )}
        {!slot.result && !slot.loading && !slot.error && (
          <p className="text-xs text-slate-400 text-center py-4">No result yet</p>
        )}
        {slot.result && (
          <div className="space-y-3">
            {/* Hero */}
            <div className="bg-blue-600 rounded-lg p-3 text-white">
              <p className="text-blue-200 text-xs mb-0.5">Max Incentive</p>
              <p className="text-2xl font-bold">{fmtUSD(slot.result.total_incentive_usd)}</p>
              {slot.result.effective_rate !== null && (
                <p className="text-blue-200 text-xs mt-0.5 flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" />
                  {fmtPct(slot.result.effective_rate)} effective rate
                </p>
              )}
            </div>
            {/* Rules */}
            <div className="space-y-1">
              {slot.result.applied_rules.map((r, i) => (
                <div key={i} className="flex items-center justify-between text-xs">
                  <span className="text-slate-600 truncate flex-1 mr-2">{r.rule_key}</span>
                  <span className="text-slate-900 font-medium shrink-0">{fmtUSD(r.computed_value)}</span>
                </div>
              ))}
            </div>
            {/* Opt-in */}
            {slot.result.warnings.some(w => w.includes('opt-in')) && (
              <div className="bg-amber-50 border border-amber-200 rounded p-2">
                <p className="text-xs font-medium text-amber-700 mb-1">Opt-in upside:</p>
                {slot.result.warnings.filter(w => w.includes('opt-in')).map((w, i) => (
                  <p key={i} className="text-xs text-amber-600">
                    +{w.match(/\$[\d,]+/)?.[0] ?? '?'}
                  </p>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/** Compliance requirements panel — shown in "Requirements" results tab */
function RequirementsPanel({ codes, projectType }: { codes: string[]; projectType: string }) {
  const [data, setData] = useState<Record<string, ChecklistResponse>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (codes.length === 0) return;
    setLoading(true);
    setError(null);
    Promise.all(
      codes.map(code =>
        api.requirements.getChecklist(code, projectType)
          .then(r => ({ code, r }))
          .catch(() => ({ code, r: null }))
      )
    ).then(results => {
      const map: Record<string, ChecklistResponse> = {};
      for (const { code, r } of results) if (r) map[code] = r;
      setData(map);
    }).catch(e => setError(String(e)))
     .finally(() => setLoading(false));
  }, [codes.join(','), projectType]); // eslint-disable-line

  if (loading) return (
    <div className="py-8 text-center text-slate-400 text-sm">
      <Loader2 className="w-5 h-5 mx-auto mb-2 animate-spin" />
      Loading requirements…
    </div>
  );

  if (error) return (
    <p className="text-xs text-red-600 p-4">{error}</p>
  );

  const allItems = Object.values(data).flatMap(d => d.requirements);

  if (allItems.length === 0) return (
    <div className="py-8 text-center text-slate-400 text-sm">
      <ClipboardList className="w-8 h-8 mx-auto mb-2 opacity-30" />
      <p>No compliance requirements on record for these jurisdictions.</p>
      <p className="text-xs mt-1">Requirements are populated from government feeds via monitor.py.</p>
    </div>
  );

  // Group by category
  const byCategory: Record<string, typeof allItems> = {};
  for (const item of allItems) {
    (byCategory[item.category] ??= []).push(item);
  }

  return (
    <div className="space-y-4">
      {Object.entries(byCategory).map(([category, items]) => (
        <div key={category} className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-4 py-2.5 border-b border-slate-100 flex items-center gap-2">
            <span className={`px-2 py-0.5 rounded text-xs font-semibold capitalize ${REQ_CATEGORY_COLORS[category] ?? REQ_CATEGORY_COLORS.other}`}>
              {category}
            </span>
            <span className="text-xs text-slate-400">{items.length} requirement{items.length !== 1 ? 's' : ''}</span>
          </div>
          <div className="divide-y divide-slate-100">
            {items.map(item => (
              <div key={item.id} className="px-4 py-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-800">{item.name}</p>
                    {item.fromParent && (
                      <p className="text-xs text-slate-400 mb-0.5">
                        Inherited from {item.parentJurisdictionName}
                      </p>
                    )}
                    <p className="text-xs text-slate-500 mt-0.5">{item.description}</p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className="text-xs text-slate-400 capitalize">{item.requirementType.replace('_', ' ')}</span>
                    {item.portalUrl && (
                      <a href={item.portalUrl} target="_blank" rel="noopener noreferrer"
                         title="Open portal"
                         className="text-blue-500 hover:text-blue-700">
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>
                </div>
                {item.contactInfo && (
                  <p className="text-xs text-slate-400 mt-1">Contact: {item.contactInfo}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

// ── main component ────────────────────────────────────────────────────────────

export default function Maximizer() {
  // ── page-level mode ──
  const [pageMode, setPageMode] = useState<PageMode>('maximize');

  // ── maximize form state ──
  const [mode,        setMode]        = useState<InputMode>('codes');
  const [lat,         setLat]         = useState('');
  const [lng,         setLng]         = useState('');
  const [codesRaw,    setCodesRaw]    = useState('NY, NY-NYC');
  const [projectType, setProjectType] = useState('film');
  const [spendRaw,    setSpendRaw]    = useState('5000000');
  const [loading,     setLoading]     = useState(false);
  const [result,      setResult]      = useState<MaximizeResult | null>(null);
  const [error,       setError]       = useState<string | null>(null);
  const [resultTab,   setResultTab]   = useState<ResultTab>('incentives');

  // ── split spend ──
  const [splitEnabled, setSplitEnabled] = useState(false);
  const [splitSpend,   setSplitSpend]   = useState<Record<string, string>>({});

  // ── saved scenarios ──
  const [savedScenarios, setSavedScenarios] = useState<SavedScenario[]>(loadScenarios);
  const [savePrompt, setSavePrompt] = useState(false);
  const [saveName,   setSaveName]   = useState('');

  // ── compare slots ──
  const [compareSlots, setCompareSlots] = useState<CompareSlot[]>([
    { id: '1', label: 'NYC',     codes: 'NY, NY-NYC',  spend: '5000000', type: 'film', result: null, loading: false, error: null },
    { id: '2', label: 'Chicago', codes: 'IL, IL-COOK', spend: '5000000', type: 'film', result: null, loading: false, error: null },
    { id: '3', label: 'LA',      codes: 'CA, CA-LA',   spend: '5000000', type: 'film', result: null, loading: false, error: null },
  ]);

  const spendNum = parseFloat(spendRaw.replace(/[^0-9.]/g, '')) || undefined;
  const parsedCodes = useMemo(() =>
    codesRaw.split(/[\s,]+/).map(s => s.trim().toUpperCase()).filter(Boolean),
    [codesRaw]
  );

  function handleCodesChange(raw: string) {
    setCodesRaw(raw);
    const next = raw.split(/[\s,]+/).map(s => s.trim().toUpperCase()).filter(Boolean);
    setSplitSpend(prev => {
      const pruned: Record<string, string> = {};
      for (const code of next) if (code in prev) pruned[code] = prev[code];
      return pruned;
    });
  }

  const spendByLocation: Record<string, number> | undefined = useMemo(() => {
    if (!splitEnabled) return undefined;
    const out: Record<string, number> = {};
    for (const [code, raw] of Object.entries(splitSpend)) {
      const n = parseFloat(raw.replace(/[^0-9.]/g, ''));
      if (!isNaN(n) && n > 0) out[code] = n;
    }
    return Object.keys(out).length > 0 ? out : undefined;
  }, [splitEnabled, splitSpend]);

  // ── maximize submit ──
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null); setResult(null); setLoading(true);
    try {
      const params: Parameters<typeof api.maximizer.maximize>[0] = {
        project_type: projectType, qualified_spend: spendNum, spend_by_location: spendByLocation,
      };
      if (mode === 'latLng') {
        const latN = parseFloat(lat), lngN = parseFloat(lng);
        if (isNaN(latN) || isNaN(lngN)) { setError('Enter valid lat/lng coordinates.'); return; }
        params.lat = latN; params.lng = lngN;
      } else {
        if (parsedCodes.length === 0) { setError('Enter at least one jurisdiction code.'); return; }
        params.jurisdiction_codes = parsedCodes;
      }
      setResult(await api.maximizer.maximize(params));
      setResultTab('incentives');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Unexpected error');
    } finally {
      setLoading(false);
    }
  }

  // ── save scenario ──
  function handleSave() {
    if (!saveName.trim()) return;
    const scenario: SavedScenario = {
      id: Date.now().toString(),
      name: saveName.trim(),
      codes: codesRaw, spend: spendRaw, type: projectType,
      splitSpend: splitEnabled ? splitSpend : {},
      savedAt: new Date().toISOString(),
    };
    const updated = [scenario, ...savedScenarios];
    setSavedScenarios(updated);
    saveScenarios(updated);
    setSavePrompt(false); setSaveName('');
  }

  function deleteScenario(id: string) {
    const updated = savedScenarios.filter(s => s.id !== id);
    setSavedScenarios(updated);
    saveScenarios(updated);
  }

  function loadScenario(s: SavedScenario) {
    setMode('codes');
    handleCodesChange(s.codes);
    setSpendRaw(s.spend);
    setProjectType(s.type);
    if (Object.keys(s.splitSpend).length > 0) {
      setSplitEnabled(true);
      setSplitSpend(s.splitSpend);
    } else {
      setSplitEnabled(false);
      setSplitSpend({});
    }
  }

  // ── compare slot actions ──
  function updateSlot(id: string, field: keyof CompareSlot, value: string) {
    setCompareSlots(prev => prev.map(s => s.id === id ? { ...s, [field]: value } : s));
  }

  function removeSlot(id: string) {
    setCompareSlots(prev => prev.filter(s => s.id !== id));
  }

  function addSlot() {
    if (compareSlots.length >= 4) return;
    setCompareSlots(prev => [...prev, {
      id: Date.now().toString(), label: `Market ${prev.length + 1}`,
      codes: '', spend: '5000000', type: 'film',
      result: null, loading: false, error: null,
    }]);
  }

  const runCompareSlot = useCallback(async (id: string) => {
    const slot = compareSlots.find(s => s.id === id);
    if (!slot) return;
    setCompareSlots(prev => prev.map(s => s.id === id ? { ...s, loading: true, error: null, result: null } : s));
    try {
      const codes = slot.codes.split(/[\s,]+/).map(s => s.trim().toUpperCase()).filter(Boolean);
      if (codes.length === 0) throw new Error('Enter jurisdiction codes');
      const spend = parseFloat(slot.spend.replace(/[^0-9.]/g, '')) || undefined;
      const r = await api.maximizer.maximize({ jurisdiction_codes: codes, project_type: slot.type, qualified_spend: spend });
      setCompareSlots(prev => prev.map(s => s.id === id ? { ...s, loading: false, result: r } : s));
    } catch (err: unknown) {
      setCompareSlots(prev => prev.map(s => s.id === id ? { ...s, loading: false, error: err instanceof Error ? err.message : 'Error' } : s));
    }
  }, [compareSlots]);

  async function runAllCompare() {
    for (const slot of compareSlots) await runCompareSlot(slot.id);
  }

  // ── export PDF ──
  function handleExportPdf() {
    window.print();
  }

  // ── derived ──
  const optInWarnings = result?.warnings.filter(w => w.includes('opt-in')) ?? [];
  const otherWarnings = result?.warnings.filter(w => !w.includes('opt-in')) ?? [];
  const nonZeroBreakdown = Object.entries(result?.breakdown ?? {}).filter(([, v]) => v !== 0);

  // ─────────────────────────────────────────────────────────────────────────────
  return (
    <>
      {/* Print-only stylesheet — hides sidebar, nav, form; shows only result card */}
      <style>{`
        @media print {
          aside, form, .no-print { display: none !important; }
          .print-target { display: block !important; }
          body { background: white; }
          .ml-64 { margin-left: 0 !important; }
        }
      `}</style>

      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header + page mode toggle */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
              <Zap className="w-6 h-6 text-blue-600" />
              Incentive Maximizer
            </h1>
            <p className="text-slate-500 text-sm mt-1">
              Stack-optimize tax incentives across jurisdiction layers.
            </p>
          </div>
          <div className="flex rounded-lg border border-slate-200 overflow-hidden text-sm shrink-0">
            <button
              type="button"
              onClick={() => setPageMode('maximize')}
              className={`flex items-center gap-1.5 px-4 py-2 font-medium transition-colors ${pageMode === 'maximize' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-50'}`}
            >
              <Zap className="w-3.5 h-3.5" /> Maximize
            </button>
            <button
              type="button"
              onClick={() => setPageMode('compare')}
              className={`flex items-center gap-1.5 px-4 py-2 font-medium transition-colors ${pageMode === 'compare' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-50'}`}
            >
              <GitCompare className="w-3.5 h-3.5" /> Compare
            </button>
          </div>
        </div>

        {/* ══════════════ MAXIMIZE MODE ══════════════ */}
        {pageMode === 'maximize' && (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            {/* ── Input Panel ── */}
            <div className="lg:col-span-2 space-y-4 no-print">
              <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 p-5 space-y-5">
                {/* Mode toggle */}
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Input Mode</p>
                  <div className="flex rounded-lg border border-slate-200 overflow-hidden text-sm">
                    <button type="button" onClick={() => setMode('codes')}
                      className={`flex-1 flex items-center justify-center gap-1.5 py-2 font-medium transition-colors ${mode === 'codes' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-50'}`}>
                      <Hash className="w-3.5 h-3.5" /> Codes
                    </button>
                    <button type="button" onClick={() => setMode('latLng')}
                      className={`flex-1 flex items-center justify-center gap-1.5 py-2 font-medium transition-colors ${mode === 'latLng' ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-50'}`}>
                      <MapPin className="w-3.5 h-3.5" /> Lat / Lng
                    </button>
                  </div>
                </div>

                {/* Location inputs */}
                {mode === 'codes' ? (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Jurisdiction Codes</label>
                    <input type="text" value={codesRaw} onChange={e => handleCodesChange(e.target.value)}
                      placeholder="e.g. NY, NY-NYC"
                      className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                    <p className="text-xs text-slate-400 mt-1">Comma or space separated. Stack parent + sub codes (e.g. IL, IL-COOK).</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Latitude</label>
                        <input type="number" step="any" value={lat} onChange={e => setLat(e.target.value)} placeholder="40.7128"
                          className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Longitude</label>
                        <input type="number" step="any" value={lng} onChange={e => setLng(e.target.value)} placeholder="-74.0060"
                          className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                      </div>
                    </div>
                    <LatLngMap lat={lat} lng={lng} onPick={(la, lo) => { setLat(la); setLng(lo); }} />
                    <p className="text-xs text-slate-400">Click the map or drag the pin to set coordinates.</p>
                  </div>
                )}

                {/* Project type */}
                <div>
                  <label htmlFor="project-type" className="block text-sm font-medium text-slate-700 mb-1">Project Type</label>
                  <select id="project-type" value={projectType} onChange={e => setProjectType(e.target.value)}
                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white">
                    {PROJECT_TYPES.map(pt => <option key={pt.value} value={pt.value}>{pt.label}</option>)}
                  </select>
                </div>

                {/* Qualified spend */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Qualified Spend (USD)</label>
                  <div className="relative">
                    <DollarSign className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input type="text" value={spendRaw} onChange={e => setSpendRaw(e.target.value)} placeholder="5000000"
                      className="w-full border border-slate-300 rounded-lg pl-8 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  </div>
                  {spendNum && <p className="text-xs text-slate-400 mt-1">{fmtUSD(spendNum)}</p>}
                </div>

                {/* Split spend by location */}
                {mode === 'codes' && parsedCodes.length > 1 && (
                  <div>
                    <button type="button" onClick={() => setSplitEnabled(v => !v)}
                      className={`flex items-center gap-2 text-xs font-medium transition-colors ${splitEnabled ? 'text-blue-600' : 'text-slate-500 hover:text-slate-700'}`}>
                      <SplitSquareHorizontal className="w-3.5 h-3.5" />
                      Split spend by location
                      <span className={`ml-auto w-7 h-4 rounded-full transition-colors relative ${splitEnabled ? 'bg-blue-500' : 'bg-slate-300'}`}>
                        <span className={`absolute top-0.5 w-3 h-3 rounded-full bg-white shadow transition-transform ${splitEnabled ? 'translate-x-3.5' : 'translate-x-0.5'}`} />
                      </span>
                    </button>
                    {splitEnabled && (
                      <div className="mt-3 space-y-2 border border-slate-200 rounded-lg p-3 bg-slate-50">
                        <p className="text-xs text-slate-500 mb-2">Sub-jurisdiction bonuses use their specific spend; state rules use the total above.</p>
                        {parsedCodes.map(code => (
                          <div key={code} className="flex items-center gap-2">
                            <span className="text-xs font-mono font-semibold text-slate-600 w-20 shrink-0">{code}</span>
                            <div className="relative flex-1">
                              <DollarSign className="absolute left-2 top-1/2 -translate-y-1/2 w-3 h-3 text-slate-400" />
                              <input type="text" value={splitSpend[code] ?? ''}
                                onChange={e => setSplitSpend(prev => ({ ...prev, [code]: e.target.value }))}
                                placeholder={spendRaw}
                                className="w-full border border-slate-300 rounded pl-6 pr-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white" />
                            </div>
                            {splitSpend[code] && (
                              <span className="text-xs text-slate-400 shrink-0 w-14 text-right">
                                {fmtUSD(parseFloat(splitSpend[code].replace(/[^0-9.]/g, '')) || 0)}
                              </span>
                            )}
                          </div>
                        ))}
                        <p className="text-xs text-slate-400 mt-1">Leave blank to use total qualified spend.</p>
                      </div>
                    )}
                  </div>
                )}

                <button type="submit" disabled={loading}
                  className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold py-2.5 rounded-lg transition-colors text-sm">
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
                  {loading ? 'Calculating…' : 'Maximize Incentives'}
                </button>
              </form>

              {/* Action bar (save / export) */}
              {result && (
                <div className="flex gap-2 no-print">
                  {!savePrompt ? (
                    <button type="button" onClick={() => { setSavePrompt(true); setSaveName(codesRaw.replace(/[\s,]+/g, '-')); }}
                      className="flex-1 flex items-center justify-center gap-1.5 text-xs font-medium text-slate-600 border border-slate-200 rounded-lg py-2 hover:bg-slate-50 transition-colors">
                      <Bookmark className="w-3.5 h-3.5" /> Save Scenario
                    </button>
                  ) : (
                    <div className="flex-1 flex gap-1.5">
                      <input autoFocus value={saveName} onChange={e => setSaveName(e.target.value)}
                        onKeyDown={e => { if (e.key === 'Enter') handleSave(); if (e.key === 'Escape') setSavePrompt(false); }}
                        placeholder="Scenario name"
                        className="flex-1 border border-blue-400 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500" />
                      <button type="button" aria-label="Confirm save" onClick={handleSave} className="px-2.5 py-1.5 bg-blue-600 text-white text-xs rounded-lg hover:bg-blue-700">
                        <BookmarkCheck className="w-3.5 h-3.5" />
                      </button>
                      <button type="button" aria-label="Cancel save" onClick={() => setSavePrompt(false)} className="px-2.5 py-1.5 text-slate-400 hover:text-slate-600 text-xs rounded-lg border border-slate-200">
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  )}
                  <button type="button" onClick={handleExportPdf}
                    className="flex items-center justify-center gap-1.5 text-xs font-medium text-slate-600 border border-slate-200 rounded-lg px-3 py-2 hover:bg-slate-50 transition-colors">
                    <Download className="w-3.5 h-3.5" /> Export PDF
                  </button>
                </div>
              )}

              {/* Quick presets */}
              <div className="bg-white rounded-xl border border-slate-200 p-4 no-print">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Quick Presets</p>
                <div className="space-y-1.5">
                  {[
                    { label: 'NYC — $5M Film',         codes: 'NY, NY-NYC',  spend: '5000000', type: 'film' },
                    { label: 'Chicago — $5M Film',      codes: 'IL, IL-COOK', spend: '5000000', type: 'film' },
                    { label: 'Los Angeles — $5M Film',  codes: 'CA, CA-LA',   spend: '5000000', type: 'film' },
                    { label: 'Erie County — $5M Film',  codes: 'NY, NY-ERIE', spend: '5000000', type: 'film' },
                    { label: 'Georgia — $5M Film',      codes: 'GA',          spend: '5000000', type: 'film' },
                  ].map(preset => (
                    <button key={preset.label} type="button"
                      onClick={() => { setMode('codes'); handleCodesChange(preset.codes); setSpendRaw(preset.spend); setProjectType(preset.type); setSplitEnabled(false); setSplitSpend({}); }}
                      className="w-full flex items-center justify-between px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 rounded-lg transition-colors group">
                      <span>{preset.label}</span>
                      <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-slate-600" />
                    </button>
                  ))}
                </div>

                {/* Saved scenarios */}
                {savedScenarios.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-slate-100">
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Saved</p>
                    <div className="space-y-1">
                      {savedScenarios.map(s => (
                        <div key={s.id} className="flex items-center gap-1">
                          <button type="button" onClick={() => loadScenario(s)}
                            className="flex-1 flex items-center justify-between px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50 rounded-lg transition-colors group text-left">
                            <span className="truncate">{s.name}</span>
                            <ChevronRight className="w-3 h-3 text-slate-400 group-hover:text-slate-600 shrink-0" />
                          </button>
                          <button type="button" aria-label="Delete scenario" onClick={() => deleteScenario(s.id)} className="p-1 text-slate-300 hover:text-red-400 transition-colors">
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* ── Results Panel ── */}
            <div className="lg:col-span-3 space-y-4 print-target">
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3 no-print">
                  <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}

              {!result && !loading && !error && (
                <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-400 no-print">
                  <Zap className="w-10 h-10 mx-auto mb-3 opacity-30" />
                  <p className="text-sm">Enter location or jurisdiction codes and click Maximize.</p>
                </div>
              )}

              {loading && (
                <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-400 no-print">
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
                        <p className="text-4xl font-bold tracking-tight">{fmtUSD(result.total_incentive_usd)}</p>
                        {result.effective_rate !== null && (
                          <p className="text-blue-200 text-sm mt-1 flex items-center gap-1">
                            <TrendingUp className="w-3.5 h-3.5" />
                            {fmtPct(result.effective_rate)} effective rate
                          </p>
                        )}
                      </div>
                      <div className="text-right text-sm text-blue-200 space-y-0.5">
                        {result.resolved_state && <p>State: <span className="text-white font-semibold">{result.resolved_state}</span></p>}
                        <p>Jurisdictions: <span className="text-white font-semibold">{result.jurisdictions_evaluated}</span></p>
                        {result.qualified_spend && (
                          <p>Spend: <span className="text-white font-semibold">{fmtUSD(result.qualified_spend)}</span>
                            {spendByLocation && <span className="ml-1 text-[10px] bg-blue-500/50 px-1.5 py-0.5 rounded font-medium">split</span>}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Result tabs */}
                  <div className="flex rounded-lg border border-slate-200 overflow-hidden text-sm bg-white no-print">
                    <button type="button" onClick={() => setResultTab('incentives')}
                      className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 font-medium transition-colors ${resultTab === 'incentives' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-50'}`}>
                      <BarChart3 className="w-3.5 h-3.5" /> Incentives
                    </button>
                    <button type="button" onClick={() => setResultTab('requirements')}
                      className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 font-medium transition-colors ${resultTab === 'requirements' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-50'}`}>
                      <ClipboardList className="w-3.5 h-3.5" /> Requirements
                    </button>
                  </div>

                  {/* ── Incentives tab ── */}
                  {resultTab === 'incentives' && (
                    <>
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
                                  <p className="text-sm font-semibold text-slate-900">{fmtUSD(rule.computed_value)}</p>
                                  {rule.value_unit === 'percent' && <p className="text-xs text-slate-400">{rule.raw_value.toFixed(0)}%</p>}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {nonZeroBreakdown.length > 0 && (
                        <div className="bg-white rounded-xl border border-slate-200 p-4">
                          <h3 className="text-sm font-semibold text-slate-700 mb-3">Breakdown by Category</h3>
                          <div className="space-y-2">
                            {nonZeroBreakdown.map(([cat, val]) => {
                              const pct = Math.abs(val / (result.total_incentive_usd || 1)) * 100;
                              return (
                                <div key={cat}>
                                  <div className="flex justify-between text-xs text-slate-600 mb-1">
                                    <span className="capitalize">{cat.replace('_', ' ')}</span>
                                    <span className={val < 0 ? 'text-red-600' : 'font-medium'}>{fmtUSD(val)}</span>
                                  </div>
                                  <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                    <div className={`h-full rounded-full ${val < 0 ? 'bg-red-400' : 'bg-blue-500'}`}
                                      style={{ width: `${Math.min(pct, 100)}%` }} />
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}

                      {optInWarnings.length > 0 && (
                        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
                          <div className="flex items-center gap-2 mb-2">
                            <Info className="w-4 h-4 text-amber-600 shrink-0" />
                            <h3 className="text-sm font-semibold text-amber-800">Opt-In Upside Available</h3>
                          </div>
                          <p className="text-xs text-amber-700 mb-2">Bonuses requiring a production-specific election — excluded from base total.</p>
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

                      {otherWarnings.length > 0 && (
                        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                          <h3 className="text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                            <AlertTriangle className="w-4 h-4 text-slate-500" /> Notes
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

                  {/* ── Requirements tab ── */}
                  {resultTab === 'requirements' && (
                    <RequirementsPanel
                      codes={mode === 'codes' ? parsedCodes : (result.resolved_state ? [result.resolved_state] : [])}
                      projectType={projectType}
                    />
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* ══════════════ COMPARE MODE ══════════════ */}
        {pageMode === 'compare' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-500">Side-by-side incentive comparison across markets. Each column runs independently.</p>
              <div className="flex gap-2">
                {compareSlots.length < 4 && (
                  <button type="button" onClick={addSlot}
                    className="flex items-center gap-1.5 text-xs font-medium text-slate-600 border border-slate-200 rounded-lg px-3 py-2 hover:bg-slate-50 transition-colors">
                    <Plus className="w-3.5 h-3.5" /> Add Market
                  </button>
                )}
                <button type="button" onClick={runAllCompare}
                  className="flex items-center gap-1.5 text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 transition-colors">
                  <Zap className="w-3.5 h-3.5" /> Run All
                </button>
              </div>
            </div>

            <div className={`grid gap-4 ${compareSlots.length === 2 ? 'grid-cols-2' : compareSlots.length === 3 ? 'grid-cols-3' : 'grid-cols-4'}`}>
              {compareSlots.map((slot, i) => (
                <CompareColumn
                  key={slot.id}
                  slot={slot} index={i} total={compareSlots.length}
                  onChange={updateSlot} onRemove={removeSlot} onRun={runCompareSlot}
                />
              ))}
            </div>

            {/* Summary table — only when all slots have results */}
            {compareSlots.every(s => s.result) && (
              <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
                <div className="px-4 py-3 border-b border-slate-100">
                  <h3 className="text-sm font-semibold text-slate-700">Comparison Summary</h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-slate-100">
                        <th className="px-4 py-2.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">Metric</th>
                        {compareSlots.map(s => (
                          <th key={s.id} className="px-4 py-2.5 text-left text-xs font-semibold text-slate-700">{s.label}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      <tr>
                        <td className="px-4 py-2.5 text-xs text-slate-500">Max Incentive</td>
                        {compareSlots.map(s => (
                          <td key={s.id} className="px-4 py-2.5 font-semibold text-slate-900">{fmtUSD(s.result!.total_incentive_usd)}</td>
                        ))}
                      </tr>
                      <tr>
                        <td className="px-4 py-2.5 text-xs text-slate-500">Effective Rate</td>
                        {compareSlots.map(s => (
                          <td key={s.id} className="px-4 py-2.5 text-slate-900">{fmtPct(s.result!.effective_rate)}</td>
                        ))}
                      </tr>
                      <tr>
                        <td className="px-4 py-2.5 text-xs text-slate-500">Rules Applied</td>
                        {compareSlots.map(s => (
                          <td key={s.id} className="px-4 py-2.5 text-slate-600">{s.result!.applied_rules.length}</td>
                        ))}
                      </tr>
                      <tr>
                        <td className="px-4 py-2.5 text-xs text-slate-500">Opt-In Upside</td>
                        {compareSlots.map(s => {
                          const optIns = s.result!.warnings.filter(w => w.includes('opt-in'));
                          const amounts = optIns.map(w => w.match(/\$([\d,]+)/)?.[1].replace(/,/g, '')).filter(Boolean);
                          const total = amounts.reduce((sum, a) => sum + (parseFloat(a ?? '0') || 0), 0);
                          return (
                            <td key={s.id} className="px-4 py-2.5 text-amber-600">
                              {total > 0 ? `+${fmtUSD(total)}` : '—'}
                            </td>
                          );
                        })}
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}

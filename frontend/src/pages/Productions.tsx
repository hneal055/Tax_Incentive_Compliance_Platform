import { useState } from 'react';
import { Search, Plus, Filter, ChevronRight, X } from 'lucide-react';
import type { Production } from '../types';

interface ProductionsProps {
  productions: Production[];
  onAddProduction?: (production: Production) => void;
  onUpdateProduction?: (production: Production) => void;
  onDeleteProduction?: (id: string) => void;
}

const JURISDICTIONS = [
  { id: 'ca', name: 'California' },
  { id: 'ga', name: 'Georgia' },
  { id: 'la', name: 'Louisiana' },
  { id: 'ny', name: 'New York' },
  { id: 'bc', name: 'British Columbia' },
  { id: 'on', name: 'Ontario' },
  { id: 'gb', name: 'United Kingdom' },
  { id: 'au', name: 'Australia' },
];

const EMPTY_FORM = { title: '', budget: '', jurisdiction_id: '', status: 'planning' as const };

export default function Productions({
  productions = [],
  onAddProduction,
}: ProductionsProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'active' | 'planning' | 'completed'>('all');
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState<{ title?: string; budget?: string }>({});

  const displayProductions: any[] = productions.length > 0
    ? productions.map((p, i) => ({
        id: p.id,
        title: p.title,
        budget: p.budget,
        status: (['active', 'planning', 'completed'] as const)[i % 3] || 'active',
        taxCredits: p.budget * 0.25,
        jurisdiction: JURISDICTIONS.find(j => j.id === p.jurisdiction_id)?.name ?? 'TBD',
        startDate: p.created_at?.split('T')[0] ?? new Date().toISOString().split('T')[0],
        progress: 0,
      }))
    : [
        { id: '1', title: 'The Silent Horizon',  status: 'active',   budget: 15000000, taxCredits: 3750000, jurisdiction: 'California', startDate: '2025-01-15', progress: 65 },
        { id: '2', title: 'Echoes of Midnight',  status: 'active',   budget: 8000000,  taxCredits: 2000000, jurisdiction: 'Georgia',    startDate: '2025-02-01', progress: 40 },
        { id: '3', title: 'Neon Pulse',           status: 'planning', budget: 4000000,  taxCredits: 1000000, jurisdiction: 'Louisiana',  startDate: '2025-03-01', progress: 15 },
      ];

  const filteredProductions = displayProductions.filter(p => {
    const matchesSearch = p.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || p.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const statusColors = {
    active:    'bg-green-100 text-green-800',
    planning:  'bg-blue-100 text-blue-800',
    completed: 'bg-slate-100 text-slate-800',
  };
  const statusLabels = { active: 'Active', planning: 'Planning', completed: 'Completed' };

  function validate() {
    const e: { title?: string; budget?: string } = {};
    if (!form.title.trim()) e.title = 'Title is required';
    const b = Number(form.budget);
    if (!form.budget || isNaN(b) || b <= 0) e.budget = 'Enter a valid budget';
    return e;
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }

    const now = new Date().toISOString();
    const newProduction: Production = {
      id: `${Date.now()}`,
      title: form.title.trim(),
      budget: Number(form.budget),
      jurisdiction_id: form.jurisdiction_id || undefined,
      created_at: now,
      updated_at: now,
    };
    onAddProduction?.(newProduction);
    setForm(EMPTY_FORM);
    setErrors({});
    setShowModal(false);
  }

  function handleClose() {
    setShowModal(false);
    setForm(EMPTY_FORM);
    setErrors({});
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-8 py-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-[28px] font-bold text-slate-900">Productions</h1>
            <p className="text-slate-500 mt-1 text-[15px]">Manage and track all film productions.</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium text-sm"
          >
            <Plus className="w-4 h-4" />
            New Production
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-8 max-w-6xl mx-auto">
        {/* Search and Filter */}
        <div className="flex gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-2.5 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search productions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors text-slate-700 font-medium text-sm">
            <Filter className="w-4 h-4" />
            Filter
          </button>
        </div>

        {/* Status Filter Tabs */}
        <div className="flex gap-2 mb-6">
          {(['all', 'active', 'planning', 'completed'] as const).map((status) => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm ${
                filterStatus === status
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-slate-700 border border-slate-300 hover:border-slate-400'
              }`}
            >
              {status === 'all' ? 'All' : status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>

        {/* Productions List */}
        <div className="space-y-4">
          {filteredProductions.map((production) => (
            <div
              key={production.id}
              className="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-md transition-shadow cursor-pointer group"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1.5">
                    <h3 className="text-base font-bold text-slate-900">{production.title}</h3>
                    <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full ${statusColors[production.status as 'active' | 'planning' | 'completed']}`}>
                      {statusLabels[production.status as 'active' | 'planning' | 'completed']}
                    </span>
                  </div>
                  <p className="text-slate-500 text-sm">{production.jurisdiction} • Started {production.startDate}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-slate-600 transition-colors" />
              </div>

              <div className="mb-4">
                <div className="w-full bg-slate-200 rounded-full h-1.5">
                  <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: `${production.progress}%` }} />
                </div>
                <p className="text-xs text-slate-500 mt-1">{production.progress}% Complete</p>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <p className="text-slate-500 text-xs font-medium mb-0.5">Budget</p>
                  <p className="text-base font-bold text-slate-900">${(production.budget / 1000000).toFixed(1)}M</p>
                </div>
                <div>
                  <p className="text-slate-500 text-xs font-medium mb-0.5">Tax Credits</p>
                  <p className="text-base font-bold text-green-600">${(production.taxCredits / 1000000).toFixed(1)}M</p>
                </div>
                <div>
                  <p className="text-slate-500 text-xs font-medium mb-0.5">Credit Rate</p>
                  <p className="text-base font-bold text-slate-900">
                    {((production.taxCredits / production.budget) * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredProductions.length === 0 && (
          <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
            <p className="text-slate-500 text-sm">No productions found matching your filters.</p>
          </div>
        )}
      </div>

      {/* New Production Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={handleClose} />

          {/* Panel */}
          <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-8">
            {/* Header */}
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-xl font-bold text-slate-900">New Production</h2>
                <p className="text-slate-500 text-sm mt-0.5">Add a new film production to track.</p>
              </div>
              <button type="button" onClick={handleClose} title="Close" aria-label="Close" className="text-slate-400 hover:text-slate-600 transition-colors mt-0.5">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Title */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                  Production Title <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  placeholder="e.g. The Silent Horizon"
                  value={form.title}
                  onChange={(e) => { setForm(f => ({ ...f, title: e.target.value })); setErrors(er => ({ ...er, title: undefined })); }}
                  className={`w-full px-3.5 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.title ? 'border-red-400' : 'border-slate-300'}`}
                  autoFocus
                />
                {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
              </div>

              {/* Budget */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                  Total Budget (USD) <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <span className="absolute left-3.5 top-2.5 text-slate-400 text-sm select-none">$</span>
                  <input
                    type="number"
                    placeholder="5000000"
                    min="1"
                    value={form.budget}
                    onChange={(e) => { setForm(f => ({ ...f, budget: e.target.value })); setErrors(er => ({ ...er, budget: undefined })); }}
                    className={`w-full pl-7 pr-3.5 py-2.5 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.budget ? 'border-red-400' : 'border-slate-300'}`}
                  />
                </div>
                {errors.budget && <p className="text-red-500 text-xs mt-1">{errors.budget}</p>}
              </div>

              {/* Jurisdiction */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">Jurisdiction</label>
                <select
                  value={form.jurisdiction_id}
                  onChange={(e) => setForm(f => ({ ...f, jurisdiction_id: e.target.value }))}
                  title="Jurisdiction"
                  aria-label="Jurisdiction"
                  className="w-full px-3.5 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-slate-700"
                >
                  <option value="">Select jurisdiction (optional)</option>
                  {JURISDICTIONS.map(j => (
                    <option key={j.id} value={j.id}>{j.name}</option>
                  ))}
                </select>
              </div>

              {/* Status */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">Status</label>
                <div className="flex gap-2">
                  {(['planning', 'active', 'completed'] as const).map(s => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => setForm(f => ({ ...f, status: s }))}
                      className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-colors ${
                        form.status === s
                          ? 'bg-blue-600 text-white border-blue-600'
                          : 'bg-white text-slate-600 border-slate-300 hover:border-slate-400'
                      }`}
                    >
                      {s.charAt(0).toUpperCase() + s.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-1">
                <button
                  type="button"
                  onClick={handleClose}
                  className="flex-1 py-2.5 border border-slate-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                >
                  Create Production
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

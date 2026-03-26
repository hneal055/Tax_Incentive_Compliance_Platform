import { useState, useEffect, useCallback } from 'react';
import { Bell, BellOff, Save, Check } from 'lucide-react';
import api from '../api';
import type { Jurisdiction, NotificationPreference } from '../types';

function Settings() {
  const [jurisdictions, setJurisdictions] = useState<Jurisdiction[]>([]);
  const [pref, setPref] = useState<NotificationPreference | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [saved, setSaved] = useState(false);

  // Form state
  const [email, setEmail] = useState('');
  const [active, setActive] = useState(true);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const load = useCallback(async () => {
    setLoading(true);
    const [jurs, existing] = await Promise.all([
      api.jurisdictions.list(),
      api.notifications.getPreferences(),
    ]);
    setJurisdictions(jurs.filter(j => j.active));
    if (existing) {
      setPref(existing);
      setEmail(existing.emailAddress);
      setActive(existing.active);
      setSelected(new Set(existing.jurisdictions));
    }
    setLoading(false);
  }, []);

  useEffect(() => { load(); }, [load]);

  function toggleJurisdiction(code: string) {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(code)) next.delete(code);
      else next.add(code);
      return next;
    });
  }

  function selectAll() {
    setSelected(new Set(jurisdictions.map(j => j.code)));
  }

  function clearAll() {
    setSelected(new Set());
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!email.trim()) return;
    setSaving(true);
    setSaved(false);
    try {
      const updated = await api.notifications.upsertPreferences({
        emailAddress: email.trim(),
        jurisdictions: Array.from(selected),
        active,
      });
      setPref(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    if (!confirm('Remove all notification preferences? You will stop receiving regulatory alerts.')) return;
    setDeleting(true);
    try {
      await api.notifications.deletePreferences();
      setPref(null);
      setEmail('');
      setActive(true);
      setSelected(new Set());
    } finally {
      setDeleting(false);
    }
  }

  const byCountry = jurisdictions.reduce<Record<string, Jurisdiction[]>>((acc, j) => {
    (acc[j.country] ??= []).push(j);
    return acc;
  }, {});

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
          <Bell className="w-5 h-5 text-blue-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Notification Settings</h1>
          <p className="text-sm text-slate-500 mt-0.5">Get email alerts when regulatory rules change</p>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20 text-slate-400">
          <div className="w-6 h-6 border-2 border-slate-200 border-t-blue-500 rounded-full animate-spin mr-3" />
          Loading…
        </div>
      ) : (
        <form onSubmit={handleSave} className="space-y-6">
          {/* Email + active toggle */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
            <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide">Alert Delivery</h2>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Email address</label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex items-center justify-between py-1">
              <div>
                <p className="text-sm font-medium text-slate-800">Enable alerts</p>
                <p className="text-xs text-slate-500 mt-0.5">Pause without losing your preferences</p>
              </div>
              <button
                type="button"
                onClick={() => setActive(v => !v)}
                className={`relative w-11 h-6 rounded-full transition-colors ${active ? 'bg-blue-600' : 'bg-slate-300'}`}
                role="switch"
                aria-checked={active}
              >
                <span
                  className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${active ? 'translate-x-5' : 'translate-x-0'}`}
                />
              </button>
            </div>
          </div>

          {/* Jurisdiction filter */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wide">Jurisdictions</h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  {selected.size === 0
                    ? 'No filter — you will receive alerts for all jurisdictions'
                    : `Filtered to ${selected.size} jurisdiction${selected.size === 1 ? '' : 's'}`}
                </p>
              </div>
              <div className="flex gap-2">
                <button type="button" onClick={selectAll} className="text-xs text-blue-600 hover:underline">All</button>
                <span className="text-slate-300">|</span>
                <button type="button" onClick={clearAll} className="text-xs text-slate-500 hover:underline">None</button>
              </div>
            </div>

            <div className="space-y-5">
              {Object.entries(byCountry).sort(([a], [b]) => a.localeCompare(b)).map(([country, jurs]) => (
                <div key={country}>
                  <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">{country}</p>
                  <div className="flex flex-wrap gap-2">
                    {jurs.map(j => {
                      const on = selected.has(j.code);
                      return (
                        <button
                          key={j.id}
                          type="button"
                          onClick={() => toggleJurisdiction(j.code)}
                          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                            on
                              ? 'bg-blue-50 border-blue-300 text-blue-700'
                              : 'bg-slate-50 border-slate-200 text-slate-600 hover:border-slate-300'
                          }`}
                        >
                          {on && <Check className="w-3 h-3" />}
                          {j.code} — {j.name}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between">
            {pref ? (
              <button
                type="button"
                onClick={handleDelete}
                disabled={deleting}
                className="flex items-center gap-2 px-4 py-2 text-sm text-red-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-40"
              >
                <BellOff className="w-4 h-4" />
                {deleting ? 'Removing…' : 'Unsubscribe'}
              </button>
            ) : (
              <span />
            )}

            <button
              type="submit"
              disabled={saving || !email.trim()}
              className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {saved ? (
                <><Check className="w-4 h-4" /> Saved</>
              ) : saving ? (
                <><div className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" /> Saving…</>
              ) : (
                <><Save className="w-4 h-4" /> Save preferences</>
              )}
            </button>
          </div>

          {/* Status note if prefs exist */}
          {pref && (
            <p className="text-xs text-slate-400 text-right -mt-2">
              Last updated {new Date(pref.updatedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </p>
          )}
        </form>
      )}
    </div>
  );
}

export default Settings;

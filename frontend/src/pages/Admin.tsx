import { useState, useEffect, useCallback } from 'react';
import { Users, Plus, Trash2, ShieldCheck, ShieldOff, KeyRound, X } from 'lucide-react';
import api from '../api';
import type { UserProfile } from '../types';

function roleBadge(role: string) {
  return role === 'admin'
    ? 'bg-purple-100 text-purple-700 border border-purple-200'
    : 'bg-slate-100 text-slate-600 border border-slate-200';
}

function statusBadge(isActive: boolean) {
  return isActive
    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    : 'bg-red-50 text-red-500 border border-red-200';
}

interface InviteForm {
  email: string;
  password: string;
  role: 'admin' | 'viewer';
}

const emptyForm: InviteForm = { email: '', password: '', role: 'viewer' };

function Admin() {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [showInvite, setShowInvite] = useState(false);
  const [form, setForm] = useState<InviteForm>(emptyForm);
  const [formError, setFormError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const [actionTarget, setActionTarget] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.admin.listUsers();
      setUsers(res.users);
    } catch {
      setError('Failed to load users.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);
    if (!form.email.trim() || !form.password.trim()) {
      setFormError('Email and password are required.');
      return;
    }
    setSaving(true);
    try {
      await api.admin.createUser({ email: form.email.trim(), password: form.password, role: form.role });
      setShowInvite(false);
      setForm(emptyForm);
      await load();
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setFormError(msg || 'Failed to create user.');
    } finally {
      setSaving(false);
    }
  }

  async function toggleActive(user: UserProfile) {
    setActionTarget(user.id);
    try {
      const updated = await api.admin.updateUser(user.id, { isActive: !user.isActive });
      setUsers(prev => prev.map(u => u.id === user.id ? updated : u));
    } catch {
      /* ignore */
    } finally {
      setActionTarget(null);
    }
  }

  async function toggleRole(user: UserProfile) {
    setActionTarget(user.id);
    const newRole = user.role === 'admin' ? 'viewer' : 'admin';
    try {
      const updated = await api.admin.updateUser(user.id, { role: newRole });
      setUsers(prev => prev.map(u => u.id === user.id ? updated : u));
    } catch {
      /* ignore */
    } finally {
      setActionTarget(null);
    }
  }

  async function handleDelete(user: UserProfile) {
    if (!confirm(`Permanently delete ${user.email}? This cannot be undone.`)) return;
    setActionTarget(user.id);
    try {
      await api.admin.deleteUser(user.id);
      setUsers(prev => prev.filter(u => u.id !== user.id));
    } catch {
      /* ignore */
    } finally {
      setActionTarget(null);
    }
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
            <Users className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">User Management</h1>
            <p className="text-sm text-slate-500 mt-0.5">Manage platform access and roles</p>
          </div>
        </div>
        <button
          onClick={() => { setShowInvite(true); setFormError(null); setForm(emptyForm); }}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Invite User
        </button>
      </div>

      {/* Invite Modal */}
      {showInvite && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
              <h2 className="text-lg font-semibold text-slate-900">Invite New User</h2>
              <button onClick={() => setShowInvite(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleCreate} className="px-6 py-5 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Email address</label>
                <input
                  type="email"
                  value={form.email}
                  onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
                  placeholder="user@example.com"
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                <input
                  type="password"
                  value={form.password}
                  onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
                  placeholder="Minimum 8 characters"
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Role</label>
                <select
                  value={form.role}
                  onChange={e => setForm(f => ({ ...f, role: e.target.value as 'admin' | 'viewer' }))}
                  className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                >
                  <option value="viewer">Viewer — read-only access</option>
                  <option value="admin">Admin — full access</option>
                </select>
              </div>
              {formError && (
                <p className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">{formError}</p>
              )}
              <div className="flex gap-3 pt-1">
                <button
                  type="button"
                  onClick={() => setShowInvite(false)}
                  className="flex-1 px-4 py-2 border border-slate-200 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                  {saving ? 'Creating…' : 'Create User'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center py-20 text-slate-400">
          <div className="w-6 h-6 border-2 border-slate-200 border-t-blue-500 rounded-full animate-spin mr-3" />
          Loading users…
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
          <p className="text-red-600 font-medium">{error}</p>
          <button onClick={load} className="mt-3 text-sm text-red-500 underline">Retry</button>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
          <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-700">
              {users.length} {users.length === 1 ? 'user' : 'users'}
            </h2>
            <p className="text-xs text-slate-400">Click role or status badges to toggle</p>
          </div>
          {users.length === 0 ? (
            <div className="py-16 text-center text-slate-400">
              <Users className="w-10 h-10 mx-auto mb-3 opacity-30" />
              <p className="text-sm">No users yet. Invite someone to get started.</p>
            </div>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-100">
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">User</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Role</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Created</th>
                  <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map(user => {
                  const busy = actionTarget === user.id;
                  return (
                    <tr key={user.id} className="hover:bg-slate-50/60 transition-colors">
                      <td className="px-6 py-3.5">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 bg-slate-100 rounded-full flex items-center justify-center text-xs font-semibold text-slate-600 shrink-0">
                            {user.email.slice(0, 2).toUpperCase()}
                          </div>
                          <span className="font-medium text-slate-800 truncate max-w-[220px]">{user.email}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3.5">
                        <button
                          onClick={() => toggleRole(user)}
                          disabled={busy}
                          title="Toggle role"
                          className={`inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full capitalize cursor-pointer hover:opacity-80 transition-opacity disabled:opacity-40 ${roleBadge(user.role)}`}
                        >
                          {user.role === 'admin'
                            ? <ShieldCheck className="w-3 h-3" />
                            : <ShieldOff className="w-3 h-3" />
                          }
                          {user.role}
                        </button>
                      </td>
                      <td className="px-4 py-3.5">
                        <button
                          onClick={() => toggleActive(user)}
                          disabled={busy}
                          title="Toggle active status"
                          className={`inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full cursor-pointer hover:opacity-80 transition-opacity disabled:opacity-40 ${statusBadge(user.isActive)}`}
                        >
                          <span className={`w-1.5 h-1.5 rounded-full ${user.isActive ? 'bg-emerald-500' : 'bg-red-400'}`} />
                          {user.isActive ? 'Active' : 'Inactive'}
                        </button>
                      </td>
                      <td className="px-4 py-3.5 text-slate-500">
                        {new Date(user.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                      </td>
                      <td className="px-4 py-3.5">
                        <div className="flex items-center justify-end gap-1">
                          <button
                            onClick={() => {
                              const pw = prompt(`Set new password for ${user.email}:`);
                              if (pw) api.admin.updateUser(user.id, { password: pw });
                            }}
                            disabled={busy}
                            title="Reset password"
                            className="p-1.5 text-slate-400 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors disabled:opacity-40"
                          >
                            <KeyRound className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(user)}
                            disabled={busy}
                            title="Delete user"
                            className="p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-40"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

export default Admin;

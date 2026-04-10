import { useState, useEffect } from 'react';
import {
  ClipboardCheck, CheckCircle, XCircle, Clock, ExternalLink,
  ChevronDown, ChevronUp, AlertCircle, Loader2, RefreshCw
} from 'lucide-react';
import type { PendingRule, ExtractedRule } from '../types';
import { pendingRulesApi } from '../api';

// ── Status config ─────────────────────────────────────────────────────────────

const STATUS_FILTERS = [
  { value: '',         label: 'All' },
  { value: 'pending',  label: 'Pending' },
  { value: 'approved', label: 'Approved' },
  { value: 'rejected', label: 'Rejected' },
];

const STATUS_STYLES: Record<string, string> = {
  pending:  'bg-amber-100 text-amber-800',
  approved: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
};

const STATUS_ICONS: Record<string, React.ReactNode> = {
  pending:  <Clock className="w-3.5 h-3.5" />,
  approved: <CheckCircle className="w-3.5 h-3.5" />,
  rejected: <XCircle className="w-3.5 h-3.5" />,
};

const CONFIDENCE_COLOR = (c: number | null) => {
  if (!c) return 'text-gray-400';
  if (c >= 0.7) return 'text-green-600';
  if (c >= 0.4) return 'text-amber-600';
  return 'text-red-500';
};

// ── Extracted rule card ───────────────────────────────────────────────────────

function RuleCard({ rule }: { rule: ExtractedRule }) {
  return (
    <div className="border border-gray-200 rounded-lg p-3 bg-gray-50 text-sm space-y-1">
      <div className="flex items-start justify-between gap-2">
        <span className="font-medium text-gray-900">{rule.name}</span>
        <div className="flex gap-1 shrink-0">
          <span className="px-1.5 py-0.5 rounded text-xs bg-blue-100 text-blue-700">{rule.category}</span>
          <span className="px-1.5 py-0.5 rounded text-xs bg-purple-100 text-purple-700">{rule.rule_type}</span>
        </div>
      </div>
      <p className="text-gray-600">{rule.description}</p>
      {(rule.amount != null || rule.percentage != null) && (
        <div className="flex gap-3 text-xs text-gray-500">
          {rule.amount != null && <span>Amount: <strong>${rule.amount.toLocaleString()}</strong></span>}
          {rule.percentage != null && <span>Rate: <strong>{rule.percentage}%</strong></span>}
        </div>
      )}
      {rule.requirements && (
        <p className="text-xs text-gray-500 italic">{rule.requirements}</p>
      )}
      {rule.effective_date && (
        <p className="text-xs text-gray-400">Effective: {rule.effective_date}</p>
      )}
    </div>
  );
}

// ── Review modal ──────────────────────────────────────────────────────────────

function ReviewModal({
  rule,
  action,
  onConfirm,
  onCancel,
}: {
  rule: PendingRule;
  action: 'approve' | 'reject';
  onConfirm: (notes: string) => void;
  onCancel: () => void;
}) {
  const [notes, setNotes] = useState('');
  const isApprove = action === 'approve';
  const ruleCount = rule.extractedData?.rules?.length ?? 0;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6 space-y-4">
        <div className="flex items-center gap-3">
          {isApprove
            ? <CheckCircle className="w-6 h-6 text-green-500" />
            : <XCircle className="w-6 h-6 text-red-500" />}
          <h2 className="text-lg font-semibold text-gray-900">
            {isApprove ? 'Approve' : 'Reject'} Pending Rule
          </h2>
        </div>

        <div className="text-sm text-gray-600 space-y-1">
          <p><span className="font-medium">Jurisdiction:</span> {rule.jurisdiction?.name}</p>
          <p><span className="font-medium">Source:</span> <a href={rule.sourceUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline truncate">{rule.sourceUrl}</a></p>
          {isApprove && ruleCount > 0 && (
            <p className="text-green-700 font-medium">
              This will promote {ruleCount} extracted rule{ruleCount !== 1 ? 's' : ''} into Local Rules.
            </p>
          )}
        </div>

        <textarea
          className="w-full border border-gray-300 rounded-lg p-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows={3}
          placeholder="Review notes (optional)"
          value={notes}
          onChange={e => setNotes(e.target.value)}
        />

        <div className="flex gap-3 justify-end">
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded-lg border border-gray-300 text-sm text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            onClick={() => onConfirm(notes)}
            className={`px-4 py-2 rounded-lg text-sm text-white font-medium ${
              isApprove ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'
            }`}
          >
            {isApprove ? 'Approve & Promote' : 'Reject'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Row ───────────────────────────────────────────────────────────────────────

function PendingRuleRow({
  rule,
  onAction,
}: {
  rule: PendingRule;
  onAction: (id: string, action: 'approve' | 'reject') => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const ruleCount = rule.extractedData?.rules?.length ?? 0;
  const confidence = rule.confidence ?? 0;

  return (
    <div className="border border-gray-200 rounded-xl bg-white overflow-hidden">
      {/* Header row */}
      <div className="flex items-center gap-3 px-4 py-3">
        <button
          onClick={() => setExpanded(e => !e)}
          className="text-gray-400 hover:text-gray-600 shrink-0"
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-medium text-gray-900 text-sm">
              {rule.jurisdiction?.name ?? rule.jurisdictionId}
            </span>
            <span className="text-xs text-gray-400">{rule.jurisdiction?.code}</span>
            <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_STYLES[rule.status]}`}>
              {STATUS_ICONS[rule.status]}
              {rule.status.charAt(0).toUpperCase() + rule.status.slice(1)}
            </span>
          </div>
          <div className="flex items-center gap-3 mt-0.5 text-xs text-gray-500">
            <a href={rule.sourceUrl} target="_blank" rel="noopener noreferrer"
               className="flex items-center gap-1 hover:text-blue-600 truncate max-w-xs">
              <ExternalLink className="w-3 h-3 shrink-0" />
              {rule.sourceUrl}
            </a>
            <span>·</span>
            <span>{ruleCount} rule{ruleCount !== 1 ? 's' : ''}</span>
            <span>·</span>
            <span className={`font-medium ${CONFIDENCE_COLOR(rule.confidence)}`}>
              {(confidence * 100).toFixed(0)}% confidence
            </span>
            <span>·</span>
            <span>{new Date(rule.createdAt).toLocaleDateString()}</span>
          </div>
        </div>

        {rule.status === 'pending' && (
          <div className="flex gap-2 shrink-0">
            <button
              onClick={() => onAction(rule.id, 'approve')}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium bg-green-600 text-white hover:bg-green-700"
            >
              <CheckCircle className="w-3.5 h-3.5" /> Approve
            </button>
            <button
              onClick={() => onAction(rule.id, 'reject')}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium bg-red-50 text-red-700 hover:bg-red-100 border border-red-200"
            >
              <XCircle className="w-3.5 h-3.5" /> Reject
            </button>
          </div>
        )}

        {rule.status !== 'pending' && rule.reviewedAt && (
          <div className="text-xs text-gray-400 shrink-0">
            Reviewed {new Date(rule.reviewedAt).toLocaleDateString()}
          </div>
        )}
      </div>

      {/* Expanded detail */}
      {expanded && (
        <div className="border-t border-gray-100 px-4 py-3 bg-gray-50 space-y-3">
          {rule.extractedData?.summary && (
            <p className="text-sm text-gray-600 italic">{rule.extractedData.summary}</p>
          )}

          {ruleCount > 0 ? (
            <div className="space-y-2">
              <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                Extracted Rules ({ruleCount})
              </p>
              {rule.extractedData.rules.map((r, i) => (
                <RuleCard key={i} rule={r} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-400 italic">No rules extracted from this source.</p>
          )}

          {rule.reviewNotes && (
            <div className="border-t border-gray-200 pt-2 text-xs text-gray-500">
              <span className="font-medium">Review notes:</span> {rule.reviewNotes}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function PendingRules() {
  const [rules, setRules] = useState<PendingRule[]>([]);
  const [pendingCount, setPendingCount] = useState(0);
  const [statusFilter, setStatusFilter] = useState('pending');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modal, setModal] = useState<{ rule: PendingRule; action: 'approve' | 'reject' } | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await pendingRulesApi.list(statusFilter || undefined);
      setRules(res.rules);
      setPendingCount(res.pendingCount);
    } catch {
      setError('Failed to load pending rules');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [statusFilter]);

  const handleAction = (id: string, action: 'approve' | 'reject') => {
    const rule = rules.find(r => r.id === id);
    if (rule) setModal({ rule, action });
  };

  const handleConfirm = async (notes: string) => {
    if (!modal) return;
    setActionLoading(true);
    try {
      if (modal.action === 'approve') {
        await pendingRulesApi.approve(modal.rule.id, notes);
      } else {
        await pendingRulesApi.reject(modal.rule.id, notes);
      }
      setModal(null);
      load();
    } catch {
      setError(`Failed to ${modal.action} rule`);
      setModal(null);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <ClipboardCheck className="w-6 h-6 text-blue-600" />
          <div>
            <h1 className="text-xl font-bold text-gray-900">Pending Rules Review</h1>
            <p className="text-sm text-gray-500">
              Review Claude-extracted rules from sub-jurisdiction feeds
            </p>
          </div>
          {pendingCount > 0 && (
            <span className="px-2.5 py-1 rounded-full text-sm font-medium bg-amber-100 text-amber-800">
              {pendingCount} pending
            </span>
          )}
        </div>
        <button
          onClick={load}
          className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-300 text-sm text-gray-600 hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-1 bg-gray-100 p-1 rounded-lg w-fit">
        {STATUS_FILTERS.map(f => (
          <button
            key={f.value}
            onClick={() => setStatusFilter(f.value)}
            className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
              statusFilter === f.value
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {f.label}
          </button>
        ))}
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
      ) : rules.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          <ClipboardCheck className="w-10 h-10 mx-auto mb-3 opacity-30" />
          <p className="text-sm">No {statusFilter || ''} rules found.</p>
          {statusFilter === 'pending' && (
            <p className="text-xs mt-1">Run <code className="bg-gray-100 px-1 rounded">python monitor.py</code> to fetch new rules.</p>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {rules.map(rule => (
            <PendingRuleRow key={rule.id} rule={rule} onAction={handleAction} />
          ))}
        </div>
      )}

      {/* Review modal */}
      {modal && !actionLoading && (
        <ReviewModal
          rule={modal.rule}
          action={modal.action}
          onConfirm={handleConfirm}
          onCancel={() => setModal(null)}
        />
      )}
      {actionLoading && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
          <Loader2 className="w-8 h-8 text-white animate-spin" />
        </div>
      )}
    </div>
  );
}

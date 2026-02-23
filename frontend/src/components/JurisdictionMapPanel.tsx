import { useEffect, useCallback, memo } from 'react';
import { createPortal } from 'react-dom';
import { X, MapPin, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type { Jurisdiction, Production, IncentiveRuleDetailed } from '../types';

interface JurisdictionMapPanelProps {
  isOpen: boolean;
  onClose: () => void;
  jurisdiction: Jurisdiction | null;
  rules: IncentiveRuleDetailed[];
  productions: Production[];
}

const JurisdictionMapPanel: React.FC<JurisdictionMapPanelProps> = memo(({
  isOpen,
  onClose,
  jurisdiction,
  rules,
  productions,
}) => {
  const navigate = useNavigate();

  const handleEscape = useCallback(
    (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); },
    [onClose],
  );

  useEffect(() => {
    if (!isOpen) return;
    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, handleEscape]);

  if (!isOpen || !jurisdiction) return null;

  const bestRate = rules.reduce((best, r) => Math.max(best, r.percentage ?? 0), 0);
  const jurisdictionProductions = productions.filter(
    p => p.jurisdictionId === jurisdiction.id,
  );

  const panel = (
    <div className="fixed inset-0 flex" style={{ zIndex: 99999 }}>
      {/* Backdrop */}
      <div
        className="absolute inset-0"
        onClick={onClose}
        style={{ backgroundColor: 'rgba(17, 24, 39, 0.45)', backdropFilter: 'blur(4px)' }}
      />

      {/* Panel */}
      <div
        className="ml-auto relative w-full max-w-md bg-white dark:bg-gray-800
                   shadow-2xl border-l border-gray-200 dark:border-gray-700
                   overflow-y-auto animate-slide-in-right"
      >
        {/* Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between p-5
                        border-b border-gray-200 dark:border-gray-700
                        bg-white dark:bg-gray-800">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg
                           bg-gradient-to-br from-accent-blue/20 to-accent-teal/20">
              <MapPin className="h-5 w-5 text-accent-blue dark:text-accent-teal" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                {jurisdiction.name}
              </h3>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {jurisdiction.code} &middot; {jurisdiction.country}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="flex h-8 w-8 items-center justify-center rounded-lg
                       text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700
                       transition-colors"
            aria-label="Close panel"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Best rate badge */}
        {bestRate > 0 && (
          <div className="mx-5 mt-5 rounded-lg bg-gradient-to-r from-accent-teal/10
                         to-accent-blue/10 dark:from-accent-teal/20 dark:to-accent-blue/20
                         border border-accent-teal/30 p-4 text-center">
            <p className="text-xs font-semibold uppercase text-accent-teal tracking-wide">
              Best Incentive Rate
            </p>
            <p className="text-4xl font-black text-accent-blue dark:text-accent-teal mt-1">
              {bestRate}%
            </p>
          </div>
        )}

        {/* Incentive rules */}
        <div className="p-5">
          <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100
                        uppercase tracking-wide mb-3">
            Incentive Rules ({rules.length})
          </h4>

          {rules.length === 0 ? (
            <p className="text-sm text-gray-500 dark:text-gray-400">
              No active incentive programs
            </p>
          ) : (
            <div className="space-y-2">
              {rules.map(rule => (
                <div
                  key={rule.id}
                  className="rounded-lg border border-gray-200 dark:border-gray-600
                             p-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      {rule.ruleName}
                    </span>
                    <span className="text-sm font-bold text-accent-blue dark:text-accent-teal">
                      {rule.percentage ?? 0}%
                    </span>
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-500 dark:text-gray-400">
                    <span>{rule.incentiveType.replace(/_/g, ' ')}</span>
                    {rule.minSpend != null && rule.minSpend > 0 && (
                      <span>Min: ${rule.minSpend.toLocaleString()}</span>
                    )}
                    {rule.maxCredit != null && rule.maxCredit > 0 && (
                      <span>Max: ${rule.maxCredit.toLocaleString()}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Productions */}
        <div className="px-5 pb-5">
          <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100
                        uppercase tracking-wide mb-3">
            Productions ({jurisdictionProductions.length})
          </h4>

          {jurisdictionProductions.length === 0 ? (
            <p className="text-sm text-gray-500 dark:text-gray-400">
              No productions in this jurisdiction
            </p>
          ) : (
            <div className="space-y-2">
              {jurisdictionProductions.map(prod => (
                <div
                  key={prod.id}
                  className="flex items-center justify-between rounded-lg border
                             border-gray-100 dark:border-gray-600 p-3
                             hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <div>
                    <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                      {prod.title}
                    </p>
                    {prod.status && (
                      <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">
                        {prod.status.replace(/_/g, ' ')}
                      </p>
                    )}
                  </div>
                  <p className="text-sm font-bold text-gray-900 dark:text-gray-100">
                    ${((prod.budgetTotal ?? prod.budget ?? 0) / 1000).toFixed(0)}k
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 p-5 border-t border-gray-200 dark:border-gray-700
                       bg-white dark:bg-gray-800">
          <button
            onClick={() => { onClose(); navigate('/jurisdictions'); }}
            className="w-full flex items-center justify-center gap-2 rounded-lg
                       bg-accent-blue text-white py-2.5 text-sm font-bold
                       hover:bg-accent-blue/90 transition-colors"
          >
            View All Jurisdictions
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );

  return createPortal(panel, document.body);
});

JurisdictionMapPanel.displayName = 'JurisdictionMapPanel';
export default JurisdictionMapPanel;

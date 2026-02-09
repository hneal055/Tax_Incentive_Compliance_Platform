import React, { useEffect, useRef, useCallback } from 'react';
import { MapPin, Globe, Building2, Percent, DollarSign, Info } from 'lucide-react';
import Card from '../components/Card';
import Spinner from '../components/Spinner';
import EmptyState from '../components/EmptyState';
import IncentiveTicker from '../components/IncentiveTicker';
import { useAppStore } from '../store';

const fmtCurrency = (n: number) =>
  `$${n.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;

const Jurisdictions: React.FC = () => {
  const {
    jurisdictions,
    fetchJurisdictions,
    fetchDetailedRules,
    rulesByJurisdiction,
    isLoading,
  } = useAppStore();

  const cardRefs = useRef<Record<string, HTMLDivElement | null>>({});

  useEffect(() => {
    fetchJurisdictions();
    fetchDetailedRules();
  }, [fetchJurisdictions, fetchDetailedRules]);

  const scrollToJurisdiction = useCallback((id: string) => {
    const el = cardRefs.current[id];
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      el.classList.add('ring-2', 'ring-accent-blue');
      setTimeout(() => el.classList.remove('ring-2', 'ring-accent-blue'), 2000);
    }
  }, []);

  if (isLoading && jurisdictions.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  const getTypeIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'state':
      case 'province':
        return Building2;
      case 'country':
        return Globe;
      default:
        return MapPin;
    }
  };

  const getTypeBadgeColor = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'state':
      case 'province':
        return 'bg-accent-blue/20 text-accent-blue dark:bg-accent-blue/30 dark:text-accent-blue';
      case 'country':
        return 'bg-accent-emerald/20 text-accent-emerald dark:bg-accent-emerald/30 dark:text-accent-emerald';
      default:
        return 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          Jurisdictions
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          {jurisdictions.length} global jurisdictions with tax incentive programs
        </p>
      </div>

      {/* Incentive Ticker */}
      <IncentiveTicker
        jurisdictions={jurisdictions}
        rulesByJurisdiction={rulesByJurisdiction}
        onJurisdictionClick={scrollToJurisdiction}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {jurisdictions.length === 0 ? (
          <div className="col-span-full">
            <Card>
              <EmptyState
                icon={MapPin}
                title="No jurisdictions available"
                description="Jurisdiction data will be loaded from the API. Please check your connection and ensure the backend is running."
                actionLabel="Retry loading"
                onAction={fetchJurisdictions}
              />
            </Card>
          </div>
        ) : (
          jurisdictions.map((jurisdiction) => {
            const TypeIcon = getTypeIcon(jurisdiction.type);
            const rules = rulesByJurisdiction[jurisdiction.id] || [];
            const hasRules = rules.length > 0;

            return (
              <div
                key={jurisdiction.id}
                ref={(el) => { cardRefs.current[jurisdiction.id] = el; }}
                className="animate-fade-in transition-all duration-300"
              >
                <Card hoverable className="h-full">
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-gradient-to-br from-accent-blue/20 to-accent-teal/20 dark:from-accent-blue/30 dark:to-accent-teal/30 rounded-lg">
                          <TypeIcon className="h-5 w-5 text-accent-blue dark:text-accent-teal" />
                        </div>
                        <span className="text-3xl font-bold bg-gradient-to-r from-accent-blue to-accent-teal bg-clip-text text-transparent">
                          {jurisdiction.code}
                        </span>
                      </div>
                      <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getTypeBadgeColor(jurisdiction.type)}`}>
                        {jurisdiction.type}
                      </span>
                    </div>

                    <div className="space-y-2">
                      <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100">
                        {jurisdiction.name}
                      </h3>
                      <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                        <Globe className="h-4 w-4" />
                        <span>{jurisdiction.country}</span>
                      </div>
                    </div>

                    {/* Incentive Rules Section */}
                    {hasRules ? (
                      <div className="space-y-2">
                        {rules.map((rule) => (
                          <div
                            key={rule.id}
                            className="flex items-center justify-between rounded-lg bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border border-green-200 dark:border-green-800 px-3 py-2"
                          >
                            <div className="flex items-center gap-2 min-w-0">
                              <Percent className="h-3.5 w-3.5 text-green-600 dark:text-green-400 flex-shrink-0" />
                              <span className="text-xs font-medium text-green-800 dark:text-green-300 truncate">
                                {rule.ruleName}
                              </span>
                            </div>
                            <div className="flex items-center gap-2 flex-shrink-0 ml-2">
                              <span className="text-sm font-bold text-green-700 dark:text-green-300">
                                {rule.percentage || 0}%
                              </span>
                              {rule.minSpend != null && rule.minSpend > 0 && (
                                <span className="text-[10px] text-gray-500 dark:text-gray-400 flex items-center gap-0.5" title={`Minimum spend: ${fmtCurrency(rule.minSpend)}`}>
                                  <DollarSign className="h-3 w-3" />
                                  {fmtCurrency(rule.minSpend)} min
                                </span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 rounded-lg bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 px-3 py-2">
                        <Info className="h-3.5 w-3.5 text-gray-400" />
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          No active incentive programs
                        </span>
                      </div>
                    )}

                    {jurisdiction.description && jurisdiction.description !== 'string' && (
                      <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
                        {jurisdiction.description}
                      </p>
                    )}

                    {jurisdiction.website && jurisdiction.website !== 'string' && (
                      <div className="group relative inline-block">
                        <a
                          href={jurisdiction.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-xs text-accent-blue hover:underline"
                        >
                          Official Website →
                        </a>
                        {hasRules && (
                          <div className="absolute bottom-full left-0 mb-2 hidden group-hover:block z-20">
                            <div className="bg-gray-900 text-white text-xs rounded-lg px-3 py-2 whitespace-nowrap shadow-lg">
                              Current rate per our records: {rules.reduce((best, r) => Math.max(best, r.percentage || 0), 0)}%
                              <br />
                              Click to visit official source
                              <div className="absolute top-full left-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-900" />
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </Card>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default Jurisdictions;

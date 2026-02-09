import { useMemo } from 'react';
import type { Jurisdiction, IncentiveRuleDetailed } from '../types';

interface IncentiveTickerProps {
  jurisdictions: Jurisdiction[];
  rulesByJurisdiction: Record<string, IncentiveRuleDetailed[]>;
  onJurisdictionClick?: (id: string) => void;
}

interface TickerItem {
  id: string;
  code: string;
  rate: number;
  ruleName: string;
}

export default function IncentiveTicker({
  jurisdictions,
  rulesByJurisdiction,
  onJurisdictionClick,
}: IncentiveTickerProps) {
  const items = useMemo<TickerItem[]>(() => {
    return jurisdictions
      .map((j) => {
        const rules = rulesByJurisdiction[j.id];
        if (!rules?.length) return null;
        const best = rules.reduce((a, b) =>
          (b.percentage || 0) > (a.percentage || 0) ? b : a
        , rules[0]);
        return {
          id: j.id,
          code: j.code,
          rate: best.percentage || 0,
          ruleName: best.ruleName,
        };
      })
      .filter((item): item is TickerItem => item !== null);
  }, [jurisdictions, rulesByJurisdiction]);

  if (items.length === 0) return null;

  // Duplicate items for seamless loop
  const doubled = [...items, ...items];

  return (
    <div className="relative overflow-hidden rounded-lg bg-gradient-to-r from-gray-900 to-gray-800 dark:from-gray-950 dark:to-gray-900 border border-gray-700">
      <div className="flex items-center">
        <div className="flex-shrink-0 px-4 py-2.5 bg-accent-blue text-white text-xs font-bold uppercase tracking-wider z-10">
          Incentive Rates
        </div>
        <div className="overflow-hidden flex-1">
          <div
            className="flex gap-6 py-2.5 animate-marquee hover:[animation-play-state:paused] whitespace-nowrap"
            style={{
              animationDuration: `${items.length * 4}s`,
            }}
          >
            {doubled.map((item, i) => (
              <button
                key={`${item.id}-${i}`}
                type="button"
                onClick={() => onJurisdictionClick?.(item.id)}
                className="flex items-center gap-2 text-sm text-gray-300 hover:text-white transition-colors cursor-pointer flex-shrink-0"
                title={item.ruleName}
              >
                <span className="font-bold text-white">{item.code}</span>
                <span className="text-accent-teal font-semibold">{item.rate}%</span>
                <span className="text-gray-600">|</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

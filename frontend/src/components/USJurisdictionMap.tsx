import { useState, useMemo, useEffect, useCallback, memo } from 'react';
// @ts-expect-error react-simple-maps has no type declarations
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import { useAppStore } from '../store';
import { FIPS_TO_STATE_CODE, isUSStateCode, STATE_CENTROIDS } from '../utils/usStatesFips';
import { getHeatColor, NO_DATA_COLOR_LIGHT, NO_DATA_COLOR_DARK } from '../utils/colorScale';
import JurisdictionMapPanel from './JurisdictionMapPanel';
import type { Jurisdiction, IncentiveRuleDetailed } from '../types';

const GEO_URL = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

interface MapStateData {
  stateCode: string;
  jurisdiction: Jurisdiction;
  bestRate: number;
  rules: IncentiveRuleDetailed[];
  productionCount: number;
}

const USJurisdictionMap: React.FC = memo(() => {
  const {
    jurisdictions,
    productions,
    rulesByJurisdiction,
  } = useAppStore();

  const [hoveredState, setHoveredState] = useState<string | null>(null);
  const [tooltipContent, setTooltipContent] = useState('');
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const [selectedJurisdiction, setSelectedJurisdiction] = useState<Jurisdiction | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);

  // React to dark mode changes
  const [isDark, setIsDark] = useState(
    () => document.documentElement.classList.contains('dark'),
  );

  useEffect(() => {
    const observer = new MutationObserver(() => {
      setIsDark(document.documentElement.classList.contains('dark'));
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });
    return () => observer.disconnect();
  }, []);

  // Pre-compute per-state data
  const stateDataMap = useMemo<Record<string, MapStateData>>(() => {
    const map: Record<string, MapStateData> = {};
    const usJurisdictions = jurisdictions.filter(
      j => isUSStateCode(j.code) && (j.country === 'US' || j.country === 'USA'),
    );

    for (const j of usJurisdictions) {
      const rules = rulesByJurisdiction[j.id] ?? [];
      const bestRate = rules.reduce((best, r) => Math.max(best, r.percentage ?? 0), 0);
      const productionCount = productions.filter(p => p.jurisdictionId === j.id).length;
      map[j.code.toUpperCase()] = { stateCode: j.code, jurisdiction: j, bestRate, rules, productionCount };
    }
    return map;
  }, [jurisdictions, productions, rulesByJurisdiction]);

  // Non-US jurisdictions for the badge list
  const nonUSJurisdictions = useMemo(
    () => jurisdictions.filter(j => !isUSStateCode(j.code)),
    [jurisdictions],
  );

  // Production markers — only states that have productions
  const productionMarkers = useMemo(
    () => Object.entries(stateDataMap)
      .filter(([, d]) => d.productionCount > 0 && STATE_CENTROIDS[d.stateCode.toUpperCase()])
      .map(([code, d]) => ({
        code,
        coords: STATE_CENTROIDS[code] as [number, number],
        count: d.productionCount,
      })),
    [stateDataMap],
  );

  const handleStateClick = useCallback((stateCode: string) => {
    const data = stateDataMap[stateCode];
    if (data?.jurisdiction) {
      setSelectedJurisdiction(data.jurisdiction);
      setPanelOpen(true);
    }
  }, [stateDataMap]);

  const handleMouseMove = useCallback((event: React.MouseEvent) => {
    setTooltipPos({ x: event.clientX, y: event.clientY });
  }, []);

  const handleClosePanel = useCallback(() => {
    setPanelOpen(false);
    setSelectedJurisdiction(null);
  }, []);

  // Legend
  const legendItems = [
    { label: '30%+', color: getHeatColor(35, isDark) },
    { label: '25%',  color: getHeatColor(25, isDark) },
    { label: '15%',  color: getHeatColor(15, isDark) },
    { label: '5%',   color: getHeatColor(5, isDark) },
    { label: 'None', color: isDark ? NO_DATA_COLOR_DARK : NO_DATA_COLOR_LIGHT },
  ];

  return (
    <div className="rounded-xl border border-card-border bg-card-bg shadow-sm overflow-hidden">
      {/* Header + Legend */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-6 pb-2 gap-3">
        <div>
          <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100">
            US Incentive Map
          </h3>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            Click a state to view incentive details
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          {legendItems.map(item => (
            <div key={item.label} className="flex items-center gap-1.5">
              <span
                className="h-3 w-3 rounded-sm border border-gray-300 dark:border-gray-600"
                style={{ backgroundColor: item.color }}
              />
              <span className="text-[10px] text-gray-500 dark:text-gray-400">
                {item.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Map */}
      <div className="relative px-4 pb-2" onMouseMove={handleMouseMove}>
        <ComposableMap
          projection="geoAlbersUsa"
          projectionConfig={{ scale: 1000 }}
          style={{ width: '100%', height: 'auto' }}
        >
          <Geographies geography={GEO_URL}>
            {({ geographies }: { geographies: Array<{ id: string; rsmKey: string }> }) =>
              geographies.map((geo: { id: string; rsmKey: string }) => {
                const fips = String(geo.id).padStart(2, '0');
                const stateCode = FIPS_TO_STATE_CODE[fips];
                const data = stateCode ? stateDataMap[stateCode] : undefined;
                const hasJurisdiction = !!data?.jurisdiction;

                let fillColor: string;
                if (data && data.bestRate > 0) {
                  fillColor = getHeatColor(data.bestRate, isDark);
                } else {
                  fillColor = isDark ? NO_DATA_COLOR_DARK : NO_DATA_COLOR_LIGHT;
                }

                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill={hoveredState === stateCode && hasJurisdiction
                      ? (isDark ? '#60a5fa' : '#2563eb')
                      : fillColor}
                    stroke={isDark ? '#475569' : '#94a3b8'}
                    strokeWidth={hoveredState === stateCode ? 1.5 : 0.5}
                    style={{
                      default: { outline: 'none', transition: 'fill 0.2s ease' },
                      hover: { outline: 'none', cursor: hasJurisdiction ? 'pointer' : 'default' },
                      pressed: { outline: 'none' },
                    }}
                    onMouseEnter={() => {
                      if (stateCode) {
                        setHoveredState(stateCode);
                        setTooltipContent(
                          data?.jurisdiction
                            ? `${data.jurisdiction.name} (${stateCode}) — ${data.bestRate}%`
                            : stateCode,
                        );
                      }
                    }}
                    onMouseLeave={() => {
                      setHoveredState(null);
                      setTooltipContent('');
                    }}
                    onClick={() => { if (stateCode) handleStateClick(stateCode); }}
                  />
                );
              })
            }
          </Geographies>

          {/* Production markers */}
          {productionMarkers.map(({ code, coords, count }) => (
            <Marker key={code} coordinates={coords}>
              <circle r={5} fill="#3b82f6" stroke="#fff" strokeWidth={1.5} />
              {count > 1 && (
                <text
                  textAnchor="middle"
                  y={-10}
                  style={{ fontSize: 9, fontWeight: 700, fill: isDark ? '#93c5fd' : '#1d4ed8' }}
                >
                  {count}
                </text>
              )}
            </Marker>
          ))}
        </ComposableMap>

        {/* Hover tooltip */}
        {tooltipContent && (
          <div
            className="fixed z-50 px-3 py-1.5 text-xs font-medium text-white
                       bg-gray-900 dark:bg-gray-700 rounded-lg shadow-lg
                       pointer-events-none whitespace-nowrap"
            style={{ left: tooltipPos.x + 14, top: tooltipPos.y - 28 }}
          >
            {tooltipContent}
          </div>
        )}
      </div>

      {/* Non-US jurisdiction badges */}
      {nonUSJurisdictions.length > 0 && (
        <div className="px-6 pb-5 border-t border-gray-100 dark:border-gray-700 pt-4">
          <h4 className="text-xs font-semibold uppercase tracking-wide
                        text-gray-500 dark:text-gray-400 mb-3">
            International Jurisdictions
          </h4>
          <div className="flex flex-wrap gap-2">
            {nonUSJurisdictions.map(j => {
              const rules = rulesByJurisdiction[j.id] ?? [];
              const bestRate = rules.reduce((best, r) => Math.max(best, r.percentage ?? 0), 0);
              return (
                <button
                  key={j.id}
                  onClick={() => {
                    setSelectedJurisdiction(j);
                    setPanelOpen(true);
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg
                             border border-gray-200 dark:border-gray-600
                             bg-gray-50 dark:bg-gray-700/50
                             hover:border-accent-blue/40 hover:bg-accent-blue/5
                             dark:hover:border-accent-teal/40
                             transition-all text-sm cursor-pointer"
                >
                  <span className="font-bold text-gray-900 dark:text-gray-100">
                    {j.code}
                  </span>
                  {bestRate > 0 && (
                    <span className="text-accent-teal font-semibold text-xs">
                      {bestRate}%
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Detail side panel */}
      <JurisdictionMapPanel
        isOpen={panelOpen}
        onClose={handleClosePanel}
        jurisdiction={selectedJurisdiction}
        rules={selectedJurisdiction ? (rulesByJurisdiction[selectedJurisdiction.id] ?? []) : []}
        productions={productions}
      />
    </div>
  );
});

USJurisdictionMap.displayName = 'USJurisdictionMap';
export default USJurisdictionMap;

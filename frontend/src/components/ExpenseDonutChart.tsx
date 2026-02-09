import { useState, useMemo } from 'react';
import {
  PieChart,
  Pie,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from 'recharts';

type ViewMode = 'jurisdiction' | 'status';
type DonutDataPoint = { name: string; value: number; code: string; fill: string };

const COLORS = ['#3b82f6', '#14b8a6', '#f59e0b', '#ef4444', '#8b5cf6', '#6b7280'];

interface ExpenseDonutChartProps {
  jurisdictionData?: DonutDataPoint[];
  statusData?: DonutDataPoint[];
}

// Fallback sample data
const defaultJurisdictionData: DonutDataPoint[] = [
  { name: 'California', value: 1850000, code: 'CA', fill: COLORS[0] },
  { name: 'New York', value: 1420000, code: 'NY', fill: COLORS[1] },
  { name: 'Georgia', value: 980000, code: 'GA', fill: COLORS[2] },
  { name: 'Louisiana', value: 720000, code: 'LA', fill: COLORS[3] },
  { name: 'British Columbia', value: 650000, code: 'BC', fill: COLORS[4] },
  { name: 'Other', value: 880000, code: 'OT', fill: COLORS[5] },
];

const defaultStatusData: DonutDataPoint[] = [
  { name: 'Pre-Production', value: 1200000, code: 'PRE', fill: COLORS[0] },
  { name: 'Production', value: 2800000, code: 'PROD', fill: COLORS[1] },
  { name: 'Post-Production', value: 1650000, code: 'POST', fill: COLORS[2] },
  { name: 'Distribution', value: 850000, code: 'DIST', fill: COLORS[3] },
];

function formatCurrency(value: number): string {
  if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
  if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
  return `$${value}`;
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{ name: string; value: number; payload: { fill: string } }>;
}

function CustomTooltip({ active, payload }: CustomTooltipProps) {
  if (!active || !payload?.length) return null;
  const entry = payload[0];
  return (
    <div className="rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-lg">
      <div className="flex items-center gap-2 text-sm">
        <span
          className="h-3 w-3 rounded-full"
          style={{ backgroundColor: entry.payload.fill }}
        />
        <span className="font-semibold text-gray-800">{entry.name}</span>
      </div>
      <p className="mt-1 text-sm font-bold text-gray-900">
        {formatCurrency(entry.value)}
      </p>
    </div>
  );
}

export default function ExpenseDonutChart({ jurisdictionData, statusData }: ExpenseDonutChartProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('jurisdiction');
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const usingRealData = !!(
    (jurisdictionData && jurisdictionData.length > 0) ||
    (statusData && statusData.length > 0)
  );

  const jData = useMemo(() => {
    if (jurisdictionData && jurisdictionData.length > 0) return jurisdictionData;
    return defaultJurisdictionData;
  }, [jurisdictionData]);

  const sData = useMemo(() => {
    if (statusData && statusData.length > 0) return statusData;
    return defaultStatusData;
  }, [statusData]);

  const data = viewMode === 'jurisdiction' ? jData : sData;
  const total = data.reduce((acc, d) => acc + d.value, 0);

  const centerLabel = hoveredIndex !== null && data[hoveredIndex]
    ? { name: data[hoveredIndex].name, value: formatCurrency(data[hoveredIndex].value), percent: ((data[hoveredIndex].value / total) * 100).toFixed(1) + '%' }
    : { name: 'Total', value: formatCurrency(total), percent: '100%' };

  return (
    <div className="rounded-xl border border-card-border bg-card-bg p-6 shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-semibold text-gray-900">
            Expense Distribution
          </h3>
          <p className="text-xs text-gray-500 mt-0.5">
            Total: {formatCurrency(total)}
            {!usingRealData && (
              <span className="ml-2 px-1.5 py-0.5 bg-amber-100 text-amber-700 rounded text-[10px] font-semibold">
                Sample Data
              </span>
            )}
          </p>
        </div>
        {/* View toggle */}
        <div className="flex rounded-lg border border-gray-200 bg-gray-50 p-0.5">
          <button
            type="button"
            onClick={() => { setViewMode('jurisdiction'); setHoveredIndex(null); }}
            className={`rounded-md px-3 py-1.5 text-xs font-semibold transition-all ${
              viewMode === 'jurisdiction'
                ? 'tab-active'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Jurisdiction
          </button>
          <button
            type="button"
            onClick={() => { setViewMode('status'); setHoveredIndex(null); }}
            className={`rounded-md px-3 py-1.5 text-xs font-semibold transition-all ${
              viewMode === 'status'
                ? 'tab-active'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Status
          </button>
        </div>
      </div>

      {/* Donut chart with center label */}
      <div className="h-64 relative">
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none" style={{ marginBottom: 24 }}>
          <div className="text-center">
            <p className="text-sm font-bold text-gray-900">{centerLabel.name}</p>
            <p className="text-xs text-gray-500">{centerLabel.value}</p>
            <p className="text-[10px] text-gray-400">{centerLabel.percent}</p>
          </div>
        </div>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={90}
              dataKey="value"
              nameKey="name"
              paddingAngle={2}
              stroke="none"
              onMouseEnter={(_, index) => setHoveredIndex(index)}
              onMouseLeave={() => setHoveredIndex(null)}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              iconType="circle"
              iconSize={8}
              layout="horizontal"
              verticalAlign="bottom"
              wrapperStyle={{ fontSize: 11, paddingTop: 8 }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Breakdown list */}
      <div className="mt-4 space-y-2">
        {data.map((item, index) => (
          <div
            key={item.code}
            className={`flex items-center justify-between rounded-lg px-3 py-2 text-sm transition-colors cursor-pointer ${
              hoveredIndex === index ? 'bg-gray-50' : 'hover:bg-gray-50'
            }`}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <div className="flex items-center gap-2">
              <span
                className="h-2.5 w-2.5 rounded-full"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              />
              <span className="text-gray-700 font-medium">{item.name}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-gray-500 text-xs">
                {((item.value / total) * 100).toFixed(1)}%
              </span>
              <span className="font-semibold text-gray-900">
                {formatCurrency(item.value)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

import { useState, useMemo } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

type TimePeriod = 'week' | 'month' | 'year';

type ChartDataPoint = { name: string; expenses: number; credits: number };

interface MonthlyBarChartProps {
  monthlyData?: ChartDataPoint[];
}

// Fallback sample data generators
function generateWeeklyData(): ChartDataPoint[] {
  return [
    { name: 'Mon', expenses: 45000, credits: 18000 },
    { name: 'Tue', expenses: 52000, credits: 22000 },
    { name: 'Wed', expenses: 38000, credits: 15000 },
    { name: 'Thu', expenses: 61000, credits: 28000 },
    { name: 'Fri', expenses: 55000, credits: 24000 },
    { name: 'Sat', expenses: 32000, credits: 12000 },
    { name: 'Sun', expenses: 28000, credits: 10000 },
  ];
}

function generateMonthlyData(): ChartDataPoint[] {
  return [
    { name: 'Jan', expenses: 320000, credits: 128000 },
    { name: 'Feb', expenses: 280000, credits: 112000 },
    { name: 'Mar', expenses: 450000, credits: 180000 },
    { name: 'Apr', expenses: 390000, credits: 156000 },
    { name: 'May', expenses: 520000, credits: 208000 },
    { name: 'Jun', expenses: 480000, credits: 192000 },
    { name: 'Jul', expenses: 610000, credits: 244000 },
    { name: 'Aug', expenses: 550000, credits: 220000 },
    { name: 'Sep', expenses: 470000, credits: 188000 },
    { name: 'Oct', expenses: 590000, credits: 236000 },
    { name: 'Nov', expenses: 530000, credits: 212000 },
    { name: 'Dec', expenses: 620000, credits: 248000 },
  ];
}

function generateYearlyData(): ChartDataPoint[] {
  return [
    { name: '2020', expenses: 2800000, credits: 1120000 },
    { name: '2021', expenses: 3500000, credits: 1400000 },
    { name: '2022', expenses: 4200000, credits: 1680000 },
    { name: '2023', expenses: 5100000, credits: 2040000 },
    { name: '2024', expenses: 5800000, credits: 2320000 },
    { name: '2025', expenses: 6400000, credits: 2560000 },
  ];
}

function formatCurrency(value: number): string {
  if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
  if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
  return `$${value}`;
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{ value: number; name: string; color: string }>;
  label?: string;
}

function CustomTooltip({ active, payload, label }: CustomTooltipProps) {
  if (!active || !payload) return null;
  return (
    <div className="rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-lg">
      <p className="text-xs font-semibold text-gray-700 mb-2">{label}</p>
      {payload.map((entry, i) => (
        <div key={i} className="flex items-center gap-2 text-xs">
          <span
            className="h-2.5 w-2.5 rounded-full"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-gray-500">{entry.name}:</span>
          <span className="font-semibold text-gray-800">
            {formatCurrency(entry.value)}
          </span>
        </div>
      ))}
    </div>
  );
}

export default function MonthlyBarChart({ monthlyData }: MonthlyBarChartProps) {
  const [period, setPeriod] = useState<TimePeriod>('month');
  const usingRealData = !!monthlyData && monthlyData.length > 0;

  const data = useMemo(() => {
    if (usingRealData && period === 'month') return monthlyData;
    switch (period) {
      case 'week':
        return generateWeeklyData();
      case 'year':
        return generateYearlyData();
      default:
        return generateMonthlyData();
    }
  }, [period, monthlyData, usingRealData]);

  const tabs: { key: TimePeriod; label: string }[] = [
    { key: 'week', label: 'Week' },
    { key: 'month', label: 'Month' },
    { key: 'year', label: 'Year' },
  ];

  return (
    <div className="rounded-xl border border-card-border bg-card-bg p-6 shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-base font-semibold text-gray-900">
            Monthly Overview
          </h3>
          <p className="text-xs text-gray-500 mt-0.5">
            Expenses vs Credits Awarded
            {!usingRealData && (
              <span className="ml-2 px-1.5 py-0.5 bg-amber-100 text-amber-700 rounded text-[10px] font-semibold">
                Sample Data
              </span>
            )}
          </p>
        </div>
        {/* Period tabs */}
        <div className="flex rounded-lg border border-gray-200 bg-gray-50 p-0.5">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              type="button"
              onClick={() => setPeriod(tab.key)}
              className={`rounded-md px-4 py-1.5 text-xs font-semibold transition-all ${
                period === tab.key
                  ? 'tab-active'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Chart */}
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 10, left: 10, bottom: 5 }}
            barGap={4}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis
              dataKey="name"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#94a3b8' }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: '#94a3b8' }}
              tickFormatter={formatCurrency}
              width={60}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f8fafc' }} />
            <Legend
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ paddingTop: 16, fontSize: 12 }}
            />
            <Bar
              dataKey="expenses"
              name="Expenses"
              fill="#3b82f6"
              radius={[4, 4, 0, 0]}
              maxBarSize={40}
            />
            <Bar
              dataKey="credits"
              name="Credits Awarded"
              fill="#14b8a6"
              radius={[4, 4, 0, 0]}
              maxBarSize={40}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

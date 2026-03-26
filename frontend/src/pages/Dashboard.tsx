import { useState, useEffect } from 'react';
import { Wallet, TrendingUp, Users, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { Production } from '../types';
import api from '../api';

function fmtMoney(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

export default function Dashboard() {
  const [productions, setProductions] = useState<Production[]>([]);

  useEffect(() => {
    api.productions.list().then(setProductions).catch(() => {});
  }, []);

  // ── Derived metrics ──────────────────────────────────────────────────────────
  const totalBudget  = productions.reduce((s, p) => s + (p.budgetTotal ?? 0), 0);
  const estCredits   = totalBudget * 0.25;
  const activeCount  = productions.filter(p => ['production', 'pre_production'].includes(p.status)).length;
  const alertCount   = productions.filter(p => p.status === 'planning').length;

  const metrics = [
    { title: 'Budget Volume',    value: fmtMoney(totalBudget), subtitle: 'Total planned',        icon: Wallet,      iconClass: 'bg-blue-500'    },
    { title: 'Est. Tax Credits', value: fmtMoney(estCredits),  subtitle: 'Avg 25% rate',         icon: TrendingUp,  iconClass: 'bg-emerald-500' },
    { title: 'Active Projects',  value: String(activeCount),   subtitle: 'Tracked productions',  icon: Users,       iconClass: 'bg-violet-500'  },
    { title: 'Alerts',           value: String(alertCount),    subtitle: 'Action required',      icon: AlertCircle, iconClass: 'bg-orange-500'  },
  ];

  // ── Chart data — top 5 by budget ─────────────────────────────────────────────
  const chartData = [...productions]
    .sort((a, b) => b.budgetTotal - a.budgetTotal)
    .slice(0, 5)
    .map(p => ({
      name:   p.title.length > 16 ? p.title.slice(0, 14) + '…' : p.title,
      budget: parseFloat((p.budgetTotal / 1_000_000).toFixed(2)),
      actual: 0,
    }));

  const maxBudget = chartData.length ? Math.max(...chartData.map(d => d.budget)) : 20;
  const yMax      = Math.ceil(maxBudget / 4) * 4 || 20;
  const yTicks    = Array.from({ length: 5 }, (_, i) => parseFloat(((yMax / 4) * i).toFixed(2)));

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-[28px] font-bold text-slate-900 tracking-tight">
          Executive Dashboard
        </h1>
        <p className="text-slate-500 mt-1.5 text-[15px]">
          Overview of active productions and tax incentive performance.
        </p>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div
              key={metric.title}
              className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-slate-500 text-sm font-medium">{metric.title}</p>
                  <p className="text-[32px] font-bold text-slate-900 mt-2 leading-none tracking-tight">
                    {metric.value}
                  </p>
                  <p className="text-[13px] text-slate-400 mt-2 font-medium">{metric.subtitle}</p>
                </div>
                <div
                  className={`w-12 h-12 rounded-xl flex items-center justify-center text-white shrink-0 ${metric.iconClass}`}
                >
                  <Icon className="w-5 h-5" strokeWidth={2} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Budget vs. Actual Spend Chart */}
      <div className="bg-white rounded-2xl p-8 shadow-sm border border-slate-100">
        <h2 className="text-lg font-bold text-slate-900 mb-7">Budget vs. Actual Spend</h2>

        {chartData.length === 0 ? (
          <div className="h-[380px] flex items-center justify-center text-slate-400 text-sm">
            No productions yet — add one to see chart data.
          </div>
        ) : (
          <div className="h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
                barCategoryGap="35%"
                barGap={3}
              >
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis
                  dataKey="name"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#64748b', fontSize: 13 }}
                  dy={10}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#64748b', fontSize: 13 }}
                  tickFormatter={(v) => `$${v}M`}
                  domain={[0, yMax]}
                  ticks={yTicks}
                />
                <Tooltip
                  cursor={{ fill: 'rgba(148,163,184,0.08)' }}
                  formatter={(value: unknown) => [`$${Number(value)}M`, '']}
                  contentStyle={{
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                    fontSize: 13,
                  }}
                />
                <Bar dataKey="budget" fill="#38bdf8" radius={[4, 4, 0, 0]} barSize={52} name="Budget" />
                <Bar dataKey="actual" fill="#818cf8" radius={[4, 4, 0, 0]} barSize={52} name="Actual"  />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );


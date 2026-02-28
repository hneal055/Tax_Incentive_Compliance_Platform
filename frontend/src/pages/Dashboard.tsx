import { Wallet, TrendingUp, Users, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const metrics = [
  {
    title: 'Budget Volume',
    value: '$23.5M',
    subtitle: 'Total planned',
    icon: Wallet,
    iconClass: 'bg-blue-500',
  },
  {
    title: 'Est. Tax Credits',
    value: '$3.5M',
    subtitle: 'Avg 25% rate',
    icon: TrendingUp,
    iconClass: 'bg-emerald-500',
  },
  {
    title: 'Active Projects',
    value: '3',
    subtitle: 'Tracked productions',
    icon: Users,
    iconClass: 'bg-violet-500',
  },
  {
    title: 'Alerts',
    value: '3',
    subtitle: 'Action required',
    icon: AlertCircle,
    iconClass: 'bg-orange-500',
  },
];

const chartData = [
  { name: 'The Silent Hori...', budget: 15.5, actual: 8.5 },
  { name: 'Echoes of Midni...', budget: 8.0, actual: 0 },
  { name: 'Neon Pulse',         budget: 0.5, actual: 0 },
];

function Dashboard() {
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
                domain={[0, 16]}
                ticks={[0, 4, 8, 12, 16]}
              />
              <Tooltip
                cursor={{ fill: 'rgba(148,163,184,0.08)' }}
                formatter={(value: number) => [`$${value}M`, '']}
                contentStyle={{
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  fontSize: 13,
                }}
              />
              <Bar dataKey="budget" fill="#38bdf8" radius={[4, 4, 0, 0]} barSize={52} name="Budget" />
              <Bar dataKey="actual" fill="#818cf8" radius={[4, 4, 0, 0]} barSize={52} name="Actual" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

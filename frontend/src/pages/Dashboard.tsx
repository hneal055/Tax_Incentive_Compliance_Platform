import { useEffect, useMemo } from 'react';
import {
  Clapperboard,
  Globe,
  DollarSign,
  Award,
  ShieldCheck,
  ArrowUpRight,
  ArrowDownRight,
  TrendingUp,
  Clock,
  CheckCircle2,
  AlertCircle,
  ChevronRight,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../store';
import TopBar from '../components/TopBar';
import MonthlyBarChart from '../components/MonthlyBarChart';
import ExpenseDonutChart from '../components/ExpenseDonutChart';
import Spinner from '../components/Spinner';

// ─── Metric Card ────────────────────────────────────────────────
interface MetricProps {
  label: string;
  value: string;
  icon: React.ElementType;
  color: string;
  bgColor: string;
  trend: string;
  trendUp: boolean;
}

function MetricCard({ label, value, icon: Icon, color, bgColor, trend, trendUp }: MetricProps) {
  return (
    <div className="metric-card rounded-xl border border-card-border bg-card-bg p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div className={`flex h-11 w-11 items-center justify-center rounded-lg ${bgColor}`}>
          <Icon className={`h-5 w-5 ${color}`} />
        </div>
        <div
          className={`flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-bold ${
            trendUp
              ? 'bg-green-50 text-status-active'
              : 'bg-red-50 text-status-error'
          }`}
        >
          {trendUp ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
          {trend}
        </div>
      </div>
      <p className="mt-4 text-2xl font-extrabold text-gray-900">{value}</p>
      <p className="mt-1 text-xs font-medium uppercase tracking-wider text-gray-500">
        {label}
      </p>
    </div>
  );
}

// ─── Compliance Card ────────────────────────────────────────────
function ComplianceCard() {
  const navigate = useNavigate();
  return (
    <div className="rounded-xl bg-gradient-to-br from-accent-blue via-blue-600 to-blue-700 p-6 text-white shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <ShieldCheck className="h-5 w-5 text-blue-200" />
        <p className="text-xs font-bold uppercase tracking-widest text-blue-200">
          Compliance Status
        </p>
      </div>
      <div className="flex items-end gap-3">
        <p className="text-5xl font-black leading-none">98.2%</p>
        <div className="mb-1 flex items-center gap-1 text-green-300">
          <ArrowUpRight className="h-4 w-4" />
          <span className="text-sm font-bold">+0.5%</span>
        </div>
      </div>
      <p className="mt-2 text-sm text-blue-200/80">
        All productions are meeting compliance thresholds
      </p>
      {/* Mini progress bar */}
      <div className="mt-4 h-2 rounded-full bg-white/20">
        <div
          className="h-2 rounded-full bg-white/80 transition-all duration-700"
          style={{ width: '98.2%' }}
        />
      </div>
      <button
        type="button"
        onClick={() => navigate('/reports')}
        className="mt-5 w-full rounded-lg bg-white/20 py-2.5 text-sm font-bold backdrop-blur-sm hover:bg-white/30 transition-colors"
      >
        View Full Report
      </button>
    </div>
  );
}

// ─── Recent Activity ────────────────────────────────────────────
function RecentActivity() {
  const activities = [
    { action: 'Audit Completed', project: 'Project Phoenix', time: '2h ago', icon: CheckCircle2, color: 'text-status-active', bgColor: 'bg-green-50' },
    { action: 'Incentive Updated', project: 'Desert Storm', time: '4h ago', icon: Clock, color: 'text-accent-blue', bgColor: 'bg-blue-50' },
    { action: 'Flag Raised', project: 'Neon Nights', time: '6h ago', icon: AlertCircle, color: 'text-status-error', bgColor: 'bg-red-50' },
    { action: 'Budget Approved', project: 'Arctic Venture', time: '8h ago', icon: TrendingUp, color: 'text-accent-teal', bgColor: 'bg-teal-50' },
  ];

  return (
    <div className="rounded-xl border border-card-border bg-card-bg p-6 shadow-sm">
      <h3 className="text-base font-semibold text-gray-900 mb-4">
        Recent Activity
      </h3>
      <div className="space-y-4">
        {activities.map((a, i) => (
          <div key={i} className="flex items-start gap-3">
            <div className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${a.bgColor}`}>
              <a.icon className={`h-4 w-4 ${a.color}`} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-gray-900">{a.action}</p>
              <p className="text-xs text-gray-500">
                {a.project} &bull; {a.time}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Quick Production List ──────────────────────────────────────
function QuickProductionList() {
  const { productions, selectProduction } = useAppStore();
  const navigate = useNavigate();

  const handleView = (id: string) => {
    const prod = productions.find((p) => p.id === id);
    if (prod) {
      selectProduction(prod);
      navigate('/productions');
    }
  };

  return (
    <div className="rounded-xl border border-card-border bg-card-bg p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-gray-900">
          Top Productions
        </h3>
        <button
          type="button"
          onClick={() => navigate('/productions')}
          className="text-xs font-semibold text-accent-blue hover:text-accent-blue/80 transition-colors"
        >
          View All
        </button>
      </div>
      <div className="space-y-2">
        {productions.slice(0, 5).map((prod) => (
          <div
            key={prod.id}
            className="flex items-center justify-between rounded-lg border border-gray-100 p-3 hover:border-accent-blue/40 hover:bg-accent-blue/5 transition-all cursor-pointer group"
            onClick={() => handleView(prod.id)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => { if (e.key === 'Enter') handleView(prod.id); }}
          >
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gray-100 text-sm font-bold text-gray-500">
                {prod.title.charAt(0)}
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-900">{prod.title}</p>
                <p className="text-[11px] text-gray-500">{prod.productionCompany || 'No company'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden text-right sm:block">
                <p className="text-sm font-bold text-gray-900">
                  ${((prod.budgetTotal || prod.budget || 0) / 1000).toFixed(0)}k
                </p>
                <p className="text-[10px] uppercase font-bold text-gray-400">Budget</p>
              </div>
              <ChevronRight className="h-4 w-4 text-gray-300 group-hover:text-accent-blue transition-colors" />
            </div>
          </div>
        ))}
        {productions.length === 0 && (
          <p className="py-8 text-center text-sm text-gray-400">
            No productions found
          </p>
        )}
      </div>
    </div>
  );
}

// ─── Main Dashboard ─────────────────────────────────────────────
export default function Dashboard() {
  const {
    productions,
    jurisdictions,
    fetchProductions,
    fetchJurisdictions,
    isLoading,
  } = useAppStore();

  useEffect(() => {
    fetchProductions();
    fetchJurisdictions();
  }, [fetchProductions, fetchJurisdictions]);

  const stats: MetricProps[] = useMemo(() => {
    const totalBudget = productions.reduce(
      (acc, p) => acc + (p.budgetTotal || p.budget || 0),
      0
    );
    const estimatedCredits = totalBudget * 0.4;

    return [
      {
        label: 'Total Productions',
        value: productions.length.toString(),
        icon: Clapperboard,
        color: 'text-accent-blue',
        bgColor: 'bg-blue-50',
        trend: '+12%',
        trendUp: true,
      },
      {
        label: 'Total Jurisdictions',
        value: jurisdictions.length.toString(),
        icon: Globe,
        color: 'text-purple-600',
        bgColor: 'bg-purple-50',
        trend: '+3',
        trendUp: true,
      },
      {
        label: 'Total Expenses',
        value: totalBudget >= 1000000
          ? `$${(totalBudget / 1000000).toFixed(1)}M`
          : `$${(totalBudget / 1000).toFixed(0)}K`,
        icon: DollarSign,
        color: 'text-accent-teal',
        bgColor: 'bg-teal-50',
        trend: '+8.2%',
        trendUp: true,
      },
      {
        label: 'Credits Awarded',
        value: estimatedCredits >= 1000000
          ? `$${(estimatedCredits / 1000000).toFixed(1)}M`
          : `$${(estimatedCredits / 1000).toFixed(0)}K`,
        icon: Award,
        color: 'text-amber-600',
        bgColor: 'bg-amber-50',
        trend: '+5.4%',
        trendUp: true,
      },
    ];
  }, [productions, jurisdictions]);

  if (isLoading && productions.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <TopBar
        title="Dashboard"
        subtitle={`Monitoring ${productions.length} production${productions.length !== 1 ? 's' : ''} across ${jurisdictions.length} jurisdiction${jurisdictions.length !== 1 ? 's' : ''}`}
      />

      <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
        {/* ── Row 1: Metric cards ── */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
          {stats.map((stat) => (
            <MetricCard key={stat.label} {...stat} />
          ))}
        </div>

        {/* ── Row 2: Charts + Compliance ── */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2">
            <MonthlyBarChart />
          </div>
          <ComplianceCard />
        </div>

        {/* ── Row 3: Donut chart + Activity + Productions ── */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <ExpenseDonutChart />
          <RecentActivity />
          <QuickProductionList />
        </div>
      </div>
    </div>
  );
}

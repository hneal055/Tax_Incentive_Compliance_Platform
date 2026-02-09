import { useEffect, useMemo } from 'react';
import {
  Clapperboard,
  Globe,
  DollarSign,
  Award,
  ShieldCheck,
  ArrowUpRight,
  CheckCircle2,
  Clock,
  AlertCircle,
  TrendingUp,
  ChevronRight,
  Info,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../store';
import TopBar from '../components/TopBar';
import MetricCard from '../components/MetricCard';
import MonthlyBarChart from '../components/MonthlyBarChart';
import ExpenseDonutChart from '../components/ExpenseDonutChart';
import Spinner from '../components/Spinner';

const DONUT_COLORS = ['#3b82f6', '#14b8a6', '#f59e0b', '#ef4444', '#8b5cf6', '#6b7280'];

// ─── Helpers ─────────────────────────────────────────────────
function formatCurrency(value: number): string {
  if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
  if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
  return `$${value}`;
}

function relativeTime(dateStr: string): string {
  const now = Date.now();
  const then = new Date(dateStr).getTime();
  const diffMs = now - then;
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return 'Just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffH = Math.floor(diffMin / 60);
  if (diffH < 24) return `${diffH}h ago`;
  const diffD = Math.floor(diffH / 24);
  return `${diffD}d ago`;
}

// ─── Compliance Card ────────────────────────────────────────
function ComplianceCard({ rate }: { rate: number | null }) {
  const navigate = useNavigate();
  const displayRate = rate !== null ? rate.toFixed(1) : 'N/A';
  const barWidth = rate !== null ? `${rate}%` : '0%';

  return (
    <div className="rounded-xl bg-gradient-to-br from-accent-blue via-blue-600 to-blue-700 p-6 text-white shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <ShieldCheck className="h-5 w-5 text-blue-200" />
        <p className="text-xs font-bold uppercase tracking-widest text-blue-200">
          Compliance Status
        </p>
      </div>
      <div className="flex items-end gap-3">
        <p className="text-5xl font-black leading-none">
          {rate !== null ? `${displayRate}%` : 'N/A'}
        </p>
        {rate !== null && rate >= 90 && (
          <div className="mb-1 flex items-center gap-1 text-green-300">
            <ArrowUpRight className="h-4 w-4" />
            <span className="text-sm font-bold">Good</span>
          </div>
        )}
      </div>
      <p className="mt-2 text-sm text-blue-200/80">
        {rate === null
          ? 'No productions with assigned jurisdictions yet'
          : rate >= 90
            ? 'All productions are meeting compliance thresholds'
            : 'Some productions may not meet minimum spend requirements'}
      </p>
      <div className="mt-4 h-2 rounded-full bg-white/20">
        <div
          className="h-2 rounded-full bg-white/80 transition-all duration-700"
          style={{ width: barWidth }}
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

// ─── Recent Activity ────────────────────────────────────────
function RecentActivity() {
  const { monitoringEvents } = useAppStore();

  const iconMap: Record<string, { icon: React.ElementType; color: string; bgColor: string }> = {
    rate_change: { icon: TrendingUp, color: 'text-accent-teal', bgColor: 'bg-teal-50' },
    new_program: { icon: CheckCircle2, color: 'text-status-active', bgColor: 'bg-green-50' },
    expiring_soon: { icon: Clock, color: 'text-accent-blue', bgColor: 'bg-blue-50' },
    compliance_alert: { icon: AlertCircle, color: 'text-status-error', bgColor: 'bg-red-50' },
  };

  const severityMap: Record<string, { color: string; bgColor: string }> = {
    info: { color: 'text-accent-blue', bgColor: 'bg-blue-50' },
    warning: { color: 'text-status-warning', bgColor: 'bg-amber-50' },
    critical: { color: 'text-status-error', bgColor: 'bg-red-50' },
  };

  const events = monitoringEvents.slice(0, 5);

  return (
    <div className="rounded-xl border border-card-border bg-card-bg p-6 shadow-sm">
      <h3 className="text-base font-semibold text-gray-900 mb-4">
        Recent Activity
      </h3>
      {events.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-gray-400">
          <Info className="h-8 w-8 mb-2 opacity-40" />
          <p className="text-sm">No recent activity</p>
          <p className="text-xs mt-1">Monitoring events will appear here</p>
        </div>
      ) : (
        <div className="space-y-4">
          {events.map((event) => {
            const mapping = iconMap[event.eventType] || severityMap[event.severity] || { color: 'text-gray-500', bgColor: 'bg-gray-50' };
            const IconComp = iconMap[event.eventType]?.icon || Info;
            return (
              <div key={event.id} className="flex items-start gap-3">
                <div className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${mapping.bgColor}`}>
                  <IconComp className={`h-4 w-4 ${mapping.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-gray-900">{event.title}</p>
                  <p className="text-xs text-gray-500">
                    {event.summary ? `${event.summary.slice(0, 50)}${event.summary.length > 50 ? '...' : ''}` : event.eventType}
                    {' '}&bull; {relativeTime(event.detectedAt)}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ─── Quick Production List ──────────────────────────────────
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

// ─── Main Dashboard ─────────────────────────────────────────
export default function Dashboard() {
  const {
    productions,
    jurisdictions,
    dashboardMetrics,
    rulesByJurisdiction,
    unreadEventCount,
    refreshAll,
    isLoading,
  } = useAppStore();

  useEffect(() => {
    refreshAll();
  }, [refreshAll]);

  // Compute chart data from real productions
  const monthlyChartData = useMemo(() => {
    if (productions.length === 0) return undefined;
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const monthMap: Record<string, { expenses: number; credits: number }> = {};
    monthNames.forEach((m) => { monthMap[m] = { expenses: 0, credits: 0 }; });

    productions.forEach((prod) => {
      const dateStr = prod.createdAt || prod.created_at;
      const budget = prod.budgetTotal || prod.budget || 0;
      if (dateStr) {
        const monthIdx = new Date(dateStr).getMonth();
        const month = monthNames[monthIdx];
        monthMap[month].expenses += budget;
        // Compute credits using real rule rate
        const jId = prod.jurisdictionId;
        if (jId && rulesByJurisdiction[jId]?.length) {
          const bestRule = rulesByJurisdiction[jId].reduce((best, rule) =>
            (rule.percentage || 0) > (best.percentage || 0) ? rule : best
          , rulesByJurisdiction[jId][0]);
          monthMap[month].credits += budget * ((bestRule.percentage || 0) / 100);
        }
      }
    });

    const result = monthNames.map((name) => ({
      name,
      expenses: Math.round(monthMap[name].expenses),
      credits: Math.round(monthMap[name].credits),
    }));
    // Only return if we have actual data
    return result.some((d) => d.expenses > 0) ? result : undefined;
  }, [productions, rulesByJurisdiction]);

  // Compute donut data from real productions
  const donutJurisdictionData = useMemo(() => {
    if (productions.length === 0) return undefined;
    const jMap: Record<string, { name: string; code: string; value: number }> = {};
    productions.forEach((prod) => {
      const budget = prod.budgetTotal || prod.budget || 0;
      const jId = prod.jurisdictionId;
      if (jId) {
        const jur = jurisdictions.find((j) => j.id === jId);
        const key = jId;
        if (!jMap[key]) {
          jMap[key] = { name: jur?.name || 'Unknown', code: jur?.code || '??', value: 0 };
        }
        jMap[key].value += budget;
      }
    });
    const entries = Object.values(jMap).sort((a, b) => b.value - a.value);
    if (entries.length === 0) return undefined;
    return entries.map((e, i) => ({
      ...e,
      fill: ['#3b82f6', '#14b8a6', '#f59e0b', '#ef4444', '#8b5cf6', '#6b7280'][i % 6],
    }));
  }, [productions, jurisdictions]);

  const donutStatusData = useMemo(() => {
    if (productions.length === 0) return undefined;
    const statusMap: Record<string, number> = {};
    productions.forEach((prod) => {
      const status = prod.status || 'Unknown';
      statusMap[status] = (statusMap[status] || 0) + (prod.budgetTotal || prod.budget || 0);
    });
    const entries = Object.entries(statusMap).sort((a, b) => b[1] - a[1]);
    if (entries.length === 0) return undefined;
    return entries.map(([name, value], i) => ({
      name: name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
      value,
      code: name.slice(0, 4).toUpperCase(),
      fill: DONUT_COLORS[i % DONUT_COLORS.length],
    }));
  }, [productions]);

  // Format metric values
  const { totalBudget, estimatedCredits, complianceRate } = dashboardMetrics;

  const formattedExpenses = totalBudget >= 1000000
    ? `$${(totalBudget / 1000000).toFixed(1)}M`
    : `$${(totalBudget / 1000).toFixed(0)}K`;

  const formattedCredits = estimatedCredits >= 1000000
    ? `$${(estimatedCredits / 1000000).toFixed(1)}M`
    : estimatedCredits > 0
      ? `$${(estimatedCredits / 1000).toFixed(0)}K`
      : '$0';

  // Detail content for each metric card
  const productionDetailContent = (
    <div className="space-y-3">
      {productions.length === 0 ? (
        <p className="text-sm text-gray-500">No productions yet.</p>
      ) : (
        productions.map((prod) => (
          <div key={prod.id} className="flex items-center justify-between p-3 rounded-lg border border-gray-100 hover:bg-gray-50">
            <div>
              <p className="text-sm font-semibold text-gray-900">{prod.title}</p>
              <p className="text-xs text-gray-500">{prod.productionCompany || 'No company'}</p>
            </div>
            <p className="text-sm font-bold text-gray-900">
              {formatCurrency(prod.budgetTotal || prod.budget || 0)}
            </p>
          </div>
        ))
      )}
    </div>
  );

  const jurisdictionDetailContent = (
    <div className="space-y-3">
      {jurisdictions.map((jur) => {
        const rules = rulesByJurisdiction[jur.id];
        const bestRate = rules?.reduce((best, r) => Math.max(best, r.percentage || 0), 0) || 0;
        return (
          <div key={jur.id} className="flex items-center justify-between p-3 rounded-lg border border-gray-100 hover:bg-gray-50">
            <div>
              <p className="text-sm font-semibold text-gray-900">{jur.name}</p>
              <p className="text-xs text-gray-500">{jur.code} - {jur.country}</p>
            </div>
            {bestRate > 0 ? (
              <span className="text-lg font-black text-accent-blue">{bestRate}%</span>
            ) : (
              <span className="text-xs text-gray-400">No rules</span>
            )}
          </div>
        );
      })}
    </div>
  );

  const creditsDetailContent = (
    <div className="space-y-3">
      {productions.filter((p) => p.jurisdictionId && rulesByJurisdiction[p.jurisdictionId]?.length).length === 0 ? (
        <p className="text-sm text-gray-500">No productions with assigned jurisdiction rules.</p>
      ) : (
        productions.map((prod) => {
          const budget = prod.budgetTotal || prod.budget || 0;
          const jId = prod.jurisdictionId;
          const rules = jId ? rulesByJurisdiction[jId] : undefined;
          if (!rules?.length) return null;
          const bestRule = rules.reduce((best, r) => (r.percentage || 0) > (best.percentage || 0) ? r : best, rules[0]);
          const credit = budget * ((bestRule.percentage || 0) / 100);
          const jur = jurisdictions.find((j) => j.id === jId);
          return (
            <div key={prod.id} className="flex items-center justify-between p-3 rounded-lg border border-gray-100 hover:bg-gray-50">
              <div>
                <p className="text-sm font-semibold text-gray-900">{prod.title}</p>
                <p className="text-xs text-gray-500">{jur?.name} ({bestRule.percentage}%)</p>
              </div>
              <p className="text-sm font-bold text-status-active">{formatCurrency(credit)}</p>
            </div>
          );
        }).filter(Boolean)
      )}
    </div>
  );

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
        onRefresh={refreshAll}
        unreadCount={unreadEventCount}
      />

      <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
        {/* Row 1: Metric cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
          <MetricCard
            title="Total Productions"
            value={productions.length}
            icon={Clapperboard}
            detailContent={productionDetailContent}
          />
          <MetricCard
            title="Total Jurisdictions"
            value={jurisdictions.length}
            icon={Globe}
            detailContent={jurisdictionDetailContent}
          />
          <MetricCard
            title="Total Expenses"
            value={formattedExpenses}
            icon={DollarSign}
            detailContent={productionDetailContent}
          />
          <MetricCard
            title="Credits Awarded"
            value={formattedCredits}
            icon={Award}
            detailContent={creditsDetailContent}
          />
        </div>

        {/* Row 2: Charts + Compliance */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2">
            <MonthlyBarChart monthlyData={monthlyChartData} />
          </div>
          <ComplianceCard rate={complianceRate} />
        </div>

        {/* Row 3: Donut chart + Activity + Productions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <ExpenseDonutChart
            jurisdictionData={donutJurisdictionData}
            statusData={donutStatusData}
          />
          <RecentActivity />
          <QuickProductionList />
        </div>
      </div>
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import { Film, MapPin, Award, Plus, Calculator, BarChart3, Settings } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import MetricCard from '../components/MetricCard';
import SystemHealth from '../components/SystemHealth';
import InsightCard from '../components/InsightCard';
import EmptyState from '../components/EmptyState';
import { useAppStore } from '../store';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { productions, jurisdictions, fetchProductions, fetchJurisdictions } = useAppStore();
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'degraded' | 'offline' | 'checking'>('checking');
  const [isLoading, setIsLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState<Date>(new Date());
  const [responseTime, setResponseTime] = useState<number | undefined>(undefined);

  const checkHealth = async () => {
    const startTime = Date.now();
    setHealthStatus('checking');
    try {
      const health = await api.health();
      const endTime = Date.now();
      setResponseTime(endTime - startTime);
      setHealthStatus(health.status === 'healthy' ? 'healthy' : 'degraded');
      setLastChecked(new Date());
    } catch {
      setHealthStatus('offline');
      setResponseTime(undefined);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        await Promise.all([
          fetchProductions(),
          fetchJurisdictions(),
          checkHealth(),
        ]);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [fetchProductions, fetchJurisdictions]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  // Calculate sample chart data for metrics
  const productionChartData = Array.from({ length: 10 }, () => ({
    value: Math.max(0, productions.length + Math.random() * 5 - 2.5),
  }));

  const jurisdictionChartData = Array.from({ length: 10 }, () => ({
    value: Math.max(0, jurisdictions.length + Math.random() * 10 - 5),
  }));

  return (
    <div className="space-y-8">
      {/* Header with System Health */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
            Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Monitoring {productions.length} production{productions.length !== 1 ? 's' : ''} across {jurisdictions.length} jurisdiction{jurisdictions.length !== 1 ? 's' : ''}
          </p>
        </div>
        <SystemHealth
          status={healthStatus}
          lastChecked={lastChecked}
          responseTime={responseTime}
          onRefresh={checkHealth}
        />
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          title="Active Productions"
          value={productions.length}
          icon={Film}
          trend="neutral"
          chartData={productionChartData}
        />

        <MetricCard
          title="Jurisdictions"
          value={jurisdictions.length}
          icon={MapPin}
          trend="neutral"
          chartData={jurisdictionChartData}
        />

        <MetricCard
          title="Tax Programs"
          value="33+"
          icon={Award}
          trend="up"
          trendValue="+3 this month"
        />
      </div>

      {/* AI Insights */}
      {productions.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <InsightCard
            type="suggestion"
            title="New Incentive Opportunities"
            description="Based on your production locations, you may qualify for 3 additional tax credit programs."
            action={{
              label: "View recommendations",
              onClick: () => navigate('/calculator'),
            }}
          />
          <InsightCard
            type="insight"
            title="Compliance Deadline Approaching"
            description="2 productions have incentive reporting deadlines within the next 30 days."
            action={{
              label: "View details",
              onClick: () => navigate('/productions'),
            }}
          />
        </div>
      )}

      {/* Quick Actions - Floating Action Toolbar */}
      <Card title="Quick Actions" className="bg-gradient-to-br from-accent-blue/5 to-accent-teal/5 dark:from-accent-blue/10 dark:to-accent-teal/10">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Button 
            variant="primary" 
            icon={Plus}
            onClick={() => navigate('/productions')}
            className="w-full h-20 text-lg"
          >
            Create Production
          </Button>
          <Button 
            variant="outline" 
            icon={Calculator}
            onClick={() => navigate('/calculator')}
            className="w-full h-20 text-lg"
          >
            Calculate Incentives
          </Button>
          <Button 
            variant="outline" 
            icon={BarChart3}
            onClick={() => navigate('/productions')}
            className="w-full h-20 text-lg"
          >
            View Reports
          </Button>
          <Button 
            variant="outline" 
            icon={Settings}
            onClick={() => {}}
            className="w-full h-20 text-lg"
          >
            Settings
          </Button>
        </div>
      </Card>

      {/* Recent Productions */}
      <Card 
        title="Recent Productions" 
        subtitle={`${productions.length} total production${productions.length !== 1 ? 's' : ''}`}
        hoverable
      >
        {productions.length === 0 ? (
          <EmptyState
            icon={Film}
            title="No productions yet"
            description="Create your first production to start tracking tax incentives and managing compliance."
            actionLabel="Create your first production"
            onAction={() => navigate('/productions')}
          />
        ) : (
          <div className="space-y-3">
            {productions.slice(0, 5).map((production) => (
              <div 
                key={production.id} 
                className="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-900/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800/50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-accent-blue/10 dark:bg-accent-teal/10 rounded-lg">
                    <Film className="h-5 w-5 text-accent-blue dark:text-accent-teal" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-gray-100">{production.title}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Budget: ${production.budget.toLocaleString()}
                    </p>
                  </div>
                </div>
                <Button size="sm" variant="ghost">
                  View Details →
                </Button>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Jurisdiction Coverage */}
      <Card 
        title="Jurisdiction Coverage" 
        subtitle="Global tax incentive programs"
        hoverable
      >
        {jurisdictions.length === 0 ? (
          <EmptyState
            icon={MapPin}
            title="No jurisdictions available"
            description="Jurisdiction data will be loaded from the API. Check your connection."
            actionLabel="Refresh data"
            onAction={checkHealth}
          />
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {jurisdictions.slice(0, 8).map((jurisdiction) => (
              <div 
                key={jurisdiction.id} 
                className="text-center p-4 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 rounded-lg hover:shadow-md transition-all border border-gray-200 dark:border-gray-700"
              >
                <p className="font-bold text-lg text-accent-blue dark:text-accent-teal">{jurisdiction.code}</p>
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">{jurisdiction.name}</p>
              </div>
            ))}
            {jurisdictions.length > 8 && (
              <div className="text-center p-4 bg-gradient-to-br from-accent-blue to-accent-teal dark:from-accent-blue/80 dark:to-accent-teal/80 text-white rounded-lg flex items-center justify-center hover:shadow-lg transition-all cursor-pointer">
                <p className="font-bold">+{jurisdictions.length - 8} more</p>
              </div>
            )}
          </div>
        )}
      </Card>
    </div>
  );
};

export default Dashboard;

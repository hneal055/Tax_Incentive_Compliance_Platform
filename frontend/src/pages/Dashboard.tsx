import React, { useEffect, useState } from 'react';
import { Film, MapPin, Award, Plus, Calculator, BarChart3, Settings, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import MetricCard from '../components/MetricCard';
import SystemHealth from '../components/SystemHealth';
import InsightCard from '../components/InsightCard';
import EmptyState from '../components/EmptyState';
import CreateProductionModal from '../components/CreateProductionModal';
import { useAppStore } from '../store';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const ZOOM_LEVELS = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2];
const DEFAULT_ZOOM_INDEX = 3; // 1.0 = 100%

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { productions, jurisdictions, fetchProductions, fetchJurisdictions } = useAppStore();
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'degraded' | 'offline' | 'checking'>('checking');
  const [isLoading, setIsLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState<Date>(new Date());
  const [responseTime, setResponseTime] = useState<number | undefined>(undefined);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [zoomIndex, setZoomIndex] = useState(() => {
    const saved = localStorage.getItem('dashboard-zoom');
    return saved ? parseInt(saved, 10) : DEFAULT_ZOOM_INDEX;
  });

  const zoom = ZOOM_LEVELS[zoomIndex];

  const handleZoomIn = () => {
    if (zoomIndex < ZOOM_LEVELS.length - 1) {
      const newIndex = zoomIndex + 1;
      setZoomIndex(newIndex);
      localStorage.setItem('dashboard-zoom', String(newIndex));
    }
  };

  const handleZoomOut = () => {
    if (zoomIndex > 0) {
      const newIndex = zoomIndex - 1;
      setZoomIndex(newIndex);
      localStorage.setItem('dashboard-zoom', String(newIndex));
    }
  };

  const handleZoomReset = () => {
    setZoomIndex(DEFAULT_ZOOM_INDEX);
    localStorage.setItem('dashboard-zoom', String(DEFAULT_ZOOM_INDEX));
  };

  const productionChartData = React.useMemo(() => 
    Array.from({ length: 10 }, (_, i) => ({
      value: Math.max(0, productions.length + ((i % 3) * 2 - 3)),
    }))
  , [productions.length]);

  const jurisdictionChartData = React.useMemo(() =>
    Array.from({ length: 10 }, (_, i) => ({
      value: Math.max(0, jurisdictions.length + ((i % 4) * 3 - 5)),
    }))
  , [jurisdictions.length]);

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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleProductionCreated = () => {
    fetchProductions();
  };

  const getBudget = (production: typeof productions[0]) => {
    return production.budgetTotal ?? production.budget ?? 0;
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-48">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Create Production Modal - outside scaled container for proper interaction */}
      <CreateProductionModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        jurisdictions={jurisdictions}
        onSuccess={handleProductionCreated}
      />
      {/* Zoom Controls - Fixed position */}
      <div className="absolute -top-1 right-0 flex items-center gap-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-1 shadow-sm z-10">
        <button
          onClick={handleZoomOut}
          disabled={zoomIndex === 0}
          className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          title="Zoom out"
        >
          <ZoomOut className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>
        <span className="text-xs font-medium text-gray-600 dark:text-gray-400 min-w-[3rem] text-center">
          {Math.round(zoom * 100)}%
        </span>
        <button
          onClick={handleZoomIn}
          disabled={zoomIndex === ZOOM_LEVELS.length - 1}
          className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          title="Zoom in"
        >
          <ZoomIn className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>
        <button
          onClick={handleZoomReset}
          className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ml-1 border-l border-gray-200 dark:border-gray-600 pl-2"
          title="Reset zoom"
        >
          <RotateCcw className="w-3.5 h-3.5 text-gray-500 dark:text-gray-400" />
        </button>
      </div>

      {/* Zoomable Content */}
      <div 
        className="origin-top-left transition-transform duration-200"
        style={{ transform: `scale(${zoom})`, width: `${100 / zoom}%` }}
      >
        <div className="space-y-3 pl-8 pr-4 py-2">
          {/* Header with System Health */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 pr-36">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
                Dashboard
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-0.5">
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
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
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

          {/* Quick Actions */}
          <Card title="Quick Actions" className="bg-gradient-to-br from-accent-blue/5 to-accent-teal/5 dark:from-accent-blue/10 dark:to-accent-teal/10">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <Button 
                variant="primary" 
                icon={Plus}
                onClick={() => setShowCreateModal(true)}
                className="w-full h-12"
              >
                Create Production
              </Button>
              <Button 
                variant="outline" 
                icon={Calculator}
                onClick={() => navigate('/calculator')}
                className="w-full h-12"
              >
                Calculate Incentives
              </Button>
              <Button 
                variant="outline" 
                icon={BarChart3}
                onClick={() => navigate('/productions')}
                className="w-full h-12"
              >
                View Reports
              </Button>
              <Button 
                variant="outline" 
                icon={Settings}
                onClick={() => {}}
                className="w-full h-12"
              >
                Settings
              </Button>
            </div>
          </Card>

          {/* Recent Productions */}
          <Card 
            title="Recent Productions" 
            subtitle={`${productions.length} total`}
            hoverable
          >
            {productions.length === 0 ? (
              <EmptyState
                icon={Film}
                title="No productions yet"
                description="Create your first production to start tracking tax incentives."
                actionLabel="Create production"
                onAction={() => setShowCreateModal(true)}
              />
            ) : (
              <div className="space-y-2">
                {productions.slice(0, 5).map((production) => (
                  <div 
                    key={production.id} 
                    className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800/50 transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <div className="p-1.5 bg-accent-blue/10 dark:bg-accent-teal/10 rounded">
                        <Film className="h-4 w-4 text-accent-blue dark:text-accent-teal" />
                      </div>
                      <div>
                        <p className="font-medium text-sm text-gray-900 dark:text-gray-100">{production.title}</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          ${getBudget(production).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <Button size="sm" variant="ghost" onClick={() => navigate(`/productions`)}>View →</Button>
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
                description="Jurisdiction data will be loaded from the API."
                actionLabel="Refresh"
                onAction={checkHealth}
              />
            ) : (
              <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
                {jurisdictions.slice(0, 11).map((jurisdiction) => (
                  <div 
                    key={jurisdiction.id} 
                    className="text-center p-2.5 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 rounded-lg hover:shadow-sm transition-all border border-gray-200 dark:border-gray-700"
                  >
                    <p className="font-bold text-sm text-accent-blue dark:text-accent-teal">{jurisdiction.code}</p>
                    <p className="text-[10px] text-gray-500 dark:text-gray-400 mt-0.5 truncate">{jurisdiction.name}</p>
                  </div>
                ))}
                {jurisdictions.length > 11 && (
                  <div className="text-center p-2.5 bg-gradient-to-br from-accent-blue to-accent-teal text-white rounded-lg flex items-center justify-center hover:shadow-md transition-all cursor-pointer">
                    <p className="font-bold text-sm">+{jurisdictions.length - 11}</p>
                  </div>
                )}
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;




import React, { useEffect, useState } from 'react';
import { 
  BarChart3, Users, Globe, Plus, 
  ArrowUpRight, ArrowDownRight, Clock, CheckCircle2, 
  AlertCircle, ChevronRight, ZoomIn, ZoomOut, RotateCcw
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import SystemHealth from '../components/SystemHealth';
import { useAppStore } from '../store';


const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { 
    productions, 
    jurisdictions, 
    fetchProductions, 
    fetchJurisdictions, 
    isLoading,
    selectProduction 
  } = useAppStore();
  
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'degraded' | 'offline' | 'checking'>('healthy');
  const [zoomLevel, setZoomLevel] = useState(() => {
    const saved = localStorage.getItem('dashboard-zoom');
    return saved ? parseFloat(saved) : 1;
  });

  const ZOOM_LEVELS = [0.75, 0.85, 1, 1.15, 1.25];
  const zoomIndex = ZOOM_LEVELS.indexOf(zoomLevel) !== -1 ? ZOOM_LEVELS.indexOf(zoomLevel) : 2;

  useEffect(() => {
    fetchProductions();
    fetchJurisdictions();
    
    const checkHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) setHealthStatus('healthy');
        else setHealthStatus('degraded');
      } catch (error) {
        setHealthStatus('offline');
      }
    };
    checkHealth();
  }, [fetchProductions, fetchJurisdictions]);

  const handleZoomIn = () => {
    if (zoomIndex < ZOOM_LEVELS.length - 1) {
      const newZoom = ZOOM_LEVELS[zoomIndex + 1];
      setZoomLevel(newZoom);
      localStorage.setItem('dashboard-zoom', newZoom.toString());
    }
  };

  const handleZoomOut = () => {
    if (zoomIndex > 0) {
      const newZoom = ZOOM_LEVELS[zoomIndex - 1];
      setZoomLevel(newZoom);
      localStorage.setItem('dashboard-zoom', newZoom.toString());
    }
  };

  const handleZoomReset = () => {
    setZoomLevel(1);
    localStorage.setItem('dashboard-zoom', '1');
  };

  const handleViewProduction = (id: string) => {
    const prod = productions.find(p => p.id === id);
    if (prod) {
      selectProduction(prod);
      navigate('/productions');
    }
  };

  if (isLoading && productions.length === 0) {
    return (
      <div className="flex justify-center items-center h-full">
        <Spinner size="lg" />
      </div>
    );
  }

  const stats = [
    { label: 'Active Productions', value: productions.filter(p => p.status === 'PRODUCTION').length.toString(), icon: BarChart3, color: 'text-accent-blue', trend: '+12%', trendUp: true },
    { label: 'Total Budget', value: `$${(productions.reduce((acc, p) => acc + (p.budgetTotal || p.budget || 0), 0) / 1000000).toFixed(1)}M`, icon: Users, color: 'text-accent-teal', trend: '+5%', trendUp: true },
    { label: 'Jurisdictions', value: jurisdictions.length.toString(), icon: Globe, color: 'text-purple-500', trend: '0%', trendUp: true },
    { label: 'Compliance Rate', value: '98.2%', icon: CheckCircle2, color: 'text-status-active', trend: '+0.5%', trendUp: true }
  ];

  return (
    <div className="relative min-h-screen">
      {/* Zoom controls — fixed position, outside any transform */}
      <div className="fixed top-20 right-6 z-50 flex items-center bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-1">
        <button
          onClick={handleZoomOut}
          disabled={zoomIndex === 0}
          className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          title="Zoom out"
        >
          <ZoomOut className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>
        <div className="px-2 text-[10px] font-bold text-gray-400 min-w-[40px] text-center">
          {Math.round(zoomLevel * 100)}%
        </div>
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

      {/* Dashboard content — uses CSS zoom (does not create stacking context like transform) */}
      <div style={{ zoom: zoomLevel }} className="transition-all duration-300">
        <div className="space-y-3 px-8 py-2">
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
            />
            <div className="flex gap-2">
              <Button onClick={() => navigate('/productions')} icon={Plus} size="sm">
                New Production
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map((stat, index) => (
              <Card key={index} className="overflow-hidden group">
                <div className="flex items-start justify-between">
                  <div className="p-2 rounded-lg bg-gray-50 dark:bg-gray-900 group-hover:scale-110 transition-transform">
                    <stat.icon className={`h-5 w-5 ${stat.color}`} />
                  </div>
                  <div className={`flex items-center gap-1 text-[10px] font-bold ${stat.trendUp ? 'text-status-active' : 'text-status-error'}`}>
                    {stat.trendUp ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
                    {stat.trend}
                  </div>
                </div>
                <div className="mt-3">
                  <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">{stat.label}</p>
                  <p className="text-2xl font-black text-gray-900 dark:text-white mt-1">{stat.value}</p>
                </div>
              </Card>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <Card title="Quick Overview" className="lg:col-span-2">
              <div className="space-y-3">
                {productions.slice(0, 5).map((prod) => (
                  <div 
                    key={prod.id} 
                    className="flex items-center justify-between p-3 rounded-xl border border-gray-100 dark:border-gray-800 hover:border-accent-blue/50 hover:bg-accent-blue/5 transition-all cursor-pointer group"
                    onClick={() => handleViewProduction(prod.id)}
                  >
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center font-bold text-gray-500">
                        {prod.title.charAt(0)}
                      </div>
                      <div>
                        <p className="font-bold text-sm text-gray-900 dark:text-white">{prod.title}</p>
                        <p className="text-xs text-gray-500">{prod.productionCompany}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right hidden sm:block">
                        <p className="font-bold text-sm text-gray-900 dark:text-white">${((prod.budgetTotal || prod.budget || 0) / 1000).toFixed(0)}k</p>
                        <p className="text-[10px] uppercase font-bold text-gray-400">Budget</p>
                      </div>
                      <ChevronRight className="h-4 w-4 text-gray-300 group-hover:text-accent-blue transition-colors" />
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800 flex justify-center">
                <Button variant="outline" size="sm" onClick={() => navigate('/productions')}>
                  View All Productions
                </Button>
              </div>
            </Card>

            <div className="space-y-4">
              <Card title="Recent Activity">
                <div className="space-y-4">
                  {[
                    { action: 'Audit Completed', project: 'Project Phoenix', time: '2h ago', icon: CheckCircle2, color: 'text-status-active' },
                    { action: 'Incentive Updated', project: 'Desert Storm', time: '4h ago', icon: Clock, color: 'text-accent-blue' },
                    { action: 'Flag Raised', project: 'Neon Nights', time: '6h ago', icon: AlertCircle, color: 'text-status-error' }
                  ].map((activity, i) => (
                    <div key={i} className="flex gap-3 items-start">
                      <div className={`mt-0.5 p-1 rounded-full ${activity.color} bg-current opacity-10`}>
                        <activity.icon className={`h-3 w-3 ${activity.color}`} />
                      </div>
                      <div>
                        <p className="text-xs font-bold text-gray-900 dark:text-white">{activity.action}</p>
                        <p className="text-[10px] text-gray-500">{activity.project} &bull; {activity.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className="bg-gradient-to-br from-accent-blue to-blue-700 text-white border-none shadow-blue-200">
                <p className="text-xs font-bold uppercase tracking-widest opacity-80">System Compliance</p>
                <div className="mt-4 flex items-end gap-2">
                  <p className="text-4xl font-black">98.2%</p>
                  <ArrowUpRight className="h-6 w-6 mb-1 text-green-300" />
                </div>
                <p className="text-xs mt-2 opacity-80">Up 0.5% from last month. Keep it up!</p>
                <button 
                  onClick={() => navigate('/reports')}
                  className="mt-6 w-full py-2 bg-white/20 hover:bg-white/30 rounded-lg text-xs font-bold transition-colors backdrop-blur-sm"
                >
                  View Full Report
                </button>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

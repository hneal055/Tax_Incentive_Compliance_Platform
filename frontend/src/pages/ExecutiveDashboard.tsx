import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Grid, Clapperboard, Calculator, Globe, Zap, Menu, X } from 'lucide-react';

interface MetricCard {
  title: string;
  value: string;
  subtitle: string;
  iconChar?: string;
}

interface ChartData {
  name: string;
  budget: number;
  actual: number;
}

export default function ExecutiveDashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const chartData: ChartData[] = [
    { name: 'The Silent Hori...', budget: 15000000, actual: 9000000 },
    { name: 'Echoes of Midni...', budget: 8000000, actual: 6000000 },
    { name: 'Neon Pulse', budget: 4000000, actual: 2000000 },
  ];

  const metrics: MetricCard[] = [
    { title: 'Budget Volume',    value: '$23.5M', subtitle: 'Total planned',        iconChar: '📋' },
    { title: 'Est. Tax Credits', value: '$3.5M',  subtitle: 'Avg 25% rate',         iconChar: '📈' },
    { title: 'Active Projects',  value: '3',      subtitle: 'Tracked productions',  iconChar: '🏢' },
    { title: 'Alerts',           value: '3',      subtitle: 'Action required',      iconChar: '⏰' },
  ];

  return (
    <div className="flex h-screen bg-white overflow-hidden">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} bg-white border-r border-gray-300 overflow-hidden transition-all duration-300`}>
        <div className="p-4 border-b border-gray-300">
          <div className="flex items-center gap-2">
            <div className="text-2xl font-bold">⊞</div>
            <h1 className="text-xl font-bold text-black">PilotForge</h1>
          </div>
        </div>

        <nav className="p-4 space-y-1 overflow-y-auto h-[calc(100vh-80px)]">
          <div className="flex items-center gap-2 px-3 py-2 text-blue-600 font-medium cursor-pointer hover:bg-gray-100">
            <Grid className="w-5 h-5" />
            <span>Dashboard</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 text-gray-700 font-medium cursor-pointer hover:bg-gray-100">
            <Clapperboard className="w-5 h-5" />
            <span>Productions</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 text-gray-700 font-medium cursor-pointer hover:bg-gray-100">
            <Calculator className="w-5 h-5" />
            <span>Incentive Calculator</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 text-gray-700 font-medium cursor-pointer hover:bg-gray-100">
            <Globe className="w-5 h-5" />
            <span>Jurisdictions</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 text-gray-700 font-medium cursor-pointer hover:bg-gray-100">
            <Zap className="w-5 h-5" />
            <span>AI Advisor</span>
            <span className="ml-auto text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded font-semibold">NEW</span>
          </div>
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-300 bg-white">
          <div className="flex items-center gap-2 px-3 py-2">
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-xs font-bold">FM</div>
            <span className="text-sm font-medium">Finance Manager</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <div className="bg-white border-b border-gray-300 px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="text-gray-600">
              {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <h1 className="text-lg font-semibold text-gray-800">PilotForge</h1>
          </div>
          <div className="flex items-center gap-4">
            <button className="px-3 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded border border-gray-300">Remix</button>
            <button className="px-3 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded border border-gray-300">Device</button>
            <button className="w-8 h-8 flex items-center justify-center text-gray-600 hover:bg-gray-100 rounded">⚡</button>
            <button className="w-8 h-8 flex items-center justify-center text-gray-600 hover:bg-gray-100 rounded">⊞</button>
          </div>
        </div>

        {/* Page Content */}
        <div className="flex-1 overflow-auto bg-gray-50">
          {/* Dashboard Header */}
          <div className="bg-white border-b border-gray-300 px-6 py-6">
            <h1 className="text-4xl font-bold text-black mb-2">Executive Dashboard</h1>
            <p className="text-gray-600">Overview of active productions and tax incentive performance.</p>
          </div>

          {/* Metrics Section */}
          <div className="p-6 space-y-4">
            {metrics.map((metric, idx) => (
              <div key={idx} className="bg-white border border-gray-300 p-6 rounded hover:shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-sm text-gray-600 font-medium">{metric.title}</p>
                    {metric.title === 'Budget Volume' && <p className="text-xs text-gray-500">FMFinance Manager</p>}
                  </div>
                  <span className="text-2xl">{metric.iconChar}</span>
                </div>
                <h3 className="text-3xl font-bold text-black mb-1">{metric.value}</h3>
                <p className="text-sm text-blue-600">{metric.subtitle}</p>
              </div>
            ))}

            {/* Chart Section */}
            <div className="bg-white border border-gray-300 p-6 rounded mt-6">
              <h2 className="text-xl font-bold text-black mb-6">Budget vs. Actual Spend</h2>

              <ResponsiveContainer width="100%
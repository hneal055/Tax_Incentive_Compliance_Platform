import { Search, Bell, Sun, Moon, RefreshCw } from 'lucide-react';
import { useState, useEffect } from 'react';
import SystemHealth from './SystemHealth';

interface TopBarProps {
  title?: string;
  subtitle?: string;
}

export default function TopBar({ title = 'Dashboard', subtitle }: TopBarProps) {
  const [darkMode, setDarkMode] = useState(() => {
    return document.documentElement.classList.contains('dark');
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'degraded' | 'offline' | 'checking'>('checking');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8080/api/v1/health');
        setHealthStatus(response.ok ? 'healthy' : 'degraded');
      } catch {
        setHealthStatus('offline');
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const toggleDarkMode = () => {
    const next = !darkMode;
    setDarkMode(next);
    document.documentElement.classList.toggle('dark', next);
    localStorage.setItem('theme', next ? 'dark' : 'light');
  };

  const refreshHealth = async () => {
    setHealthStatus('checking');
    try {
      const response = await fetch('http://127.0.0.1:8080/api/v1/health');
      setHealthStatus(response.ok ? 'healthy' : 'degraded');
    } catch {
      setHealthStatus('offline');
    }
  };

  return (
    <header className="flex items-center justify-between px-8 py-4 bg-white border-b border-card-border">
      {/* Left: page title */}
      <div>
        <h1 className="text-xl font-bold text-gray-900">{title}</h1>
        {subtitle && (
          <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>
        )}
      </div>

      {/* Right: search, health, theme, notifications */}
      <div className="flex items-center gap-4">
        {/* Search */}
        <div className="relative hidden md:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search productions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-64 rounded-lg border border-gray-200 bg-gray-50 py-2 pl-9 pr-4 text-sm text-gray-700 placeholder:text-gray-400 focus:border-accent-blue focus:outline-none focus:ring-1 focus:ring-accent-blue transition-colors"
            aria-label="Search productions"
          />
        </div>

        {/* System Health */}
        <SystemHealth status={healthStatus} onRefresh={refreshHealth} />

        {/* Theme toggle */}
        <button
          type="button"
          onClick={toggleDarkMode}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-700 transition-colors"
          aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>

        {/* Notifications */}
        <button
          type="button"
          className="relative flex h-9 w-9 items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-700 transition-colors"
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4" />
          <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-status-error text-[10px] font-bold text-white">
            3
          </span>
        </button>

        {/* Refresh */}
        <button
          type="button"
          onClick={refreshHealth}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-700 transition-colors"
          aria-label="Refresh data"
        >
          <RefreshCw className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}

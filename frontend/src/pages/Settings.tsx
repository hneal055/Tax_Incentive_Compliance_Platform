import React, { useState, useEffect, useCallback } from 'react';
import {
  Settings as SettingsIcon,
  Monitor,
  Bell,
  Server,
  Database,
  RefreshCw,
  Trash2,
  Download,
  CheckCircle2,
  XCircle,
  Loader2,
  Sun,
  Moon,
} from 'lucide-react';
import Card from '../components/Card';
import { useAppStore } from '../store';
import { useSettings } from '../hooks/useSettings';
import api from '../api';
import type { HealthStatus } from '../types';

// ─── Toggle Switch ──────────────────────────────────────────────────────
function Toggle({ checked, onChange, label }: { checked: boolean; onChange: (v: boolean) => void; label: string }) {
  return (
    <label className="flex items-center justify-between cursor-pointer group">
      <span className="text-sm text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-gray-100 transition-colors">
        {label}
      </span>
      <button
        type="button"
        role="switch"
        aria-checked={checked ? "true" : "false"}
        aria-label={label}
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          checked ? 'bg-accent-blue' : 'bg-gray-300 dark:bg-gray-600'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
            checked ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    </label>
  );
}

// ─── Section Header ─────────────────────────────────────────────────────
function SectionHeader({ icon: Icon, title, description }: {
  icon: React.ElementType;
  title: string;
  description: string;
}) {
  return (
    <div className="flex items-start gap-3 mb-5">
      <div className="p-2 bg-gradient-to-br from-accent-blue/10 to-accent-teal/10 dark:from-accent-blue/20 dark:to-accent-teal/20 rounded-lg flex-shrink-0">
        <Icon className="h-5 w-5 text-accent-blue dark:text-accent-teal" />
      </div>
      <div>
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{description}</p>
      </div>
    </div>
  );
}

// ─── Main Settings Page ─────────────────────────────────────────────────
const Settings: React.FC = () => {
  const { jurisdictions, refreshAll } = useAppStore();
  const { settings, updateSettings, resetSettings } = useSettings();

  // Health check state
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [healthLoading, setHealthLoading] = useState(false);
  const [healthError, setHealthError] = useState(false);

  // Action feedback
  const [refreshing, setRefreshing] = useState(false);
  const [exported, setExported] = useState(false);
  const [cacheCleared, setCacheCleared] = useState(false);

  const testConnection = useCallback(async () => {
    setHealthLoading(true);
    setHealthError(false);
    try {
      const result = await api.health();
      setHealth(result);
    } catch {
      setHealthError(true);
      setHealth(null);
    } finally {
      setHealthLoading(false);
    }
  }, []);

  useEffect(() => {
    testConnection();
  }, [testConnection]);

  const handleRefreshAll = async () => {
    setRefreshing(true);
    try {
      await refreshAll();
    } finally {
      setRefreshing(false);
    }
  };

  const handleClearCache = () => {
    const keys = Object.keys(localStorage).filter((k) => k.startsWith('pilotforge_'));
    keys.forEach((k) => {
      if (k !== 'pilotforge_settings') localStorage.removeItem(k);
    });
    setCacheCleared(true);
    setTimeout(() => setCacheCleared(false), 2000);
  };

  const handleExportData = () => {
    const { productions, jurisdictions: jurisdictionData, detailedRules, monitoringEvents } = useAppStore.getState();
    const data = { productions, jurisdictions: jurisdictionData, detailedRules, monitoringEvents, exportedAt: new Date().toISOString() };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `PilotForge_Export_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setExported(true);
    setTimeout(() => setExported(false), 2000);
  };

  // Dark mode toggle handler - applies to the document
  const handleDarkModeToggle = (enabled: boolean) => {
    updateSettings({ darkMode: enabled });
    if (enabled) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          Settings
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Configure your PilotForge experience
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* General Preferences */}
        <Card>
          <SectionHeader icon={SettingsIcon} title="General Preferences" description="Currency, defaults, and auto-refresh settings" />
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Currency Format
              </label>
              <select
                value={settings.currency}
                onChange={(e) => updateSettings({ currency: e.target.value })}
                aria-label="Currency Format"
                className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm px-3 py-2 focus:ring-2 focus:ring-accent-blue/40 outline-none"
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (&euro;)</option>
                <option value="GBP">GBP (&pound;)</option>
                <option value="CAD">CAD (C$)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Default Jurisdiction
              </label>
              <select
                value={settings.defaultJurisdiction}
                onChange={(e) => updateSettings({ defaultJurisdiction: e.target.value })}
                aria-label="Default Jurisdiction"
                className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm px-3 py-2 focus:ring-2 focus:ring-accent-blue/40 outline-none"
              >
                <option value="">None</option>
                {jurisdictions.map((j) => (
                  <option key={j.id} value={j.id}>{j.name} ({j.code})</option>
                ))}
              </select>
            </div>
            <Toggle checked={settings.autoRefresh} onChange={(v) => updateSettings({ autoRefresh: v })} label="Auto-refresh data" />
            {settings.autoRefresh && (
              <div>
                <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                  Refresh Interval (seconds)
                </label>
                <input
                  type="number"
                  min={10}
                  max={600}
                  value={settings.refreshInterval}
                  onChange={(e) => updateSettings({ refreshInterval: parseInt(e.target.value) || 60 })}
                  aria-label="Refresh Interval"
                  placeholder="60"
                  className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm px-3 py-2 focus:ring-2 focus:ring-accent-blue/40 outline-none"
                />
              </div>
            )}
          </div>
        </Card>

        {/* Display & Theme */}
        <Card>
          <SectionHeader icon={Monitor} title="Display & Theme" description="Appearance and layout preferences" />
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {settings.darkMode ? <Moon className="h-4 w-4 text-accent-teal" /> : <Sun className="h-4 w-4 text-amber-500" />}
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  {settings.darkMode ? 'Dark Mode' : 'Light Mode'}
                </span>
              </div>
              <button
                type="button"
                role="switch"
                aria-checked={settings.darkMode ? "true" : "false"}
                aria-label="Toggle dark mode"
                onClick={() => handleDarkModeToggle(!settings.darkMode)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.darkMode ? 'bg-accent-teal' : 'bg-gray-300 dark:bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
                    settings.darkMode ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
            <Toggle checked={settings.compactMode} onChange={(v) => updateSettings({ compactMode: v })} label="Compact mode" />
            <Toggle checked={settings.showSparklines} onChange={(v) => updateSettings({ showSparklines: v })} label="Show sparkline charts on metric cards" />
          </div>
        </Card>

        {/* Notifications */}
        <Card>
          <SectionHeader icon={Bell} title="Notifications" description="Monitoring alerts and event notifications" />
          <div className="space-y-4">
            <Toggle
              checked={settings.notificationsEnabled}
              onChange={(v) => updateSettings({ notificationsEnabled: v })}
              label="Enable monitoring notifications"
            />
            {settings.notificationsEnabled && (
              <div>
                <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
                  Severity Filters
                </label>
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.severityFilters.info}
                      onChange={(e) =>
                        updateSettings({
                          severityFilters: { ...settings.severityFilters, info: e.target.checked },
                        })
                      }
                      className="rounded border-gray-300 text-accent-blue focus:ring-accent-blue/40"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">Info</span>
                    <span className="ml-auto px-2 py-0.5 text-[10px] font-semibold rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
                      Low
                    </span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.severityFilters.warning}
                      onChange={(e) =>
                        updateSettings({
                          severityFilters: { ...settings.severityFilters, warning: e.target.checked },
                        })
                      }
                      className="rounded border-gray-300 text-accent-blue focus:ring-accent-blue/40"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">Warning</span>
                    <span className="ml-auto px-2 py-0.5 text-[10px] font-semibold rounded-full bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400">
                      Medium
                    </span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.severityFilters.critical}
                      onChange={(e) =>
                        updateSettings({
                          severityFilters: { ...settings.severityFilters, critical: e.target.checked },
                        })
                      }
                      className="rounded border-gray-300 text-accent-blue focus:ring-accent-blue/40"
                    />
                    <span className="text-sm text-gray-700 dark:text-gray-300">Critical</span>
                    <span className="ml-auto px-2 py-0.5 text-[10px] font-semibold rounded-full bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400">
                      High
                    </span>
                  </label>
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* API Configuration */}
        <Card>
          <SectionHeader icon={Server} title="API Configuration" description="Backend connection status and diagnostics" />
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                API Base URL
              </label>
              <div className="flex items-center gap-2 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/50 px-3 py-2">
                <code className="text-sm text-gray-700 dark:text-gray-300 font-mono">
                  http://127.0.0.1:8080/api/v1
                </code>
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                Connection Status
              </label>
              <div className="flex items-center gap-2 py-2">
                {healthLoading ? (
                  <Loader2 className="h-4 w-4 text-gray-400 animate-spin" />
                ) : healthError ? (
                  <XCircle className="h-4 w-4 text-red-500" />
                ) : (
                  <CheckCircle2 className="h-4 w-4 text-green-500" />
                )}
                <span className={`text-sm font-medium ${healthLoading ? 'text-gray-400' : healthError ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'}`}>
                  {healthLoading ? 'Checking...' : healthError ? 'Disconnected' : 'Connected'}
                </span>
              </div>
              {health && (
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="text-xs">
                    <span className="text-gray-500 dark:text-gray-400">Version: </span>
                    <span className="font-medium text-gray-700 dark:text-gray-300">{health.version || 'N/A'}</span>
                  </div>
                  <div className="text-xs">
                    <span className="text-gray-500 dark:text-gray-400">Database: </span>
                    <span className="font-medium text-gray-700 dark:text-gray-300">{health.database || 'N/A'}</span>
                  </div>
                  <div className="text-xs">
                    <span className="text-gray-500 dark:text-gray-400">Environment: </span>
                    <span className="font-medium text-gray-700 dark:text-gray-300">{health.environment || 'N/A'}</span>
                  </div>
                  <div className="text-xs">
                    <span className="text-gray-500 dark:text-gray-400">Status: </span>
                    <span className="font-medium text-gray-700 dark:text-gray-300">{health.status}</span>
                  </div>
                </div>
              )}
            </div>
            <button
              type="button"
              onClick={testConnection}
              disabled={healthLoading}
              className="flex items-center gap-2 text-sm font-medium text-accent-blue hover:text-accent-blue/80 transition-colors disabled:text-gray-400"
            >
              <RefreshCw className={`h-4 w-4 ${healthLoading ? 'animate-spin' : ''}`} />
              Test Connection
            </button>
          </div>
        </Card>

        {/* Data Management - full width */}
        <Card className="lg:col-span-2">
          <SectionHeader icon={Database} title="Data Management" description="Refresh, export, and clear application data" />
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={handleRefreshAll}
              disabled={refreshing}
              className="flex items-center gap-2 rounded-lg bg-accent-blue hover:bg-accent-blue/90 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white font-semibold text-sm px-5 py-2.5 transition-colors"
            >
              <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
              {refreshing ? 'Refreshing...' : 'Refresh All Data'}
            </button>
            <button
              type="button"
              onClick={handleExportData}
              className="flex items-center gap-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 font-semibold text-sm px-5 py-2.5 transition-colors"
            >
              <Download className="h-4 w-4" />
              {exported ? 'Exported!' : 'Export Data as JSON'}
            </button>
            <button
              type="button"
              onClick={handleClearCache}
              className="flex items-center gap-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 font-semibold text-sm px-5 py-2.5 transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              {cacheCleared ? 'Cache Cleared!' : 'Clear Local Cache'}
            </button>
            <button
              type="button"
              onClick={resetSettings}
              className="flex items-center gap-2 rounded-lg border border-red-300 dark:border-red-600 bg-white dark:bg-gray-700 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 font-semibold text-sm px-5 py-2.5 transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              Reset to Defaults
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Settings;

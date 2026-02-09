import { useState, useCallback } from 'react';
import type { UserSettings } from '../types';

const STORAGE_KEY = 'pilotforge_settings';

const DEFAULT_SETTINGS: UserSettings = {
  currency: 'USD',
  defaultJurisdiction: '',
  notificationsEnabled: true,
  darkMode: false,
  autoRefresh: false,
  refreshInterval: 60,
  compactMode: false,
  showSparklines: true,
  severityFilters: { info: true, warning: true, critical: true },
};

function loadSettings(): UserSettings {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return { ...DEFAULT_SETTINGS, ...JSON.parse(stored) };
    }
  } catch {
    // Corrupted data; reset
  }
  return DEFAULT_SETTINGS;
}

export function useSettings() {
  const [settings, setSettings] = useState<UserSettings>(loadSettings);

  const updateSettings = useCallback((patch: Partial<UserSettings>) => {
    setSettings((prev) => {
      const next = { ...prev, ...patch };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const resetSettings = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setSettings(DEFAULT_SETTINGS);
  }, []);

  return { settings, updateSettings, resetSettings };
}

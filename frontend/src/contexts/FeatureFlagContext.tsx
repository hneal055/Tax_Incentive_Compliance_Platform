import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import staticFlags from '../config/featureFlags';

export type Flags = {
  USE_REAL_API: boolean;
  USE_REAL_AUTH: boolean;
  MOCK_DELAY_MS: number;
  ENABLE_ANALYTICS: boolean;
  ENABLE_SENTRY: boolean;
};

// Named constants so callers avoid raw strings: useFeatureFlag(features.USE_REAL_API)
export const features = {
  USE_REAL_API:      'USE_REAL_API',
  USE_REAL_AUTH:     'USE_REAL_AUTH',
  MOCK_DELAY_MS:     'MOCK_DELAY_MS',
  ENABLE_ANALYTICS:  'ENABLE_ANALYTICS',
  ENABLE_SENTRY:     'ENABLE_SENTRY',
} as const satisfies Record<string, keyof Flags>;

// Module-level snapshot — lets api/index.ts (non-React code) read current flag values.
// Initialized from env; kept in sync by the Provider on every state change.
let _snapshot: Flags = { ...staticFlags };
export const getFlagSnapshot = (): Flags => _snapshot;

const defaultFlags: Flags = { ...staticFlags };

// Dev-only: persist panel overrides across page refreshes.
// Production builds skip this entirely (import.meta.env.DEV is tree-shaken).
const STORAGE_KEY = '__pilotforge_ff__';

function loadPersistedFlags(): Partial<Flags> {
  if (!import.meta.env.DEV) return {};
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function persistFlags(flags: Flags): void {
  if (!import.meta.env.DEV) return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(flags));
}

interface FeatureFlagContextValue {
  flags: Flags;
  toggleFlag: (key: keyof Omit<Flags, 'MOCK_DELAY_MS'>) => void;
  setFlag: <K extends keyof Flags>(key: K, value: Flags[K]) => void;
}

const FeatureFlagContext = createContext<FeatureFlagContextValue | null>(null);

export function FeatureFlagProvider({
  children,
  initialFlags = defaultFlags,
}: {
  children: ReactNode;
  initialFlags?: Flags;
}) {
  const [flags, setFlags] = useState<Flags>(() => ({
    ...initialFlags,
    ...loadPersistedFlags(), // dev panel overrides win over env defaults
  }));

  // Keep the module-level snapshot in sync and persist dev overrides
  useEffect(() => {
    _snapshot = flags;
    persistFlags(flags);
  }, [flags]);

  const toggleFlag = (key: keyof Omit<Flags, 'MOCK_DELAY_MS'>) => {
    setFlags(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const setFlag = <K extends keyof Flags>(key: K, value: Flags[K]) => {
    setFlags(prev => ({ ...prev, [key]: value }));
  };

  return (
    <FeatureFlagContext.Provider value={{ flags, toggleFlag, setFlag }}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

export function useFeatureFlags(): FeatureFlagContextValue {
  const ctx = useContext(FeatureFlagContext);
  if (!ctx) throw new Error('useFeatureFlags must be used within a FeatureFlagProvider');
  return ctx;
}

// Convenience hook for reading a single flag
export function useFeatureFlag<K extends keyof Flags>(key: K): Flags[K] {
  return useFeatureFlags().flags[key];
}

import { useState } from 'react';
import { Settings, ChevronDown, ChevronUp, Globe, FlaskConical } from 'lucide-react';
import { useFeatureFlags, features, type Flags } from '../../contexts/FeatureFlagContext';

// Only boolean flags get toggle switches
const booleanFlags: { key: keyof Omit<Flags, 'MOCK_DELAY_MS'>; label: string }[] = [
  { key: features.USE_REAL_API,     label: 'Real API'       },
  { key: features.USE_REAL_AUTH,    label: 'Real Auth'      },
  { key: features.ENABLE_ANALYTICS, label: 'Analytics'      },
  { key: features.ENABLE_SENTRY,    label: 'Sentry'         },
];

function Toggle({ on, onToggle }: { on: boolean; onToggle: () => void }) {
  return (
    <button
      role="switch"
      aria-checked={on}
      onClick={onToggle}
      className={`relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors focus:outline-none ${
        on ? 'bg-blue-500' : 'bg-slate-600'
      }`}
    >
      <span
        className={`inline-block h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
          on ? 'translate-x-4' : 'translate-x-0'
        }`}
      />
    </button>
  );
}

export function FeatureFlagPanel() {
  const { flags, toggleFlag, setFlag } = useFeatureFlags();
  const [open, setOpen] = useState(false);

  // Strip out in production builds
  if (!import.meta.env.DEV) return null;

  const isRealApi = flags[features.USE_REAL_API];

  return (
    <div className="fixed bottom-4 right-4 z-50 w-64 font-sans">
      {/* Header / toggle button */}
      <button
        onClick={() => setOpen(v => !v)}
        className="w-full flex items-center justify-between px-3 py-2 bg-[#1a1d24] border border-white/10 rounded-lg text-slate-300 text-xs font-semibold hover:border-white/20 transition-colors shadow-xl"
      >
        <span className="flex items-center gap-2">
          <Settings className="w-3.5 h-3.5" />
          Feature Flags
          {/* Compact API mode pill */}
          <span className={`flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold ${
            isRealApi ? 'bg-blue-500/20 text-blue-400' : 'bg-amber-500/20 text-amber-400'
          }`}>
            {isRealApi ? <Globe className="w-2.5 h-2.5" /> : <FlaskConical className="w-2.5 h-2.5" />}
            {isRealApi ? 'REAL' : 'MOCK'}
          </span>
        </span>
        {open ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronUp className="w-3.5 h-3.5" />}
      </button>

      {/* Expanded panel */}
      {open && (
        <div className="mt-1 bg-[#1a1d24] border border-white/10 rounded-lg shadow-xl overflow-hidden">
          {/* Boolean flag toggles */}
          <div className="px-3 py-2 space-y-2.5">
            {booleanFlags.map(({ key, label }) => (
              <div key={key} className="flex items-center justify-between">
                <span className="text-slate-400 text-xs">{label}</span>
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-medium ${flags[key] ? 'text-blue-400' : 'text-slate-500'}`}>
                    {flags[key] ? 'on' : 'off'}
                  </span>
                  <Toggle on={flags[key]} onToggle={() => toggleFlag(key)} />
                </div>
              </div>
            ))}
          </div>

          {/* MOCK_DELAY_MS — number input */}
          <div className="px-3 py-2 border-t border-white/8">
            <div className="flex items-center justify-between gap-3">
              <span className="text-slate-400 text-xs">Mock Delay</span>
              <div className="flex items-center gap-1.5">
                <input
                  type="number"
                  min={0}
                  max={3000}
                  step={100}
                  value={flags.MOCK_DELAY_MS}
                  onChange={e => setFlag('MOCK_DELAY_MS', Number(e.target.value))}
                  className="w-16 px-2 py-0.5 bg-[#13151a] border border-white/10 rounded text-xs text-white text-right focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                <span className="text-slate-500 text-[10px]">ms</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

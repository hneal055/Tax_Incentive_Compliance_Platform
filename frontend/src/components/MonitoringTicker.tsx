import { useMemo } from 'react';
import { AlertTriangle, AlertCircle, Bell, ExternalLink } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type { MonitoringEvent } from '../types';

interface MonitoringTickerProps {
  events: MonitoringEvent[];
}

const SEVERITY_CONFIG: Record<string, { icon: React.ElementType; color: string; bg: string; badge: string }> = {
  critical: { icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-100', badge: 'bg-red-500 text-white' },
  warning:  { icon: AlertTriangle, color: 'text-amber-600', bg: 'bg-amber-100', badge: 'bg-amber-500 text-white' },
  info:     { icon: Bell, color: 'text-blue-600', bg: 'bg-blue-100', badge: 'bg-blue-500 text-white' },
};

function relativeTime(dateStr: string): string {
  const diffMs = Date.now() - new Date(dateStr).getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return 'Just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffH = Math.floor(diffMin / 60);
  if (diffH < 24) return `${diffH}h ago`;
  const diffD = Math.floor(diffH / 24);
  return `${diffD}d ago`;
}

export default function MonitoringTicker({ events }: MonitoringTickerProps) {
  const navigate = useNavigate();

  // Filter to critical/warning events, prioritize unread, take top 5
  const topEvents = useMemo(() => {
    const relevant = events
      .filter((e) => e.severity === 'critical' || e.severity === 'warning')
      .sort((a, b) => {
        // Unread first
        if (!a.readAt && b.readAt) return -1;
        if (a.readAt && !b.readAt) return 1;
        // Then by severity (critical first)
        if (a.severity === 'critical' && b.severity !== 'critical') return -1;
        if (a.severity !== 'critical' && b.severity === 'critical') return 1;
        // Then most recent
        return new Date(b.detectedAt).getTime() - new Date(a.detectedAt).getTime();
      })
      .slice(0, 5);
    return relevant;
  }, [events]);

  if (topEvents.length === 0) return null;

  // Duplicate items for seamless infinite scroll
  const tickerItems = [...topEvents, ...topEvents];

  return (
    <div className="relative overflow-hidden rounded-lg border border-amber-200 bg-gradient-to-r from-amber-50 via-orange-50 to-red-50">
      {/* Left label */}
      <div className="absolute left-0 top-0 bottom-0 z-10 flex items-center px-3 bg-gradient-to-r from-amber-100 to-amber-100/80 border-r border-amber-200">
        <AlertTriangle className="h-3.5 w-3.5 text-amber-600 mr-1.5" />
        <span className="text-[11px] font-bold uppercase tracking-wider text-amber-700">
          Alerts
        </span>
      </div>

      {/* Scrolling ticker */}
      <div className="ml-[88px] mr-[90px] overflow-hidden py-2">
        <div className="flex animate-marquee whitespace-nowrap hover:[animation-play-state:paused]">
          {tickerItems.map((event, idx) => {
            const config = SEVERITY_CONFIG[event.severity] || SEVERITY_CONFIG.info;
            const Icon = config.icon;
            return (
              <button
                key={`${event.id}-${idx}`}
                type="button"
                onClick={() => navigate('/settings')}
                className="inline-flex items-center gap-2 mx-4 shrink-0 group cursor-pointer"
              >
                <span className={`inline-flex items-center justify-center h-5 w-5 rounded-full ${config.bg}`}>
                  <Icon className={`h-3 w-3 ${config.color}`} />
                </span>
                <span className={`text-[10px] font-bold uppercase px-1.5 py-0.5 rounded ${config.badge}`}>
                  {event.severity}
                </span>
                <span className="text-xs font-semibold text-gray-800 group-hover:text-accent-blue transition-colors">
                  {event.title}
                </span>
                {event.summary && (
                  <span className="text-[11px] text-gray-500 max-w-[200px] truncate">
                    — {event.summary}
                  </span>
                )}
                <span className="text-[10px] text-gray-400">
                  {relativeTime(event.detectedAt)}
                </span>
                <span className="text-gray-300">|</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Right: View all button */}
      <div className="absolute right-0 top-0 bottom-0 z-10 flex items-center px-3 bg-gradient-to-l from-red-50 to-red-50/80 border-l border-amber-200">
        <button
          type="button"
          onClick={() => navigate('/settings')}
          className="inline-flex items-center gap-1 text-[11px] font-bold text-amber-700 hover:text-amber-900 transition-colors"
        >
          View All
          <ExternalLink className="h-3 w-3" />
        </button>
      </div>
    </div>
  );
}

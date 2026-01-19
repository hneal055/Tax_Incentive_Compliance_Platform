import React from 'react';
import { Activity, Wifi, WifiOff, Clock } from 'lucide-react';
import { motion } from 'framer-motion';
import Tooltip from './Tooltip';

interface SystemHealthProps {
  status: 'healthy' | 'degraded' | 'offline' | 'checking';
  lastChecked?: Date;
  responseTime?: number;
  onRefresh?: () => void;
}

const SystemHealth: React.FC<SystemHealthProps> = ({
  status,
  lastChecked,
  responseTime,
  onRefresh,
}) => {
  const statusConfig = {
    healthy: {
      color: 'text-status-active',
      bgColor: 'bg-status-active/20',
      borderColor: 'border-status-active',
      label: 'Healthy',
      icon: Wifi,
      pulse: true,
    },
    degraded: {
      color: 'text-status-warning',
      bgColor: 'bg-status-warning/20',
      borderColor: 'border-status-warning',
      label: 'Degraded',
      icon: Activity,
      pulse: false,
    },
    offline: {
      color: 'text-status-error',
      bgColor: 'bg-status-error/20',
      borderColor: 'border-status-error',
      label: 'Offline',
      icon: WifiOff,
      pulse: false,
    },
    checking: {
      color: 'text-gray-500',
      bgColor: 'bg-gray-100 dark:bg-gray-800',
      borderColor: 'border-gray-300 dark:border-gray-700',
      label: 'Checking...',
      icon: Activity,
      pulse: true,
    },
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <div className="inline-flex items-center gap-3">
      <Tooltip content={`API Status: ${config.label}`}>
        <div className={`relative inline-flex items-center gap-2 px-3 py-1.5 rounded-full border ${config.borderColor} ${config.bgColor}`}>
          <div className="relative">
            <Icon className={`h-4 w-4 ${config.color}`} />
            {config.pulse && (
              <motion.div
                className={`absolute inset-0 rounded-full ${config.bgColor}`}
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.5, 0, 0.5],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
              />
            )}
          </div>
          <span className={`text-xs font-semibold ${config.color}`}>
            {config.label}
          </span>
        </div>
      </Tooltip>

      {responseTime !== undefined && (
        <Tooltip content="Average response time">
          <div className="flex items-center gap-1 text-xs text-gray-600 dark:text-gray-400">
            <Clock className="h-3 w-3" />
            <span>{responseTime}ms</span>
          </div>
        </Tooltip>
      )}

      {lastChecked && (
        <Tooltip content={`Last checked: ${lastChecked.toLocaleTimeString()}`}>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {getRelativeTime(lastChecked)}
          </div>
        </Tooltip>
      )}

      {onRefresh && (
        <button
          onClick={onRefresh}
          className="text-xs text-accent-blue hover:text-accent-blue/80 dark:text-accent-teal dark:hover:text-accent-teal/80 font-medium transition-colors"
          aria-label="Refresh system health"
        >
          Refresh
        </button>
      )}
    </div>
  );
};

function getRelativeTime(date: Date): string {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  
  if (seconds < 60) return 'Just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export default SystemHealth;

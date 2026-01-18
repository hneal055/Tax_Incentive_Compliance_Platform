import React, { useEffect, useState } from 'react';
import type { LucideIcon } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';

interface MetricCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  chartData?: Array<{ value: number }>;
  className?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  icon: Icon,
  trend,
  trendValue,
  chartData,
  className = '',
}) => {
  const [displayValue, setDisplayValue] = useState(0);

  // Animate number counting if value is a number
  useEffect(() => {
    if (typeof value === 'number') {
      const duration = 1000;
      const steps = 30;
      const stepValue = value / steps;
      let current = 0;

      const timer = setInterval(() => {
        current += stepValue;
        if (current >= value) {
          setDisplayValue(value);
          clearInterval(timer);
        } else {
          setDisplayValue(Math.floor(current));
        }
      }, duration / steps);

      return () => clearInterval(timer);
    }
  }, [value]);

  const trendConfig = {
    up: 'text-status-active',
    down: 'text-status-error',
    neutral: 'text-gray-500 dark:text-gray-400',
  };

  // Generate sample chart data if none provided
  const defaultChartData = chartData || Array.from({ length: 10 }, () => ({
    value: Math.random() * 100 + 50,
  }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden border border-gray-200 dark:border-gray-700 ${className}`}
    >
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
              {title}
            </p>
            <motion.p
              className="text-3xl font-bold text-gray-900 dark:text-gray-100 mt-2"
              key={displayValue}
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            >
              {typeof value === 'number' ? displayValue : value}
            </motion.p>
            {trend && trendValue && (
              <p className={`text-sm font-medium mt-1 ${trendConfig[trend]}`}>
                {trend === 'up' && '↑ '}
                {trend === 'down' && '↓ '}
                {trendValue}
              </p>
            )}
          </div>
          <div className="flex-shrink-0 p-3 bg-gradient-to-br from-accent-blue/20 to-accent-teal/20 dark:from-accent-blue/30 dark:to-accent-teal/30 rounded-lg">
            <Icon className="h-6 w-6 text-accent-blue dark:text-accent-teal" />
          </div>
        </div>

        {/* Mini chart */}
        <div className="h-16 -mx-2 -mb-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={defaultChartData}>
              <defs>
                <linearGradient id="metricGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <Area
                type="monotone"
                dataKey="value"
                stroke="#3b82f6"
                strokeWidth={2}
                fill="url(#metricGradient)"
                animationDuration={1000}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.div>
  );
};

export default MetricCard;

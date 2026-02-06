import React, { useEffect, useState, memo } from 'react';
import type { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  chartData?: Array<{ value: number }>;
  className?: string;
}

// Simple sparkline using SVG instead of recharts
const MiniChart = memo(({ data }: { data: Array<{ value: number }> }) => {
  const values = data.map(d => d.value);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = max - min || 1;
  
  const points = values.map((v, i) => {
    const x = (i / (values.length - 1)) * 100;
    const y = 100 - ((v - min) / range) * 80; // Scale to 80% height, leave padding
    return `${x},${y}`;
  }).join(' ');
  
  return (
    <svg 
      viewBox="0 0 100 100" 
      preserveAspectRatio="none" 
      className="w-full h-full"
      style={{ display: 'block' }}
    >
      <defs>
        <linearGradient id="sparklineGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon
        points={`0,100 ${points} 100,100`}
        fill="url(#sparklineGradient)"
      />
      <polyline
        points={points}
        fill="none"
        stroke="#3b82f6"
        strokeWidth="2"
        vectorEffect="non-scaling-stroke"
      />
    </svg>
  );
});

MiniChart.displayName = 'MiniChart';

const MetricCard: React.FC<MetricCardProps> = memo(({
  title,
  value,
  icon: Icon,
  trend,
  trendValue,
  chartData,
  className = '',
}) => {
  const [displayValue, setDisplayValue] = useState(typeof value === 'number' ? 0 : value);
  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    if (typeof value === 'number' && !hasAnimated) {
      const duration = 600;
      const steps = 20;
      const stepValue = value / steps;
      let current = 0;
      let step = 0;

      const timer = setInterval(() => {
        step++;
        current = Math.min(value, Math.floor(stepValue * step));
        setDisplayValue(current);
        
        if (step >= steps) {
          setDisplayValue(value);
          setHasAnimated(true);
          clearInterval(timer);
        }
      }, duration / steps);

      return () => clearInterval(timer);
    } else if (typeof value === 'number') {
      setDisplayValue(value);
    }
  }, [value, hasAnimated]);

  const trendConfig = {
    up: 'text-status-active',
    down: 'text-status-error',
    neutral: 'text-gray-500 dark:text-gray-400',
  };

  const defaultChartData = React.useMemo(() => {
    if (chartData) return chartData;
    return Array.from({ length: 10 }, (_, i) => ({
      value: 50 + (i * 5) + ((i % 3) * 10),
    }));
  }, [chartData]);

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden border border-gray-200 dark:border-gray-700 ${className}`}>
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wide">
              {title}
            </p>
            <p className="text-3xl font-bold text-gray-900 dark:text-gray-100 mt-2">
              {displayValue}
            </p>
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
      </div>
      {/* Chart container with fixed height and overflow hidden */}
      <div className="h-16 overflow-hidden">
        <MiniChart data={defaultChartData} />
      </div>
    </div>
  );
});

MetricCard.displayName = 'MetricCard';

export default MetricCard;

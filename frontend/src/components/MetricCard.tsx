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

// Simple sparkline using SVG
const MiniChart = memo(({ data }: { data: Array<{ value: number }> }) => {
  const values = data.map(d => d.value);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = max - min || 1;
  
  // Create path for the line
  const width = 200;
  const height = 40;
  const padding = 2;
  
  const points = values.map((v, i) => {
    const x = padding + (i / (values.length - 1)) * (width - padding * 2);
    const y = padding + (1 - (v - min) / range) * (height - padding * 2);
    return `${x},${y}`;
  });
  
  const linePath = `M ${points.join(' L ')}`;
  const areaPath = `${linePath} L ${width - padding},${height} L ${padding},${height} Z`;
  
  return (
    <svg 
      width="100%" 
      height="40"
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
    >
      <defs>
        <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.2" />
          <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.02" />
        </linearGradient>
      </defs>
      <path d={areaPath} fill="url(#chartGradient)" />
      <path d={linePath} fill="none" stroke="#3b82f6" strokeWidth="1.5" />
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
      <div className="p-5">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              {title}
            </p>
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-1">
              {displayValue}
            </p>
            {trend && trendValue && (
              <p className={`text-xs font-medium mt-1 ${trendConfig[trend]}`}>
                {trend === 'up' && '↑ '}
                {trend === 'down' && '↓ '}
                {trendValue}
              </p>
            )}
          </div>
          <div className="flex-shrink-0 p-2.5 bg-gradient-to-br from-accent-blue/10 to-accent-teal/10 dark:from-accent-blue/20 dark:to-accent-teal/20 rounded-lg">
            <Icon className="h-5 w-5 text-accent-blue dark:text-accent-teal" />
          </div>
        </div>
      </div>
      <div className="px-5 pb-4">
        <MiniChart data={defaultChartData} />
      </div>
    </div>
  );
});

MetricCard.displayName = 'MetricCard';

export default MetricCard;

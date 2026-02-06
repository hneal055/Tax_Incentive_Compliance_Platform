import React, { memo } from 'react';
import { Sparkles, TrendingUp, Lightbulb } from 'lucide-react';

interface InsightCardProps {
  type?: 'suggestion' | 'prediction' | 'insight';
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

const typeConfig = {
  suggestion: {
    icon: Lightbulb,
    gradient: 'from-amber-500/20 to-yellow-500/20 dark:from-amber-500/30 dark:to-yellow-500/30',
    iconColor: 'text-amber-600 dark:text-amber-400',
    borderColor: 'border-amber-200 dark:border-amber-800',
  },
  prediction: {
    icon: TrendingUp,
    gradient: 'from-purple-500/20 to-pink-500/20 dark:from-purple-500/30 dark:to-pink-500/30',
    iconColor: 'text-purple-600 dark:text-purple-400',
    borderColor: 'border-purple-200 dark:border-purple-800',
  },
  insight: {
    icon: Sparkles,
    gradient: 'from-accent-blue/20 to-accent-teal/20 dark:from-accent-blue/30 dark:to-accent-teal/30',
    iconColor: 'text-accent-blue dark:text-accent-teal',
    borderColor: 'border-blue-200 dark:border-blue-800',
  },
};

const InsightCard: React.FC<InsightCardProps> = memo(({
  type = 'insight',
  title,
  description,
  action,
  className = '',
}) => {
  const config = typeConfig[type];
  const Icon = config.icon;

  return (
    <div className={`relative overflow-hidden rounded-xl border ${config.borderColor} bg-white dark:bg-gray-800 p-4 transition-transform duration-200 hover:scale-[1.01] ${className}`}>
      <div className={`absolute inset-0 bg-gradient-to-br ${config.gradient} opacity-50`} />
      
      <div className="relative flex items-start gap-4">
        <div className="flex-shrink-0">
          <div className="p-2 rounded-lg bg-white dark:bg-gray-900 shadow-sm">
            <Icon className={`h-5 w-5 ${config.iconColor}`} />
          </div>
        </div>
        
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-1">
            {title}
          </h4>
          <p className="text-sm text-gray-700 dark:text-gray-300">
            {description}
          </p>
          
          {action && (
            <button
              onClick={action.onClick}
              className={`mt-3 text-sm font-medium ${config.iconColor} hover:underline focus:outline-none focus:underline`}
            >
              {action.label} →
            </button>
          )}
        </div>
      </div>
    </div>
  );
});

InsightCard.displayName = 'InsightCard';

export default InsightCard;

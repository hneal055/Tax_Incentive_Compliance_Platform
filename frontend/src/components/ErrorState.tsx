import React from 'react';
import { AlertCircle, RefreshCw, HelpCircle } from 'lucide-react';
import Button from './Button';

interface ErrorStateProps {
  title?: string;
  message: string;
  severity?: 'error' | 'warning' | 'info';
  onRetry?: () => void;
  helpLink?: string;
  className?: string;
}

const ErrorState: React.FC<ErrorStateProps> = ({
  title,
  message,
  severity = 'error',
  onRetry,
  helpLink,
  className = '',
}) => {
  const severityConfig = {
    error: {
      icon: AlertCircle,
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      borderColor: 'border-red-200 dark:border-red-800',
      iconColor: 'text-red-600 dark:text-red-400',
      titleColor: 'text-red-900 dark:text-red-200',
      textColor: 'text-red-700 dark:text-red-300',
    },
    warning: {
      icon: AlertCircle,
      bgColor: 'bg-amber-50 dark:bg-amber-900/20',
      borderColor: 'border-amber-200 dark:border-amber-800',
      iconColor: 'text-amber-600 dark:text-amber-400',
      titleColor: 'text-amber-900 dark:text-amber-200',
      textColor: 'text-amber-700 dark:text-amber-300',
    },
    info: {
      icon: HelpCircle,
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      borderColor: 'border-blue-200 dark:border-blue-800',
      iconColor: 'text-blue-600 dark:text-blue-400',
      titleColor: 'text-blue-900 dark:text-blue-200',
      textColor: 'text-blue-700 dark:text-blue-300',
    },
  };

  const config = severityConfig[severity];
  const Icon = config.icon;

  return (
    <div
      className={`rounded-lg border p-6 ${config.bgColor} ${config.borderColor} ${className}`}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <Icon className={`h-6 w-6 ${config.iconColor}`} aria-hidden="true" />
        </div>
        <div className="ml-4 flex-1">
          {title && (
            <h3 className={`text-lg font-semibold mb-2 ${config.titleColor}`}>
              {title}
            </h3>
          )}
          <p className={`text-sm ${config.textColor}`}>
            {message}
          </p>
          {(onRetry || helpLink) && (
            <div className="mt-4 flex gap-3">
              {onRetry && (
                <Button
                  size="sm"
                  onClick={onRetry}
                  variant="secondary"
                  className="inline-flex items-center gap-2"
                  aria-label="Retry action"
                >
                  <RefreshCw className="h-4 w-4" />
                  Retry
                </Button>
              )}
              {helpLink && (
                <a
                  href={helpLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`text-sm font-medium underline hover:no-underline ${config.textColor}`}
                >
                  View troubleshooting guide →
                </a>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorState;

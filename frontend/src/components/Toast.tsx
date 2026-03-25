/**
 * Toast notification component for transient alert messages.
 */
import { useEffect, useState } from 'react';
import { AlertTriangle, X } from 'lucide-react';

export interface ToastMessage {
  id: string;
  title: string;
  summary?: string;
  severity: 'info' | 'warning' | 'critical';
}

interface ToastProps {
  toast: ToastMessage;
  onDismiss: (id: string) => void;
}

const SEVERITY_STYLES: Record<
  ToastMessage['severity'],
  { container: string; icon: string }
> = {
  info: {
    container:
      'bg-white border-accent-blue text-gray-900',
    icon: 'text-accent-blue',
  },
  warning: {
    container:
      'bg-white border-status-warning text-gray-900',
    icon: 'text-status-warning',
  },
  critical: {
    container:
      'bg-white border-status-error text-gray-900',
    icon: 'text-status-error',
  },
};

const AUTO_DISMISS_MS: Record<ToastMessage['severity'], number> = {
  info: 4_000,
  warning: 6_000,
  critical: 10_000, // critical toasts stay longer
};

/** A single toast notification card. */
function Toast({ toast, onDismiss }: ToastProps) {
  const [visible, setVisible] = useState(true);
  const styles = SEVERITY_STYLES[toast.severity] ?? SEVERITY_STYLES.info;

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      setTimeout(() => onDismiss(toast.id), 300); // wait for fade-out
    }, AUTO_DISMISS_MS[toast.severity] ?? 4_000);
    return () => clearTimeout(timer);
  }, [toast.id, toast.severity, onDismiss]);

  return (
    <div
      role="alert"
      aria-live="assertive"
      data-testid="toast"
      data-severity={toast.severity}
      className={`
        flex items-start gap-3 w-80 rounded-xl border-l-4 p-4 shadow-lg
        transition-all duration-300
        ${styles.container}
        ${visible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-4'}
      `}
    >
      <AlertTriangle className={`h-5 w-5 mt-0.5 shrink-0 ${styles.icon}`} />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold leading-tight">{toast.title}</p>
        {toast.summary && (
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">{toast.summary}</p>
        )}
      </div>
      <button
        type="button"
        onClick={() => onDismiss(toast.id)}
        className="shrink-0 rounded p-0.5 text-gray-400 hover:text-gray-600 transition-colors"
        aria-label="Dismiss notification"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
}

interface ToastContainerProps {
  toasts: ToastMessage[];
  onDismiss: (id: string) => void;
}

/** Container that renders all active toasts in the bottom-right corner. */
export function ToastContainer({ toasts, onDismiss }: ToastContainerProps) {
  if (toasts.length === 0) return null;

  return (
    <div
      aria-label="Notifications"
      className="fixed bottom-6 right-6 z-50 flex flex-col gap-3 pointer-events-none"
    >
      {toasts.map((t) => (
        <div key={t.id} className="pointer-events-auto">
          <Toast toast={t} onDismiss={onDismiss} />
        </div>
      ))}
    </div>
  );
}

export default Toast;

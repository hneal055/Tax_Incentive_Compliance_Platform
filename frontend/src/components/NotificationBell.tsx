import { useEffect, useState } from 'react';
import { useMonitoringStore } from '../store/monitoringStore';

export default function NotificationBell() {
  const { unreadCount, fetchUnreadCount, wsConnected } = useMonitoringStore();
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    // Fetch initial unread count
    fetchUnreadCount();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchUnreadCount, 30000);
    return () => clearInterval(interval);
  }, [fetchUnreadCount]);

  const connectionColor = wsConnected ? 'bg-green-500' : 'bg-gray-400';

  return (
    <div className="relative">
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="relative p-2 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors"
        aria-label="Notifications"
      >
        {/* Bell Icon */}
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>

        {/* Unread badge */}
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}

        {/* Connection status indicator */}
        <span
          className={`absolute bottom-0 right-0 w-2 h-2 ${connectionColor} rounded-full border-2 border-white dark:border-gray-800`}
          title={wsConnected ? 'Connected' : 'Disconnected'}
        />
      </button>

      {/* Dropdown (placeholder for now) */}
      {showDropdown && (
        <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50">
          <div className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Notifications
              </h3>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {unreadCount} unread
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 text-center py-8">
              View full monitoring dashboard for details
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

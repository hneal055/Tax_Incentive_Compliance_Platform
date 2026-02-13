import { useEffect } from 'react';
import { useMonitoringStore } from '../store/monitoringStore';
import type { MonitoringEvent } from '../types';
import Card from '../components/Card';

export default function MonitoringDashboard() {
  const { 
    events, 
    unreadCount, 
    isLoading, 
    fetchEvents, 
    markEventAsRead,
    connectWebSocket,
    disconnectWebSocket,
    wsConnected
  } = useMonitoringStore();

  useEffect(() => {
    // Fetch initial events
    fetchEvents();
    
    // Connect to WebSocket for real-time updates
    connectWebSocket();
    
    // Cleanup on unmount
    return () => {
      disconnectWebSocket();
    };
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600 bg-red-50 border-red-200 dark:text-red-400 dark:bg-red-900/20 dark:border-red-800';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200 dark:text-yellow-400 dark:bg-yellow-900/20 dark:border-yellow-800';
      case 'info':
        return 'text-blue-600 bg-blue-50 border-blue-200 dark:text-blue-400 dark:bg-blue-900/20 dark:border-blue-800';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200 dark:text-gray-400 dark:bg-gray-900/20 dark:border-gray-800';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return '🚨';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      default:
        return '📢';
    }
  };

  const getEventTypeLabel = (eventType: string) => {
    switch (eventType) {
      case 'incentive_change':
        return 'Incentive Change';
      case 'new_program':
        return 'New Program';
      case 'expiration':
        return 'Expiration';
      case 'news':
        return 'News';
      default:
        return eventType;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    
    return date.toLocaleDateString();
  };

  const handleEventClick = (event: MonitoringEvent) => {
    if (!event.readAt) {
      markEventAsRead(event.id);
    }
    
    // Open source URL if available
    if (event.sourceUrl) {
      window.open(event.sourceUrl, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Jurisdiction Monitoring
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Real-time legislative and tax incentive change tracking
          </p>
        </div>
        
        <div className="flex items-center gap-3">
          {/* WebSocket status */}
          <div className="flex items-center gap-2 px-3 py-2 bg-white dark:bg-gray-800 rounded-lg shadow">
            <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-gray-400'}`} />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {wsConnected ? 'Live' : 'Offline'}
            </span>
          </div>
          
          {/* Unread count */}
          {unreadCount > 0 && (
            <div className="px-3 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg">
              <span className="text-sm font-medium">{unreadCount} unread</span>
            </div>
          )}
        </div>
      </div>

      {/* Events List */}
      <Card>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {isLoading ? (
            <div className="p-8 text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-2 text-gray-600 dark:text-gray-400">Loading events...</p>
            </div>
          ) : events.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-600 dark:text-gray-400">No monitoring events yet</p>
              <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">
                Events will appear here as jurisdictions are monitored
              </p>
            </div>
          ) : (
            events.map((event) => (
              <div
                key={event.id}
                onClick={() => handleEventClick(event)}
                className={`p-4 cursor-pointer transition-colors hover:bg-gray-50 dark:hover:bg-gray-800/50 ${
                  !event.readAt ? 'bg-blue-50/30 dark:bg-blue-900/10' : ''
                }`}
              >
                <div className="flex items-start gap-3">
                  {/* Severity Icon */}
                  <div className="flex-shrink-0 text-2xl mt-1">
                    {getSeverityIcon(event.severity)}
                  </div>
                  
                  {/* Event Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="text-base font-semibold text-gray-900 dark:text-white">
                        {event.title}
                      </h3>
                      <span className="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">
                        {formatDate(event.detectedAt)}
                      </span>
                    </div>
                    
                    <p className="mt-1 text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                      {event.summary}
                    </p>
                    
                    <div className="mt-2 flex items-center gap-2">
                      <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium border ${getSeverityColor(event.severity)}`}>
                        {event.severity.toUpperCase()}
                      </span>
                      <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                        {getEventTypeLabel(event.eventType)}
                      </span>
                      {!event.readAt && (
                        <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300">
                          NEW
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </Card>
    </div>
  );
}

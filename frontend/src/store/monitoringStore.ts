import { create } from 'zustand';
import type { MonitoringEvent } from '../types';
import wsManager from '../utils/wsClient';

interface MonitoringState {
  // Events
  events: MonitoringEvent[];
  unreadCount: number;
  
  // WebSocket connection
  wsConnected: boolean;
  
  // Loading states
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchEvents: () => Promise<void>;
  fetchUnreadCount: () => Promise<void>;
  markEventAsRead: (eventId: string) => Promise<void>;
  addEvent: (event: MonitoringEvent) => void;
  connectWebSocket: () => void;
  disconnectWebSocket: () => void;
  setError: (error: string | null) => void;
}

export const useMonitoringStore = create<MonitoringState>((set, get) => ({
  events: [],
  unreadCount: 0,
  wsConnected: false,
  isLoading: false,
  error: null,

  fetchEvents: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('http://localhost:8000/api/v1/monitoring/events?page_size=50');
      if (!response.ok) throw new Error('Failed to fetch events');
      
      const data = await response.json();
      set({ events: data.events || [], isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to fetch events', 
        isLoading: false 
      });
    }
  },

  fetchUnreadCount: async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/monitoring/events/unread');
      if (!response.ok) throw new Error('Failed to fetch unread count');
      
      const data = await response.json();
      set({ unreadCount: data.unreadCount || 0 });
    } catch (error) {
      console.error('Failed to fetch unread count:', error);
    }
  },

  markEventAsRead: async (eventId: string) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/monitoring/events/${eventId}/read`,
        { method: 'PATCH' }
      );
      
      if (!response.ok) throw new Error('Failed to mark event as read');
      
      // Update local state
      set((state) => ({
        events: state.events.map(event =>
          event.id === eventId
            ? { ...event, readAt: new Date().toISOString() }
            : event
        ),
        unreadCount: Math.max(0, state.unreadCount - 1)
      }));
    } catch (error) {
      console.error('Failed to mark event as read:', error);
    }
  },

  addEvent: (event: MonitoringEvent) => {
    set((state) => ({
      events: [event, ...state.events],
      unreadCount: state.unreadCount + 1
    }));
  },

  connectWebSocket: () => {
    // Set up WebSocket listeners
    wsManager.addListener((message) => {
      if (message.type === 'monitoring_event' && message.event) {
        get().addEvent(message.event);
        
        // Show toast notification for critical events
        if (message.event.severity === 'critical') {
          const title = message.event.title || 'Critical Alert';
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('🚨 PilotForge Alert', {
              body: title,
              icon: '/favicon.ico'
            });
          }
        }
      }
    });

    wsManager.addStatusListener((status) => {
      set({ wsConnected: status === 'connected' });
    });

    // Connect to WebSocket
    wsManager.connect();
  },

  disconnectWebSocket: () => {
    wsManager.disconnect();
    set({ wsConnected: false });
  },

  setError: (error) => {
    set({ error });
  },
}));

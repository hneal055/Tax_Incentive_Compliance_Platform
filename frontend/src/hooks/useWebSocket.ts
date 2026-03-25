/**
 * React hook that manages the application-wide WebSocket connection and
 * pipes incoming monitoring events into the Zustand store.
 *
 * An optional ``onEvent`` callback can be provided for side-effects such as
 * showing toast notifications – it is called *in addition to* the default
 * store update.
 *
 * Usage (mount once, e.g. in your root layout or Dashboard):
 *
 * ```tsx
 * useWebSocket();
 * // or with a custom side-effect:
 * useWebSocket((event) => { if (event.severity === 'critical') showToast(event); });
 * ```
 */

import { useEffect, useRef } from 'react';
import wsClient from '../utils/wsClient';
import { useAppStore } from '../store';
import type { MonitoringEvent } from '../types';

export function useWebSocket(onEvent?: (event: MonitoringEvent) => void): void {
  const addEvent = useAppStore((s) => s.addEvent);
  // Keep the callback in a ref so changing it doesn't restart the effect.
  const onEventRef = useRef(onEvent);
  onEventRef.current = onEvent;

  useEffect(() => {
    wsClient.connect();

    const unsubscribe = wsClient.subscribe((event: MonitoringEvent) => {
      addEvent(event);
      onEventRef.current?.(event);
    });

    return () => {
      unsubscribe();
      wsClient.disconnect();
    };
  }, [addEvent]);
}

export default useWebSocket;

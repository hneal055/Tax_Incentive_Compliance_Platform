const featureFlags = {
  USE_REAL_API:      import.meta.env.VITE_USE_REAL_API === 'true',
  USE_REAL_AUTH:     import.meta.env.VITE_USE_REAL_AUTH === 'true',
  MOCK_DELAY_MS:     Number(import.meta.env.VITE_MOCK_DELAY_MS ?? 500),
  ENABLE_ANALYTICS:  import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
  ENABLE_SENTRY:     import.meta.env.VITE_ENABLE_SENTRY === 'true',
} as const;

export default featureFlags;

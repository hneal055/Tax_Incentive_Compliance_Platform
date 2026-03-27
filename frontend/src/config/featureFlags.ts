const featureFlags = {
  USE_REAL_API:      true,
  USE_REAL_AUTH:     true,
  MOCK_DELAY_MS:     500,
  ENABLE_ANALYTICS:  true,
  ENABLE_SENTRY:     false,
} as const;
export default featureFlags;

import { useMemo } from 'react';
import { useAuthStore } from '../store/auth';
import { gradualRollout, rolloutConfig, type RolloutFeature } from '../utils/gradualRollout';

/**
 * Returns true if the current authenticated user falls within the enabled
 * cohort for the given feature and percentage.
 *
 * The result is memoized — it won't change mid-session even if the store
 * re-renders, which gives users a consistent experience.
 *
 * Usage:
 *   const canSeeExecDashboard = useGradualRollout('EXECUTIVE_DASHBOARD');
 *   const canSeeFeature = useGradualRollout('EXECUTIVE_DASHBOARD', 50); // override %
 */
export function useGradualRollout(
  featureName: RolloutFeature,
  percentageOverride?: number,
): boolean {
  const userId = useAuthStore(state => state.user?.id ?? 'anonymous');
  const percentage = percentageOverride ?? rolloutConfig[featureName];

  return useMemo(
    () => gradualRollout.isEnabled(userId, featureName, percentage),
    // userId is stable per session; featureName and percentage are constants in practice
    [userId, featureName, percentage],
  );
}

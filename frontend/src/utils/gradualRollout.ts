// Deterministic hash: same userId+featureName always produces the same bucket (0–99).
// Uses the djb2-style bit-shift algorithm — fast, no external deps, good distribution.
function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0; // clamp to 32-bit integer
  }
  return Math.abs(hash);
}

export class GradualRollout {
  /**
   * Returns true if this user is in the enabled cohort for this feature.
   *
   * @param userId          - Stable user identifier (auth store user.id)
   * @param featureName     - Feature key (use the features.* constants)
   * @param percentage      - 0–100. 0 = nobody, 100 = everybody, 25 = 1-in-4 users
   *
   * In development (`import.meta.env.DEV`) the percentage is always honoured
   * so rollout logic can be verified locally. Set to 100 to force-enable,
   * or 0 to force-disable, during development.
   */
  isEnabled(userId: string, featureName: string, percentage: number): boolean {
    if (percentage >= 100) return true;
    if (percentage <= 0) return false;

    const bucket = hashString(userId + featureName) % 100;
    return bucket < percentage;
  }
}

export const gradualRollout = new GradualRollout();

// Rollout percentages per feature — edit here to adjust cohort size.
// Keep at 0 until ready to ramp; raise incrementally (5 → 25 → 50 → 100).
export const rolloutConfig = {
  EXECUTIVE_DASHBOARD: 0,   // not yet rolled out
  AI_ADVISOR_V2:       0,   // placeholder for future feature
} as const;

export type RolloutFeature = keyof typeof rolloutConfig;

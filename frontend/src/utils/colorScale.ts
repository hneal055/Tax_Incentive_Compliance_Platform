interface ColorStop { percent: number; r: number; g: number; b: number }

const LIGHT_STOPS: ColorStop[] = [
  { percent: 0,  r: 226, g: 232, b: 240 }, // slate-200
  { percent: 5,  r: 167, g: 243, b: 233 }, // teal-100
  { percent: 15, r: 20,  g: 184, b: 166 }, // accent-teal
  { percent: 25, r: 16,  g: 185, b: 129 }, // accent-emerald
  { percent: 35, r: 59,  g: 130, b: 246 }, // accent-blue
];

const DARK_STOPS: ColorStop[] = [
  { percent: 0,  r: 51,  g: 65,  b: 85  }, // slate-700
  { percent: 5,  r: 19,  g: 78,  b: 74  }, // teal-900
  { percent: 15, r: 20,  g: 184, b: 166 }, // accent-teal
  { percent: 25, r: 16,  g: 185, b: 129 }, // accent-emerald
  { percent: 35, r: 59,  g: 130, b: 246 }, // accent-blue
];

export function getHeatColor(percentage: number, isDark = false): string {
  const stops = isDark ? DARK_STOPS : LIGHT_STOPS;
  const clamped = Math.max(0, Math.min(percentage, 40));

  let lower = stops[0];
  let upper = stops[stops.length - 1];

  for (let i = 0; i < stops.length - 1; i++) {
    if (clamped >= stops[i].percent && clamped <= stops[i + 1].percent) {
      lower = stops[i];
      upper = stops[i + 1];
      break;
    }
  }

  const range = upper.percent - lower.percent || 1;
  const t = (clamped - lower.percent) / range;

  const r = Math.round(lower.r + (upper.r - lower.r) * t);
  const g = Math.round(lower.g + (upper.g - lower.g) * t);
  const b = Math.round(lower.b + (upper.b - lower.b) * t);

  return `rgb(${r}, ${g}, ${b})`;
}

export const NO_DATA_COLOR_LIGHT = '#e2e8f0';
export const NO_DATA_COLOR_DARK  = '#334155';

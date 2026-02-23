/** Mapping of US state 2-letter codes to FIPS numerical codes */
export const STATE_CODE_TO_FIPS: Record<string, string> = {
  AL: '01', AK: '02', AZ: '04', AR: '05', CA: '06',
  CO: '08', CT: '09', DE: '10', DC: '11', FL: '12',
  GA: '13', HI: '15', ID: '16', IL: '17', IN: '18',
  IA: '19', KS: '20', KY: '21', LA: '22', ME: '23',
  MD: '24', MA: '25', MI: '26', MN: '27', MS: '28',
  MO: '29', MT: '30', NE: '31', NV: '32', NH: '33',
  NJ: '34', NM: '35', NY: '36', NC: '37', ND: '38',
  OH: '39', OK: '40', OR: '41', PA: '42', RI: '44',
  SC: '45', SD: '46', TN: '47', TX: '48', UT: '49',
  VT: '50', VA: '51', WA: '53', WV: '54', WI: '55',
  WY: '56', PR: '72',
};

export const FIPS_TO_STATE_CODE: Record<string, string> = Object.fromEntries(
  Object.entries(STATE_CODE_TO_FIPS).map(([code, fips]) => [fips, code]),
);

const US_STATE_CODES = new Set(Object.keys(STATE_CODE_TO_FIPS));

export function isUSStateCode(code: string): boolean {
  return US_STATE_CODES.has(code.toUpperCase());
}

/** Approximate centroids (lng, lat) for production markers */
export const STATE_CENTROIDS: Record<string, [number, number]> = {
  AL: [-86.9, 32.8], AK: [-153.5, 64.3], AZ: [-111.9, 34.2],
  AR: [-92.4, 34.8], CA: [-119.4, 36.8], CO: [-105.5, 39.0],
  CT: [-72.7, 41.6], DE: [-75.5, 39.0], DC: [-77.0, 38.9],
  FL: [-81.7, 28.1], GA: [-83.5, 32.7], HI: [-155.5, 19.9],
  ID: [-114.7, 44.1], IL: [-89.4, 40.0], IN: [-86.3, 39.8],
  IA: [-93.5, 42.0], KS: [-98.3, 38.5], KY: [-84.3, 37.8],
  LA: [-92.0, 31.0], ME: [-69.4, 45.3], MD: [-76.6, 39.0],
  MA: [-71.8, 42.4], MI: [-84.5, 44.3], MN: [-94.3, 46.3],
  MS: [-89.7, 32.7], MO: [-92.5, 38.6], MT: [-109.6, 46.9],
  NE: [-99.9, 41.5], NV: [-116.6, 38.8], NH: [-71.6, 43.7],
  NJ: [-74.7, 40.1], NM: [-105.9, 34.5], NY: [-75.5, 43.0],
  NC: [-79.4, 35.5], ND: [-100.5, 47.4], OH: [-82.8, 40.4],
  OK: [-97.5, 35.5], OR: [-120.6, 43.8], PA: [-77.6, 41.2],
  RI: [-71.5, 41.7], SC: [-80.9, 34.0], SD: [-100.2, 44.4],
  TN: [-86.6, 35.7], TX: [-99.0, 31.5], UT: [-111.9, 39.3],
  VT: [-72.6, 44.1], VA: [-79.5, 37.8], WA: [-120.7, 47.4],
  WV: [-80.6, 38.6], WI: [-89.6, 44.6], WY: [-107.6, 43.0],
  PR: [-66.6, 18.2],
};

import axios, { AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_VERSION = '0.1.0';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/${API_VERSION}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Jurisdictions
export async function getJurisdictions() {
  try {
    const res = await apiClient.get('/jurisdictions/');
    return res.data;
  } catch (err) {
    handleApiError(err);
    return null;
  }
}

// Productions
export async function getProductions() {
  try {
    const res = await apiClient.get('/productions/');
    return res.data;
  } catch (err) {
    handleApiError(err);
    return null;
  }
}

// Incentive Rules
export async function getIncentiveRules() {
  try {
    const res = await apiClient.get('/incentive-rules/');
    return res.data;
  } catch (err) {
    handleApiError(err);
    return null;
  }
}

// Health Check
export async function getHealth() {
  try {
    const res = await apiClient.get('/health');
    return res.data;
  } catch (err) {
    handleApiError(err);
    return null;
  }
}

// Generic error handler
function handleApiError(error: unknown) {
  if (axios.isAxiosError(error)) {
    console.error('API Error:', error.message);
    throw error;
  } else {
    throw error;
  }
}

export default apiClient;
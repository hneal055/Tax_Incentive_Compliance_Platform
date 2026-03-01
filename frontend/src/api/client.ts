import axios from 'axios';

// ?? instead of || so empty string (Docker: relative URL via nginx) is kept as-is
const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
const API_VERSION = import.meta.env.VITE_API_VERSION || '0.1.0';
const TOKEN_KEY = 'pilotforge_token';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/${API_VERSION}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Inject Bearer token on every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, clear session and reload to show login page
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      window.location.href = '/';
    }
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export function getApiUrl(endpoint: string): string {
  return `/api/${API_VERSION}/${endpoint}`;
}

export default apiClient;

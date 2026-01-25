import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/${API_VERSION}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export function getApiUrl(endpoint: string): string {
  if (!API_VERSION) {
    throw new Error('API version is not defined in environment variables.');
  }
  return `/api/${API_VERSION}/${endpoint}`;
}

export default apiClient;

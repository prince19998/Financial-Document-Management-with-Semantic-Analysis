import axios from 'axios';

// When deployed together on HF Spaces, frontend and backend share the same origin.
// In local dev, VITE_API_URL points to http://localhost:8000.
// If neither is set, use same origin (empty string = relative URLs).
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
    return Promise.reject(error);
  }
);

export default api;

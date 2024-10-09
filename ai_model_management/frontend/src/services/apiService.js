// src/services/apiService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Adjust this to your API URL

const apiClient = axios.create({
  baseURL: API_URL,
});

// Add a request interceptor to include the token in headers
apiClient.interceptors.request.use(
  (config) => {
    const token = JSON.parse(localStorage.getItem('token'))?.access_token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;

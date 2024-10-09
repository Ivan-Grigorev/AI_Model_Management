// src/services/authService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Adjust this to your API URL

class AuthService {
  // Login function
  async login(email, password) {
    const response = await axios.post(`${API_URL}/token`, {
      email,
      password,
    });

    if (response.data.access_token) {
      localStorage.setItem('token', JSON.stringify(response.data));
    }

    return response.data;
  }

  // Signup function
  async signup(email, password) {
    const response = await axios.post(`${API_URL}/signin`, {
      email: email,
      password: password,
    });

    return response.data; // Return the response for further use
  }

  // Logout function
  logout() {
    localStorage.removeItem('token');
  }

  // Function to get current user
  async getCurrentUser() {
    const token = JSON.parse(localStorage.getItem('token'))?.access_token;
    const response = await axios.get(`${API_URL}/users/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  }

  // Create dataset function
  async createDataset(dataset) {
    const token = JSON.parse(localStorage.getItem('token'))?.access_token; // Get the token
    const response = await axios.post(`${API_URL}/datasets`, dataset, {
      headers: {
        Authorization: `Bearer ${token}`, // Attach the token to the headers
      },
    });
    return response.data; // Return the created dataset
  }
}

export default new AuthService();

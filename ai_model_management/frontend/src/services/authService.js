import axios from 'axios';

const API_URL = 'http://localhost:8000/';  // Update this URL as necessary

class AuthService {
  async signup(email, password) {
    const response = await axios.post(`${API_URL}signin`, { email, password });
    return response.data;
  }

  async login(email, password) {
    const response = await axios.post(`${API_URL}login`, { email, password });
    // Save token to localStorage or sessionStorage for future requests
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  }

  logout() {
    localStorage.removeItem('user');  // Clear user data on logout
  }
}

export default new AuthService();

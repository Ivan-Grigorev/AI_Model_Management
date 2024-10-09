<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-lg">
      <h2 class="text-2xl font-bold text-center">Login</h2>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            v-model="email"
            class="w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="password"
            class="w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>
        <div>
          <button
            type="submit"
            class="w-full px-4 py-2 text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Login
          </button>
        </div>
      </form>
      <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
      <p class="text-center">
        Don't have an account?
        <router-link to="/signin" class="text-indigo-600 hover:text-indigo-800">Sign up here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import AuthService from '@/services/authService';

export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async handleLogin() {
      try {
        // Call the login service and capture the response
        const response = await AuthService.login(this.email, this.password);

        // Extract the redirect_url from the backend response
        const redirectUrl = response.redirect_url;

        // Check if the user is an admin or not and redirect accordingly
        if (redirectUrl) {
          this.$router.push(redirectUrl); // Dynamically push the route
        } else {
          this.errorMessage = 'Login failed. Please try again.';
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Login failed. Please try again.';
      }
    }
  }
};
</script>

<style scoped>
/* Additional custom styles can be added here if needed */
</style>

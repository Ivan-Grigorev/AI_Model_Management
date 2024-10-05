<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="text-center">
      <img alt="Vue logo" src="../assets/logo.png" class="mb-4" />
      <h1 class="text-3xl font-bold">Welcome to the AI Model Management App</h1>
      <p class="mt-6 mb-8 text-gray-700">To manage your AI models, please log in.</p>
      <router-link
        to="/login"
        class="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Log In
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  // No need for methods since we're redirecting to login page
};
</script>

<style scoped>
/* Additional custom styles can go here if needed */
</style>

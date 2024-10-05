<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 class="text-3xl font-bold text-center mb-4">About the AI Model Management Application</h1>
      <p class="text-gray-700 mb-4">
        Welcome to the AI Model Management Application, designed specifically for Japanese employees with basic computer literacy. This web application aims to simplify the management of AI models and datasets without requiring any prior knowledge of AI technologies.
      </p>
      <h2 class="text-2xl font-semibold mb-2">Key Features:</h2>
      <ul class="list-disc list-inside mb-4">
        <li>Create an account using your email address and password.</li>
        <li>Log in and log out easily.</li>
        <li>Admin users can log in using provided credentials.</li>
        <li>Both users and admins can create datasets and models.</li>
        <li>Admins have the ability to delete datasets and models.</li>
        <li>All users can launch model training using their datasets.</li>
        <li>Consult results of training sessions easily.</li>
        <li>Additional features aimed at enhancing user experience may also be included.</li>
      </ul>
      <h2 class="text-2xl font-semibold mb-2">User-Friendly Interface</h2>
      <p class="text-gray-700 mb-4">
        The application is designed with a simple and intuitive interface to make it accessible for all users, regardless of their technical background.
      </p>
      <h2 class="text-2xl font-semibold mb-2">Get Started Today!</h2>
      <p class="text-gray-700 mb-4">
        Sign up now and start managing your AI models and datasets with ease. We are committed to helping you navigate through your AI model management journey.
      </p>
      <div class="flex justify-center">
        <router-link to="/signin" class="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Create Account
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
};
</script>

<style scoped>
/* Additional custom styles can go here if needed */
</style>

<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-green-600 text-white p-4 flex justify-between items-center">
      <router-link to="/dashboard" class="text-2xl hover:underline">User Dashboard</router-link>
    </header>

    <!-- User Buttons -->
    <div class="p-4">
      <h2 class="text-xl font-bold mb-4">AI Model Management</h2>
      <div class="space-x-4">
        <router-link to="/datasets" class="bg-orange-500 text-white px-4 py-2 rounded">Manage Datasets</router-link>
        <router-link to="/models" class="bg-blue-500 text-white px-4 py-2 rounded">Manage Models</router-link>
        <router-link to="/trainings" class="bg-pink-500 text-white px-4 py-2 rounded">Manage Trainings</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null, // Initialize user as null
    };
  },
  created() {
    // Fetch the user from localStorage or another source
    const token = localStorage.getItem('token');
    // if (storedUser) {
    //   this.user = JSON.parse(storedUser);
    // }
    if (token) {
    // Use the token directly, don't attempt to parse it
        console.log('User token:', token);
    } else {
    console.log('No token found');
    }
  }
};
</script>

<style scoped>
/* Add any custom styles if needed */
</style>

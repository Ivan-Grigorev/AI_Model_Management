<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-blue-600 text-white p-4 flex justify-between items-center">
      <router-link to="/admin" class="text-2xl hover:underline">Admin Panel</router-link>
    </header>

    <!-- Admin Buttons -->
    <div class="p-4">
      <h2 class="text-xl font-bold mb-4">Admin Functions</h2>
      <div class="space-x-4">
        <router-link to="/admin/users" class="bg-blue-500 text-white px-4 py-2 rounded">Manage Users</router-link>
        <router-link to="/admin/datasets" class="bg-green-500 text-white px-4 py-2 rounded">Manage Datasets</router-link>
        <router-link to="/admin/models" class="bg-purple-500 text-white px-4 py-2 rounded">Manage Models</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      // Log out logic here
      alert('Logging out');
    }
  }
};
</script>

<style scoped>
/* Add any custom styles if needed */
</style>

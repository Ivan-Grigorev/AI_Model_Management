<template>
  <!-- Header -->
  <header class="bg-green-600 text-white p-4 flex justify-between items-center">
    <router-link to="/dashboard" class="text-2xl hover:underline">User Dashboard</router-link>
    <h2 class="text-xl font-bold">Model Details</h2>
  </header>

  <div class="container mx-auto py-6 px-4">
    <div class="border p-4 rounded-lg bg-white">
      <p><strong>ID:</strong> {{ model.id }}</p>
      <p><strong>Name:</strong> {{ model.name }}</p>
      <p><strong>Creation Date:</strong> {{ model.creation_date }}</p>
    </div>

    <button @click="$router.push('/models')" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
      Back to All Models
    </button>
  </div>
</template>

<script>
import apiClient from '@/services/apiService'; // Import the centralized API client

export default {
  data() {
    return {
      model: null,
    };
  },
  methods: {
    async fetchModel() {
      const modelId = this.$route.params.model_id; // Ensure this matches the route parameter
      try {
        const response = await apiClient.get(`/models/${modelId}`); // Use apiClient
        this.model = response.data;
      } catch (error) {
        console.error('Model not found', error);
      }
    }
  },
  created() {
    this.fetchModel();
  }
};
</script>

<template>
  <!-- Header -->
  <header class="bg-blue-600 text-white p-4 flex justify-between items-center">
    <router-link to="/admin" class="text-2xl hover:underline">Admin Panel</router-link>
    <h2 class="text-xl font-bold">Model Details</h2>
  </header>

  <div class="container mx-auto py-6 px-4">
    <div class="border p-4 rounded-lg bg-white">
      <p><strong>ID:</strong> {{ model.id }}</p>
      <p><strong>Name:</strong> {{ model.name }}</p>
      <p><strong>Creation Date:</strong> {{ model.creation_date }}</p>
    </div>

    <div class="flex flex-col space-y-4 mt-4 items-center">
      <button
        @click="$router.push('/admin/models')"
        class="w-48 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
        Back to All Models
      </button>
      <button
        @click="deleteModel(model.id)"
        class="w-48 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-700">
        Delete
      </button>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiService'; // Import the centralized API service

export default {
  data() {
    return {
      model: null,
    };
  },
  methods: {
    async fetchModel() {
      const modelId = this.$route.params.model_id;
      try {
        const response = await apiClient.get(`/admin/models/${modelId}`); // Use apiClient to fetch the model
        this.model = response.data;
      } catch (error) {
        console.error('Model not found:', error);
      }
    },
    async deleteModel(modelId) {
      if (confirm('Are you sure you want to delete this model?')) {
        try {
          await apiClient.delete(`/admin/models/${modelId}`); // Use apiClient to delete the model
          this.$router.push('/admin/models'); // Redirect to the models page
        } catch (error) {
          console.error('Error deleting model:', error);
        }
      }
    },
  },
  created() {
    this.fetchModel(); // Fetch the model when the component is created
  }
};
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

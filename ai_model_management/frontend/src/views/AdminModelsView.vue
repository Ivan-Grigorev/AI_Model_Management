<template>
  <!-- Header -->
  <header class="bg-blue-600 text-white p-4 flex justify-between items-center">
    <router-link to="/admin" class="text-2xl hover:underline">Admin Panel</router-link>
    <h2 class="text-xl font-bold">Models Management</h2>
  </header>
  <div class="container mx-auto p-4">

    <!-- Add Model Form -->
    <div class="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">Add New Model</h2>
      <form @submit.prevent="addModel">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="modelName">
            Model Name
          </label>
          <input
            v-model="newModel.name"
            id="modelName"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter model name"
            required
          />
        </div>
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Add Model
        </button>
      </form>
    </div>

    <!-- Search Model Form -->
    <div class="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">Search Model</h2>
      <form @submit.prevent="searchModel">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="searchQuery">
            Search by ID or Name
          </label>
          <input
            v-model="searchQuery"
            id="searchQuery"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter model ID or name"
          />
        </div>
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Search
        </button>
      </form>

      <!-- Display error message if model not found -->
      <div v-if="searchError" class="mt-4 text-red-500 font-bold">
        Model not found. Please try again.
      </div>

      <!-- Display found model message -->
      <div v-if="foundModelId" class="mt-4 text-green-500 font-bold">
        <a :href="`/admin/models/${foundModelId}`"
        class="text-blue-500 underline hover:text-blue-700"
        style="text-decoration:none; color:green;">
        Model found. View model details.</a>
      </div>
    </div>

    <!-- Model List Table -->
    <div class="bg-white shadow-md rounded-lg p-6">
      <h2 class="text-2xl font-semibold mb-4">All Models</h2>
      <table class="min-w-full table-auto">
        <thead>
          <tr class="bg-gray-200">
            <th class="px-4 py-2">ID</th>
            <th class="px-4 py-2">Name</th>
            <th class="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="model in models" :key="model.id" class="border-b">
            <td class="px-4 py-2">
              <a :href="`/admin/models/${model.id}`" class="text-blue-500 underline hover:text-blue-700">
                {{ model.id }}
              </a>
            </td>
            <td class="px-4 py-2">{{ model.name }}</td>
            <td class="px-4 py-2">
              <button @click="deleteModel(model.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-3 rounded">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiService'; // Import the centralized API service

export default {
  data() {
    return {
      newModel: {
        name: ''
      },
      models: [],
      searchQuery: '',  // For the search functionality
      searchError: false,  // For handling search errors
      foundModelId: null  // To hold the ID of the found model
    };
  },
  methods: {
    async addModel() {
      try {
        const response = await apiClient.post('/admin/models', this.newModel);
        this.models.push(response.data);
        this.newModel.name = ''; // Reset the form
      } catch (error) {
        console.error('Error adding model:', error);
      }
    },
    async fetchModels() {
      try {
        const response = await apiClient.get('/admin/models'); // Ensure the correct endpoint for admin
        this.models = response.data;
      } catch (error) {
        console.error('Error fetching models:', error);
      }
    },
    async deleteModel(modelId) {
      if (confirm('Are you sure you want to delete this model?')) {
        try {
          await apiClient.delete(`/admin/models/${modelId}`);
          this.models = this.models.filter(model => model.id !== modelId);
        } catch (error) {
          console.error('Error deleting model:', error);
        }
      }
    },
    async searchModel() {
      const query = this.searchQuery.trim();
      this.searchError = false;
      this.foundModelId = null; // Reset found model ID

      if (query) {
        try {
          const modelId = parseInt(query);
          if (!isNaN(modelId)) {
            // Searching by ID
            const response = await apiClient.get(`/admin/models/${modelId}`);
            if (response.data) {
              this.foundModelId = modelId; // Set the found model ID
            } else {
              this.searchError = true; // Model not found
            }
          } else {
            // Searching by Name
            const response = await apiClient.get('/admin/models');
            const model = response.data.find(m => m.name.toLowerCase() === query.toLowerCase());
            if (model) {
              this.foundModelId = model.id; // Set the found model ID
            } else {
              this.searchError = true; // Model not found
            }
          }
        } catch (error) {
          console.error('Error searching for model:', error);
          this.searchError = true;
        }
      }
    }
  },
  mounted() {
    this.fetchModels();
  }
};
</script>

<style scoped>
/* Add any custom styles if needed */
</style>

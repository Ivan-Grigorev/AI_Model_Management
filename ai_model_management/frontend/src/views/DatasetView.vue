<template>
  <!-- Header -->
  <header class="bg-green-600 text-white p-4 flex justify-between items-center">
    <router-link to="/dashboard" class="text-2xl hover:underline">User Dashboard</router-link>
    <h2 class="text-xl font-bold">Datasets Management</h2>
  </header>

  <div class="container mx-auto p-4">
    <!-- Add Dataset Form -->
    <div class="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">Add New Dataset</h2>
      <form @submit.prevent="addDataset">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="datasetName">
            Dataset Name
          </label>
          <input
            v-model="newDataset.name"
            id="datasetName"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter dataset name"
            required
          />
        </div>
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Add Dataset
        </button>
      </form>
    </div>

    <!-- Search Dataset Form -->
    <div class="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 class="text-2xl font-semibold mb-4">Search Dataset</h2>
      <form @submit.prevent="searchDataset">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="searchQuery">
            Search by ID or Name
          </label>
          <input
            v-model="searchQuery"
            id="searchQuery"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter dataset ID or name"
            required
          />
        </div>
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Search
        </button>
      </form>

      <!-- Display error message if dataset not found -->
      <div v-if="searchError" class="mt-4 text-red-500 font-bold">
        Dataset not found. Please try again.
      </div>

      <!-- Display found dataset message -->
      <div v-if="foundDatasetId" class="mt-4 text-green-500 font-bold">
        <a :href="`/datasets/${foundDatasetId}`"
        class="text-blue-500 underline hover:text-blue-700"
        style="text-decoration:none; color:green;">
        Dataset found. View dataset details.</a>
      </div>
    </div>

    <!-- Dataset List Table -->
    <div class="bg-white shadow-md rounded-lg p-6">
      <h2 class="text-2xl font-semibold mb-4">All Datasets</h2>
      <table class="min-w-full table-auto">
        <thead>
          <tr class="bg-gray-200">
            <th class="px-4 py-2">ID</th>
            <th class="px-4 py-2">Name</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dataset in datasets" :key="dataset.id" class="border-b">
            <td class="px-4 py-2">
              <a :href="`/datasets/${dataset.id}`" class="text-blue-500 underline hover:text-blue-700">
                {{ dataset.id }}
              </a>
            </td>
            <td class="px-4 py-2">{{ dataset.name }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiService';

export default {
  data() {
    return {
      newDataset: {
        name: ''
      },
      datasets: [],
      searchQuery: '',  // For the search functionality
      searchError: false,  // For handling search errors
      foundDatasetId: null  // To hold the ID of the found dataset
    };
  },
  methods: {
    async addDataset() {
      try {
        const response = await apiClient.post('/datasets', this.newDataset);
        this.datasets.push(response.data);
        this.newDataset.name = ''; // Reset the form
      } catch (error) {
        console.error('Error adding dataset:', error);
      }
    },
    async fetchDatasets() {
      try {
        const response = await apiClient.get('/datasets');
        this.datasets = response.data;
      } catch (error) {
        console.error('Error fetching datasets:', error);
      }
    },
    async searchDataset() {
      const query = this.searchQuery.trim();
      this.searchError = false;
      this.foundDatasetId = null; // Reset found dataset ID

      if (query) {
        try {
          const datasetId = parseInt(query);
          if (!isNaN(datasetId)) {
            // Searching by ID
            const response = await apiClient.get(`/datasets/${datasetId}`);
            if (response.data) {
              this.foundDatasetId = datasetId; // Set the found dataset ID
            } else {
              this.searchError = true; // Dataset not found
            }
          } else {
            // Searching by Name
            const response = await apiClient.get(`/datasets`);
            const dataset = response.data.find(d => d.name.toLowerCase() === query.toLowerCase());
            if (dataset) {
              this.foundDatasetId = dataset.id; // Set the found dataset ID
            } else {
              this.searchError = true; // Dataset not found
            }
          }
        } catch (error) {
          console.error('Error searching for dataset:', error);
          this.searchError = true;
        }
      }
    }
  },
  mounted() {
    this.fetchDatasets();
  }
};
</script>

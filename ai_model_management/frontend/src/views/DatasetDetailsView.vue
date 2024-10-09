<template>
  <!-- Header -->
  <header class="bg-green-600 text-white p-4 flex justify-between items-center">
    <router-link to="/dashboard" class="text-2xl hover:underline">User Dashboard</router-link>
    <h2 class="text-xl font-bold">Dataset Details</h2>
  </header>

  <div class="container mx-auto py-6 px-4">
    <div class="border p-4 rounded-lg bg-white">
      <p><strong>ID:</strong> {{ dataset.id }}</p>
      <p><strong>Name:</strong> {{ dataset.name }}</p>
      <p><strong>Creation Date:</strong> {{ dataset.creation_date }}</p>
    </div>

    <button @click="$router.push('/datasets')" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
      Back to All Datasets
    </button>
  </div>
</template>

<script>
import apiClient from '@/services/apiService';

export default {
  data() {
    return {
      dataset: null,
    };
  },
  methods: {
    async fetchDataset() {
      const datasetId = this.$route.params.dataset_id;
      try {
        const response = await apiClient.get(`/datasets/${datasetId}`);
        this.dataset = response.data;
      } catch (error) {
        console.error('Dataset not found:', error);
      }
    }
  },
  created() {
    this.fetchDataset();
  }
};
</script>

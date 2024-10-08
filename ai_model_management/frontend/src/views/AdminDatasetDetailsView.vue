<template>
  <!-- Header -->
  <header class="bg-blue-600 text-white p-4 flex justify-between items-center">
    <router-link to="/admin" class="text-2xl hover:underline">Admin Panel</router-link>
    <h2 class="text-xl font-bold">Datasets Management</h2>
  </header>
  <div class="container mx-auto py-6 px-4">
    <h1 class="text-2xl font-bold mb-4">Dataset Details</h1>

    <div class="border p-4 rounded-lg bg-gray-100">
      <p><strong>ID:</strong> {{ dataset.id }}</p>
      <p><strong>Name:</strong> {{ dataset.name }}</p>
      <p><strong>Creation Date:</strong> {{ dataset.creation_date }}</p>
    </div>

    <div class="flex flex-col space-y-4 mt-4 items-center">
      <button
        @click="$router.push('/admin/datasets')"
        class="w-48 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
        Back to All Datasets
      </button>
      <button
        @click="deleteDataset(dataset.id)"
        class="w-48 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-700">
        Delete
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      dataset: null,
    };
  },
  methods: {
    fetchDataset() {
      const datasetId = this.$route.params.dataset_id;
      axios.get(`/admin/datasets/${datasetId}`)
        .then(response => {
          this.dataset = response.data;
        })
        .catch(error => {
          console.error('Dataset not found', error);
        });
    },
    async deleteDataset(datasetId) {
      if (confirm('Are you sure you want to delete this dataset?')) {
        try {
          await axios.delete(`/admin/datasets/${datasetId}`);
          this.$router.push('/admin/datasets'); // Redirect to the datasets page
        } catch (error) {
          console.error('Error deleting dataset:', error);
        }
      }
    },
  },
  created() {
    this.fetchDataset();
  }
};
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

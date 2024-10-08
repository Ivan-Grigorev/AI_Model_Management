<template>
  <div class="container mx-auto py-6 px-4">
    <h1 class="text-2xl font-bold mb-4">Dataset Details</h1>

    <div class="border p-4 rounded-lg bg-gray-100">
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
      axios.get(`/datasets/${datasetId}`)
        .then(response => {
          this.dataset = response.data;
        })
        .catch(error => {
          console.error('Dataset not found', error);
        });
    }
  },
  created() {
    this.fetchDataset();
  }
};
</script>

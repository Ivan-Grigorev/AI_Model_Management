<template>
  <!-- Header -->
  <header class="bg-green-600 text-white p-4 flex justify-between items-center">
    <router-link to="/dashboard" class="text-2xl hover:underline">User Dashboard</router-link>
    <h2 class="text-xl font-bold">Training Details</h2>
  </header>

  <div class="container mx-auto py-6 px-4">
    <div class="border p-4 rounded-lg bg-white">
      <p><strong>ID:</strong> {{ training.id }}</p>
      <p><strong>Experiment Name:</strong> {{ training.experiment_name }}</p>
      <p><strong>Model:</strong> {{ training.model_name }} (ID: {{ training.model_id }})</p>
      <p><strong>Dataset:</strong> {{ training.dataset_name }} (ID: {{ training.dataset_id }})</p>
      <p><strong>Precision:</strong> {{ (training.precision * 100).toFixed(2) }}%</p>
      <p><strong>Recall:</strong> {{ (training.recall * 100).toFixed(2) }}%</p>
      <p><strong>Creation Date:</strong> {{ training.creation_date }} </p>
    </div>

    <button @click="$router.push('/trainings')" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
      Back to All Trainings
    </button>
  </div>
</template>

<script>
import apiClient from '@/services/apiService'; // Import the centralized API service

export default {
  data() {
    return {
      training: null,
    };
  },
  methods: {
    async fetchTraining() {
      const trainingId = this.$route.params.training_id; // Get the training ID from route params
      try {
        const response = await apiClient.get(`/trainings/${trainingId}`); // Use apiClient to make the request
        this.training = response.data;
      } catch (error) {
        console.error('Error fetching training:', error);
      }
    }
  },
  created() {
    this.fetchTraining(); // Fetch the training details when the component is created
  }
};
</script>

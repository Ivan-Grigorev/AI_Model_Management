<template>
  <div class="container mx-auto py-6 px-4">
    <h1 class="text-2xl font-bold mb-4">Training Details</h1>

    <div class="border p-4 rounded-lg bg-gray-100">
      <p><strong>ID:</strong> {{ training.id }}</p>
      <p><strong>Experiment Name:</strong> {{ training.experiment_name }}</p>
      <p><strong>Model:</strong> {{ training.model_name }} (ID: {{ training.model_id }})</p>
      <p><strong>Dataset:</strong> {{ training.dataset_name }} (ID: {{ training.dataset_id }})</p>
      <p><strong>Precision:</strong> {{ training.precision }}</p>
      <p><strong>Recall:</strong> {{ training.recall }}</p>
    </div>

    <button @click="$router.push('/trainings')" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
      Back to All Trainings
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      training: null,
    };
  },
  methods: {
    fetchTraining() {
      const trainingId = this.$route.params.training_id;
      axios.get(`/trainings/${trainingId}`)
        .then(response => {
          this.training = response.data;
        })
        .catch(error => {
          console.error('Error fetching training:', error);
        });
    }
  },
  created() {
    this.fetchTraining();
  }
};
</script>
